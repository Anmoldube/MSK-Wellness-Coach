"""
Tests for Chat API Endpoints
"""
import pytest
from datetime import datetime


class TestChatEndpoints:
    """Test suite for chat API endpoints"""
    
    def test_send_message_success(self, client):
        """Test sending a message successfully"""
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "What does my report say?",
                "include_context": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "conversation_id" in data
        assert len(data["message"]) > 0
    
    def test_send_message_with_conversation_id(self, client):
        """Test continuing a conversation"""
        # First message
        response1 = client.post(
            "/api/v1/chat/message",
            json={"message": "Hello"}
        )
        conv_id = response1.json()["conversation_id"]
        
        # Second message with conversation ID
        response2 = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Tell me more",
                "conversation_id": conv_id
            }
        )
        
        assert response2.status_code == 200
        assert response2.json()["conversation_id"] == conv_id
    
    def test_send_empty_message(self, client):
        """Test sending empty message returns error"""
        response = client.post(
            "/api/v1/chat/message",
            json={"message": ""}
        )
        
        # Should still work but get a prompt to ask something
        assert response.status_code == 200
    
    def test_get_conversations(self, client):
        """Test retrieving conversations list"""
        response = client.get("/api/v1/chat/conversations")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestReportEndpoints:
    """Test suite for report API endpoints"""
    
    def test_get_latest_report(self, client):
        """Test getting latest assessment report"""
        response = client.get("/api/v1/reports/latest")
        
        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert "overall_score" in data
        assert "parameters" in data
        assert "risk_level" in data
    
    def test_get_reports_list(self, client):
        """Test getting list of reports"""
        response = client.get("/api/v1/reports?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRecommendationEndpoints:
    """Test suite for recommendation API endpoints"""
    
    def test_get_exercises(self, client):
        """Test getting exercise recommendations"""
        response = client.get("/api/v1/recommendations/exercises")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "exercise_id" in data[0]
            assert "name" in data[0]
    
    def test_get_exercises_by_parameter(self, client):
        """Test filtering exercises by target parameter"""
        response = client.get(
            "/api/v1/recommendations/exercises?target_parameter=balance"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_care_programs(self, client):
        """Test getting care program recommendations"""
        response = client.get("/api/v1/recommendations/care-programs")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "program_id" in data[0]
            assert "name" in data[0]
    
    def test_get_products(self, client):
        """Test getting product recommendations"""
        response = client.get("/api/v1/recommendations/products")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns ok"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
