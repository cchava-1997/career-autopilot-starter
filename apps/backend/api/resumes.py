from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import json
import pathlib

router = APIRouter(prefix="/resume", tags=["resumes"])

# Pydantic models
class ResumeCreate(BaseModel):
    track: str
    version: str
    notes: Optional[str] = None
    is_default: bool = False

class ResumeUpdate(BaseModel):
    version: Optional[str] = None
    notes: Optional[str] = None
    is_default: Optional[bool] = None

class Resume(BaseModel):
    id: str
    track: str
    version: str
    notes: Optional[str] = None
    is_default: bool = False
    created_at: datetime
    updated_at: datetime
    file_path: Optional[str] = None
    overleaf_url: Optional[str] = None

# In-memory storage for demo (replace with database)
resumes_db = {}

def log_event(event: dict):
    log_path = pathlib.Path("apps/backend/logs")
    log_path.mkdir(parents=True, exist_ok=True)
    (log_path / "app.log").open("a").write(json.dumps(event) + "\n")

@router.get("/list", response_model=List[Resume])
async def list_resumes(track: Optional[str] = Query(None, description="Filter by track")):
    """List resumes with optional track filtering"""
    resumes = list(resumes_db.values())
    if track:
        resumes = [r for r in resumes if r.track == track]
    
    log_event({"type": "resumes_list", "track": track, "count": len(resumes)})
    return resumes

@router.post("/upload", response_model=Resume)
async def upload_resume(
    file: UploadFile = File(...),
    track: str = Query(..., description="Resume track"),
    version: str = Query(..., description="Version identifier"),
    notes: Optional[str] = Query(None, description="Version notes"),
    is_default: bool = Query(False, description="Set as default for track")
):
    """Upload a resume file"""
    if not file.filename.endswith(('.pdf', '.docx', '.tex')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TEX files are allowed")
    
    # Create resume directory
    resume_dir = pathlib.Path("data/resumes") / track
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = resume_dir / f"{version}_{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create resume record
    resume_id = f"{track}_{version}"
    now = datetime.utcnow()
    
    new_resume = Resume(
        id=resume_id,
        track=track,
        version=version,
        notes=notes,
        is_default=is_default,
        created_at=now,
        updated_at=now,
        file_path=str(file_path)
    )
    
    # If this is set as default, unset others for this track
    if is_default:
        for existing_resume in resumes_db.values():
            if existing_resume.track == track and existing_resume.id != resume_id:
                existing_resume.is_default = False
    
    resumes_db[resume_id] = new_resume
    
    log_event({
        "type": "resume_uploaded", 
        "resume_id": resume_id, 
        "track": track, 
        "version": version,
        "file_path": str(file_path)
    })
    
    return new_resume

@router.post("/set-default")
async def set_default_resume(resume_id: str = Query(..., description="Resume ID")):
    """Set a resume as default for its track"""
    if resume_id not in resumes_db:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume = resumes_db[resume_id]
    
    # Unset other defaults for this track
    for existing_resume in resumes_db.values():
        if existing_resume.track == resume.track and existing_resume.id != resume_id:
            existing_resume.is_default = False
    
    # Set this as default
    resume.is_default = True
    resume.updated_at = datetime.utcnow()
    resumes_db[resume_id] = resume
    
    log_event({"type": "resume_set_default", "resume_id": resume_id, "track": resume.track})
    
    return {"ok": True, "message": f"Resume {resume_id} set as default for track {resume.track}"}
