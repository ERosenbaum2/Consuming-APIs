"""
Quick setup script to help initialize the JStory project.
This script checks prerequisites and guides you through setup.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if OPENAI_API_KEY is set as environment variable."""
    # Try to load from .env if it exists (optional)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv not needed if using terminal environment variables
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("\n⚠️  OPENAI_API_KEY not set as environment variable")
        print("   Please set it in your terminal session:")
        print("   Windows PowerShell: $env:OPENAI_API_KEY='your_key_here'")
        print("   Windows CMD: set OPENAI_API_KEY=your_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY='your_key_here'")
        return False
    
    print("✓ OPENAI_API_KEY found in environment")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import flask
        import langchain
        import langchain_openai
        import langchain_community
        import chromadb
        import dotenv
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"\n❌ Missing required package: {e.name}")
        print("   Please run: pip install -r requirements.txt")
        return False

def main():
    """Main setup check."""
    print("=" * 60)
    print("JStory - Setup Check")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check environment variable
    if not check_env_file():
        all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ Setup complete! You're ready to go.")
        print("\nNext steps:")
        print("  1. Run: python collect_stories.py  (to download stories)")
        print("  2. Run: python process_stories.py  (to create vector database)")
        print("  3. Run: python app.py  (to start the web server)")
    else:
        print("⚠️  Please fix the issues above before proceeding.")
    print("=" * 60)

if __name__ == "__main__":
    main()

