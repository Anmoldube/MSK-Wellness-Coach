"""
File Upload Endpoints for Reports
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
import aiofiles
import uuid
from datetime import datetime
import structlog

from app.db.session import get_db
from app.models.user import User
from app.models.report import Report
from app.core.config import settings
from app.schemas.report import ReportUploadResponse

logger = structlog.get_logger()

router = APIRouter()


@router.post("/upload/report/{user_id}", response_model=ReportUploadResponse)
async def upload_performance_report(
    user_id: str,
    file: UploadFile = File(...),
    report_title: str = "Performance Report",
    report_type: str = "game_performance",
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a performance report file (PDF, image, CSV, etc.)
    
    Supports: PDF reports, screenshots, CSV data exports
    """
    try:
        # Validate user exists
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}{file_ext}"
        
        # Create user directory if it doesn't exist
        user_dir = Path(settings.UPLOAD_DIR) / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = user_dir / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        logger.info("file_uploaded", user_id=user_id, filename=filename, size=len(content))
        
        # Create report record in database
        new_report = Report(
            user_id=user_id,
            title=report_title,
            report_type=report_type,
            file_path=str(file_path),
            file_name=file.filename,
            metrics={},  # Can be populated by analysis service later
        )
        
        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        
        logger.info("report_created", report_id=new_report.id, user_id=user_id)
        
        return ReportUploadResponse(
            report_id=new_report.id,
            user_id=user_id,
            filename=file.filename,
            file_path=str(file_path),
            upload_time=new_report.created_at,
            message="File uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_uploading_file", user_id=user_id, error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file"
        )


@router.get("/upload/reports/{user_id}")
async def get_user_reports(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all uploaded reports for a user"""
    try:
        result = await db.execute(
            select(Report)
            .where(Report.user_id == user_id)
            .order_by(Report.created_at.desc())
        )
        reports = result.scalars().all()
        
        return {
            "user_id": user_id,
            "total_reports": len(reports),
            "reports": [
                {
                    "report_id": r.id,
                    "title": r.title,
                    "report_type": r.report_type,
                    "file_name": r.file_name,
                    "created_at": r.created_at,
                    "analysis_summary": r.analysis_summary
                }
                for r in reports
            ]
        }
        
    except Exception as e:
        logger.error("error_fetching_reports", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reports"
        )


@router.delete("/upload/report/{report_id}")
async def delete_report(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a report and its associated file"""
    try:
        result = await db.execute(select(Report).where(Report.id == report_id))
        report = result.scalar_one_or_none()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        # Delete file if it exists
        if report.file_path:
            file_path = Path(report.file_path)
            if file_path.exists():
                file_path.unlink()
                logger.info("file_deleted", file_path=str(file_path))
        
        # Delete database record
        await db.delete(report)
        await db.commit()
        
        logger.info("report_deleted", report_id=report_id)
        
        return {"message": "Report deleted successfully", "report_id": report_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_deleting_report", report_id=report_id, error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete report"
        )


# ---------------------------------------------------------------------------
# Document Upload & Indexing Endpoints (RAG)
# ---------------------------------------------------------------------------

@router.post("/upload/document/{user_id}")
async def upload_document(
    user_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a document (PDF, TXT, CSV) for RAG indexing.
    The file is parsed into page-level chunks and indexed into ChromaDB.
    """
    from app.services.document_service import get_document_service
    from app.models.document import Document as DocumentModel

    try:
        # Validate user exists
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate extension
        file_ext = Path(file.filename).suffix.lower()
        allowed = [".pdf", ".txt", ".csv"]
        if file_ext not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{file_ext}'. Allowed: {', '.join(allowed)}",
            )

        # Read and save file
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

        doc_id = str(uuid.uuid4())
        user_dir = Path(settings.UPLOAD_DIR) / user_id / "documents"
        user_dir.mkdir(parents=True, exist_ok=True)
        file_path = user_dir / f"{doc_id}{file_ext}"

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Create DB record
        doc_record = DocumentModel(
            id=doc_id,
            user_id=user_id,
            filename=file.filename,
            file_type=file_ext.lstrip("."),
            status="processing",
        )
        db.add(doc_record)
        await db.flush()

        # Ingest & index into ChromaDB
        doc_service = get_document_service()
        result_info = doc_service.ingest_file(
            file_path=str(file_path),
            filename=file.filename,
            user_id=user_id,
            doc_id=doc_id,
        )

        doc_record.page_count = result_info.get("page_count", 0)
        doc_record.chunk_count = result_info.get("chunk_count", 0)
        doc_record.status = result_info.get("status", "failed")
        await db.commit()

        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "status": doc_record.status,
            "page_count": doc_record.page_count,
            "chunk_count": doc_record.chunk_count,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("document_upload_failed", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to upload document")


@router.get("/upload/documents/{user_id}")
async def get_user_documents(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get all indexed documents for a user."""
    from app.models.document import Document as DocumentModel

    result = await db.execute(
        select(DocumentModel)
        .where(DocumentModel.user_id == user_id)
        .order_by(DocumentModel.created_at.desc())
    )
    docs = result.scalars().all()
    return [
        {
            "doc_id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "page_count": d.page_count,
            "chunk_count": d.chunk_count,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


@router.delete("/upload/document/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a document and its ChromaDB chunks."""
    from app.services.document_service import get_document_service
    from app.models.document import Document as DocumentModel

    result = await db.execute(select(DocumentModel).where(DocumentModel.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove chunks from ChromaDB
    get_document_service().delete_document(doc_id)

    # Delete DB record
    await db.delete(doc)
    await db.commit()
    return {"status": "deleted", "doc_id": doc_id}
