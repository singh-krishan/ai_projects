#!/usr/bin/env python3
"""
Test script to validate the Python to C translator installation.
"""

import os
import sys
from dotenv import load_dotenv

def test_installation():
    """Test if all required components are properly installed."""
    
    print("🧪 Testing Python to C Translator Installation...")
    print("=" * 50)
    
    # Test 1: Check Python version
    print("1. Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"   ✅ Python {sys.version.split()[0]} (OK)")
    else:
        print(f"   ❌ Python {sys.version.split()[0]} (Requires 3.8+)")
        return False
    
    # Test 2: Check required modules
    print("\n2. Checking required modules...")
    required_modules = ['openai', 'gradio', 'dotenv']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module} (OK)")
        except ImportError:
            print(f"   ❌ {module} (Missing)")
            return False
    
    # Test 3: Check API key
    print("\n3. Checking OpenAI API key...")
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        print("   ✅ OpenAI API key found (OK)")
    else:
        print("   ⚠️  OpenAI API key not found")
        print("      Please set OPENAI_API_KEY environment variable")
        print("      or create a .env file with your API key")
    
    # Test 4: Test translator import
    print("\n4. Testing translator module...")
    try:
        from translator import PythonToCTranslator
        print("   ✅ Translator module imported successfully (OK)")
    except Exception as e:
        print(f"   ❌ Failed to import translator: {e}")
        return False
    
    # Test 5: Test Gradio app import
    print("\n5. Testing Gradio app module...")
    try:
        from gradio_app import create_gradio_interface
        print("   ✅ Gradio app module imported successfully (OK)")
    except Exception as e:
        print(f"   ❌ Failed to import Gradio app: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Installation test completed!")
    
    if api_key:
        print("\n✅ Everything looks good! You can now run:")
        print("   python main.py --web")
    else:
        print("\n⚠️  Please set your OpenAI API key before using the translator.")
    
    return True

if __name__ == "__main__":
    success = test_installation()
    sys.exit(0 if success else 1)