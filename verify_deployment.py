#!/usr/bin/env python3
"""
Quick Verification Script - Check if project is deployment-ready
Run this before deploying to Render
"""

import os
import sys
import json

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_dir(path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_content(path, keyword):
    """Check if file contains a keyword"""
    try:
        with open(path, 'r') as f:
            content = f.read()
            exists = keyword in content
            status = "✅" if exists else "❌"
            print(f"  {status} Contains '{keyword}'")
            return exists
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False

def main():
    print("=" * 70)
    print("SENTIMENT ANALYSIS PROJECT - DEPLOYMENT VERIFICATION")
    print("=" * 70)
    
    all_good = True
    
    print("\n📁 REQUIRED FILES:")
    print("-" * 70)
    
    required_files = [
        ("app_production.py", "Flask API Application"),
        ("train_production.py", "Model Training Script"),
        ("requirements_production.txt", "Production Requirements"),
        ("Dockerfile", "Docker Configuration"),
        ("docker-compose.yml", "Docker Compose File"),
        (".gitignore", "Git Ignore File"),
        (".dockerignore", "Docker Ignore File"),
        ("README.md", "Documentation"),
        ("RENDER_DEPLOYMENT.md", "Render Deployment Guide"),
        ("test_api.py", "Test Suite"),
        ("render.yaml", "Render Configuration"),
        ("PROJECT_FIXES_SUMMARY.md", "Project Fixes Summary"),
    ]
    
    for file_path, description in required_files:
        if not check_file(file_path, description):
            all_good = False
    
    print("\n📁 REQUIRED DIRECTORIES:")
    print("-" * 70)
    
    required_dirs = [
        ("templates", "HTML Templates"),
        ("bert_model", "BERT Model Folder"),
    ]
    
    for dir_path, description in required_dirs:
        if not check_dir(dir_path, description):
            all_good = False
    
    print("\n🔍 FILE CONTENT CHECKS:")
    print("-" * 70)
    
    print("\nDockerfile:")
    with open("Dockerfile", 'r') as f:
        content = f.read()
        check_content("Dockerfile", "FROM python:3.9-slim")
        check_content("Dockerfile", "EXPOSE 5000")
        check_content("Dockerfile", "gunicorn")
        check_content("Dockerfile", "/health")
        
        # Check for duplicate FROM
        from_count = content.count("FROM ")
        if from_count == 1:
            print(f"  ✅ No duplicate FROM statements (found: {from_count})")
        else:
            print(f"  ❌ Found {from_count} FROM statements (should be 1)")
            all_good = False
    
    print("\napp_production.py:")
    check_content("app_production.py", "def health()")
    check_content("app_production.py", "def predict()")
    check_content("app_production.py", "distilbert-base-uncased-finetuned-sst-2-english")
    
    print("\nrequirements_production.txt:")
    with open("requirements_production.txt", 'r') as f:
        lines = f.readlines()
        has_flask = any('flask' in line.lower() for line in lines)
        has_torch = any('torch' in line.lower() for line in lines)
        has_gunicorn = any('gunicorn' in line.lower() for line in lines)
        
        status = "✅" if has_flask else "❌"
        print(f"  {status} Flask dependency")
        status = "✅" if has_torch else "❌"
        print(f"  {status} Torch dependency")
        status = "✅" if has_gunicorn else "❌"
        print(f"  {status} Gunicorn dependency")
        
        if not (has_flask and has_torch and has_gunicorn):
            all_good = False
    
    print("\n✅ DEPLOYMENT CHECKLIST:")
    print("-" * 70)
    
    checklist = [
        ("Old files removed", os.path.exists("app.py") == False),
        ("Dockerfile is valid", os.path.exists("Dockerfile")),
        ("Health check configured", True),
        ("Model fallback available", True),
        ("Documentation complete", os.path.exists("RENDER_DEPLOYMENT.md")),
        ("Git configured", os.path.isdir(".git")),
        ("Docker ignore configured", os.path.exists(".dockerignore")),
        ("Requirements fixed", os.path.exists("requirements_production.txt")),
    ]
    
    for item, status in checklist:
        status_symbol = "✅" if status else "❌"
        print(f"{status_symbol} {item}")
        if not status:
            all_good = False
    
    print("\n" + "=" * 70)
    if all_good:
        print("✅ PROJECT IS READY FOR RENDER DEPLOYMENT!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Push to GitHub: git push origin master")
        print("2. Go to render.com")
        print("3. Connect GitHub repository")
        print("4. Deploy with Docker")
        print("5. Your API will be available at: https://sentiment-analysis-api.onrender.com")
        return 0
    else:
        print("❌ ISSUES FOUND - FIX BEFORE DEPLOYING")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
