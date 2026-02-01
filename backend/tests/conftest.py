"""
Pytest Configuration and Fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    """Create test client for API testing"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_report():
    """Sample user report data for testing"""
    return {
        "report_id": "test_report_001",
        "user_id": "test_user_001",
        "assessment_date": "2026-02-01",
        "overall_score": 72,
        "risk_level": "moderate",
        "parameters": [
            {
                "parameter_name": "balance_dynamic",
                "parameter_category": "balance",
                "value": 6.5,
                "unit": "score",
                "percentile": 45,
                "interpretation": "Average dynamic balance"
            },
            {
                "parameter_name": "reaction_time_simple",
                "parameter_category": "reaction_time",
                "value": 285,
                "unit": "ms",
                "percentile": 55,
                "interpretation": "Normal reaction time"
            },
            {
                "parameter_name": "rom_shoulder",
                "parameter_category": "rom",
                "value": 165,
                "unit": "degrees",
                "percentile": 60,
                "interpretation": "Good shoulder flexibility"
            }
        ]
    }


@pytest.fixture
def sample_chat_request():
    """Sample chat request for testing"""
    return {
        "message": "What exercises should I do for balance?",
        "include_context": True
    }
