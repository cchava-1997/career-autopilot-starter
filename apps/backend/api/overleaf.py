from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
import json
import pathlib
import webbrowser
from tools.overleaf import OverleafClient

router = APIRouter(prefix="/overleaf", tags=["overleaf"])

class OverleafBuildRequest(BaseModel):
    track: str
    job_id: str

class OverleafOpenRequest(BaseModel):
    url: str

def log_event(event: dict):
    log_path = pathlib.Path("apps/backend/logs")
    log_path.mkdir(parents=True, exist_ok=True)
    (log_path / "app.log").open("a").write(json.dumps(event) + "\n")

@router.post("/build")
async def build_pdf(request: OverleafBuildRequest):
    """Build PDF from Overleaf project"""
    try:
        client = OverleafClient()
        result = client.build_pdf(request.track, request.job_id)
        
        if result["success"]:
            log_event({
                "type": "overleaf_build_success",
                "track": request.track,
                "job_id": request.job_id,
                "pdf_path": result["pdf_path"]
            })
            return result
        else:
            log_event({
                "type": "overleaf_build_failure",
                "track": request.track,
                "job_id": request.job_id,
                "error": result["error"]
            })
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        log_event({
            "type": "overleaf_build_error",
            "track": request.track,
            "job_id": request.job_id,
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Build failed: {str(e)}")

@router.post("/open-link")
async def open_overleaf_link(request: OverleafOpenRequest):
    """Open Overleaf project in browser"""
    try:
        # Open URL in default browser
        webbrowser.open(request.url)
        
        log_event({
            "type": "overleaf_opened",
            "url": request.url
        })
        
        return {"ok": True, "message": "Overleaf project opened in browser"}
        
    except Exception as e:
        log_event({
            "type": "overleaf_open_error",
            "url": request.url,
            "error": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Failed to open link: {str(e)}")

@router.get("/project-url/{track}")
async def get_project_url(track: str):
    """Get Overleaf project URL for track"""
    try:
        client = OverleafClient()
        url = client.get_project_url(track)
        
        if url:
            return {"url": url, "track": track}
        else:
            raise HTTPException(status_code=404, detail=f"No Overleaf project configured for track: {track}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get project URL: {str(e)}")
