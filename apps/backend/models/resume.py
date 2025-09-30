from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ResumeTrack(str, Enum):
    PO = "PO"
    PM = "PM"
    TPM = "TPM"

class ResumeBase(BaseModel):
    track: ResumeTrack = Field(..., description="Resume track")
    version: str = Field(..., description="Version identifier")
    notes: Optional[str] = Field(None, description="Version notes")
    is_default: bool = Field(default=False, description="Is this the default version for the track")

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(BaseModel):
    version: Optional[str] = None
    notes: Optional[str] = None
    is_default: Optional[bool] = None

class Resume(ResumeBase):
    id: str = Field(..., description="Unique resume identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    file_path: Optional[str] = Field(None, description="Path to resume file")
    overleaf_url: Optional[str] = Field(None, description="Overleaf project URL")
    
    class Config:
        use_enum_values = True
