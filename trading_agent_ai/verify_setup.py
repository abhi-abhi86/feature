#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all components are properly configured for the AI Trading Agent
"""

import sys
from pathlib import Path
import importlib.util

def check_python_version():
    """Check Python version compatibility."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required. Current version:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def check_required_files():
    """Check if required configuration files exist."""
    required_files = [
        "config/main_config.ini",
        "config/logging.ini", 
        "config/prompts.json",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        "data/raw",
        "data/processed", 
        "data/chart_annotations",
        "models/vision",
        "models/prediction",
        "local_database",
        "logs"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"✅ Found directory: {dir_path}")
    
    if missing_dirs:
        print("❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}")
        return False
    
    return True

def check_api_keys():
    """Check if API keys are configured."""
    api_key_file = Path("config/broker_api_keys.env")
    if not api_key_file.exists():
        print("⚠️  Broker API keys not configured")
        print("   Create config/broker_api_keys.env with your broker credentials")
        return False
    
    # Check if it has actual keys (not just template)
    content = api_key_file.read_text()
    if "your_actual_api_key_here" in content:
        print("⚠️  Please update config/broker_api_keys.env with your actual API keys")
        return False
    
    print("✅ API keys file configured")
    return True

def check_models():
    """Check if trained models are available."""
    vision_model = Path("models/vision/best.pt")
    if not vision_model.exists():
        print("⚠️  Vision model not found at models/vision/best.pt")
        print("   Vision features will be disabled until you add a trained YOLOv8 model")
    else:
        print("✅ Vision model found")
    
    return True

def main():
    """Run all verification checks."""
    print("AI Trading Agent - Setup Verification")
    print("=====================================")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Directory Structure", check_directories),
        ("API Configuration", check_api_keys),
        ("Model Files", check_models)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed! Ready to run the application.")
        print("\nTo start the application, run:")
        print("   ./scripts/run_app.sh")
    else:
        print("❌ Some issues found. Please fix them before running the application.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)