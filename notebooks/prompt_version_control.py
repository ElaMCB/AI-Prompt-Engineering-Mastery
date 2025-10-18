"""
Version Control System for Prompts
Track changes, rollbacks, and performance across prompt versions
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class PromptVersion:
    version_id: str
    prompt_text: str
    description: str
    author: str
    timestamp: str
    parent_version: Optional[str] = None
    performance_metrics: Optional[Dict] = None
    tags: Optional[List[str]] = None

class PromptVersionControl:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.versions: Dict[str, PromptVersion] = {}
        self.current_version: Optional[str] = None
        self.branches: Dict[str, str] = {"main": None}  # branch_name -> latest_version_id
        self.current_branch = "main"
        self.load_project()
    
    def create_version(self, prompt_text: str, description: str, author: str, 
                      tags: List[str] = None) -> str:
        """Create a new version of the prompt"""
        # Generate version ID based on content hash
        content_hash = hashlib.md5(prompt_text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_id = f"v_{timestamp}_{content_hash}"
        
        version = PromptVersion(
            version_id=version_id,
            prompt_text=prompt_text,
            description=description,
            author=author,
            timestamp=datetime.now().isoformat(),
            parent_version=self.current_version,
            tags=tags or []
        )
        
        self.versions[version_id] = version
        self.current_version = version_id
        self.branches[self.current_branch] = version_id
        self.save_project()
        
        return version_id
    
    def get_version(self, version_id: str) -> Optional[PromptVersion]:
        """Get a specific version"""
        return self.versions.get(version_id)
    
    def get_current_prompt(self) -> Optional[str]:
        """Get the current prompt text"""
        if self.current_version:
            return self.versions[self.current_version].prompt_text
        return None
    
    def rollback_to_version(self, version_id: str) -> bool:
        """Rollback to a specific version"""
        if version_id in self.versions:
            self.current_version = version_id
            self.branches[self.current_branch] = version_id
            self.save_project()
            return True
        return False
    
    def create_branch(self, branch_name: str, from_version: str = None) -> bool:
        """Create a new branch"""
        if branch_name in self.branches:
            return False
        
        base_version = from_version or self.current_version
        self.branches[branch_name] = base_version
        self.save_project()
        return True
    
    def switch_branch(self, branch_name: str) -> bool:
        """Switch to a different branch"""
        if branch_name in self.branches:
            self.current_branch = branch_name
            self.current_version = self.branches[branch_name]
            return True
        return False
    
    def merge_branch(self, source_branch: str, target_branch: str = None) -> bool:
        """Merge one branch into another"""
        target_branch = target_branch or self.current_branch
        
        if source_branch not in self.branches or target_branch not in self.branches:
            return False
        
        source_version = self.branches[source_branch]
        if source_version:
            self.branches[target_branch] = source_version
            if target_branch == self.current_branch:
                self.current_version = source_version
            self.save_project()
            return True
        return False
    
    def update_performance_metrics(self, version_id: str, metrics: Dict) -> bool:
        """Update performance metrics for a version"""
        if version_id in self.versions:
            if self.versions[version_id].performance_metrics is None:
                self.versions[version_id].performance_metrics = {}
            self.versions[version_id].performance_metrics.update(metrics)
            self.save_project()
            return True
        return False
    
    def get_version_history(self) -> List[Dict]:
        """Get chronological history of versions"""
        history = []
        for version in sorted(self.versions.values(), key=lambda v: v.timestamp, reverse=True):
            metrics = version.performance_metrics or {}
            history.append({
                "version_id": version.version_id,
                "description": version.description,
                "author": version.author,
                "timestamp": version.timestamp[:19].replace('T', ' '),
                "tags": version.tags or [],
                "performance": {
                    "avg_score": metrics.get("avg_score", "N/A"),
                    "usage_count": metrics.get("usage_count", 0)
                },
                "is_current": version.version_id == self.current_version
            })
        return history
    
    def compare_versions(self, version1_id: str, version2_id: str) -> Dict:
        """Compare two versions"""
        v1 = self.versions.get(version1_id)
        v2 = self.versions.get(version2_id)
        
        if not v1 or not v2:
            return {"error": "One or both versions not found"}
        
        # Simple diff (word-level)
        words1 = v1.prompt_text.split()
        words2 = v2.prompt_text.split()
        
        # Calculate similarity
        common_words = set(words1) & set(words2)
        total_words = set(words1) | set(words2)
        similarity = len(common_words) / len(total_words) if total_words else 0
        
        return {
            "version1": {
                "id": v1.version_id,
                "description": v1.description,
                "word_count": len(words1),
                "performance": v1.performance_metrics or {}
            },
            "version2": {
                "id": v2.version_id,
                "description": v2.description,
                "word_count": len(words2),
                "performance": v2.performance_metrics or {}
            },
            "similarity": round(similarity * 100, 1),
            "word_diff": {
                "added": list(set(words2) - set(words1)),
                "removed": list(set(words1) - set(words2))
            }
        }
    
    def find_best_performing_version(self) -> Optional[str]:
        """Find the version with the best performance metrics"""
        best_version = None
        best_score = -1
        
        for version_id, version in self.versions.items():
            if version.performance_metrics and "avg_score" in version.performance_metrics:
                score = version.performance_metrics["avg_score"]
                if score > best_score:
                    best_score = score
                    best_version = version_id
        
        return best_version
    
    def generate_changelog(self) -> str:
        """Generate a changelog for the project"""
        changelog = f"# {self.project_name} - Prompt Changelog\n\n"
        
        history = self.get_version_history()
        for version in history:
            status = " (CURRENT)" if version["is_current"] else ""
            changelog += f"## {version['version_id']}{status}\n"
            changelog += f"**Date:** {version['timestamp']}\n"
            changelog += f"**Author:** {version['author']}\n"
            changelog += f"**Description:** {version['description']}\n"
            
            if version['tags']:
                changelog += f"**Tags:** {', '.join(version['tags'])}\n"
            
            if version['performance']['avg_score'] != "N/A":
                changelog += f"**Performance:** {version['performance']['avg_score']}/10 "
                changelog += f"({version['performance']['usage_count']} uses)\n"
            
            changelog += "\n---\n\n"
        
        return changelog
    
    def save_project(self):
        """Save project data to file"""
        data = {
            "project_name": self.project_name,
            "versions": {vid: asdict(version) for vid, version in self.versions.items()},
            "current_version": self.current_version,
            "branches": self.branches,
            "current_branch": self.current_branch
        }
        
        filename = f"{self.project_name.lower().replace(' ', '_')}_versions.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    
    def load_project(self):
        """Load project data from file"""
        filename = f"{self.project_name.lower().replace(' ', '_')}_versions.json"
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            # Load versions
            for vid, version_data in data.get("versions", {}).items():
                self.versions[vid] = PromptVersion(**version_data)
            
            self.current_version = data.get("current_version")
            self.branches = data.get("branches", {"main": None})
            self.current_branch = data.get("current_branch", "main")
            
        except FileNotFoundError:
            pass  # New project

# Example usage
if __name__ == "__main__":
    # Create a new project
    vc = PromptVersionControl("Customer Support Bot")
    
    # Create initial version
    v1 = vc.create_version(
        prompt_text="Help the customer with their question",
        description="Initial basic prompt",
        author="Elena",
        tags=["basic", "v1"]
    )
    
    # Create improved version
    v2 = vc.create_version(
        prompt_text="You are a helpful customer support agent. Analyze the customer's question carefully and provide a clear, actionable solution. Be empathetic and professional.",
        description="Added role definition and tone guidance",
        author="Elena",
        tags=["improved", "role-based"]
    )
    
    # Add performance metrics
    vc.update_performance_metrics(v1, {"avg_score": 6.2, "usage_count": 50})
    vc.update_performance_metrics(v2, {"avg_score": 8.7, "usage_count": 30})
    
    # Generate reports
    print("Version History:")
    for version in vc.get_version_history():
        print(f"- {version['version_id']}: {version['description']} (Score: {version['performance']['avg_score']})")
    
    print(f"\nBest performing version: {vc.find_best_performing_version()}")
    print(f"\nCurrent prompt: {vc.get_current_prompt()}")