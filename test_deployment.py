#!/usr/bin/env python
"""
Local Deployment Test Script
Run this before deploying to catch issues early
"""
import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - FAILED with exception: {e}")
        return False

def test_django_setup():
    """Test Django configuration"""
    print("\n🔄 Testing Django setup...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personalfinance.settings')
        django.setup()
        print("✅ Django setup - SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Django setup - FAILED: {e}")
        return False

def test_imports():
    """Test critical imports"""
    print("\n🔄 Testing critical imports...")
    try:
        import nltk
        import matplotlib
        import pandas
        import sklearn
        from django.conf import settings
        print("✅ Critical imports - SUCCESS")
        return True
    except Exception as e:
        print(f"❌ Critical imports - FAILED: {e}")
        return False

def main():
    print("🚀 LOCAL DEPLOYMENT TEST SCRIPT")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Check manage.py
    if run_command("python manage.py check", "Django system check"):
        tests_passed += 1
    
    # Test 2: Test Django setup
    if test_django_setup():
        tests_passed += 1
    
    # Test 3: Test imports
    if test_imports():
        tests_passed += 1
    
    # Test 4: Test migrations
    if run_command("python manage.py makemigrations --dry-run", "Migration check"):
        tests_passed += 1
    
    # Test 5: Test static files collection
    if run_command("python manage.py collectstatic --noinput --dry-run", "Static files check"):
        tests_passed += 1
    
    # Test 6: Test WSGI application
    if run_command("python -c \"from personalfinance.wsgi import application; print('WSGI OK')\"", "WSGI application check"):
        tests_passed += 1
    
    # Test 7: Test requirements
    if run_command("pip check", "Dependencies check"):
        tests_passed += 1
    
    # Test 8: Test NLTK data
    if run_command("python -c \"import nltk; nltk.data.find('tokenizers/punkt'); nltk.data.find('corpora/stopwords'); print('NLTK OK')\"", "NLTK data check"):
        tests_passed += 1
    
    print(f"\n🎯 RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ ALL TESTS PASSED! Ready for deployment! 🚀")
        return True
    else:
        print("❌ Some tests failed. Fix issues before deploying!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)