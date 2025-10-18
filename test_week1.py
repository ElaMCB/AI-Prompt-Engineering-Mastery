"""
Test Foundations Lab functionality
Run this to make sure all Foundations Lab tools are working
"""

import sys
import os
sys.path.append('notebooks')

from prompt_validator import PromptValidator
from progress_tracker import ProgressTracker
from prompt_version_control import PromptVersionControl

def test_prompt_validator():
    """Test the prompt validation system"""
    print("🧪 Testing Prompt Validator...")
    
    validator = PromptValidator()
    
    # Test with a bad prompt
    bad_prompt = "Write something good"
    bad_result = validator.score_prompt(bad_prompt)
    
    # Test with a good prompt
    good_prompt = """You are a professional copywriter specializing in email marketing. 
    Write a 150-word welcome email for new subscribers to a productivity newsletter. 
    Target audience: busy professionals who want to optimize their workflow. 
    Include a clear call-to-action to download our free productivity guide. 
    Tone should be friendly but professional."""
    
    good_result = validator.score_prompt(good_prompt)
    
    print(f"   Bad prompt score: {bad_result['overall_score']:.2f} - {bad_result['grade']}")
    print(f"   Good prompt score: {good_result['overall_score']:.2f} - {good_result['grade']}")
    
    if good_result['overall_score'] > bad_result['overall_score']:
        print("   ✅ Validator working correctly")
        return True
    else:
        print("   ❌ Validator not working properly")
        return False

def test_progress_tracker():
    """Test the progress tracking system"""
    print("\n🧪 Testing Progress Tracker...")
    
    tracker = ProgressTracker("Test Student")
    
    # Update some skills
    tracker.update_skill("week1_foundations", "prompt_debugging", 0.8)
    tracker.update_skill("week1_foundations", "clear_framework", 0.9)
    
    # Record an assessment
    tracker.record_assessment("week1_foundations", "test_assessment", 0.85)
    
    # Get progress
    progress = tracker.get_overall_progress()
    
    print(f"   Overall progress: {progress['overall_progress']}%")
    print(f"   Skills mastered: {progress['skills_mastered']}")
    
    if progress['overall_progress'] > 0:
        print("   ✅ Progress tracker working correctly")
        return True
    else:
        print("   ❌ Progress tracker not working properly")
        return False

def test_version_control():
    """Test the version control system"""
    print("\n🧪 Testing Version Control...")
    
    vc = PromptVersionControl("Test Project")
    
    # Create a version
    v1 = vc.create_version(
        prompt_text="Test prompt version 1",
        description="Initial test version",
        author="Test User"
    )
    
    # Create another version
    v2 = vc.create_version(
        prompt_text="Test prompt version 2 - improved",
        description="Improved test version",
        author="Test User"
    )
    
    # Get history
    history = vc.get_version_history()
    
    print(f"   Created {len(history)} versions")
    print(f"   Current version: {vc.current_version}")
    
    if len(history) == 2 and vc.current_version == v2:
        print("   ✅ Version control working correctly")
        return True
    else:
        print("   ❌ Version control not working properly")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = [
        "progress.json",
        "test_project_versions.json"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)

def main():
    """Run all tests"""
    print("🧪 Week 1 Functionality Test")
    print("=" * 40)
    
    tests = [
        test_prompt_validator,
        test_progress_tracker,
        test_version_control
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    # Cleanup
    cleanup_test_files()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All Foundations Lab tools are working!")
        print("\nYou can now start the course:")
        print("jupyter notebook notebooks/foundations_lab.ipynb")
    else:
        print("❌ Some tools are not working. Check the errors above.")

if __name__ == "__main__":
    main()