"""
LLM Service - Claude API Integration with Function Calling
"""
from typing import List, Dict, Any, Optional
import os

from app.core.config import settings
from app.services.knowledge_base import KnowledgeBaseService
from app.api.endpoints.reports import reports_db, SAMPLE_REPORT


class LLMService:
    """
    Handles all interactions with Claude API.
    Implements prompt engineering, function calling, and response parsing.
    """
    
    def __init__(self):
        self.knowledge_base = KnowledgeBaseService()
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize Anthropic client if API key is available"""
        api_key = settings.ANTHROPIC_API_KEY
        if api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                print("anthropic package not installed, using mock responses")
    
    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        include_context: bool = True
    ) -> Dict[str, Any]:
        """
        Main chat method that orchestrates the conversation flow.
        """
        conversation_history = conversation_history or []
        
        # Load user context
        user_context = self._get_user_context() if include_context else {}
        
        # If we have a real Claude client, use it
        if self.client:
            return await self._call_claude(user_message, user_context, conversation_history)
        
        # Otherwise, use intelligent mock responses
        return self._generate_mock_response(user_message, user_context)
    
    async def _call_claude(
        self,
        user_message: str,
        user_context: Dict,
        conversation_history: List[Dict]
    ) -> Dict[str, Any]:
        """Call Claude API with tools"""
        
        # Build system prompt
        system_prompt = self._build_system_prompt()
        
        # Build messages
        messages = self._build_messages(user_message, user_context, conversation_history)
        
        # Define tools
        tools = self._get_tools()
        
        try:
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tools,
                temperature=0.7
            )
            
            return self._process_claude_response(response)
            
        except Exception as e:
            print(f"Claude API error: {e}")
            return self._generate_mock_response(user_message, user_context)
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for Claude"""
        return """You are an expert musculoskeletal (MSK) wellness coach AI assistant. Your role is to help users understand their MSK assessment results and provide personalized recommendations for improvement.

**Your Capabilities:**
- Analyze and explain MSK assessment parameters (Balance, Reaction Time, ROM, Strength, etc.)
- Recommend personalized care programs based on user needs
- Suggest specific exercises to improve deficiencies
- Recommend supportive products (nutraceuticals, ergonomic aids)
- Provide evidence-based health information

**Guidelines:**
1. Always base recommendations on the user's actual assessment data when available
2. Be encouraging and supportive while being honest about areas needing improvement
3. Explain medical/technical terms in simple language
4. Prioritize safety - mention contraindications and when to consult healthcare providers
5. Be conversational and empathetic
6. Use bullet points for lists of exercises/programs/products
7. Include actionable next steps
8. Offer follow-up questions to guide the conversation

**Important Disclaimers:**
- You are not a replacement for professional medical advice
- Always recommend consulting healthcare providers for medical concerns
- Do not diagnose conditions or prescribe medications"""
    
    def _build_messages(
        self,
        user_message: str,
        user_context: Dict,
        conversation_history: List[Dict]
    ) -> List[Dict]:
        """Build messages array for Claude API"""
        messages = []
        
        # Add conversation history (last 10 messages)
        for msg in conversation_history[-10:]:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                messages.append({
                    "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                    "content": msg.content
                })
        
        # Format user message with context
        context_str = self._format_user_context(user_context)
        full_message = f"{user_message}\n\n{context_str}" if context_str else user_message
        
        messages.append({
            "role": "user",
            "content": full_message
        })
        
        return messages
    
    def _format_user_context(self, user_context: Dict) -> str:
        """Format user context for inclusion in messages"""
        if not user_context:
            return ""
        
        report = user_context.get("latest_report")
        if not report:
            return ""
        
        context = f"""[User's Latest MSK Assessment - {report.get('assessment_date', 'N/A')}]
Overall Score: {report.get('overall_score', 'N/A')}/100
Risk Level: {report.get('risk_level', 'N/A').upper()}

Key Parameters:"""
        
        for param in report.get("parameters", [])[:7]:
            name = param.get("parameter_name", "Unknown")
            value = param.get("value", "N/A")
            unit = param.get("unit", "")
            interp = param.get("interpretation", "")
            context += f"\n- {name}: {value} {unit}"
            if interp:
                context += f" ({interp})"
        
        return context
    
    def _get_tools(self) -> List[Dict]:
        """Return list of tools available to Claude"""
        return [
            {
                "name": "get_user_parameters",
                "description": "Retrieve user's MSK assessment parameters",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "parameter_names": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of parameters to retrieve"
                        }
                    },
                    "required": ["parameter_names"]
                }
            },
            {
                "name": "search_care_programs",
                "description": "Find care programs matching user's needs",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "focus_areas": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Areas to focus on (e.g., ['balance', 'rom'])"
                        },
                        "intensity_level": {
                            "type": "string",
                            "enum": ["beginner", "intermediate", "advanced"]
                        }
                    },
                    "required": ["focus_areas"]
                }
            },
            {
                "name": "get_exercises",
                "description": "Retrieve exercises for specific parameters",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "target_parameter": {
                            "type": "string",
                            "description": "Parameter to improve (e.g., 'balance')"
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "moderate", "hard"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of exercises to return"
                        }
                    },
                    "required": ["target_parameter"]
                }
            },
            {
                "name": "recommend_products",
                "description": "Suggest products based on user's condition",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "condition": {
                            "type": "string",
                            "description": "User's condition or pain point"
                        },
                        "product_type": {
                            "type": "string",
                            "enum": ["supplement", "ergonomic", "pain_relief", "recovery_tool"]
                        }
                    },
                    "required": ["condition"]
                }
            }
        ]
    
    def _process_claude_response(self, response) -> Dict[str, Any]:
        """Process Claude's response"""
        result = {
            "message": "",
            "function_calls": [],
            "citations": [],
            "suggested_questions": []
        }
        
        for block in response.content:
            if block.type == "text":
                result["message"] += block.text
        
        # Extract suggested questions from response
        result["suggested_questions"] = self._extract_suggested_questions(result["message"])
        
        return result
    
    def _get_user_context(self) -> Dict[str, Any]:
        """Get user's MSK data"""
        return {"latest_report": SAMPLE_REPORT}
    
    def _generate_mock_response(
        self,
        user_message: str,
        user_context: Dict
    ) -> Dict[str, Any]:
        """
        Generate intelligent mock responses when Claude API is not available.
        Uses keyword matching to provide relevant responses.
        """
        message_lower = user_message.lower()
        report = user_context.get("latest_report", SAMPLE_REPORT)
        
        # Report analysis
        if any(kw in message_lower for kw in ["report", "assessment", "results", "score", "status"]):
            return self._mock_report_analysis(report)
        
        # Balance questions
        if "balance" in message_lower:
            if any(kw in message_lower for kw in ["improve", "increase", "better", "exercise"]):
                return self._mock_balance_exercises()
            return self._mock_balance_analysis(report)
        
        # ROM questions
        if any(kw in message_lower for kw in ["rom", "range of motion", "flexibility", "stretch"]):
            if any(kw in message_lower for kw in ["improve", "increase", "better", "exercise"]):
                return self._mock_rom_exercises()
            return self._mock_rom_analysis(report)
        
        # Reaction time
        if "reaction" in message_lower:
            return self._mock_reaction_time_analysis(report)
        
        # Care programs
        if any(kw in message_lower for kw in ["program", "care", "recommend", "which"]):
            return self._mock_program_recommendation(report)
        
        # Products
        if any(kw in message_lower for kw in ["product", "supplement", "back", "pain", "support"]):
            return self._mock_product_recommendation()
        
        # Exercise requests
        if any(kw in message_lower for kw in ["exercise", "workout", "train"]):
            return self._mock_general_exercises()
        
        # Default greeting/help
        return self._mock_greeting()
    
    def _mock_report_analysis(self, report: Dict) -> Dict[str, Any]:
        """Generate report analysis response"""
        return {
            "message": f"""Based on your recent assessment from **{report.get('assessment_date', 'January 15, 2026')}**:

📊 **Overall Score**: {report.get('overall_score', 62)}/100 ({report.get('risk_level', 'Moderate').upper()} Risk)

**✅ Strengths:**
- Upper body ROM is excellent (95th percentile)
- Reaction time is within normal range (340ms simple, 580ms choice)
- Grip strength is good (60th percentile)

**⚠️ Areas Needing Attention:**
- **Dynamic Balance**: 4.2/10 (below average - priority area)
- **Single-Leg Balance**: 8 seconds (target: 20-30 seconds)
- **Lumbar ROM**: Restricted at 35° (15th percentile)

**My Recommendations:**
1. Start with balance-focused exercises daily
2. Add ROM stretches for your lower back
3. Consider a structured care program for comprehensive improvement

Would you like me to suggest specific exercises for balance or ROM?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "How can I improve my balance?",
                "What exercises help with lumbar ROM?",
                "Which care program is best for me?"
            ]
        }
    
    def _mock_balance_analysis(self, report: Dict) -> Dict[str, Any]:
        """Generate balance-specific analysis"""
        return {
            "message": """Let me break down your **balance scores**:

📊 **Your Balance Parameters:**
- **Dynamic Balance**: 4.2/10 (25th percentile) - *Needs improvement*
- **Single-Leg Balance**: 8 seconds (target: 20-30s) - *Significantly below target*

**What This Means:**
Your balance scores indicate you may have difficulty with:
- Quick direction changes
- Standing on one leg for extended periods
- Activities requiring stability (like climbing stairs)

**Why This Matters:**
Good balance is essential for preventing falls and maintaining independence. The good news? Balance is very trainable!

Would you like me to recommend exercises to improve your balance?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "Show me balance exercises",
                "How long until I see improvement?",
                "What causes poor balance?"
            ]
        }
    
    def _mock_balance_exercises(self) -> Dict[str, Any]:
        """Generate balance exercise recommendations"""
        exercises = self.knowledge_base.search_exercises(target_parameter="balance", limit=3)
        
        exercise_text = ""
        for i, ex in enumerate(exercises, 1):
            exercise_text += f"""
**{i}. {ex.name}** ({ex.difficulty.value.capitalize()})
   - **How to do it**: {' '.join(ex.instructions[:2])}
   - **Frequency**: {ex.frequency}
   - **Sets/Reps**: {ex.sets_reps}
   - **Expected improvement**: {ex.expected_timeline}
"""
        
        return {
            "message": f"""Great question! Here are my top recommended exercises to improve your balance:
{exercise_text}
**Pro Tips:**
- Start with the Single-Leg Stand - it's the foundation
- Practice near a wall or chair for safety
- Consistency is key - aim for daily practice

**Safety First:**
- Stop if you feel dizzy
- Have something sturdy nearby to grab
- Progress gradually

Would you like more details on any of these exercises, or shall I recommend a structured balance program?""",
            "function_calls": [{"name": "get_exercises", "arguments": {"target_parameter": "balance"}, "result": {"count": len(exercises)}}],
            "citations": [],
            "suggested_questions": [
                "Show me video demonstrations",
                "What equipment do I need?",
                "Recommend a balance care program"
            ]
        }
    
    def _mock_rom_analysis(self, report: Dict) -> Dict[str, Any]:
        """Generate ROM analysis"""
        return {
            "message": """Here's your **Range of Motion (ROM)** breakdown:

📊 **Your ROM Parameters:**
- **Lumbar (Lower Back)**: 35° (15th percentile) - *Restricted*
- **Upper Body**: 85° (95th percentile) - *Excellent!*

**What This Means:**
Your lower back mobility is restricted, which may affect:
- Bending to pick things up
- Twisting movements
- Overall comfort during prolonged sitting

Your upper body ROM is excellent though! 🎉

**Common Causes of Restricted Lumbar ROM:**
- Prolonged sitting
- Tight hip flexors
- Weak core muscles

Would you like exercises to improve your lumbar ROM?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "Give me ROM exercises",
                "What products help with back flexibility?",
                "How long to improve ROM?"
            ]
        }
    
    def _mock_rom_exercises(self) -> Dict[str, Any]:
        """Generate ROM exercise recommendations"""
        return {
            "message": """Here are the best exercises to improve your **lumbar ROM**:

**1. Cat-Cow Stretch** (Easy)
   - Start on hands and knees
   - Alternate between arching and rounding your back
   - Do 15 repetitions, 3 sets daily
   - *Feel improvement in 1-2 weeks*

**2. Seated Spinal Twist** (Easy)
   - Sit with legs extended
   - Bend one knee, twist toward it
   - Hold 30 seconds each side
   - Do 3 sets daily

**3. Child's Pose with Reach** (Easy)
   - Kneel and sit back on heels
   - Extend arms forward on floor
   - Walk hands side to side
   - Hold 30-60 seconds

**Important Tips:**
- Never force a stretch - go to mild tension only
- Breathe deeply throughout
- Warm up first with light walking
- Consistency beats intensity

Would you like product recommendations to complement your stretching routine?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "What products help with stretching?",
                "How often should I stretch?",
                "Recommend a flexibility program"
            ]
        }
    
    def _mock_reaction_time_analysis(self, report: Dict) -> Dict[str, Any]:
        """Generate reaction time analysis"""
        return {
            "message": """Good news about your **reaction time**! 🎉

📊 **Your Reaction Time Scores:**
- **Simple Reaction Time**: 340ms (55th percentile) - *Within normal range*
- **Choice Reaction Time**: 580ms (50th percentile) - *Average*

**What These Mean:**
- **Simple**: How fast you respond to a single stimulus
- **Choice**: How fast you decide between multiple options

Your reaction times are healthy for your age group. This isn't a priority area for improvement, but you can still enhance them with practice.

**Quick Tips to Stay Sharp:**
- Stay physically active
- Get adequate sleep
- Try brain training games occasionally

Since your balance and ROM need more attention, I'd recommend focusing there first. Would you like recommendations for those areas?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "How can I improve my balance?",
                "What exercises help ROM?",
                "Show me my full report"
            ]
        }
    
    def _mock_program_recommendation(self, report: Dict) -> Dict[str, Any]:
        """Generate care program recommendation"""
        programs = self.knowledge_base.search_care_programs(
            focus_areas=["balance", "rom"],
            limit=2
        )
        
        return {
            "message": f"""Based on your needs (balance + ROM improvement), I recommend the **Comprehensive MSK Wellness Program**:

🏆 **Top Recommendation:**

**Comprehensive MSK Wellness Program**
- **Provider**: PhysioFirst Care Partners
- **Duration**: 12 weeks
- **Focus**: Balance, ROM, Strength, Flexibility
- **Intensity**: Intermediate
- **Cost**: $299

**Why This Matches You:**
✅ Addresses both your problem areas (balance & ROM)
✅ Moderate risk level fits the intermediate intensity
✅ 12-week duration allows for proper progression
✅ Includes professional guidance and tracking

**What You'll Get:**
- 3 sessions per week (45 min each)
- Personalized exercise progressions
- Regular assessments to track improvement
- Access to physiotherapists

**Expected Results:**
- 25-35% balance improvement
- 20-30% ROM improvement

**Alternative Option:**
If you want to start smaller, the **Balance Mastery Program** (8 weeks, $199) focuses specifically on balance.

Would you like help enrolling, or do you want to see more program options?""",
            "function_calls": [{"name": "search_care_programs", "arguments": {"focus_areas": ["balance", "rom"]}, "result": {"count": len(programs)}}],
            "citations": [],
            "suggested_questions": [
                "Tell me more about the Balance program",
                "How do I enroll?",
                "Are there any free alternatives?"
            ]
        }
    
    def _mock_product_recommendation(self) -> Dict[str, Any]:
        """Generate product recommendations"""
        return {
            "message": """Based on your profile (lumbar ROM restriction, need for balance training), here are my product recommendations:

**🔝 Top Picks:**

**1. ErgoSupport Lumbar Roll** - $34.99
   - *Why*: Supports your lower back while sitting
   - *Best for*: Office work, commuting
   - *Evidence*: Moderate clinical support

**2. Pro Balance Board** - $49.99
   - *Why*: Excellent for balance training at home
   - *Best for*: Daily balance exercises
   - *Evidence*: Strong research support

**3. Vitamin D3 + K2** - $24.99
   - *Why*: Supports bone and muscle health
   - *Note*: Consult doctor before starting supplements

**💡 For Pain Relief (if needed):**
- **ThermaRelief Heat Patches** - $18.99
  - Drug-free heat therapy
  - Great for muscle stiffness

**My Recommendation:**
Start with the **Lumbar Roll** - it's the most practical for immediate postural support while you work on exercises.

Would you like more details on any of these products?""",
            "function_calls": [{"name": "recommend_products", "arguments": {"condition": "back support"}, "result": {"count": 4}}],
            "citations": [],
            "suggested_questions": [
                "Where can I buy these?",
                "Are there cheaper alternatives?",
                "Which is most important?"
            ]
        }
    
    def _mock_general_exercises(self) -> Dict[str, Any]:
        """Generate general exercise recommendations"""
        return {
            "message": """Based on your assessment, here's a personalized exercise routine:

**🎯 Priority Areas:**
1. Balance (your biggest area for improvement)
2. Lumbar ROM (restricted mobility)

**📅 Recommended Weekly Routine:**

**Daily (5-10 minutes):**
- Single-Leg Stand: 3 sets × 30 seconds each leg
- Cat-Cow Stretch: 3 sets × 15 reps
- Heel-to-Toe Walk: 3 sets × 20 steps

**3x Per Week (15-20 minutes):**
- Chair Squats: 3 sets × 12 reps
- Wall Push-Ups: 3 sets × 15 reps
- Seated Spinal Twist: 3 sets × 30 seconds each side

**Tips for Success:**
✅ Start slow and build gradually
✅ Morning is often best for stretching
✅ Track your progress weekly
✅ Rest if you feel pain (not just discomfort)

Would you like detailed instructions for any specific exercise?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "Show me balance exercises",
                "How do I track progress?",
                "What if I miss a day?"
            ]
        }
    
    def _mock_greeting(self) -> Dict[str, Any]:
        """Generate greeting response"""
        return {
            "message": """Hello! 👋 I'm your MSK Wellness Coach. I'm here to help you understand your musculoskeletal health and improve it.

**I can help you with:**
- 📊 **Understanding your assessment** - What your scores mean
- 💪 **Exercise recommendations** - Personalized to your needs
- 📋 **Care programs** - Structured improvement plans
- 🛒 **Product suggestions** - Supplements and equipment

**Quick Look at Your Status:**
- Overall Score: 62/100 (Moderate Risk)
- Main Focus Areas: Balance, Lumbar ROM

What would you like to explore first?""",
            "function_calls": [],
            "citations": [],
            "suggested_questions": [
                "What does my report say?",
                "How can I improve my balance?",
                "Which care program should I follow?"
            ]
        }
    
    def _extract_suggested_questions(self, message: str) -> List[str]:
        """Extract suggested follow-up questions from response"""
        # Default suggestions based on common next steps
        return [
            "Tell me more about this",
            "What exercises should I do?",
            "Show me care programs"
        ]
