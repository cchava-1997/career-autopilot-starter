#!/bin/bash

# Career Autopilot Authentication Test Script
# This script tests all authentication connections

set -e

echo "🧪 Career Autopilot Authentication Test"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run ./scripts/setup-auth.sh first"
    exit 1
fi

# Load environment variables
source .env

echo "🔍 Testing Environment Configuration"
echo "==================================="
echo ""

# Test environment variables
echo "📋 Environment Variables:"
if [ -n "$OVERLEAF_API_KEY" ]; then
    echo "✅ OVERLEAF_API_KEY: Set (${OVERLEAF_API_KEY:0:10}...)"
else
    echo "❌ OVERLEAF_API_KEY: Not set"
fi

if [ -n "$CHROME_USER_DATA_DIR" ]; then
    echo "✅ CHROME_USER_DATA_DIR: Set ($CHROME_USER_DATA_DIR)"
else
    echo "❌ CHROME_USER_DATA_DIR: Not set"
fi

if [ -n "$PROFILE_NAME" ]; then
    echo "✅ PROFILE_NAME: Set ($PROFILE_NAME)"
else
    echo "❌ PROFILE_NAME: Not set"
fi

if [ -n "$PROFILE_EMAIL" ]; then
    echo "✅ PROFILE_EMAIL: Set ($PROFILE_EMAIL)"
else
    echo "❌ PROFILE_EMAIL: Not set"
fi

if [ -n "$PROFILE_PHONE" ]; then
    echo "✅ PROFILE_PHONE: Set ($PROFILE_PHONE)"
else
    echo "❌ PROFILE_PHONE: Not set"
fi

echo ""

# Test file paths
echo "📁 File Paths:"
if [ -n "$TRACKER_PATH" ]; then
    if [ -f "$TRACKER_PATH" ]; then
        echo "✅ TRACKER_PATH: Exists ($TRACKER_PATH)"
    else
        echo "⚠️  TRACKER_PATH: Not found ($TRACKER_PATH)"
    fi
else
    echo "❌ TRACKER_PATH: Not set"
fi

if [ -n "$APPLY_PACK_DIR" ]; then
    if [ -d "$APPLY_PACK_DIR" ]; then
        echo "✅ APPLY_PACK_DIR: Exists ($APPLY_PACK_DIR)"
    else
        echo "⚠️  APPLY_PACK_DIR: Not found ($APPLY_PACK_DIR)"
        echo "   Creating directory..."
        mkdir -p "$APPLY_PACK_DIR"
        echo "✅ APPLY_PACK_DIR: Created"
    fi
else
    echo "❌ APPLY_PACK_DIR: Not set"
fi

if [ -n "$RESUME_DIR" ]; then
    if [ -d "$RESUME_DIR" ]; then
        echo "✅ RESUME_DIR: Exists ($RESUME_DIR)"
    else
        echo "⚠️  RESUME_DIR: Not found ($RESUME_DIR)"
        echo "   Creating directory..."
        mkdir -p "$RESUME_DIR"
        echo "✅ RESUME_DIR: Created"
    fi
else
    echo "❌ RESUME_DIR: Not set"
fi

echo ""

# Test Chrome profile
echo "🌐 Chrome Profile Test"
echo "====================="
echo ""

if [ -n "$CHROME_USER_DATA_DIR" ]; then
    if [ -d "$CHROME_USER_DATA_DIR" ]; then
        echo "✅ Chrome profile directory exists"
        
        # Check for Chrome profile files
        if [ -f "$CHROME_USER_DATA_DIR/Default/Preferences" ]; then
            echo "✅ Chrome profile preferences found"
        else
            echo "⚠️  Chrome profile preferences not found"
        fi
        
        if [ -d "$CHROME_USER_DATA_DIR/Default" ]; then
            echo "✅ Chrome profile data directory exists"
        else
            echo "⚠️  Chrome profile data directory not found"
        fi
    else
        echo "❌ Chrome profile directory not found"
        echo "   Please check CHROME_USER_DATA_DIR in .env"
    fi
else
    echo "❌ CHROME_USER_DATA_DIR not set"
fi

echo ""

# Test Overleaf configuration
echo "📄 Overleaf Configuration Test"
echo "============================="
echo ""

if [ -n "$OVERLEAF_API_KEY" ]; then
    if [[ "$OVERLEAF_API_KEY" == sk-* ]]; then
        echo "✅ Overleaf API key format looks correct"
    else
        echo "⚠️  Overleaf API key format may be incorrect (should start with 'sk-')"
    fi
    
    # Test API key with curl (if backend is running)
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "🔄 Testing Overleaf API connection..."
        response=$(curl -s -X POST "http://localhost:8000/settings/test-overleaf" 2>/dev/null || echo "error")
        if [[ "$response" == *"success"* ]]; then
            echo "✅ Overleaf API connection successful"
        elif [[ "$response" == *"error"* ]]; then
            echo "❌ Overleaf API connection failed"
        else
            echo "⚠️  Could not test Overleaf API (backend not responding)"
        fi
    else
        echo "⚠️  Backend not running - cannot test Overleaf API"
    fi
else
    echo "❌ OVERLEAF_API_KEY not set"
fi

echo ""

# Test project IDs
if [ -n "$OVERLEAF_PROJECT_PO" ]; then
    echo "✅ OVERLEAF_PROJECT_PO: Set ($OVERLEAF_PROJECT_PO)"
else
    echo "❌ OVERLEAF_PROJECT_PO: Not set"
fi

if [ -n "$OVERLEAF_PROJECT_PM" ]; then
    echo "✅ OVERLEAF_PROJECT_PM: Set ($OVERLEAF_PROJECT_PM)"
else
    echo "❌ OVERLEAF_PROJECT_PM: Not set"
fi

if [ -n "$OVERLEAF_PROJECT_TPM" ]; then
    echo "✅ OVERLEAF_PROJECT_TPM: Set ($OVERLEAF_PROJECT_TPM)"
else
    echo "❌ OVERLEAF_PROJECT_TPM: Not set"
fi

echo ""

# Test backend API
echo "🔧 Backend API Test"
echo "=================="
echo ""

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is running"
    
    # Test health endpoint
    health_response=$(curl -s http://localhost:8000/health)
    if [[ "$health_response" == *"ok"* ]]; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
    fi
    
    # Test jobs endpoint
    jobs_response=$(curl -s http://localhost:8000/jobs/list)
    if [[ "$jobs_response" == *"job_id"* ]]; then
        echo "✅ Jobs API working"
    else
        echo "❌ Jobs API not working"
    fi
    
    # Test sites endpoint
    sites_response=$(curl -s http://localhost:8000/sites/)
    if [[ "$sites_response" == *"name"* ]]; then
        echo "✅ Sites API working"
    else
        echo "❌ Sites API not working"
    fi
    
else
    echo "❌ Backend API is not running"
    echo "   Start with: ./scripts/dev.sh"
fi

echo ""

# Test frontend
echo "🎨 Frontend Test"
echo "==============="
echo ""

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not running"
    echo "   Start with: ./scripts/dev.sh"
fi

echo ""

# Summary
echo "📊 Test Summary"
echo "=============="
echo ""

# Count successful tests
success_count=0
total_count=0

# Environment variables
if [ -n "$OVERLEAF_API_KEY" ]; then ((success_count++)); fi
((total_count++))

if [ -n "$CHROME_USER_DATA_DIR" ]; then ((success_count++)); fi
((total_count++))

if [ -n "$PROFILE_NAME" ]; then ((success_count++)); fi
((total_count++))

if [ -n "$PROFILE_EMAIL" ]; then ((success_count++)); fi
((total_count++))

if [ -n "$PROFILE_PHONE" ]; then ((success_count++)); fi
((total_count++))

# File paths
if [ -n "$APPLY_PACK_DIR" ] && [ -d "$APPLY_PACK_DIR" ]; then ((success_count++)); fi
((total_count++))

if [ -n "$RESUME_DIR" ] && [ -d "$RESUME_DIR" ]; then ((success_count++)); fi
((total_count++))

# Chrome profile
if [ -n "$CHROME_USER_DATA_DIR" ] && [ -d "$CHROME_USER_DATA_DIR" ]; then ((success_count++)); fi
((total_count++))

# Overleaf
if [ -n "$OVERLEAF_API_KEY" ] && [[ "$OVERLEAF_API_KEY" == sk-* ]]; then ((success_count++)); fi
((total_count++))

# Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then ((success_count++)); fi
((total_count++))

# Frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then ((success_count++)); fi
((total_count++))

echo "✅ Passed: $success_count/$total_count tests"
echo ""

if [ $success_count -eq $total_count ]; then
    echo "🎉 All tests passed! Your setup is ready to use."
    echo ""
    echo "Next steps:"
    echo "1. Open http://localhost:3000 in your browser"
    echo "2. Go to Settings page to test connections"
    echo "3. Add your first job and start using the app!"
else
    echo "⚠️  Some tests failed. Please check the issues above."
    echo ""
    echo "Common fixes:"
    echo "1. Run ./scripts/setup-auth.sh to configure missing settings"
    echo "2. Start the application with ./scripts/dev.sh"
    echo "3. Check the authentication setup guide: docs/setup/authentication_setup.md"
fi

echo ""
echo "Happy job hunting! 🎯"
