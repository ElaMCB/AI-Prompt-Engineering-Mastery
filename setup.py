"""
Setup script for AI Prompt Engineering Mastery Course
Run this to verify everything is working correctly
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def test_imports():
    """Test if all modules can be imported"""
    modules = ['jupyter', 'notebook']
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            print(f"❌ Failed to import {module}")
            return False
    return True

def test_course_modules():
    """Test if course modules work"""
    try:
        sys.path.append('notebooks')
        from prompt_validator import PromptValidator
        from progress_tracker import ProgressTracker
        
        # Test validator
        validator = PromptValidator()
        test_result = validator.score_prompt("You are a helpful assistant. Write a 100-word summary.")
        
        # Test tracker
        tracker = ProgressTracker("Test User")
        
        print("✅ Course modules working correctly")
        print(f"   Validator test score: {test_result['overall_score']:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ Course modules failed: {e}")
        return False

def main():
    """Run all setup checks"""
    print("🚀 AI Prompt Engineering Mastery - Setup Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Install Requirements", install_requirements),
        ("Test Imports", test_imports),
        ("Test Course Modules", test_course_modules)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Setup complete! You're ready to start learning.")
        print("\nNext steps:")
        print("1. jupyter notebook notebooks/01_prompt_foundations.ipynb")
        print("2. Work through the exercises")
        print("3. Use the validation tools to check your progress")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")

if __name__ == "__main__":
    main()