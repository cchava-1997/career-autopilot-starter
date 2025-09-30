from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    NEW = "new"
    PREPARED = "prepared"
    PDF_READY = "pdf_ready"
    AUTOFILLED = "autofilled"
    SUBMITTED = "submitted"
    REJECTED = "rejected"
    INTERVIEW = "interview"

class JobTrack(str, Enum):
    PO = "PO"
    PM = "PM"
    TPM = "TPM"

class JobBase(BaseModel):
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job role/title")
    jd_url: str = Field(..., description="Job description URL")
    track: JobTrack = Field(..., description="Resume track to use")
    notes: Optional[str] = Field(None, description="Additional notes")

class JobCreate(JobBase):
    job_id: str = Field(..., description="Unique job identifier")

class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    jd_url: Optional[str] = None
    track: Optional[JobTrack] = None
    notes: Optional[str] = None

class Job(JobBase):
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(default=JobStatus.NEW, description="Current job status")
    apply_by: datetime = Field(..., description="SLA deadline for application")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
