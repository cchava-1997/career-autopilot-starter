"""
Overleaf API service for resume management
"""
import httpx
import json
import pathlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..config.settings import settings


class OverleafService:
    """Service for interacting with Overleaf API"""
    
    def __init__(self):
        self.api_key = settings.overleaf_api_key
        self.base_url = settings.overleaf_base_url
        self.projects = {
            "PO": settings.overleaf_project_po,
            "PM": settings.overleaf_project_pm,
            "TPM": settings.overleaf_project_tpm
        }
        
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Overleaf API"""
        if not self.api_key:
            raise ValueError("Overleaf API key not configured")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/api/v1{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details"""
        return await self._make_request("GET", f"/projects/{project_id}")
    
    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        response = await self._make_request("GET", "/projects")
        return response.get("projects", [])
    
    async def create_project(self, name: str, template: Optional[str] = None) -> Dict[str, Any]:
        """Create a new project"""
        data = {"name": name}
        if template:
            data["template"] = template
        return await self._make_request("POST", "/projects", json=data)
    
    async def compile_project(self, project_id: str) -> Dict[str, Any]:
        """Compile a project to PDF"""
        return await self._make_request("POST", f"/projects/{project_id}/compile")
    
    async def get_compilation_status(self, project_id: str, compile_id: str) -> Dict[str, Any]:
        """Get compilation status"""
        return await self._make_request("GET", f"/projects/{project_id}/compiles/{compile_id}")
    
    async def download_pdf(self, project_id: str, compile_id: str, output_path: str) -> bool:
        """Download compiled PDF"""
        try:
            response = await self._make_request("GET", f"/projects/{project_id}/compiles/{compile_id}/output/output.pdf")
            
            # Save PDF to file
            pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response)
            return True
        except Exception as e:
            print(f"Error downloading PDF: {e}")
            return False
    
    async def get_project_files(self, project_id: str) -> List[Dict[str, Any]]:
        """Get project files"""
        return await self._make_request("GET", f"/projects/{project_id}/files")
    
    async def upload_file(self, project_id: str, file_path: str, content: str) -> Dict[str, Any]:
        """Upload a file to project"""
        data = {
            "name": file_path,
            "content": content
        }
        return await self._make_request("POST", f"/projects/{project_id}/files", json=data)
    
    async def update_file(self, project_id: str, file_id: str, content: str) -> Dict[str, Any]:
        """Update a file in project"""
        data = {"content": content}
        return await self._make_request("PUT", f"/projects/{project_id}/files/{file_id}", json=data)
    
    async def get_resume_project_id(self, track: str) -> Optional[str]:
        """Get project ID for resume track"""
        return self.projects.get(track.upper())
    
    async def build_resume_pdf(self, track: str, output_path: str) -> bool:
        """Build resume PDF for specific track"""
        project_id = await self.get_resume_project_id(track)
        if not project_id:
            raise ValueError(f"No project configured for track: {track}")
        
        # Start compilation
        compile_result = await self.compile_project(project_id)
        compile_id = compile_result.get("compile_id")
        
        if not compile_id:
            raise ValueError("Failed to start compilation")
        
        # Wait for compilation to complete
        max_attempts = 30
        for attempt in range(max_attempts):
            status = await self.get_compilation_status(project_id, compile_id)
            if status.get("status") == "success":
                # Download PDF
                return await self.download_pdf(project_id, compile_id, output_path)
            elif status.get("status") == "error":
                raise ValueError(f"Compilation failed: {status.get('error')}")
            
            # Wait before next check
            import asyncio
            await asyncio.sleep(2)
        
        raise TimeoutError("Compilation timed out")
    
    def log_event(self, event: Dict[str, Any]):
        """Log event to JSONL file"""
        log_path = pathlib.Path("apps/backend/logs")
        log_path.mkdir(parents=True, exist_ok=True)
        
        event["timestamp"] = datetime.utcnow().isoformat()
        event["service"] = "overleaf"
        
        with open(log_path / "app.log", "a") as f:
            f.write(json.dumps(event) + "\n")


# Global service instance
overleaf_service = OverleafService()
