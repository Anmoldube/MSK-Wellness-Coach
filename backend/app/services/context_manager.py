"""
Context Manager - Manages conversation context and user state
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict


class ContextManager:
    """
    Manages conversation context, user state, and relevance scoring.
    Ensures Claude has appropriate context without token overflow.
    """
    
    def __init__(self, max_history_messages: int = 10):
        self.max_history_messages = max_history_messages
        self._conversation_contexts: Dict[str, Dict] = {}
        self._user_states: Dict[str, Dict] = {}
    
    def get_or_create_context(self, conversation_id: str, user_id: str) -> Dict:
        """Get or create a conversation context"""
        if conversation_id not in self._conversation_contexts:
            self._conversation_contexts[conversation_id] = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "messages": [],
                "started_at": datetime.utcnow(),
                "last_active": datetime.utcnow(),
                "topics_discussed": set(),
                "parameters_mentioned": set(),
                "recommendations_made": [],
                "user_intent_history": []
            }
        return self._conversation_contexts[conversation_id]
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """Add a message to conversation history"""
        if conversation_id not in self._conversation_contexts:
            return
        
        context = self._conversation_contexts[conversation_id]
        context["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        })
        context["last_active"] = datetime.utcnow()
        
        # Trim if exceeds max
        if len(context["messages"]) > self.max_history_messages * 2:
            context["messages"] = context["messages"][-self.max_history_messages:]
    
    def get_recent_messages(
        self,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Get recent messages for context"""
        if conversation_id not in self._conversation_contexts:
            return []
        
        messages = self._conversation_contexts[conversation_id]["messages"]
        limit = limit or self.max_history_messages
        return messages[-limit:]
    
    def analyze_user_intent(self, message: str) -> Dict[str, Any]:
        """
        Analyze user message to determine intent and extract entities.
        Returns intent classification and relevant parameters.
        """
        message_lower = message.lower()
        
        intent = {
            "primary_intent": "general",
            "parameters_mentioned": [],
            "action_requested": None,
            "sentiment": "neutral"
        }
        
        # Intent classification
        if any(kw in message_lower for kw in ["report", "assessment", "results", "score", "status", "what does my"]):
            intent["primary_intent"] = "report_analysis"
        elif any(kw in message_lower for kw in ["exercise", "workout", "train", "how to improve", "how can i improve", "increase"]):
            intent["primary_intent"] = "exercise_request"
        elif any(kw in message_lower for kw in ["program", "care program", "enroll", "sign up"]):
            intent["primary_intent"] = "program_inquiry"
        elif any(kw in message_lower for kw in ["product", "supplement", "buy", "purchase", "recommend"]):
            intent["primary_intent"] = "product_inquiry"
        elif any(kw in message_lower for kw in ["what is", "explain", "tell me about", "mean"]):
            intent["primary_intent"] = "information_request"
        
        # Parameter extraction
        parameter_keywords = {
            "balance": ["balance", "stability", "equilibrium", "fall", "standing"],
            "reaction_time": ["reaction", "response", "reflex", "quick"],
            "rom": ["rom", "range of motion", "flexibility", "stretch", "bend"],
            "strength": ["strength", "strong", "power", "muscle", "weak"],
            "endurance": ["endurance", "stamina", "cardio", "fatigue"]
        }
        
        for param, keywords in parameter_keywords.items():
            if any(kw in message_lower for kw in keywords):
                intent["parameters_mentioned"].append(param)
        
        # Action extraction
        if any(kw in message_lower for kw in ["show", "give", "list", "what are"]):
            intent["action_requested"] = "retrieve"
        elif any(kw in message_lower for kw in ["improve", "increase", "better", "fix"]):
            intent["action_requested"] = "improve"
        elif any(kw in message_lower for kw in ["explain", "what is", "why", "how does"]):
            intent["action_requested"] = "explain"
        
        return intent
    
    def track_recommendation(
        self,
        conversation_id: str,
        recommendation_type: str,
        items: List[str]
    ):
        """Track recommendations made in conversation"""
        if conversation_id not in self._conversation_contexts:
            return
        
        context = self._conversation_contexts[conversation_id]
        context["recommendations_made"].append({
            "type": recommendation_type,
            "items": items,
            "timestamp": datetime.utcnow()
        })
    
    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """Get a summary of the conversation for context"""
        if conversation_id not in self._conversation_contexts:
            return {}
        
        context = self._conversation_contexts[conversation_id]
        
        return {
            "message_count": len(context["messages"]),
            "duration_minutes": (datetime.utcnow() - context["started_at"]).seconds // 60,
            "topics_discussed": list(context.get("topics_discussed", [])),
            "parameters_mentioned": list(context.get("parameters_mentioned", [])),
            "recommendations_count": len(context.get("recommendations_made", []))
        }
    
    def update_user_state(self, user_id: str, key: str, value: Any):
        """Update persistent user state"""
        if user_id not in self._user_states:
            self._user_states[user_id] = {}
        self._user_states[user_id][key] = value
    
    def get_user_state(self, user_id: str) -> Dict:
        """Get user's persistent state"""
        return self._user_states.get(user_id, {})
    
    def cleanup_old_conversations(self, max_age_hours: int = 24):
        """Remove old conversations to free memory"""
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        to_remove = [
            conv_id for conv_id, context in self._conversation_contexts.items()
            if context["last_active"] < cutoff
        ]
        
        for conv_id in to_remove:
            del self._conversation_contexts[conv_id]
        
        return len(to_remove)


# Singleton instance
context_manager = ContextManager()
