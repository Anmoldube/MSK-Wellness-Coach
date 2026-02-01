"""
Tests for LLM Service
"""
import pytest
from app.services.llm_service import LLMService


class TestLLMService:
    """Test suite for LLM Service"""
    
    def test_service_initialization(self):
        """Test LLM service initializes correctly"""
        service = LLMService()
        assert service is not None
    
    def test_generate_mock_response(self):
        """Test mock response generation"""
        service = LLMService()
        
        # Test report analysis
        response = service._generate_mock_response(
            "What does my report say?",
            {}
        )
        assert "assessment" in response.lower() or "report" in response.lower()
    
    def test_intent_detection(self):
        """Test various intents are detected correctly"""
        service = LLMService()
        
        # Balance intent
        response = service._generate_mock_response(
            "How can I improve my balance?",
            {}
        )
        assert "balance" in response.lower()
        
        # Exercise intent
        response = service._generate_mock_response(
            "What exercises should I do?",
            {}
        )
        assert "exercise" in response.lower() or "recommend" in response.lower()
        
        # Program intent
        response = service._generate_mock_response(
            "Which care program should I follow?",
            {}
        )
        assert "program" in response.lower()
    
    def test_function_call_handling(self):
        """Test function calls are processed"""
        service = LLMService()
        
        # This tests that the service can generate a response
        # even when function calls would be made
        response = service._generate_mock_response(
            "Show me exercises for reaction time",
            {}
        )
        assert len(response) > 0


class TestContextManager:
    """Test suite for Context Manager"""
    
    def test_create_context(self):
        """Test creating a new conversation context"""
        from app.services.context_manager import ContextManager
        
        manager = ContextManager()
        context = manager.get_or_create_context("conv_001", "user_001")
        
        assert context["conversation_id"] == "conv_001"
        assert context["user_id"] == "user_001"
        assert len(context["messages"]) == 0
    
    def test_add_message(self):
        """Test adding messages to context"""
        from app.services.context_manager import ContextManager
        
        manager = ContextManager()
        manager.get_or_create_context("conv_002", "user_001")
        
        manager.add_message("conv_002", "user", "Hello")
        manager.add_message("conv_002", "assistant", "Hi there!")
        
        messages = manager.get_recent_messages("conv_002")
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"
    
    def test_analyze_user_intent(self):
        """Test user intent analysis"""
        from app.services.context_manager import ContextManager
        
        manager = ContextManager()
        
        # Test report analysis intent
        intent = manager.analyze_user_intent("What does my report say?")
        assert intent["primary_intent"] == "report_analysis"
        
        # Test exercise intent
        intent = manager.analyze_user_intent("How can I improve my balance?")
        assert intent["primary_intent"] == "exercise_request"
        assert "balance" in intent["parameters_mentioned"]
    
    def test_cleanup_old_conversations(self):
        """Test cleanup of old conversations"""
        from app.services.context_manager import ContextManager
        
        manager = ContextManager()
        manager.get_or_create_context("old_conv", "user_001")
        
        # Should not remove recent conversations
        removed = manager.cleanup_old_conversations(max_age_hours=24)
        assert removed == 0


class TestPromptTemplates:
    """Test suite for Prompt Templates"""
    
    def test_system_prompt_exists(self):
        """Test system prompt is defined"""
        from app.utils.prompt_templates import SYSTEM_PROMPT
        
        assert len(SYSTEM_PROMPT) > 100
        assert "MSK" in SYSTEM_PROMPT or "musculoskeletal" in SYSTEM_PROMPT.lower()
    
    def test_format_user_context(self):
        """Test formatting user context"""
        from app.utils.prompt_templates import format_user_context
        
        report = {
            "assessment_date": "2026-02-01",
            "overall_score": 75,
            "risk_level": "moderate",
            "parameters": [
                {
                    "parameter_name": "balance",
                    "value": 7,
                    "unit": "score",
                    "percentile": 50,
                    "interpretation": "Average"
                }
            ]
        }
        
        context = format_user_context(report)
        assert "75" in context
        assert "MODERATE" in context
    
    def test_get_follow_up_questions(self):
        """Test getting follow-up questions"""
        from app.utils.prompt_templates import get_follow_up_questions
        
        questions = get_follow_up_questions("balance")
        assert isinstance(questions, list)
        assert len(questions) > 0
        
        # Unknown category should return general questions
        general = get_follow_up_questions("unknown_category")
        assert len(general) > 0
