"""
Progress Tracking Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import Optional, List
from datetime import datetime, timedelta
import structlog

from app.db.session import get_db
from app.models.user import User
from app.models.progress import Progress
from app.schemas.progress import ProgressCreate, ProgressResponse, ProgressTrend

logger = structlog.get_logger()

router = APIRouter()


@router.post("/progress/{user_id}", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def record_progress(
    user_id: str,
    progress_data: ProgressCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a new progress entry for a user
    
    Track improvements in game performance metrics over time
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
        
        # Create progress record
        new_progress = Progress(
            user_id=user_id,
            metric_name=progress_data.metric_name,
            metric_value=progress_data.metric_value,
            metric_unit=progress_data.metric_unit,
            activity_type=progress_data.activity_type,
            notes=progress_data.notes,
            extra_data=progress_data.extra_data or {}
        )
        
        db.add(new_progress)
        await db.commit()
        await db.refresh(new_progress)
        
        logger.info(
            "progress_recorded",
            user_id=user_id,
            metric=progress_data.metric_name,
            value=progress_data.metric_value
        )
        
        return ProgressResponse(
            id=new_progress.id,
            user_id=new_progress.user_id,
            metric_name=new_progress.metric_name,
            metric_value=new_progress.metric_value,
            metric_unit=new_progress.metric_unit,
            activity_type=new_progress.activity_type,
            recorded_at=new_progress.recorded_at,
            notes=new_progress.notes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("error_recording_progress", user_id=user_id, error=str(e))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record progress"
        )


@router.get("/progress/{user_id}", response_model=List[ProgressResponse])
async def get_user_progress(
    user_id: str,
    metric_name: Optional[str] = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """
    Get progress history for a user
    
    Optional filters:
    - metric_name: Filter by specific metric
    - days: Number of days to look back (default 30)
    """
    try:
        # Build query
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = select(Progress).where(
            and_(
                Progress.user_id == user_id,
                Progress.recorded_at >= cutoff_date
            )
        )
        
        if metric_name:
            query = query.where(Progress.metric_name == metric_name)
        
        query = query.order_by(Progress.recorded_at.desc())
        
        result = await db.execute(query)
        progress_records = result.scalars().all()
        
        return [
            ProgressResponse(
                id=p.id,
                user_id=p.user_id,
                metric_name=p.metric_name,
                metric_value=p.metric_value,
                metric_unit=p.metric_unit,
                activity_type=p.activity_type,
                recorded_at=p.recorded_at,
                notes=p.notes
            )
            for p in progress_records
        ]
        
    except Exception as e:
        logger.error("error_fetching_progress", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch progress"
        )


@router.get("/progress/{user_id}/trends")
async def get_progress_trends(
    user_id: str,
    metric_name: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """
    Get progress trends and analytics for a specific metric
    
    Returns:
    - Current value
    - Starting value
    - Improvement percentage
    - Trend direction
    - Data points for charting
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            select(Progress)
            .where(
                and_(
                    Progress.user_id == user_id,
                    Progress.metric_name == metric_name,
                    Progress.recorded_at >= cutoff_date
                )
            )
            .order_by(Progress.recorded_at.asc())
        )
        
        progress_records = result.scalars().all()
        
        if not progress_records:
            return {
                "metric_name": metric_name,
                "message": "No data available for this metric",
                "data_points": []
            }
        
        # Calculate trend analytics
        values = [p.metric_value for p in progress_records]
        first_value = values[0]
        last_value = values[-1]
        avg_value = sum(values) / len(values)
        
        improvement = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
        trend = "improving" if improvement > 5 else "declining" if improvement < -5 else "stable"
        
        return {
            "metric_name": metric_name,
            "metric_unit": progress_records[0].metric_unit,
            "current_value": last_value,
            "starting_value": first_value,
            "average_value": round(avg_value, 2),
            "improvement_percentage": round(improvement, 2),
            "trend": trend,
            "total_entries": len(progress_records),
            "date_range": {
                "start": progress_records[0].recorded_at,
                "end": progress_records[-1].recorded_at
            },
            "data_points": [
                {
                    "date": p.recorded_at.isoformat(),
                    "value": p.metric_value,
                    "activity_type": p.activity_type,
                    "notes": p.notes
                }
                for p in progress_records
            ]
        }
        
    except Exception as e:
        logger.error("error_calculating_trends", user_id=user_id, metric=metric_name, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate progress trends"
        )


@router.get("/progress/{user_id}/summary")
async def get_progress_summary(
    user_id: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall progress summary across all metrics
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all progress records
        result = await db.execute(
            select(Progress)
            .where(
                and_(
                    Progress.user_id == user_id,
                    Progress.recorded_at >= cutoff_date
                )
            )
            .order_by(Progress.recorded_at.desc())
        )
        
        progress_records = result.scalars().all()
        
        if not progress_records:
            return {
                "user_id": user_id,
                "message": "No progress data available",
                "metrics_tracked": []
            }
        
        # Group by metric
        metrics_summary = {}
        for record in progress_records:
            metric = record.metric_name
            if metric not in metrics_summary:
                metrics_summary[metric] = {
                    "metric_name": metric,
                    "metric_unit": record.metric_unit,
                    "entries": [],
                    "latest_value": None,
                    "trend": "unknown"
                }
            metrics_summary[metric]["entries"].append(record.metric_value)
        
        # Calculate trends for each metric
        for metric, data in metrics_summary.items():
            entries = data["entries"]
            data["latest_value"] = entries[0]  # Most recent (desc order)
            data["total_entries"] = len(entries)
            
            if len(entries) >= 2:
                first = entries[-1]  # Oldest
                last = entries[0]   # Newest
                if first != 0:
                    improvement = ((last - first) / first * 100)
                    data["improvement_percentage"] = round(improvement, 2)
                    data["trend"] = "improving" if improvement > 5 else "declining" if improvement < -5 else "stable"
        
        return {
            "user_id": user_id,
            "date_range_days": days,
            "total_entries": len(progress_records),
            "metrics_tracked": list(metrics_summary.values())
        }
        
    except Exception as e:
        logger.error("error_generating_progress_summary", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate progress summary"
        )
