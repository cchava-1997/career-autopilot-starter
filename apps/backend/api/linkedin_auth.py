"""
LinkedIn OAuth authentication endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from ..services.linkedin_oauth import linkedin_oauth

router = APIRouter(prefix="/auth/linkedin", tags=["linkedin-auth"])


class LinkedInCallback(BaseModel):
    code: str
    state: Optional[str] = None


class JobSearchRequest(BaseModel):
    keywords: str
    location: str = ""
    limit: int = 25


class JobApplicationRequest(BaseModel):
    job_id: str
    resume_path: str
    cover_letter: str = ""


@router.get("/login")
async def linkedin_login():
    """Initiate LinkedIn OAuth login"""
    try:
        auth_url = linkedin_oauth.get_authorization_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate auth URL: {str(e)}")


@router.get("/callback")
async def linkedin_callback(
    code: str = Query(..., description="Authorization code from LinkedIn"),
    state: Optional[str] = Query(None, description="State parameter for security"),
    error: Optional[str] = Query(None, description="Error from LinkedIn OAuth")
):
    """Handle LinkedIn OAuth callback"""
    try:
        if error:
            raise HTTPException(status_code=400, detail=f"LinkedIn OAuth error: {error}")
        
        if not code:
            raise HTTPException(status_code=400, detail="Missing authorization code")
        
        # Exchange code for token
        result = await linkedin_oauth.exchange_code_for_token(code, state or "")
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=f"Token exchange failed: {result['error']}")
        
        # Redirect to frontend with session info
        frontend_url = f"http://localhost:3000/sources?linkedin_auth=success&session_id={result['session_id']}"
        return RedirectResponse(url=frontend_url)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Callback processing failed: {str(e)}")


@router.get("/profile")
async def get_linkedin_profile(session_id: str = Query(..., description="LinkedIn session ID")):
    """Get LinkedIn user profile"""
    try:
        session = linkedin_oauth.get_session(session_id)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        return {
            "success": True,
            "profile": session["profile"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")


@router.post("/search-jobs")
async def search_linkedin_jobs(
    request: JobSearchRequest,
    session_id: str = Query(..., description="LinkedIn session ID")
):
    """Search for jobs on LinkedIn"""
    try:
        result = await linkedin_oauth.search_jobs(
            session_id=session_id,
            keywords=request.keywords,
            location=request.location,
            limit=request.limit
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")


@router.post("/apply-job")
async def apply_to_linkedin_job(
    request: JobApplicationRequest,
    session_id: str = Query(..., description="LinkedIn session ID")
):
    """Apply to a job on LinkedIn"""
    try:
        result = await linkedin_oauth.apply_to_job(
            session_id=session_id,
            job_id=request.job_id,
            resume_path=request.resume_path,
            cover_letter=request.cover_letter
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job application failed: {str(e)}")


@router.post("/logout")
async def linkedin_logout(session_id: str = Query(..., description="LinkedIn session ID")):
    """Logout from LinkedIn"""
    try:
        success = linkedin_oauth.revoke_session(session_id)
        return {"success": success, "message": "Logged out successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


@router.get("/status")
async def linkedin_status(session_id: Optional[str] = Query(None, description="LinkedIn session ID")):
    """Check LinkedIn authentication status"""
    try:
        if not session_id:
            return {
                "authenticated": False,
                "message": "No session provided"
            }
        
        session = linkedin_oauth.get_session(session_id)
        if not session:
            return {
                "authenticated": False,
                "message": "Invalid or expired session"
            }
        
        return {
            "authenticated": True,
            "profile": session["profile"],
            "expires_at": session["created_at"].isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
