from typing import Dict, Any, Optional
from enum import Enum
import re

class ATSType(str, Enum):
    WORKDAY = "workday"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    ASHBY = "ashby"
    UNKNOWN = "unknown"

class ATSDetector:
    """Detect ATS type from URL and page content"""
    
    ATS_PATTERNS = {
        ATSType.WORKDAY: [
            r"workday\.com",
            r"wd5\.myworkday\.com",
            r"myworkdayjobs\.com"
        ],
        ATSType.GREENHOUSE: [
            r"boards\.greenhouse\.io",
            r"jobs\.greenhouse\.io"
        ],
        ATSType.LEVER: [
            r"jobs\.lever\.co",
            r"lever\.co"
        ],
        ATSType.ASHBY: [
            r"jobs\.ashbyhq\.com",
            r"ashby\.hq"
        ]
    }
    
    def detect_from_url(self, url: str) -> ATSType:
        """Detect ATS type from URL"""
        for ats_type, patterns in self.ATS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return ats_type
        return ATSType.UNKNOWN
    
    def detect_from_content(self, page_content: str) -> ATSType:
        """Detect ATS type from page content"""
        content_lower = page_content.lower()
        
        # Workday indicators
        if any(indicator in content_lower for indicator in [
            "workday", "wd5", "myworkday"
        ]):
            return ATSType.WORKDAY
        
        # Greenhouse indicators
        if any(indicator in content_lower for indicator in [
            "greenhouse", "boards.greenhouse"
        ]):
            return ATSType.GREENHOUSE
        
        # Lever indicators
        if any(indicator in content_lower for indicator in [
            "lever", "jobs.lever"
        ]):
            return ATSType.LEVER
        
        # Ashby indicators
        if any(indicator in content_lower for indicator in [
            "ashby", "ashbyhq"
        ]):
            return ATSType.ASHBY
        
        return ATSType.UNKNOWN
    
    def get_field_mappings(self, ats_type: ATSType) -> Dict[str, str]:
        """Get field mappings for specific ATS"""
        mappings = {
            ATSType.WORKDAY: {
                "first_name": "input[data-automation-id='firstName']",
                "last_name": "input[data-automation-id='lastName']",
                "email": "input[data-automation-id='email']",
                "phone": "input[data-automation-id='phone']",
                "resume": "input[type='file'][accept*='pdf']",
                "cover_letter": "textarea[data-automation-id='coverLetter']"
            },
            ATSType.GREENHOUSE: {
                "first_name": "input[name='first_name']",
                "last_name": "input[name='last_name']",
                "email": "input[name='email']",
                "phone": "input[name='phone']",
                "resume": "input[type='file'][name='resume']",
                "cover_letter": "textarea[name='cover_letter']"
            },
            ATSType.LEVER: {
                "first_name": "input[name='name']",
                "email": "input[name='email']",
                "phone": "input[name='phone']",
                "resume": "input[type='file'][name='resume']",
                "cover_letter": "textarea[name='cover_letter']"
            },
            ATSType.ASHBY: {
                "first_name": "input[name='firstName']",
                "last_name": "input[name='lastName']",
                "email": "input[name='email']",
                "phone": "input[name='phone']",
                "resume": "input[type='file'][name='resume']",
                "cover_letter": "textarea[name='coverLetter']"
            }
        }
        
        return mappings.get(ats_type, {})
