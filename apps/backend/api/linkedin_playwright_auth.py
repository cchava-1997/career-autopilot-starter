"""
LinkedIn Playwright authentication endpoints (no OAuth required)
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..services.linkedin_playwright import linkedin_playwright

router = APIRouter(prefix="/auth/linkedin-playwright", tags=["linkedin-playwright"])


class JobSearchRequest(BaseModel):
    keywords: str
    location: str = ""
    limit: int = 25


class JobApplicationRequest(BaseModel):
    job_url: str
    resume_path: str
    cover_letter: str = ""


@router.get("/status")
async def linkedin_status():
    """Check LinkedIn credentials status"""
    try:
        if not linkedin_playwright.email or not linkedin_playwright.password:
            return {
                "authenticated": False,
                "message": "LinkedIn credentials not configured"
            }
        
        return {
            "authenticated": True,
            "message": "LinkedIn credentials configured",
            "email": linkedin_playwright.email
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.post("/test-connection")
async def test_linkedin_connection():
    """Test LinkedIn connection using Playwright"""
    try:
        result = await linkedin_playwright.test_connection()
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")


@router.post("/search-jobs")
async def search_linkedin_jobs(request: JobSearchRequest):
    """Search for jobs on LinkedIn using Playwright"""
    try:
        if not linkedin_playwright.email or not linkedin_playwright.password:
            raise HTTPException(status_code=400, detail="LinkedIn credentials not configured")
        
        jobs = await linkedin_playwright.search_jobs(
            keywords=request.keywords,
            location=request.location,
            limit=request.limit
        )
        
        return {
            "success": True,
            "jobs": jobs,
            "total": len(jobs)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")


@router.post("/apply-job")
async def apply_to_linkedin_job(request: JobApplicationRequest):
    """Apply to a job on LinkedIn using Playwright"""
    try:
        if not linkedin_playwright.email or not linkedin_playwright.password:
            raise HTTPException(status_code=400, detail="LinkedIn credentials not configured")
        
        result = await linkedin_playwright.apply_to_job(
            job_url=request.job_url,
            resume_path=request.resume_path,
            cover_letter=request.cover_letter
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job application failed: {str(e)}")
