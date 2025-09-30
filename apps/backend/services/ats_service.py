"""
ATS (Applicant Tracking System) automation service using Playwright
"""
import asyncio
import json
import pathlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from ..config.settings import settings


class ATSService:
    """Service for automating ATS form filling"""
    
    def __init__(self):
        self.chrome_profile_path = settings.chrome_profile_path
        self.chrome_user_data_dir = settings.chrome_user_data_dir
        self.chrome_executable_path = settings.chrome_executable_path
        self.headless_mode = settings.ats_headless_mode
        self.timeout = settings.ats_timeout
        self.wait_for_navigation = settings.ats_wait_for_navigation
        
    async def _get_browser(self) -> Browser:
        """Get configured browser instance"""
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch(
            headless=self.headless_mode,
            executable_path=self.chrome_executable_path,
            args=[
                f"--user-data-dir={self.chrome_user_data_dir}",
                f"--profile-directory=Default",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor"
            ]
        )
        
        return browser
    
    async def _get_context(self, browser: Browser) -> BrowserContext:
        """Get browser context with profile"""
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        return context
    
    async def fill_application_form(self, job_url: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fill ATS application form with provided data"""
        browser = None
        try:
            browser = await self._get_browser()
            context = await self._get_context(browser)
            page = await context.new_page()
            
            # Navigate to job application page
            await page.goto(job_url, wait_until="networkidle", timeout=self.timeout)
            
            # Wait for page to load
            await page.wait_for_load_state("domcontentloaded")
            
            # Fill form fields
            filled_fields = []
            errors = []
            
            for field_name, field_value in form_data.items():
                try:
                    # Try different selectors for the field
                    selectors = [
                        f'input[name="{field_name}"]',
                        f'input[id="{field_name}"]',
                        f'input[placeholder*="{field_name}"]',
                        f'textarea[name="{field_name}"]',
                        f'textarea[id="{field_name}"]',
                        f'select[name="{field_name}"]',
                        f'select[id="{field_name}"]'
                    ]
                    
                    field_filled = False
                    for selector in selectors:
                        try:
                            element = await page.wait_for_selector(selector, timeout=5000)
                            if element:
                                # Clear existing value
                                await element.fill("")
                                # Fill new value
                                await element.fill(str(field_value))
                                filled_fields.append(field_name)
                                field_filled = True
                                break
                        except:
                            continue
                    
                    if not field_filled:
                        errors.append(f"Could not find field: {field_name}")
                        
                except Exception as e:
                    errors.append(f"Error filling field {field_name}: {str(e)}")
            
            # Handle file uploads
            if "resume" in form_data:
                try:
                    resume_path = form_data["resume"]
                    if pathlib.Path(resume_path).exists():
                        # Look for file input
                        file_input = await page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(resume_path)
                            filled_fields.append("resume")
                        else:
                            errors.append("Could not find file upload field")
                except Exception as e:
                    errors.append(f"Error uploading resume: {str(e)}")
            
            # Take screenshot for verification
            screenshot_path = f"data/screenshots/ats_form_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pathlib.Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=screenshot_path)
            
            result = {
                "success": len(errors) == 0,
                "filled_fields": filled_fields,
                "errors": errors,
                "screenshot_path": screenshot_path,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Log the event
            self.log_event({
                "type": "ats_form_filled",
                "job_url": job_url,
                "result": result
            })
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "errors": [f"ATS automation failed: {str(e)}"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "ats_form_error",
                "job_url": job_url,
                "error": str(e)
            })
            
            return error_result
            
        finally:
            if browser:
                await browser.close()
    
    async def test_ats_connection(self) -> Dict[str, Any]:
        """Test ATS service connection"""
        browser = None
        try:
            browser = await self._get_browser()
            context = await self._get_context(browser)
            page = await context.new_page()
            
            # Test with a simple page
            await page.goto("https://httpbin.org/get", timeout=10000)
            content = await page.content()
            
            result = {
                "success": True,
                "message": "ATS service connection successful",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "ats_connection_test",
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
                "type": "ats_connection_error",
                "error": str(e)
            })
            
            return error_result
            
        finally:
            if browser:
                await browser.close()
    
    async def get_chrome_profile_info(self) -> Dict[str, Any]:
        """Get Chrome profile information"""
        try:
            profile_path = pathlib.Path(self.chrome_profile_path)
            user_data_dir = pathlib.Path(self.chrome_user_data_dir)
            
            info = {
                "profile_path": str(profile_path),
                "profile_exists": profile_path.exists(),
                "user_data_dir": str(user_data_dir),
                "user_data_dir_exists": user_data_dir.exists(),
                "chrome_executable": self.chrome_executable_path,
                "chrome_executable_exists": pathlib.Path(self.chrome_executable_path).exists(),
                "headless_mode": self.headless_mode,
                "timeout": self.timeout
            }
            
            self.log_event({
                "type": "chrome_profile_info",
                "info": info
            })
            
            return info
            
        except Exception as e:
            error_info = {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_event({
                "type": "chrome_profile_error",
                "error": str(e)
            })
            
            return error_info
    
    def log_event(self, event: Dict[str, Any]):
        """Log event to JSONL file"""
        log_path = pathlib.Path("apps/backend/logs")
        log_path.mkdir(parents=True, exist_ok=True)
        
        event["timestamp"] = datetime.utcnow().isoformat()
        event["service"] = "ats"
        
        with open(log_path / "app.log", "a") as f:
            f.write(json.dumps(event) + "\n")


# Global service instance
ats_service = ATSService()
