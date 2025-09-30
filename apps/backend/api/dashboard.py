from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import json
import pathlib

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class ActivityItem(BaseModel):
    type: str
    description: str
    timestamp: str

class DashboardStats(BaseModel):
    total_jobs: int
    jobs_applied: int
    jobs_pending: int
    outreach_sent: int
    interviews_scheduled: int
    recent_activity: List[ActivityItem]

# In-memory storage for demonstration
_activity_db: List[ActivityItem] = []

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics and recent activity"""
    try:
        # Get jobs data
        jobs_response = await get_jobs_data()
        jobs = jobs_response.get("jobs", [])
        
        # Calculate stats
        total_jobs = len(jobs)
        jobs_applied = len([j for j in jobs if j.get("status") == "submitted"])
        jobs_pending = len([j for j in jobs if j.get("status") in ["new", "prepared", "pdf_ready", "autofilled"]])
        outreach_sent = len([j for j in jobs if j.get("status") in ["prepared", "pdf_ready", "autofilled", "submitted"]])
        interviews_scheduled = len([j for j in jobs if j.get("status") == "interview"])
        
        # Get recent activity
        recent_activity = _activity_db[-10:] if _activity_db else []
        
        return DashboardStats(
            total_jobs=total_jobs,
            jobs_applied=jobs_applied,
            jobs_pending=jobs_pending,
            outreach_sent=outreach_sent,
            interviews_scheduled=interviews_scheduled,
            recent_activity=recent_activity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {str(e)}")

async def get_jobs_data():
    """Get jobs data from the jobs API"""
    try:
        # Import here to avoid circular imports
        from .jobs import jobs_db
        return {"jobs": list(jobs_db.values())}
    except Exception as e:
        print(f"Error getting jobs data: {e}")
        return {"jobs": []}

@router.post("/activity")
async def add_activity(activity: ActivityItem):
    """Add a new activity item"""
    _activity_db.append(activity)
    return {"message": "Activity added successfully"}

@router.get("/activity", response_model=List[ActivityItem])
async def get_recent_activity():
    """Get recent activity items"""
    return _activity_db[-20:] if _activity_db else []
