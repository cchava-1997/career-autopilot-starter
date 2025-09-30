import os
import requests
from typing import Dict, Any, Optional
from pathlib import Path
import json

class OverleafClient:
    """Client for Overleaf API integration"""
    
    def __init__(self):
        self.api_url = os.getenv("OVERLEAF_API_URL", "https://www.overleaf.com/api/v1")
        self.api_key = os.getenv("OVERLEAF_API_KEY")
        self.projects = {
            "PO": os.getenv("OVERLEAF_PROJECT_PO"),
            "PM": os.getenv("OVERLEAF_PROJECT_PM"),
            "TPM": os.getenv("OVERLEAF_PROJECT_TPM")
        }
    
    def get_project_url(self, track: str) -> Optional[str]:
        """Get Overleaf project URL for track"""
        project_id = self.projects.get(track.upper())
        if not project_id:
            return None
        return f"https://www.overleaf.com/project/{project_id}"
    
    def build_pdf(self, track: str, job_id: str) -> Dict[str, Any]:
        """Build PDF from Overleaf project"""
        project_id = self.projects.get(track.upper())
        if not project_id:
            return {
                "success": False,
                "error": f"No Overleaf project configured for track: {track}"
            }
        
        try:
            # TODO: Implement actual Overleaf API call
            # This is a stub implementation
            output_dir = Path("data/applications") / job_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Simulate PDF build
            pdf_path = output_dir / "resume.pdf"
            pdf_path.touch()  # Create empty file for demo
            
            return {
                "success": True,
                "pdf_path": str(pdf_path),
                "project_id": project_id,
                "track": track
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def open_project(self, track: str) -> Dict[str, Any]:
        """Open Overleaf project in browser"""
        project_url = self.get_project_url(track)
        if not project_url:
            return {
                "success": False,
                "error": f"No Overleaf project configured for track: {track}"
            }
        
        return {
            "success": True,
            "url": project_url
        }
