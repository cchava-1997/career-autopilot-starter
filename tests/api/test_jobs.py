import pytest
from fastapi.testclient import TestClient
from apps.backend.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "ts" in data

def test_jobs_list_empty():
    """Test jobs list endpoint with no jobs"""
    response = client.get("/jobs/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_job_creation():
    """Test job creation"""
    job_data = {
        "job_id": "test_job_001",
        "company": "Test Company",
        "role": "Test Role",
        "jd_url": "https://example.com/job",
        "track": "PM",
        "notes": "Test job"
    }
    
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test_job_001"
    assert data["company"] == "Test Company"
    assert data["status"] == "new"

def test_job_creation_duplicate():
    """Test job creation with duplicate ID"""
    job_data = {
        "job_id": "test_job_001",
        "company": "Test Company",
        "role": "Test Role",
        "jd_url": "https://example.com/job",
        "track": "PM"
    }
    
    # First creation should succeed
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 200
    
    # Second creation should fail
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 400

def test_job_update():
    """Test job update"""
    # Create a job first
    job_data = {
        "job_id": "test_job_002",
        "company": "Test Company",
        "role": "Test Role",
        "jd_url": "https://example.com/job",
        "track": "PM"
    }
    
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 200
    
    # Update the job
    update_data = {
        "company": "Updated Company",
        "role": "Updated Role"
    }
    
    response = client.put("/jobs/test_job_002", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "Updated Company"
    assert data["role"] == "Updated Role"

def test_job_status_update():
    """Test job status update"""
    # Create a job first
    job_data = {
        "job_id": "test_job_003",
        "company": "Test Company",
        "role": "Test Role",
        "jd_url": "https://example.com/job",
        "track": "PM"
    }
    
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 200
    
    # Update status
    response = client.post("/jobs/status?job_id=test_job_003&status=prepared&notes=Test notes")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True

def test_job_deletion():
    """Test job deletion"""
    # Create a job first
    job_data = {
        "job_id": "test_job_004",
        "company": "Test Company",
        "role": "Test Role",
        "jd_url": "https://example.com/job",
        "track": "PM"
    }
    
    response = client.post("/jobs/add", json=job_data)
    assert response.status_code == 200
    
    # Delete the job
    response = client.delete("/jobs/test_job_004")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    
    # Verify job is deleted
    response = client.get("/jobs/test_job_004")
    assert response.status_code == 404
