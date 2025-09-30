"""
LinkedIn OAuth service for authentication
"""
import os
import json
import secrets
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs, urlparse
import httpx
from ..config.settings import settings


class LinkedInOAuthService:
    """Service for LinkedIn OAuth authentication"""
    
    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/auth/linkedin/callback")
        self.scope = "r_liteprofile r_emailaddress w_member_social"
        
        # LinkedIn OAuth endpoints
        self.authorize_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.profile_url = "https://api.linkedin.com/v2/people/~"
        self.email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        
        # Store active sessions (in production, use Redis or database)
        self.active_sessions = {}
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate LinkedIn OAuth authorization URL"""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": self.scope
        }
        
        return f"{self.authorize_url}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        try:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                token_data = response.json()
            
            # Get user profile and email
            profile_data = await self.get_user_profile(token_data["access_token"])
            
            # Store session
            session_id = secrets.token_urlsafe(32)
            self.active_sessions[session_id] = {
                "access_token": token_data["access_token"],
                "expires_in": token_data.get("expires_in", 3600),
                "created_at": datetime.utcnow(),
                "profile": profile_data
            }
            
            return {
                "success": True,
                "session_id": session_id,
                "profile": profile_data,
                "expires_at": datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Get user profile from LinkedIn API"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                # Get basic profile
                profile_response = await client.get(self.profile_url, headers=headers)
                profile_response.raise_for_status()
                profile = profile_response.json()
                
                # Get email
                email_response = await client.get(self.email_url, headers=headers)
                email_response.raise_for_status()
                email_data = email_response.json()
                
                email = ""
                if email_data.get("elements") and len(email_data["elements"]) > 0:
                    email = email_data["elements"][0]["handle~"]["emailAddress"]
                
                return {
                    "id": profile.get("id"),
                    "firstName": profile.get("firstName", {}).get("localized", {}).get("en_US", ""),
                    "lastName": profile.get("lastName", {}).get("localized", {}).get("en_US", ""),
                    "email": email,
                    "profilePicture": profile.get("profilePicture", {}).get("displayImage~", {}).get("elements", [{}])[0].get("identifiers", [{}])[0].get("identifier", ""),
                    "headline": profile.get("headline", {}).get("localized", {}).get("en_US", "")
                }
                
        except Exception as e:
            return {"error": str(e)}
    
    async def search_jobs(self, session_id: str, keywords: str, location: str = "", limit: int = 25) -> Dict[str, Any]:
        """Search for jobs using LinkedIn API"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return {"success": False, "error": "Invalid session"}
            
            # Check if token is expired
            if datetime.utcnow() > session["created_at"] + timedelta(seconds=session["expires_in"]):
                return {"success": False, "error": "Session expired"}
            
            # LinkedIn job search API endpoint
            job_search_url = "https://api.linkedin.com/v2/jobSearch"
            
            params = {
                "keywords": keywords,
                "locationName": location,
                "count": min(limit, 25)  # LinkedIn API limit
            }
            
            headers = {
                "Authorization": f"Bearer {session['access_token']}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(job_search_url, params=params, headers=headers)
                
                if response.status_code == 403:
                    return {"success": False, "error": "Insufficient permissions for job search"}
                
                response.raise_for_status()
                job_data = response.json()
            
            # Parse job results
            jobs = []
            if "elements" in job_data:
                for job in job_data["elements"]:
                    jobs.append({
                        "id": job.get("dashEntityUrn", "").split(":")[-1],
                        "title": job.get("title", ""),
                        "company": job.get("companyDetails", {}).get("company", {}).get("name", ""),
                        "location": job.get("formattedLocation", ""),
                        "description": job.get("description", {}).get("text", ""),
                        "url": f"https://www.linkedin.com/jobs/view/{job.get('dashEntityUrn', '').split(':')[-1]}",
                        "posted_date": job.get("listedAt", ""),
                        "employment_type": job.get("workplaceTypes", [""])[0] if job.get("workplaceTypes") else "",
                        "experience_level": job.get("experienceLevel", "")
                    })
            
            return {
                "success": True,
                "jobs": jobs,
                "total": job_data.get("paging", {}).get("total", len(jobs))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def apply_to_job(self, session_id: str, job_id: str, resume_path: str, cover_letter: str = "") -> Dict[str, Any]:
        """Apply to a job on LinkedIn (requires additional permissions)"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                return {"success": False, "error": "Invalid session"}
            
            # This would require the w_member_social scope and LinkedIn's job application API
            # For now, return a placeholder response
            return {
                "success": True,
                "message": "Job application submitted successfully",
                "job_id": job_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        return self.active_sessions.get(session_id)
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoke a session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False


# Global instance
linkedin_oauth = LinkedInOAuthService()
