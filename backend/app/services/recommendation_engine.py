"""
Enhanced Recommendation Engine using User Performance Data and Vector Search
"""
from typing import List, Dict, Any, Optional
import structlog

from app.services.vector_store import get_vector_store
from app.services.knowledge_base import knowledge_base

logger = structlog.get_logger()


class RecommendationEngine:
    """
    Intelligent recommendation engine that analyzes user performance data
    and provides personalized exercise recommendations
    """
    
    def __init__(self):
        try:
            self.vector_store = get_vector_store()
        except:
            self.vector_store = None
        self.kb = knowledge_base
    
    def generate_recommendations(
        self,
        user_performance_data: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized exercise recommendations based on user's performance data
        
        Args:
            user_performance_data: Dictionary containing user's game/sport performance metrics
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommended exercises with reasoning
        """
        try:
            # Analyze user data to identify needs
            analysis = self._analyze_performance(user_performance_data)
            
            # Generate search query based on analysis
            search_query = self._create_search_query(analysis)
            
            logger.info("generating_recommendations", 
                       query=search_query, 
                       focus_areas=analysis['focus_areas'])
            
            # Use vector search to find relevant exercises
            if self.vector_store:
                exercises = self.vector_store.search_exercises(
                    query=search_query,
                    n_results=limit * 2  # Get more to filter
                )
            else:
                # Fallback to basic filtering if vector store not available
                logger.info("using_fallback_no_vector_store")
                exercises = [{'id': ex.get('exercise_id', ''), 'metadata': {}} 
                           for ex in self.kb.exercises[:limit * 2]]
            
            # Enhance with detailed information and personalization
            recommendations = []
            for ex in exercises[:limit]:
                # Get full exercise details from knowledge base
                full_exercise = self._get_exercise_details(ex['id'])
                if full_exercise:
                    # Add personalization
                    full_exercise['recommendation_reason'] = self._generate_reason(
                        full_exercise, 
                        analysis
                    )
                    full_exercise['priority'] = self._calculate_priority(
                        full_exercise,
                        analysis
                    )
                    recommendations.append(full_exercise)
            
            # Sort by priority
            recommendations.sort(key=lambda x: x.get('priority', 0), reverse=True)
            
            logger.info("recommendations_generated", count=len(recommendations))
            return recommendations
            
        except Exception as e:
            logger.error("error_generating_recommendations", error=str(e))
            # Fallback to basic recommendations
            return self._get_fallback_recommendations(limit)
    
    def _analyze_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user performance data to identify strengths and weaknesses
        
        Returns analysis with focus areas and priorities
        """
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'focus_areas': [],
            'priority_metrics': []
        }
        
        # Define thresholds
        STRONG_THRESHOLD = 75
        WEAK_THRESHOLD = 50
        
        # Analyze each metric
        for metric, value in performance_data.items():
            if metric == 'custom_metrics':
                continue
                
            if isinstance(value, (int, float)):
                if value >= STRONG_THRESHOLD:
                    analysis['strengths'].append(metric)
                elif value < WEAK_THRESHOLD:
                    analysis['weaknesses'].append(metric)
                    analysis['priority_metrics'].append(metric)
        
        # Map metrics to exercise categories
        metric_to_category = {
            'reaction_time': 'reaction_time',
            'accuracy': 'balance',  # Better hand-eye coordination
            'endurance': 'strength',
            'strength': 'strength',
            'flexibility': 'rom',
            'balance': 'balance'
        }
        
        # Determine focus areas based on weaknesses
        for weakness in analysis['weaknesses']:
            category = metric_to_category.get(weakness)
            if category and category not in analysis['focus_areas']:
                analysis['focus_areas'].append(category)
        
        # If no weaknesses, focus on maintaining strengths
        if not analysis['focus_areas']:
            for strength in analysis['strengths']:
                category = metric_to_category.get(strength)
                if category and category not in analysis['focus_areas']:
                    analysis['focus_areas'].append(category)
        
        # Add general fitness if no specific areas identified
        if not analysis['focus_areas']:
            analysis['focus_areas'] = ['strength', 'balance', 'rom']
        
        return analysis
    
    def _create_search_query(self, analysis: Dict[str, Any]) -> str:
        """Create a natural language search query from analysis"""
        
        focus_areas = analysis['focus_areas']
        weaknesses = analysis['weaknesses']
        
        query_parts = []
        
        # Add focus on weaknesses
        if weaknesses:
            weakness_text = ', '.join(weaknesses)
            query_parts.append(f"Exercises to improve {weakness_text}")
        
        # Add focus areas
        if focus_areas:
            area_text = ' and '.join(focus_areas)
            query_parts.append(f"for {area_text} development")
        
        # Default query
        if not query_parts:
            query_parts.append("General fitness exercises for gamers and athletes")
        
        query = ' '.join(query_parts)
        return query
    
    def _get_exercise_details(self, exercise_id: str) -> Optional[Dict[str, Any]]:
        """Get full exercise details from knowledge base"""
        for exercise in self.kb.exercises:
            if exercise.get('exercise_id') == exercise_id:
                return exercise.copy()
        return None
    
    def _generate_reason(self, exercise: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate personalized reason for recommending this exercise"""
        
        category = exercise.get('category', '')
        weaknesses = analysis.get('weaknesses', [])
        
        reason_templates = {
            'reaction_time': "This exercise will help improve your reaction speed and quick decision-making skills.",
            'balance': "Enhancing your balance and stability will improve your overall coordination and accuracy.",
            'strength': "Building strength will increase your endurance and reduce fatigue during long gaming/training sessions.",
            'rom': "Improving flexibility and range of motion will help prevent injuries and enhance your movement quality."
        }
        
        # Get reason based on category
        reason = reason_templates.get(category, "This exercise will contribute to your overall fitness and performance.")
        
        # Add specific weakness mention if relevant
        if weaknesses:
            weakness_match = [w for w in weaknesses if w in category or category in w]
            if weakness_match:
                reason += f" Specifically targets your {weakness_match[0]} development."
        
        return reason
    
    def _calculate_priority(self, exercise: Dict[str, Any], analysis: Dict[str, Any]) -> int:
        """Calculate priority score for the exercise"""
        
        priority = 50  # Base priority
        
        category = exercise.get('category', '')
        difficulty = exercise.get('difficulty', 'intermediate')
        
        # Higher priority for focus areas
        if category in analysis.get('focus_areas', []):
            priority += 30
        
        # Adjust for difficulty (prefer easier exercises for beginners)
        if difficulty == 'easy':
            priority += 10
        elif difficulty == 'intermediate':
            priority += 5
        
        # Bonus for addressing multiple weaknesses
        target_params = exercise.get('target_parameters', [])
        weaknesses = analysis.get('weaknesses', [])
        
        for weakness in weaknesses:
            if any(weakness in param for param in target_params):
                priority += 15
        
        return priority
    
    def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Get basic recommendations as fallback"""
        logger.info("using_fallback_recommendations")
        return self.kb.exercises[:limit]
    
    def get_care_programs_for_user(
        self,
        user_performance_data: Dict[str, Any],
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Recommend care programs based on user performance
        """
        try:
            analysis = self._analyze_performance(user_performance_data)
            focus_areas = analysis['focus_areas']
            
            # Find matching care programs
            matching_programs = []
            
            for program in self.kb.care_programs:
                program_areas = program.get('focus_areas', [])
                
                # Calculate match score
                match_score = len(set(focus_areas) & set(program_areas))
                
                if match_score > 0:
                    program_copy = program.copy()
                    program_copy['match_score'] = match_score
                    program_copy['recommended_reason'] = f"Addresses your focus areas: {', '.join(program_areas)}"
                    matching_programs.append(program_copy)
            
            # Sort by match score
            matching_programs.sort(key=lambda x: x['match_score'], reverse=True)
            
            return matching_programs[:limit]
            
        except Exception as e:
            logger.error("error_recommending_care_programs", error=str(e))
            return self.kb.care_programs[:limit]


# Global instance
_recommendation_engine: Optional[RecommendationEngine] = None


def get_recommendation_engine() -> RecommendationEngine:
    """Get or create the global RecommendationEngine instance"""
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine
