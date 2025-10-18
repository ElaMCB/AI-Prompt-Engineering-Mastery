"""
Progress Tracking System for Prompt Engineering Course
Tracks skills, assessments, and portfolio completion
"""

import json
import datetime
from typing import Dict, List
from pathlib import Path

class ProgressTracker:
    def __init__(self, student_name: str = "Student"):
        self.student_name = student_name
        self.progress_file = Path("progress.json")
        self.skills_matrix = {
            "week1_foundations": {
                "prompt_debugging": 0,
                "clear_framework": 0,
                "context_setting": 0,
                "audience_targeting": 0,
                "requirement_specification": 0
            },
            "week2_context": {
                "domain_knowledge": 0,
                "data_integration": 0,
                "business_context": 0,
                "industry_specificity": 0
            },
            "week3_agents": {
                "tool_integration": 0,
                "decision_making": 0,
                "workflow_design": 0,
                "error_handling": 0
            },
            "week4_production": {
                "version_control": 0,
                "ab_testing": 0,
                "performance_monitoring": 0,
                "deployment": 0
            }
        }
        self.load_progress()
    
    def load_progress(self):
        """Load existing progress or create new file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                self.skills_matrix = data.get('skills_matrix', self.skills_matrix)
                self.assessments = data.get('assessments', {})
                self.projects = data.get('projects', {})
        else:
            self.assessments = {}
            self.projects = {}
    
    def save_progress(self):
        """Save current progress to file"""
        data = {
            'student_name': self.student_name,
            'last_updated': datetime.datetime.now().isoformat(),
            'skills_matrix': self.skills_matrix,
            'assessments': self.assessments,
            'projects': self.projects
        }
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_skill(self, week: str, skill: str, score: float):
        """Update a specific skill score (0-1)"""
        if week in self.skills_matrix and skill in self.skills_matrix[week]:
            self.skills_matrix[week][skill] = max(self.skills_matrix[week][skill], score)
            self.save_progress()
            return True
        return False
    
    def record_assessment(self, week: str, assessment_type: str, score: float, details: Dict = None):
        """Record assessment results"""
        if week not in self.assessments:
            self.assessments[week] = {}
        
        self.assessments[week][assessment_type] = {
            'score': score,
            'date': datetime.datetime.now().isoformat(),
            'details': details or {}
        }
        self.save_progress()
    
    def complete_project(self, project_name: str, description: str, github_link: str = None):
        """Mark a project as completed"""
        self.projects[project_name] = {
            'description': description,
            'completed_date': datetime.datetime.now().isoformat(),
            'github_link': github_link,
            'status': 'completed'
        }
        self.save_progress()
    
    def get_overall_progress(self) -> Dict:
        """Calculate overall progress statistics"""
        total_skills = sum(len(week_skills) for week_skills in self.skills_matrix.values())
        completed_skills = sum(
            sum(1 for score in week_skills.values() if score >= 0.7)
            for week_skills in self.skills_matrix.values()
        )
        
        skill_progress = completed_skills / total_skills if total_skills > 0 else 0
        
        assessment_progress = len(self.assessments) / 4  # 4 weeks
        project_progress = len([p for p in self.projects.values() if p['status'] == 'completed']) / 4  # 4 projects
        
        overall = (skill_progress + assessment_progress + project_progress) / 3
        
        return {
            'overall_progress': round(overall * 100, 1),
            'skills_mastered': f"{completed_skills}/{total_skills}",
            'assessments_completed': f"{len(self.assessments)}/4",
            'projects_completed': f"{len([p for p in self.projects.values() if p['status'] == 'completed'])}/4",
            'next_milestone': self._get_next_milestone()
        }
    
    def _get_next_milestone(self) -> str:
        """Determine what the student should focus on next"""
        week_progress = {}
        for week, skills in self.skills_matrix.items():
            mastered = sum(1 for score in skills.values() if score >= 0.7)
            total = len(skills)
            week_progress[week] = mastered / total
        
        for week, progress in week_progress.items():
            if progress < 0.8:  # Less than 80% mastered
                return f"Focus on {week.replace('_', ' ').title()}"
        
        return "Ready for advanced projects!"
    
    def generate_skill_report(self) -> str:
        """Generate a detailed skill progress report"""
        report = f"\n📊 SKILL PROGRESS REPORT - {self.student_name}\n"
        report += "=" * 50 + "\n\n"
        
        for week, skills in self.skills_matrix.items():
            week_name = week.replace('_', ' ').title()
            report += f"🗓️  {week_name}:\n"
            
            for skill, score in skills.items():
                skill_name = skill.replace('_', ' ').title()
                progress_bar = self._create_progress_bar(score)
                status = "✅ Mastered" if score >= 0.7 else "🔄 In Progress" if score > 0 else "⏳ Not Started"
                report += f"   {skill_name}: {progress_bar} {score:.1%} {status}\n"
            
            report += "\n"
        
        return report
    
    def _create_progress_bar(self, score: float, length: int = 10) -> str:
        """Create a visual progress bar"""
        filled = int(score * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    def generate_certificate(self, week: str) -> str:
        """Generate a completion certificate for a week"""
        week_skills = self.skills_matrix.get(week, {})
        mastery_rate = sum(1 for score in week_skills.values() if score >= 0.7) / len(week_skills)
        
        if mastery_rate >= 0.8:
            certificate = f"""
🏆 CERTIFICATE OF COMPLETION 🏆

This certifies that {self.student_name} has successfully completed
{week.replace('_', ' ').title()} of the Prompt Engineering Mastery Course

Skills Mastered: {mastery_rate:.1%}
Date: {datetime.datetime.now().strftime('%B %d, %Y')}

Verified competencies:
"""
            for skill, score in week_skills.items():
                if score >= 0.7:
                    certificate += f"✓ {skill.replace('_', ' ').title()}\n"
            
            return certificate
        else:
            return f"Complete {week} with 80% skill mastery to earn certificate. Current: {mastery_rate:.1%}"

# Example usage
if __name__ == "__main__":
    tracker = ProgressTracker("Elena")
    
    # Simulate some progress
    tracker.update_skill("week1_foundations", "prompt_debugging", 0.8)
    tracker.update_skill("week1_foundations", "clear_framework", 0.9)
    tracker.record_assessment("week1_foundations", "broken_prompts_challenge", 0.85)
    tracker.complete_project("customer_support_bot", "AI chatbot for handling customer inquiries")
    
    # Generate reports
    print(tracker.generate_skill_report())
    print("\nOverall Progress:", tracker.get_overall_progress())
    print("\nCertificate:", tracker.generate_certificate("week1_foundations"))