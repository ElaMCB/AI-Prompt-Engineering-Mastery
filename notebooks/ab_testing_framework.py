"""
A/B Testing Framework for Prompt Engineering
Compare different prompt versions and track performance
"""

import json
import random
import statistics
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class PromptTest:
    test_id: str
    prompt_a: str
    prompt_b: str
    metric: str  # 'quality', 'relevance', 'completeness', etc.
    description: str
    created_date: str
    
@dataclass
class TestResult:
    test_id: str
    prompt_version: str  # 'A' or 'B'
    score: float  # 1-10 scale
    response_text: str
    timestamp: str
    notes: Optional[str] = None

class PromptABTester:
    def __init__(self):
        self.tests: Dict[str, PromptTest] = {}
        self.results: List[TestResult] = []
        self.load_data()
    
    def create_test(self, test_id: str, prompt_a: str, prompt_b: str, 
                   metric: str, description: str) -> PromptTest:
        """Create a new A/B test"""
        test = PromptTest(
            test_id=test_id,
            prompt_a=prompt_a,
            prompt_b=prompt_b,
            metric=metric,
            description=description,
            created_date=datetime.now().isoformat()
        )
        self.tests[test_id] = test
        self.save_data()
        return test
    
    def get_random_prompt(self, test_id: str) -> Tuple[str, str]:
        """Get a random prompt version for testing"""
        if test_id not in self.tests:
            raise ValueError(f"Test {test_id} not found")
        
        test = self.tests[test_id]
        version = random.choice(['A', 'B'])
        prompt = test.prompt_a if version == 'A' else test.prompt_b
        return version, prompt
    
    def record_result(self, test_id: str, prompt_version: str, score: float, 
                     response_text: str, notes: str = None):
        """Record a test result"""
        result = TestResult(
            test_id=test_id,
            prompt_version=prompt_version,
            score=score,
            response_text=response_text,
            timestamp=datetime.now().isoformat(),
            notes=notes
        )
        self.results.append(result)
        self.save_data()
    
    def analyze_test(self, test_id: str) -> Dict:
        """Analyze results for a specific test"""
        test_results = [r for r in self.results if r.test_id == test_id]
        
        if not test_results:
            return {"error": "No results found for this test"}
        
        a_scores = [r.score for r in test_results if r.prompt_version == 'A']
        b_scores = [r.score for r in test_results if r.prompt_version == 'B']
        
        if not a_scores or not b_scores:
            return {"error": "Need results for both prompt versions"}
        
        analysis = {
            "test_id": test_id,
            "total_results": len(test_results),
            "prompt_a": {
                "count": len(a_scores),
                "mean_score": round(statistics.mean(a_scores), 2),
                "median_score": round(statistics.median(a_scores), 2),
                "std_dev": round(statistics.stdev(a_scores) if len(a_scores) > 1 else 0, 2)
            },
            "prompt_b": {
                "count": len(b_scores),
                "mean_score": round(statistics.mean(b_scores), 2),
                "median_score": round(statistics.median(b_scores), 2),
                "std_dev": round(statistics.stdev(b_scores) if len(b_scores) > 1 else 0, 2)
            }
        }
        
        # Determine winner
        a_mean = analysis["prompt_a"]["mean_score"]
        b_mean = analysis["prompt_b"]["mean_score"]
        
        if abs(a_mean - b_mean) < 0.5:  # Close results
            analysis["winner"] = "Tie (difference < 0.5 points)"
            analysis["confidence"] = "Low"
        else:
            winner = "A" if a_mean > b_mean else "B"
            difference = abs(a_mean - b_mean)
            analysis["winner"] = f"Prompt {winner} (by {difference:.1f} points)"
            analysis["confidence"] = "High" if difference > 1.0 else "Medium"
        
        # Statistical significance (simplified)
        min_sample_size = 10
        if len(a_scores) >= min_sample_size and len(b_scores) >= min_sample_size:
            analysis["statistical_significance"] = "Sufficient sample size"
        else:
            analysis["statistical_significance"] = f"Need {min_sample_size - min(len(a_scores), len(b_scores))} more results"
        
        return analysis
    
    def generate_report(self, test_id: str) -> str:
        """Generate a formatted report for a test"""
        if test_id not in self.tests:
            return f"Test {test_id} not found"
        
        test = self.tests[test_id]
        analysis = self.analyze_test(test_id)
        
        if "error" in analysis:
            return f"Cannot generate report: {analysis['error']}"
        
        report = f"""
📊 A/B TEST REPORT: {test_id}
{'=' * 50}

📝 Description: {test.description}
📏 Metric: {test.metric}
📅 Created: {test.created_date[:10]}

🅰️  PROMPT A RESULTS:
   Sample Size: {analysis['prompt_a']['count']}
   Average Score: {analysis['prompt_a']['mean_score']}/10
   Median Score: {analysis['prompt_a']['median_score']}/10
   Consistency: {10 - analysis['prompt_a']['std_dev']:.1f}/10

🅱️  PROMPT B RESULTS:
   Sample Size: {analysis['prompt_b']['count']}
   Average Score: {analysis['prompt_b']['mean_score']}/10
   Median Score: {analysis['prompt_b']['median_score']}/10
   Consistency: {10 - analysis['prompt_b']['std_dev']:.1f}/10

🏆 WINNER: {analysis['winner']}
🎯 Confidence: {analysis['confidence']}
📈 Statistical Significance: {analysis['statistical_significance']}

💡 RECOMMENDATION:
"""
        
        # Add recommendation
        if "Prompt A" in analysis['winner']:
            report += "Use Prompt A for production. It shows better performance."
        elif "Prompt B" in analysis['winner']:
            report += "Use Prompt B for production. It shows better performance."
        else:
            report += "Both prompts perform similarly. Choose based on other factors (cost, speed, etc.)"
        
        return report
    
    def list_tests(self) -> List[Dict]:
        """List all tests with basic info"""
        test_list = []
        for test_id, test in self.tests.items():
            result_count = len([r for r in self.results if r.test_id == test_id])
            test_list.append({
                "test_id": test_id,
                "description": test.description,
                "metric": test.metric,
                "results_count": result_count,
                "created_date": test.created_date[:10]
            })
        return test_list
    
    def save_data(self):
        """Save tests and results to file"""
        data = {
            "tests": {tid: asdict(test) for tid, test in self.tests.items()},
            "results": [asdict(result) for result in self.results]
        }
        with open("ab_test_data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load tests and results from file"""
        try:
            with open("ab_test_data.json", "r") as f:
                data = json.load(f)
                
            # Load tests
            for tid, test_data in data.get("tests", {}).items():
                self.tests[tid] = PromptTest(**test_data)
            
            # Load results
            for result_data in data.get("results", []):
                self.results.append(TestResult(**result_data))
                
        except FileNotFoundError:
            pass  # No existing data

# Example usage and demo
if __name__ == "__main__":
    tester = PromptABTester()
    
    # Create a test
    test = tester.create_test(
        test_id="email_subject_test",
        prompt_a="Write a subject line for our newsletter",
        prompt_b="You're an email marketing expert. Write a compelling subject line for our weekly newsletter targeting small business owners. Focus on urgency and value. Keep under 50 characters.",
        metric="click_through_rate",
        description="Testing generic vs specific prompt for email subject lines"
    )
    
    # Simulate some results
    tester.record_result("email_subject_test", "A", 4.2, "Weekly Newsletter #47")
    tester.record_result("email_subject_test", "B", 7.8, "5 Growth Hacks That Doubled Revenue This Week")
    tester.record_result("email_subject_test", "A", 3.9, "Newsletter Update")
    tester.record_result("email_subject_test", "B", 8.1, "Stop Losing Customers: 3 Fixes You Can Do Today")
    
    # Generate report
    print(tester.generate_report("email_subject_test"))
    print("\nAll Tests:", tester.list_tests())