from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import json
import pathlib

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Pydantic models
class JobCreate(BaseModel):
    job_id: str
    company: str
    role: str
    jd_url: str
    track: str
    notes: Optional[str] = None

class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    jd_url: Optional[str] = None
    track: Optional[str] = None
    notes: Optional[str] = None

class Job(BaseModel):
    job_id: str
    company: str
    role: str
    jd_url: str
    track: str
    status: str
    apply_by: datetime
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

# File-based storage for demo (replace with database)
from ..storage import load_jobs, save_jobs

jobs_db = load_jobs()

def log_event(event: dict):
    log_path = pathlib.Path("apps/backend/logs")
    log_path.mkdir(parents=True, exist_ok=True)
    (log_path / "app.log").open("a").write(json.dumps(event) + "\n")

@router.get("/list", response_model=List[Job])
async def list_jobs():
    """List all jobs with optional filtering"""
    jobs = [Job(**job_data) for job_data in jobs_db.values()]
    log_event({"type": "jobs_list", "count": len(jobs)})
    return jobs

@router.post("/add", response_model=Job)
async def add_job(job: JobCreate):
    """Add a new job"""
    if job.job_id in jobs_db:
        raise HTTPException(status_code=400, detail="Job ID already exists")
    
    now = datetime.utcnow()
    apply_by = now + timedelta(days=1)  # SLA: apply within 24h
    
    new_job = Job(
        job_id=job.job_id,
        company=job.company,
        role=job.role,
        jd_url=job.jd_url,
        track=job.track,
        status="new",
        apply_by=apply_by,
        created_at=now,
        updated_at=now,
        notes=job.notes
    )
    
    jobs_db[job.job_id] = new_job.dict()
    save_jobs(jobs_db)  # Persist to file
    log_event({"type": "job_added", "job_id": job.job_id, "company": job.company, "role": job.role})
    
    return new_job

@router.put("/{job_id}", response_model=Job)
async def update_job(job_id: str, job_update: JobUpdate):
    """Update an existing job"""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    update_data = job_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(job, field, value)
    
    job.updated_at = datetime.utcnow()
    jobs_db[job_id] = job.dict()
    save_jobs(jobs_db)  # Persist to file
    
    log_event({"type": "job_updated", "job_id": job_id, "updates": update_data})
    return job

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs_db[job_id]
    save_jobs(jobs_db)  # Persist to file
    log_event({"type": "job_deleted", "job_id": job_id})
    
    return {"ok": True, "message": "Job deleted successfully"}

@router.post("/status")
async def update_job_status(
    job_id: str = Query(..., description="Job ID"),
    status: str = Query(..., description="New status"),
    notes: Optional[str] = Query(None, description="Optional notes")
):
    """Update job status"""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    job.status = status
    job.updated_at = datetime.utcnow()
    
    if notes:
        job.notes = notes
    
    jobs_db[job_id] = job.dict()
    save_jobs(jobs_db)  # Persist to file
    
    log_event({
        "type": "job_status_updated", 
        "job_id": job_id, 
        "status": status, 
        "notes": notes
    })
    
    return {"ok": True, "message": "Status updated successfully"}
