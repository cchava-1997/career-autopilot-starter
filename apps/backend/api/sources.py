from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
import os
import json
import pathlib

router = APIRouter(prefix="/sites", tags=["job-sources"])

class SiteType(str, Enum):
    BOARD = "board"
    COMPANY = "company"
    ATS = "ats"

class SiteCreate(BaseModel):
    name: str
    type: SiteType
    url: str
    notes: Optional[str] = None
    enabled: bool = True

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[SiteType] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    enabled: Optional[bool] = None

class Site(BaseModel):
    id: str
    name: str
    type: SiteType
    url: str
    notes: Optional[str] = None
    enabled: bool = True
    created_at: datetime
    updated_at: datetime

# In-memory storage for demo (replace with database)
sites_db = {}

def log_event(event: dict):
    log_path = pathlib.Path("apps/backend/logs")
    log_path.mkdir(parents=True, exist_ok=True)
    (log_path / "app.log").open("a").write(json.dumps(event) + "\n")

@router.get("/", response_model=List[Site])
async def list_sites():
    """List all job sources"""
    sites = list(sites_db.values())
    log_event({"type": "sites_list", "count": len(sites)})
    return sites

@router.post("/", response_model=Site)
async def add_site(site: SiteCreate):
    """Add a new job source"""
    site_id = f"site_{len(sites_db) + 1}"
    now = datetime.utcnow()
    
    new_site = Site(
        id=site_id,
        name=site.name,
        type=site.type,
        url=site.url,
        notes=site.notes,
        enabled=site.enabled,
        created_at=now,
        updated_at=now
    )
    
    sites_db[site_id] = new_site
    log_event({
        "type": "site_added", 
        "site_id": site_id, 
        "name": site.name, 
        "type": site.type,
        "url": site.url
    })
    
    return new_site

@router.put("/{site_id}", response_model=Site)
async def update_site(site_id: str, site_update: SiteUpdate):
    """Update an existing job source"""
    if site_id not in sites_db:
        raise HTTPException(status_code=404, detail="Site not found")
    
    site = sites_db[site_id]
    update_data = site_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(site, field, value)
    
    site.updated_at = datetime.utcnow()
    sites_db[site_id] = site
    
    log_event({"type": "site_updated", "site_id": site_id, "updates": update_data})
    return site

@router.delete("/{site_id}")
async def delete_site(site_id: str):
    """Delete a job source"""
    if site_id not in sites_db:
        raise HTTPException(status_code=404, detail="Site not found")
    
    del sites_db[site_id]
    log_event({"type": "site_deleted", "site_id": site_id})
    
    return {"ok": True, "message": "Site deleted successfully"}

@router.post("/{site_id}/test")
async def test_site(site_id: str):
    """Test a job source URL"""
    if site_id not in sites_db:
        raise HTTPException(status_code=404, detail="Site not found")
    
    site = sites_db[site_id]
    
    try:
        import requests
        response = requests.get(site.url, timeout=10)
        
        log_event({
            "type": "site_tested", 
            "site_id": site_id, 
            "url": site.url,
            "status_code": response.status_code
        })
        
        return {
            "ok": True, 
            "status_code": response.status_code,
            "message": f"Site accessible (HTTP {response.status_code})"
        }
        
    except Exception as e:
        log_event({
            "type": "site_test_failed", 
            "site_id": site_id, 
            "url": site.url,
            "error": str(e)
        })
        
        return {
            "ok": False,
            "error": str(e),
            "message": "Site not accessible"
        }
