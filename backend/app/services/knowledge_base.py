"""
Knowledge Base Service - Stores exercises, care programs, and products
"""
from typing import List, Optional, Dict, Any
import json
import os

from app.schemas.recommendation import (
    CareProgram,
    Exercise,
    Product,
    Intensity,
    Difficulty,
    ProductType,
)


class KnowledgeBaseService:
    """
    In-memory knowledge base for MSK wellness data.
    In production, this would use ChromaDB for vector search.
    """
    
    def __init__(self):
        self.care_programs = self._load_care_programs()
        self.exercises = self._load_exercises()
        self.products = self._load_products()
    
    def _load_care_programs(self) -> List[Dict]:
        """Load care programs data"""
        return [
            {
                "program_id": "cp_001",
                "name": "Comprehensive MSK Wellness Program",
                "provider": "PhysioFirst Care Partners",
                "description": "12-week comprehensive program addressing balance, ROM, and strength with personalized progression tracking.",
                "focus_areas": ["balance", "rom", "strength", "flexibility"],
                "duration_weeks": 12,
                "intensity": "intermediate",
                "cost": 299.00,
            },
            {
                "program_id": "cp_002",
                "name": "Balance Mastery Program",
                "provider": "BalanceWell Institute",
                "description": "8-week intensive program focused on improving all aspects of balance including static, dynamic, and reactive balance.",
                "focus_areas": ["balance"],
                "duration_weeks": 8,
                "intensity": "beginner",
                "cost": 199.00,
            },
            {
                "program_id": "cp_003",
                "name": "Flexibility & ROM Recovery",
                "provider": "FlexCare Therapy",
                "description": "6-week program to restore and enhance range of motion through targeted stretching and mobility work.",
                "focus_areas": ["rom", "flexibility"],
                "duration_weeks": 6,
                "intensity": "beginner",
                "cost": 149.00,
            },
            {
                "program_id": "cp_004",
                "name": "Senior Strength & Stability",
                "provider": "ActiveAging Health",
                "description": "10-week program designed for adults 55+ to build functional strength and prevent falls.",
                "focus_areas": ["strength", "balance"],
                "duration_weeks": 10,
                "intensity": "beginner",
                "cost": 249.00,
            },
            {
                "program_id": "cp_005",
                "name": "Advanced Athletic Performance",
                "provider": "Elite MSK Training",
                "description": "16-week advanced program for athletes looking to optimize reaction time, power, and agility.",
                "focus_areas": ["reaction_time", "strength", "balance"],
                "duration_weeks": 16,
                "intensity": "advanced",
                "cost": 449.00,
            },
        ]
    
    def _load_exercises(self) -> List[Dict]:
        """Load exercises data"""
        return [
            # Balance exercises
            {
                "exercise_id": "ex_balance_001",
                "name": "Single-Leg Stand",
                "category": "balance",
                "target_parameters": ["balance_single_leg", "balance_dynamic"],
                "difficulty": "easy",
                "instructions": [
                    "Stand near a wall or sturdy chair for support",
                    "Shift weight to your right leg",
                    "Lift left foot 6-12 inches off the ground",
                    "Hold for 10-30 seconds",
                    "Repeat on opposite leg"
                ],
                "sets_reps": "3 sets x 30 seconds each leg",
                "frequency": "Daily",
                "safety_notes": [
                    "Use support if needed",
                    "Stop if experiencing dizziness",
                    "Ensure clear space around you"
                ],
                "video_url": None,
                "expected_timeline": "2-4 weeks for noticeable improvement"
            },
            {
                "exercise_id": "ex_balance_002",
                "name": "Heel-to-Toe Walk",
                "category": "balance",
                "target_parameters": ["balance_dynamic", "balance_tandem"],
                "difficulty": "easy",
                "instructions": [
                    "Stand with arms out to sides for balance",
                    "Place right heel directly in front of left toes",
                    "Walk forward in a straight line",
                    "Take 15-20 steps",
                    "Turn carefully and walk back"
                ],
                "sets_reps": "3 sets of 20 steps",
                "frequency": "5 times per week",
                "safety_notes": [
                    "Walk near a wall for support",
                    "Look ahead, not at your feet",
                    "Move slowly and deliberately"
                ],
                "video_url": None,
                "expected_timeline": "3-4 weeks for improvement"
            },
            {
                "exercise_id": "ex_balance_003",
                "name": "Balance Board Training",
                "category": "balance",
                "target_parameters": ["balance_dynamic", "proprioception"],
                "difficulty": "moderate",
                "instructions": [
                    "Stand on balance board with feet hip-width apart",
                    "Keep knees slightly bent",
                    "Try to keep board level",
                    "Hold position for 30-60 seconds",
                    "Progress to closing eyes"
                ],
                "sets_reps": "3 sets x 60 seconds",
                "frequency": "4 times per week",
                "safety_notes": [
                    "Have something sturdy nearby to grab",
                    "Start with small movements",
                    "Stop if you feel unstable"
                ],
                "video_url": None,
                "expected_timeline": "4-6 weeks for significant improvement"
            },
            # ROM exercises
            {
                "exercise_id": "ex_rom_001",
                "name": "Cat-Cow Stretch",
                "category": "rom",
                "target_parameters": ["rom_lumbar", "flexibility"],
                "difficulty": "easy",
                "instructions": [
                    "Start on hands and knees, spine neutral",
                    "Inhale: Drop belly, lift head and tailbone (Cow)",
                    "Exhale: Round spine up, tuck chin and tailbone (Cat)",
                    "Move slowly between positions",
                    "Repeat 10-15 times"
                ],
                "sets_reps": "3 sets of 15 repetitions",
                "frequency": "Daily",
                "safety_notes": [
                    "Move within comfortable range",
                    "Keep wrists under shoulders",
                    "Stop if you feel sharp pain"
                ],
                "video_url": None,
                "expected_timeline": "1-2 weeks to feel more mobile"
            },
            {
                "exercise_id": "ex_rom_002",
                "name": "Seated Spinal Twist",
                "category": "rom",
                "target_parameters": ["rom_lumbar", "rom_thoracic"],
                "difficulty": "easy",
                "instructions": [
                    "Sit with legs extended",
                    "Bend right knee, place foot outside left thigh",
                    "Place right hand behind you",
                    "Twist torso to the right",
                    "Hold for 30 seconds, then switch sides"
                ],
                "sets_reps": "3 sets of 30 seconds each side",
                "frequency": "Daily",
                "safety_notes": [
                    "Keep spine tall during twist",
                    "Don't force the stretch",
                    "Breathe deeply throughout"
                ],
                "video_url": None,
                "expected_timeline": "2-3 weeks for increased rotation"
            },
            # Reaction time exercises
            {
                "exercise_id": "ex_reaction_001",
                "name": "Ball Drop Catch",
                "category": "reaction_time",
                "target_parameters": ["reaction_time_simple", "reaction_time_choice"],
                "difficulty": "easy",
                "instructions": [
                    "Have a partner hold a tennis ball at shoulder height",
                    "Stand with hand at your side",
                    "Partner drops the ball without warning",
                    "Catch the ball before it bounces twice",
                    "Repeat 15-20 times"
                ],
                "sets_reps": "3 sets of 20 catches",
                "frequency": "3-4 times per week",
                "safety_notes": [
                    "Start close to partner and increase distance",
                    "Focus on the ball, not the hand",
                    "Stay relaxed between attempts"
                ],
                "video_url": None,
                "expected_timeline": "2-3 weeks for faster reactions"
            },
            # Strength exercises
            {
                "exercise_id": "ex_strength_001",
                "name": "Wall Push-Ups",
                "category": "strength",
                "target_parameters": ["strength_upper_body"],
                "difficulty": "easy",
                "instructions": [
                    "Stand arm's length from wall",
                    "Place palms on wall at shoulder height",
                    "Bend elbows, lowering chest toward wall",
                    "Push back to starting position",
                    "Keep body straight throughout"
                ],
                "sets_reps": "3 sets of 15 repetitions",
                "frequency": "3 times per week",
                "safety_notes": [
                    "Keep core engaged",
                    "Don't let elbows flare out too wide",
                    "Move in controlled manner"
                ],
                "video_url": None,
                "expected_timeline": "3-4 weeks for strength gains"
            },
            {
                "exercise_id": "ex_strength_002",
                "name": "Chair Squats",
                "category": "strength",
                "target_parameters": ["strength_lower_body", "balance_dynamic"],
                "difficulty": "easy",
                "instructions": [
                    "Stand in front of a sturdy chair",
                    "Feet hip-width apart, arms forward",
                    "Lower yourself until you lightly touch the chair",
                    "Stand back up immediately",
                    "Don't use momentum"
                ],
                "sets_reps": "3 sets of 12 repetitions",
                "frequency": "3 times per week",
                "safety_notes": [
                    "Keep knees over toes",
                    "Don't fully sit down",
                    "Use arms for balance if needed"
                ],
                "video_url": None,
                "expected_timeline": "3-4 weeks for improved leg strength"
            },
        ]
    
    def _load_products(self) -> List[Dict]:
        """Load products data"""
        return [
            {
                "product_id": "prod_001",
                "name": "ErgoSupport Lumbar Roll",
                "type": "ergonomic",
                "category": "back_support",
                "description": "Memory foam lumbar support for office chairs and car seats. Maintains natural spinal curve.",
                "use_cases": ["lower_back_pain", "poor_posture", "prolonged_sitting"],
                "price": 34.99,
                "evidence_level": "moderate"
            },
            {
                "product_id": "prod_002",
                "name": "Vitamin D3 + K2 Complex",
                "type": "supplement",
                "category": "bone_health",
                "description": "High-potency vitamin D3 (2000 IU) with K2 for optimal calcium absorption and bone health.",
                "use_cases": ["vitamin_d_deficiency", "bone_health", "muscle_function"],
                "price": 24.99,
                "evidence_level": "high"
            },
            {
                "product_id": "prod_003",
                "name": "ThermaRelief Heat Patches",
                "type": "pain_relief",
                "category": "topical_relief",
                "description": "Drug-free heat therapy patches providing up to 8 hours of continuous relief.",
                "use_cases": ["muscle_pain", "joint_stiffness", "back_pain"],
                "price": 18.99,
                "evidence_level": "moderate"
            },
            {
                "product_id": "prod_004",
                "name": "Pro Balance Board",
                "type": "recovery_tool",
                "category": "balance_training",
                "description": "Wooden balance board for improving stability, core strength, and proprioception.",
                "use_cases": ["balance_training", "core_strength", "rehabilitation"],
                "price": 49.99,
                "evidence_level": "high"
            },
            {
                "product_id": "prod_005",
                "name": "Omega-3 Fish Oil",
                "type": "supplement",
                "category": "joint_health",
                "description": "High-quality fish oil with EPA and DHA for joint health and inflammation support.",
                "use_cases": ["joint_pain", "inflammation", "general_wellness"],
                "price": 29.99,
                "evidence_level": "high"
            },
            {
                "product_id": "prod_006",
                "name": "Foam Roller - Medium Density",
                "type": "recovery_tool",
                "category": "self_massage",
                "description": "36-inch medium-density foam roller for myofascial release and muscle recovery.",
                "use_cases": ["muscle_tension", "flexibility", "recovery"],
                "price": 24.99,
                "evidence_level": "moderate"
            },
            {
                "product_id": "prod_007",
                "name": "Ergonomic Seat Cushion",
                "type": "ergonomic",
                "category": "seating",
                "description": "Premium gel-infused memory foam cushion for pressure relief and posture support.",
                "use_cases": ["sitting_discomfort", "tailbone_pain", "prolonged_sitting"],
                "price": 44.99,
                "evidence_level": "moderate"
            },
        ]
    
    def search_care_programs(
        self,
        focus_areas: Optional[List[str]] = None,
        intensity: Optional[Intensity] = None,
        limit: int = 5
    ) -> List[CareProgram]:
        """Search for matching care programs"""
        results = self.care_programs.copy()
        
        if focus_areas:
            results = [
                p for p in results
                if any(area in p["focus_areas"] for area in focus_areas)
            ]
        
        if intensity:
            results = [p for p in results if p["intensity"] == intensity.value]
        
        return [
            CareProgram(
                **{**p, "intensity": Intensity(p["intensity"])}
            )
            for p in results[:limit]
        ]
    
    def search_exercises(
        self,
        target_parameter: Optional[str] = None,
        difficulty: Optional[Difficulty] = None,
        limit: int = 10
    ) -> List[Exercise]:
        """Search for matching exercises"""
        results = self.exercises.copy()
        
        if target_parameter:
            # Match category or specific parameter
            results = [
                e for e in results
                if target_parameter in e["category"] or
                   any(target_parameter in p for p in e["target_parameters"])
            ]
        
        if difficulty:
            results = [e for e in results if e["difficulty"] == difficulty.value]
        
        return [
            Exercise(**{**e, "difficulty": Difficulty(e["difficulty"])})
            for e in results[:limit]
        ]
    
    def search_products(
        self,
        condition: Optional[str] = None,
        product_type: Optional[ProductType] = None,
        limit: int = 5
    ) -> List[Product]:
        """Search for matching products"""
        results = self.products.copy()
        
        if condition:
            condition_lower = condition.lower()
            results = [
                p for p in results
                if any(condition_lower in uc.lower() for uc in p["use_cases"]) or
                   condition_lower in p["description"].lower() or
                   condition_lower in p["category"].lower()
            ]
        
        if product_type:
            results = [p for p in results if p["type"] == product_type.value]
        
        return [
            Product(**{**p, "type": ProductType(p["type"])})
            for p in results[:limit]
        ]


# Singleton instance
knowledge_base = KnowledgeBaseService()
