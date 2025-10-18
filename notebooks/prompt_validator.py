"""
Prompt Engineering Validation System
Provides immediate feedback on prompt quality
"""

import re
from typing import Dict, List, Tuple

class PromptValidator:
    def __init__(self):
        self.clear_framework = {
            'context': ['you are', 'act as', 'imagine you', 'role'],
            'length': ['words', 'sentences', 'paragraphs', 'pages', 'characters'],
            'examples': ['example', 'like this', 'format', 'style', 'similar to'],
            'audience': ['audience', 'target', 'for people who', 'readers who'],
            'requirements': ['must include', 'requirements', 'should contain', 'needs to']
        }
    
    def score_prompt(self, prompt: str) -> Dict:
        """Score a prompt based on CLEAR framework and best practices"""
        prompt_lower = prompt.lower()
        
        scores = {
            'context_score': self._check_context(prompt_lower),
            'length_score': self._check_length_specification(prompt_lower),
            'examples_score': self._check_examples(prompt_lower),
            'audience_score': self._check_audience(prompt_lower),
            'requirements_score': self._check_requirements(prompt_lower),
            'specificity_score': self._check_specificity(prompt),
            'clarity_score': self._check_clarity(prompt)
        }
        
        overall_score = sum(scores.values()) / len(scores)
        
        return {
            'overall_score': round(overall_score, 2),
            'breakdown': scores,
            'feedback': self._generate_feedback(scores, prompt),
            'grade': self._get_grade(overall_score)
        }
    
    def _check_context(self, prompt: str) -> float:
        """Check if prompt sets proper context/role"""
        context_indicators = self.clear_framework['context']
        found = sum(1 for indicator in context_indicators if indicator in prompt)
        return min(found * 0.5, 1.0)
    
    def _check_length_specification(self, prompt: str) -> float:
        """Check if prompt specifies output length"""
        length_indicators = self.clear_framework['length']
        found = sum(1 for indicator in length_indicators if indicator in prompt)
        return min(found * 0.5, 1.0)
    
    def _check_examples(self, prompt: str) -> float:
        """Check if prompt provides examples or format guidance"""
        example_indicators = self.clear_framework['examples']
        found = sum(1 for indicator in example_indicators if indicator in prompt)
        return min(found * 0.3, 1.0)
    
    def _check_audience(self, prompt: str) -> float:
        """Check if prompt defines target audience"""
        audience_indicators = self.clear_framework['audience']
        found = sum(1 for indicator in audience_indicators if indicator in prompt)
        return min(found * 0.4, 1.0)
    
    def _check_requirements(self, prompt: str) -> float:
        """Check if prompt lists specific requirements"""
        req_indicators = self.clear_framework['requirements']
        found = sum(1 for indicator in req_indicators if indicator in prompt)
        return min(found * 0.3, 1.0)
    
    def _check_specificity(self, prompt: str) -> float:
        """Check for specific vs vague language"""
        vague_words = ['good', 'nice', 'great', 'awesome', 'help', 'some', 'thing']
        specific_words = ['exactly', 'specifically', 'must', 'should', 'include', 'format']
        
        vague_count = sum(1 for word in vague_words if word in prompt.lower())
        specific_count = sum(1 for word in specific_words if word in prompt.lower())
        
        if len(prompt.split()) == 0:
            return 0
        
        specificity_ratio = specific_count / max(len(prompt.split()) * 0.1, 1)
        vague_penalty = vague_count / max(len(prompt.split()) * 0.1, 1)
        
        return max(0, min(1, specificity_ratio - vague_penalty))
    
    def _check_clarity(self, prompt: str) -> float:
        """Check for clear, actionable language"""
        sentences = prompt.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Optimal sentence length is 15-25 words
        if 15 <= avg_sentence_length <= 25:
            return 1.0
        elif 10 <= avg_sentence_length <= 30:
            return 0.8
        else:
            return 0.5
    
    def _generate_feedback(self, scores: Dict, prompt: str) -> List[str]:
        """Generate specific feedback for improvement"""
        feedback = []
        
        if scores['context_score'] < 0.5:
            feedback.append("🎭 Add a clear role: 'You are a [specific role]...'")
        
        if scores['length_score'] < 0.5:
            feedback.append("📏 Specify output length: '200 words', '3 paragraphs', etc.")
        
        if scores['audience_score'] < 0.5:
            feedback.append("👥 Define your audience: 'for [specific group] who [specific situation]'")
        
        if scores['requirements_score'] < 0.5:
            feedback.append("✅ List specific requirements: 'Must include...', 'Should contain...'")
        
        if scores['specificity_score'] < 0.5:
            feedback.append("🎯 Be more specific: Replace vague words with concrete details")
        
        if scores['clarity_score'] < 0.7:
            feedback.append("💡 Improve clarity: Use shorter, clearer sentences")
        
        if not feedback:
            feedback.append("🎉 Great prompt! This follows best practices.")
        
        return feedback
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C (Needs Improvement)"
        else:
            return "D (Poor - Needs Major Revision)"

# Example usage and testing
if __name__ == "__main__":
    validator = PromptValidator()
    
    # Test with a bad prompt
    bad_prompt = "Write me something good about marketing"
    result = validator.score_prompt(bad_prompt)
    print(f"Bad Prompt Score: {result['overall_score']} - {result['grade']}")
    print("Feedback:", result['feedback'])
    
    # Test with a good prompt
    good_prompt = """You are a conversion copywriter specializing in SaaS email marketing. 
    Write a 200-word welcome email for new trial users of a project management tool. 
    Target audience: small business owners who just signed up but haven't logged in yet. 
    Must include: specific next steps, one key benefit, and a clear call-to-action. 
    Tone should be friendly but professional."""
    
    result = validator.score_prompt(good_prompt)
    print(f"\nGood Prompt Score: {result['overall_score']} - {result['grade']}")
    print("Feedback:", result['feedback'])