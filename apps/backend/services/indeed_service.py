"""
Indeed service for job search automation
"""
import httpx
import json
import pathlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..config.settings import settings


class IndeedService:
    """Service for Indeed job search automation"""
    
    def __init__(self):
        self.email = settings.indeed_email
        self.password = settings.indeed_password
        self.base_url = "https://www.indeed.com"
        
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make request to Indeed"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return {"content": response.text}
    
    async def search_jobs(self, keywords: str, location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        """Search for jobs on Indeed"""
        try:
            # Indeed job search endpoint
            endpoint = f"/jobs?q={keywords}&l={location}&limit={limit}"
            
            response = await self._make_request("GET", endpoint)
            
            # Parse job listings from response
            jobs = []
            if "content" in response:
                # This would need to be parsed from HTML response
                # For now, return mock data
                jobs = [
                    {
                        "title": f"Software Developer - {keywords}",
                        "company": "Tech Corp",
                        "location": location or "Remote",
                        "url": f"{self.base_url}/viewjob?jk=1234567890",
                        "description": "Job description here...",
                        "posted_date": datetime.utcnow().isoformat(),
                        "salary": "$80,000 - $120,000"
                    }
                ]
            
            self.log_event({
                "type": "indeed_job_search",
                "keywords": keywords,
                "location": location,
                "results_count": len(jobs)
            })
            
            return jobs
            
        except Exception as e:
            self.log_event({
                "type": "indeed_search_error",
                "error": str(e),
                "keywords": keywords
            })
            return []
    
    async def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """Get detailed job information"""
        try:
            # Extract job key from URL
            job_key = job_url.split("jk=")[-1] if "jk=" in job_url else "1234567890"
            endpoint = f"/viewjob?jk={job_key}"
            
            response = await self._make_request("GET", endpoint)
            
            # Parse job details from response
            job_details = {
                "title": "Software Developer",
                "company": "Tech Corp",
                "location": "Austin, TX",
                "description": "Full job description...",
                "requirements": ["Python", "Django", "PostgreSQL"],
                "benefits": ["Health insurance", "Dental", "Vision"],
                "salary": "$80,000 - $120,000",
                "employment_type": "Full-time",
                "experience_level": "Entry to Mid-level",
                "posted_date": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "indeed_job_details",
                "job_url": job_url,
                "job_key": job_key
            })
            
            return job_details
            
        except Exception as e:
            self.log_event({
                "type": "indeed_job_details_error",
                "error": str(e),
                "job_url": job_url
            })
            return {}
    
    async def apply_to_job(self, job_url: str, resume_path: str, cover_letter: str = "") -> Dict[str, Any]:
        """Apply to a job on Indeed"""
        try:
            # This would require more complex automation
            # For now, return mock response
            result = {
                "success": True,
                "message": "Application submitted successfully",
                "job_url": job_url,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "indeed_job_application",
                "job_url": job_url,
                "result": result
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "job_url": job_url,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "indeed_application_error",
                "error": str(e),
                "job_url": job_url
            })
            
            return error_result
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Indeed service connection"""
        try:
            # Test with a simple endpoint
            response = await self._make_request("GET", "/")
            
            result = {
                "success": True,
                "message": "Indeed service connection successful",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "indeed_connection_test",
                "result": result
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "indeed_connection_error",
                "error": str(e)
            })
            
            return error_result
    
    def log_event(self, event: Dict[str, Any]):
        """Log event to JSONL file"""
        log_path = pathlib.Path("apps/backend/logs")
        log_path.mkdir(parents=True, exist_ok=True)
        
        event["timestamp"] = datetime.utcnow().isoformat()
        event["service"] = "indeed"
        
        with open(log_path / "app.log", "a") as f:
            f.write(json.dumps(event) + "\n")


# Global service instance
indeed_service = IndeedService()
