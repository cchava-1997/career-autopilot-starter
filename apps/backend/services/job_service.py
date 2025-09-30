from typing import List, Optional
from datetime import datetime, timedelta
from ..models.job import Job, JobCreate, JobUpdate, JobStatus
import json
import pathlib

class JobService:
    def __init__(self):
        self.jobs_db = {}
        self.load_jobs()
    
    def load_jobs(self):
        """Load jobs from persistent storage"""
        # TODO: Replace with actual database
        pass
    
    def save_jobs(self):
        """Save jobs to persistent storage"""
        # TODO: Replace with actual database
        pass
    
    def list_jobs(self, status: Optional[JobStatus] = None) -> List[Job]:
        """List all jobs with optional status filter"""
        jobs = list(self.jobs_db.values())
        if status:
            jobs = [job for job in jobs if job.status == status]
        return jobs
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get a specific job by ID"""
        return self.jobs_db.get(job_id)
    
    def create_job(self, job_data: JobCreate) -> Job:
        """Create a new job"""
        if job_data.job_id in self.jobs_db:
            raise ValueError("Job ID already exists")
        
        now = datetime.utcnow()
        apply_by = now + timedelta(days=1)  # SLA: apply within 24h
        
        job = Job(
            job_id=job_data.job_id,
            company=job_data.company,
            role=job_data.role,
            jd_url=job_data.jd_url,
            track=job_data.track,
            notes=job_data.notes,
            status=JobStatus.NEW,
            apply_by=apply_by,
            created_at=now,
            updated_at=now
        )
        
        self.jobs_db[job_data.job_id] = job
        self.save_jobs()
        return job
    
    def update_job(self, job_id: str, job_update: JobUpdate) -> Job:
        """Update an existing job"""
        if job_id not in self.jobs_db:
            raise ValueError("Job not found")
        
        job = self.jobs_db[job_id]
        update_data = job_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(job, field, value)
        
        job.updated_at = datetime.utcnow()
        self.jobs_db[job_id] = job
        self.save_jobs()
        return job
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        if job_id not in self.jobs_db:
            return False
        
        del self.jobs_db[job_id]
        self.save_jobs()
        return True
    
    def update_job_status(self, job_id: str, status: JobStatus, notes: Optional[str] = None) -> Job:
        """Update job status"""
        if job_id not in self.jobs_db:
            raise ValueError("Job not found")
        
        job = self.jobs_db[job_id]
        job.status = status
        job.updated_at = datetime.utcnow()
        
        if notes:
            job.notes = notes
        
        self.jobs_db[job_id] = job
        self.save_jobs()
        return job
    
    def get_jobs_due_today(self) -> List[Job]:
        """Get jobs with SLA due today"""
        today = datetime.utcnow().date()
        return [
            job for job in self.jobs_db.values()
            if job.apply_by.date() == today and job.status in [JobStatus.NEW, JobStatus.PREPARED]
        ]
    
    def get_overdue_jobs(self) -> List[Job]:
        """Get jobs with overdue SLA"""
        now = datetime.utcnow()
        return [
            job for job in self.jobs_db.values()
            if job.apply_by < now and job.status in [JobStatus.NEW, JobStatus.PREPARED]
        ]
