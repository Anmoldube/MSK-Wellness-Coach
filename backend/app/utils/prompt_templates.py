"""
Prompt Templates for Claude LLM Integration
"""

# Main System Prompt
SYSTEM_PROMPT = """You are an expert musculoskeletal (MSK) wellness coach AI assistant. Your role is to help users understand their MSK assessment results and provide personalized recommendations for improvement.

## Your Capabilities
- Analyze and explain MSK assessment parameters (Balance, Reaction Time, ROM, Strength, etc.)
- Recommend personalized care programs based on user needs
- Suggest specific exercises to improve deficiencies
- Recommend supportive products (nutraceuticals, ergonomic aids)
- Provide evidence-based health information
- Track conversation context for coherent multi-turn dialogues

## Guidelines
1. Always base recommendations on the user's actual assessment data when available
2. Be encouraging and supportive while being honest about areas needing improvement
3. Explain medical/technical terms in simple language
4. Prioritize safety - always mention contraindications and when to consult healthcare providers
5. Use the available tools to retrieve accurate, up-to-date information
6. Cite sources when providing specific medical or exercise information
7. If uncertain, acknowledge limitations and suggest consulting a healthcare professional

## Response Format
- Be conversational and empathetic
- Use markdown formatting for better readability
- Use bullet points for lists of exercises/programs/products
- Include actionable next steps
- Offer 2-3 follow-up questions to guide the conversation
- Use emojis sparingly to add warmth (📊 💪 ✅ ⚠️)

## Important Disclaimers
- You are not a replacement for professional medical advice
- Always recommend consulting healthcare providers for medical concerns
- Do not diagnose conditions or prescribe medications

## Parameter Definitions
- **Balance (Dynamic)**: Ability to maintain equilibrium during movement (score 0-10)
- **Balance (Single-Leg)**: Time able to stand on one leg (seconds)
- **Balance (Tandem)**: Ability to maintain heel-to-toe stance
- **Reaction Time (Simple)**: Response time to single stimulus (milliseconds, lower is better)
- **Reaction Time (Choice)**: Response time when selecting between options (milliseconds)
- **ROM (Range of Motion)**: Joint flexibility measured in degrees
- **Strength**: Muscular force production capability

## Risk Levels
- **Low Risk**: Overall score 75-100, minimal intervention needed
- **Moderate Risk**: Overall score 50-74, targeted improvement recommended
- **High Risk**: Overall score below 50, comprehensive program recommended"""


# User Context Template
USER_CONTEXT_TEMPLATE = """
[User's Latest MSK Assessment - {assessment_date}]
Overall Score: {overall_score}/100
Risk Level: {risk_level}

Key Parameters:
{parameters_summary}

Areas of Concern:
{areas_of_concern}
"""


# Parameter Interpretation Prompt
PARAMETER_INTERPRETATION_PROMPT = """
Analyze the following MSK parameter and provide:
1. What this parameter measures
2. The user's current status relative to normal ranges
3. Potential impact on daily activities
4. Recommended focus level (high/medium/low priority)

Parameter: {parameter_name}
Value: {value} {unit}
Reference Range: {ref_min} - {ref_max} {unit}
Percentile: {percentile}th
"""


# Exercise Recommendation Prompt
EXERCISE_RECOMMENDATION_PROMPT = """
Based on the user's {target_parameter} score of {current_value}, recommend appropriate exercises.

Consider:
- User's current fitness level (based on overall score: {overall_score}/100)
- Safety precautions for someone with {risk_level} risk
- Progressive difficulty from beginner to advanced
- Frequency and duration appropriate for improvement

Provide 3-5 exercises with clear instructions.
"""


# Care Program Matching Prompt
CARE_PROGRAM_MATCHING_PROMPT = """
Match the user with appropriate care programs based on their assessment:

User Profile:
- Overall Score: {overall_score}/100
- Risk Level: {risk_level}
- Problem Areas: {problem_areas}
- Focus Needed: {focus_areas}

Consider:
- Program intensity vs user's current level
- Duration and commitment required
- Cost-effectiveness
- Expected outcomes and timelines

Recommend the top 1-2 programs with clear reasoning.
"""


# Product Recommendation Prompt
PRODUCT_RECOMMENDATION_PROMPT = """
Recommend products for the user based on their condition:

Condition: {condition}
Relevant Parameters: {relevant_parameters}
Current Issues: {current_issues}

Guidelines:
- Prioritize evidence-based products
- Consider user's specific needs
- Include price range when available
- Mention any contraindications
- Suggest usage instructions

Provide 2-4 product recommendations with rationale.
"""


# Follow-up Questions Templates
FOLLOW_UP_QUESTIONS = {
    "report_analysis": [
        "Would you like me to explain any specific parameter in detail?",
        "Should I recommend exercises for your priority areas?",
        "Would you like to see care program options?"
    ],
    "balance": [
        "Want me to show you specific balance exercises?",
        "Should I recommend a balance-focused care program?",
        "Would you like tips for practicing balance at home?"
    ],
    "rom": [
        "Should I show you stretches for flexibility?",
        "Would you like product recommendations for ROM improvement?",
        "Want to see a ROM-focused care program?"
    ],
    "exercise": [
        "Want more advanced progressions for these exercises?",
        "Should I recommend equipment to help with these?",
        "Would you like a weekly routine schedule?"
    ],
    "program": [
        "Would you like more details about this program?",
        "Should I compare this with other options?",
        "Do you want to know the enrollment process?"
    ],
    "product": [
        "Would you like more details on any of these products?",
        "Should I suggest complementary products?",
        "Want to see exercises to use with these products?"
    ],
    "general": [
        "What would you like to focus on improving?",
        "Do you have any specific concerns about your health?",
        "Would you like to see your assessment summary?"
    ]
}


def get_follow_up_questions(category: str) -> list:
    """Get follow-up questions for a given category"""
    return FOLLOW_UP_QUESTIONS.get(category, FOLLOW_UP_QUESTIONS["general"])


def format_user_context(report: dict) -> str:
    """Format user's report data into context string"""
    if not report:
        return ""
    
    # Build parameters summary
    params_summary = []
    areas_of_concern = []
    
    for param in report.get("parameters", []):
        name = param.get("parameter_name", "Unknown")
        value = param.get("value", "N/A")
        unit = param.get("unit", "")
        percentile = param.get("percentile", 50)
        interpretation = param.get("interpretation", "")
        
        params_summary.append(f"- {name}: {value} {unit} ({percentile}th percentile)")
        
        # Flag areas below 40th percentile as concerns
        if percentile and percentile < 40:
            areas_of_concern.append(f"- {name}: {interpretation or 'Below average'}")
    
    return USER_CONTEXT_TEMPLATE.format(
        assessment_date=report.get("assessment_date", "N/A"),
        overall_score=report.get("overall_score", "N/A"),
        risk_level=report.get("risk_level", "Unknown").upper(),
        parameters_summary="\n".join(params_summary) or "No parameters available",
        areas_of_concern="\n".join(areas_of_concern) or "None identified"
    )
