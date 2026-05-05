#!/usr/bin/env python3
"""
Resume AI Analyzer - Quick Deployment Script
Deploy to multiple cloud platforms with one command
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_prerequisites():
    """Check if required files exist"""
    required_files = [
        'App_fixed.py',
        'requirements.txt',
        'Courses.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def download_spacy_model():
    """Download spaCy model"""
    print("🧠 Downloading spaCy model...")
    try:
        subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'], 
                      check=True, capture_output=True)
        print("✅ spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download spaCy model: {e}")
        return False

def run_local_server():
    """Run the application locally"""
    print("🚀 Starting local server...")
    try:
        # Create Uploaded_Resumes directory if it doesn't exist
        os.makedirs('Uploaded_Resumes', exist_ok=True)
        
        # Run Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 
                       'App_fixed.py', '--server.port=8501', '--server.headless=true'])
        return True
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def deploy_streamlit_cloud():
    """Provide instructions for Streamlit Cloud deployment"""
    print("🌐 Streamlit Cloud Deployment Instructions:")
    print("1. Push your code to GitHub repository")
    print("2. Go to https://share.streamlit.io/")
    print("3. Connect your GitHub account")
    print("4. Select the repository")
    print("5. Choose App_fixed.py as main file")
    print("6. Click 'Deploy'")
    print("7. Your app will be available at a share.streamlit.io URL")
    
    # Try to open Streamlit Cloud in browser
    try:
        webbrowser.open('https://share.streamlit.io/')
        print("🌐 Opened Streamlit Cloud in browser")
    except:
        pass

def deploy_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    try:
        # Check if Heroku CLI is installed
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        
        # Create Heroku app
        app_name = f"resume-ai-{os.getpid()}"
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Set buildpack
        subprocess.run(['heroku', 'buildpacks:set', 'heroku/python'], check=True)
        
        # Deploy
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy Resume AI'], check=True)
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        # Open app
        subprocess.run(['heroku', 'open'])
        
        print(f"✅ Deployed to Heroku: https://{app_name}.herokuapp.com")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to deploy to Heroku: {e}")
        print("💡 Make sure Heroku CLI is installed and you're logged in")
        return False

def main():
    """Main deployment function"""
    print("🚀 Resume AI Analyzer - Quick Deployment")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Download required data
    if not download_nltk_data():
        return
    
    if not download_spacy_model():
        return
    
    print("\n🎯 Choose deployment option:")
    print("1. Run locally (for testing)")
    print("2. Deploy to Streamlit Cloud (recommended)")
    print("3. Deploy to Heroku (requires Heroku CLI)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        run_local_server()
    elif choice == '2':
        deploy_streamlit_cloud()
    elif choice == '3':
        deploy_heroku()
    else:
        print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
