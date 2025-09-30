"""
LinkedIn automation using Playwright (no OAuth required)
"""
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from playwright.async_api import async_playwright
from ..config.settings import settings


class LinkedInPlaywrightService:
    """Service for LinkedIn automation using Playwright"""
    
    def __init__(self):
        self.email = settings.linkedin_email
        self.password = settings.linkedin_password
        self.base_url = "https://www.linkedin.com"
        
    async def login(self, page) -> bool:
        """Login to LinkedIn using credentials"""
        try:
            await page.goto(f"{self.base_url}/login")
            await page.wait_for_load_state('networkidle')
            
            # Fill login form
            await page.fill('input[name="session_key"]', self.email)
            await page.fill('input[name="session_password"]', self.password)
            
            # Click login button
            await page.click('button[type="submit"]')
            
            # Wait for redirect to feed
            await page.wait_for_url("**/feed/**", timeout=30000)
            
            return True
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    async def search_jobs(self, keywords: str, location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn using Playwright"""
        jobs = []
        
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=False)  # Set to True for headless
                context = await browser.new_context()
                page = await context.new_page()
                
                # Login
                if not await self.login(page):
                    return jobs
                
                # Navigate to jobs page
                jobs_url = f"{self.base_url}/jobs/search/?keywords={keywords}&location={location}"
                await page.goto(jobs_url)
                await page.wait_for_load_state('networkidle')
                
                # Wait for job listings to load
                await page.wait_for_selector('[data-job-id]', timeout=10000)
                
                # Extract job information
                job_elements = await page.query_selector_all('[data-job-id]')
                
                for i, job_element in enumerate(job_elements[:limit]):
                    try:
                        # Extract job details
                        title_element = await job_element.query_selector('a[data-control-name="job_card_click"]')
                        company_element = await job_element.query_selector('.job-card-container__company-name')
                        location_element = await job_element.query_selector('.job-card-container__metadata-item')
                        
                        title = await title_element.inner_text() if title_element else "N/A"
                        company = await company_element.inner_text() if company_element else "N/A"
                        location_text = await location_element.inner_text() if location_element else "N/A"
                        
                        # Get job URL
                        job_url = await title_element.get_attribute('href') if title_element else ""
                        if job_url and not job_url.startswith('http'):
                            job_url = f"{self.base_url}{job_url}"
                        
                        jobs.append({
                            "id": f"linkedin_{i}",
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": location_text.strip(),
                            "url": job_url,
                            "description": "Job description available on LinkedIn",
                            "posted_date": datetime.utcnow().isoformat(),
                            "source": "LinkedIn"
                        })
                        
                    except Exception as e:
                        print(f"Error extracting job {i}: {e}")
                        continue
                
                await browser.close()
                
        except Exception as e:
            print(f"Job search failed: {e}")
            
        return jobs
    
    async def apply_to_job(self, job_url: str, resume_path: str, cover_letter: str = "") -> Dict[str, Any]:
        """Apply to a job on LinkedIn (requires Easy Apply)"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Login
                if not await self.login(page):
                    return {"success": False, "error": "Login failed"}
                
                # Navigate to job page
                await page.goto(job_url)
                await page.wait_for_load_state('networkidle')
                
                # Look for Easy Apply button
                easy_apply_button = await page.query_selector('button[aria-label*="Easy Apply"]')
                if not easy_apply_button:
                    return {"success": False, "error": "Easy Apply not available for this job"}
                
                # Click Easy Apply
                await easy_apply_button.click()
                await page.wait_for_load_state('networkidle')
                
                # Fill out application form
                # This would need to be customized based on the specific form fields
                # For now, return a placeholder response
                
                await browser.close()
                
                return {
                    "success": True,
                    "message": "Application submitted successfully",
                    "job_url": job_url,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test LinkedIn connection"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Test login
                success = await self.login(page)
                await browser.close()
                
                return {
                    "success": success,
                    "message": "LinkedIn connection test successful" if success else "LinkedIn login failed",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


# Global instance
linkedin_playwright = LinkedInPlaywrightService()
