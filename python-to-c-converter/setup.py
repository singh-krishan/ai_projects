#!/usr/bin/env python3
"""
Setup script for Python to C Translator
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Python to C Translator...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Test installation
    print("\n🧪 Testing installation...")
    if not run_command("python test_installation.py", "Running installation test"):
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Set your OpenAI API key:")
    print("   export OPENAI_API_KEY='your_api_key_here'")
    print("   # OR create a .env file with your API key")
    print("\n2. Launch the web interface:")
    print("   python main.py --web")
    print("\n3. Or use the command line:")
    print("   python main.py --file example.py")

if __name__ == "__main__":
    main()