"""
Reports API Endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.report import (
    AssessmentReportCreate,
    AssessmentReportResponse,
    ReportSummary,
    UserParameter,
    ParameterCategory,
)

router = APIRouter(prefix="/reports")

# In-memory storage for demo
reports_db: dict = {}

# Sample demo data
SAMPLE_REPORT = {
    "report_id": "demo-report-001",
    "user_id": "demo-user",
    "assessment_date": "2026-01-15",
    "overall_score": 62.0,
    "risk_level": "moderate",
    "created_at": datetime.utcnow(),
    "parameters": [
        {
            "parameter_name": "balance_dynamic",
            "parameter_category": "balance",
            "value": 4.2,
            "unit": "score/10",
            "reference_range_min": 6.0,
            "reference_range_max": 10.0,
            "percentile": 25,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Below average - needs improvement"
        },
        {
            "parameter_name": "balance_single_leg",
            "parameter_category": "balance",
            "value": 8.0,
            "unit": "seconds",
            "reference_range_min": 20.0,
            "reference_range_max": 45.0,
            "percentile": 15,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Significantly below target"
        },
        {
            "parameter_name": "reaction_time_simple",
            "parameter_category": "reaction_time",
            "value": 340.0,
            "unit": "milliseconds",
            "reference_range_min": 250.0,
            "reference_range_max": 400.0,
            "percentile": 55,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Within normal range"
        },
        {
            "parameter_name": "reaction_time_choice",
            "parameter_category": "reaction_time",
            "value": 580.0,
            "unit": "milliseconds",
            "reference_range_min": 450.0,
            "reference_range_max": 650.0,
            "percentile": 50,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Average"
        },
        {
            "parameter_name": "rom_lumbar",
            "parameter_category": "rom",
            "value": 35.0,
            "unit": "degrees",
            "reference_range_min": 45.0,
            "reference_range_max": 75.0,
            "percentile": 15,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Restricted - needs attention"
        },
        {
            "parameter_name": "rom_upper_body",
            "parameter_category": "rom",
            "value": 85.0,
            "unit": "degrees",
            "reference_range_min": 60.0,
            "reference_range_max": 90.0,
            "percentile": 95,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Excellent"
        },
        {
            "parameter_name": "strength_grip",
            "parameter_category": "strength",
            "value": 42.0,
            "unit": "kg",
            "reference_range_min": 35.0,
            "reference_range_max": 55.0,
            "percentile": 60,
            "is_lagging_indicator": True,
            "is_leading_indicator": False,
            "interpretation": "Good"
        }
    ]
}

# Initialize with sample data
reports_db["demo-report-001"] = SAMPLE_REPORT


@router.post("/", response_model=AssessmentReportResponse)
async def create_report(report: AssessmentReportCreate):
    """
    Upload a new MSK assessment report
    """
    report_id = str(uuid.uuid4())
    
    new_report = {
        "report_id": report_id,
        "user_id": "demo-user",
        "assessment_date": report.assessment_date.isoformat(),
        "overall_score": report.overall_score,
        "risk_level": report.risk_level.value,
        "created_at": datetime.utcnow(),
        "parameters": [p.model_dump() for p in report.parameters]
    }
    
    reports_db[report_id] = new_report
    
    return _format_report_response(new_report)


@router.get("/", response_model=List[ReportSummary])
async def get_reports(limit: int = 10):
    """
    Get user's assessment reports
    """
    reports = list(reports_db.values())[:limit]
    
    return [
        ReportSummary(
            report_id=r["report_id"],
            assessment_date=r["assessment_date"],
            overall_score=r["overall_score"],
            risk_level=r["risk_level"],
            parameter_count=len(r["parameters"])
        )
        for r in reports
    ]


@router.get("/latest", response_model=AssessmentReportResponse)
async def get_latest_report():
    """
    Get user's most recent assessment report
    """
    if not reports_db:
        raise HTTPException(status_code=404, detail="No reports found")
    
    # Get the most recent report
    latest = max(reports_db.values(), key=lambda x: x["created_at"])
    return _format_report_response(latest)


@router.get("/{report_id}", response_model=AssessmentReportResponse)
async def get_report(report_id: str):
    """
    Get a specific report
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return _format_report_response(reports_db[report_id])


@router.get("/{report_id}/parameters", response_model=List[UserParameter])
async def get_report_parameters(report_id: str):
    """
    Get all parameters for a specific report
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return [
        UserParameter(**p) for p in reports_db[report_id]["parameters"]
    ]


def _format_report_response(report: dict) -> AssessmentReportResponse:
    """Format report dict to response model"""
    return AssessmentReportResponse(
        report_id=report["report_id"],
        user_id=report["user_id"],
        assessment_date=report["assessment_date"],
        parameters=[UserParameter(**p) for p in report["parameters"]],
        overall_score=report["overall_score"],
        risk_level=report["risk_level"],
        created_at=report["created_at"]
    )
