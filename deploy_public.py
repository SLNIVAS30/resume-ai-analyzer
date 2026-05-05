#!/usr/bin/env python3
"""
Resume AI Analyzer - Public Deployment Script
Deploy the application with a public URL using ngrok
"""

import subprocess
import sys
import time
import webbrowser
from pyngrok import ngrok
import streamlit.web.cli as stcli

def setup_ngrok():
    """Set up ngrok tunnel"""
    print("🚀 Setting up public deployment...")
    
    # Kill any existing ngrok processes
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'ngrok.exe'], 
                      capture_output=True)
    except:
        pass
    
    # Create ngrok tunnel
    try:
        # Start Streamlit in the background
        streamlit_process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 
            'App_fixed.py', '--server.port=8503', '--server.headless=true'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for Streamlit to start
        time.sleep(5)
        
        # Create ngrok tunnel
        public_url = ngrok.connect(8503, bind_tls=True)
        
        print(f"🌐 Public URL: {public_url}")
        print(f"🚀 Application deployed successfully!")
        print(f"📱 Share this URL with others to access your Resume AI application")
        
        # Open in browser
        webbrowser.open(public_url)
        
        print(f"🔗 Your Resume AI application is now live at: {public_url}")
        print(f"⏳ The tunnel will remain active as long as this script runs")
        print(f"🛑 Press Ctrl+C to stop the deployment")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping deployment...")
            ngrok.disconnect(public_url)
            streamlit_process.terminate()
            print("✅ Deployment stopped")
            
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Resume AI Analyzer - Public Deployment")
    print("=" * 50)
    print("This will deploy your Resume AI application with a public URL")
    print("Anyone with the URL can access your application")
    print()
    
    # Confirm deployment
    confirm = input("Do you want to continue? (y/n): ").strip().lower()
    if confirm == 'y':
        setup_ngrok()
    else:
        print("❌ Deployment cancelled")
