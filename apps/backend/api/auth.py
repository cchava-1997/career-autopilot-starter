"""
Authentication API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import json
import pathlib
from ..config.settings import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

class AuthRequest(BaseModel):
    """Authentication request model"""
    service: str = Field(..., description="Service name (overleaf, linkedin, indeed, ats)")
    credentials: Dict[str, Any] = Field(..., description="Service credentials")

class AuthResponse(BaseModel):
    """Authentication response model"""
    success: bool = Field(..., description="Authentication success status")
    message: str = Field(..., description="Response message")
    token: Optional[str] = Field(None, description="JWT token if successful")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")

class ServiceStatus(BaseModel):
    """Service status model"""
    service: str = Field(..., description="Service name")
    configured: bool = Field(..., description="Whether service is configured")
    connected: bool = Field(..., description="Whether service is connected")
    last_tested: Optional[datetime] = Field(None, description="Last connection test time")
    error: Optional[str] = Field(None, description="Last error message")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login", response_model=AuthResponse)
async def login(auth_request: AuthRequest):
    """Authenticate with external service"""
    try:
        service = auth_request.service.lower()
        credentials = auth_request.credentials
        
        # Validate service
        if service not in ["overleaf", "linkedin", "indeed", "ats"]:
            raise HTTPException(status_code=400, detail="Invalid service name")
        
        # Test service connection
        connection_result = await test_service_connection(service, credentials)
        
        if connection_result["success"]:
            # Create JWT token
            token_data = {
                "service": service,
                "user_id": "user_123",  # This would come from user authentication
                "expires_at": datetime.utcnow() + timedelta(hours=24)
            }
            access_token = create_access_token(token_data)
            
            return AuthResponse(
                success=True,
                message=f"Successfully authenticated with {service}",
                token=access_token,
                expires_at=token_data["expires_at"]
            )
        else:
            return AuthResponse(
                success=False,
                message=f"Failed to authenticate with {service}: {connection_result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

@router.get("/status", response_model=Dict[str, ServiceStatus])
async def get_service_status():
    """Get status of all configured services"""
    services = {}
    
    # Check Overleaf
    overleaf_configured = bool(settings.overleaf_api_key)
    overleaf_connected = False
    overleaf_error = None
    
    if overleaf_configured:
        try:
            from ..services.overleaf_service import overleaf_service
            result = await overleaf_service.list_projects()
            overleaf_connected = True
        except Exception as e:
            overleaf_error = str(e)
    
    services["overleaf"] = ServiceStatus(
        service="overleaf",
        configured=overleaf_configured,
        connected=overleaf_connected,
        last_tested=datetime.utcnow() if overleaf_configured else None,
        error=overleaf_error
    )
    
    # Check LinkedIn
    linkedin_configured = bool(settings.linkedin_email and settings.linkedin_password)
    linkedin_connected = False
    linkedin_error = None
    
    if linkedin_configured:
        try:
            from ..services.linkedin_service import linkedin_service
            result = await linkedin_service.test_connection()
            linkedin_connected = result["success"]
        except Exception as e:
            linkedin_error = str(e)
    
    services["linkedin"] = ServiceStatus(
        service="linkedin",
        configured=linkedin_configured,
        connected=linkedin_connected,
        last_tested=datetime.utcnow() if linkedin_configured else None,
        error=linkedin_error
    )
    
    # Check Indeed
    indeed_configured = bool(settings.indeed_email and settings.indeed_password)
    indeed_connected = False
    indeed_error = None
    
    if indeed_configured:
        try:
            from ..services.indeed_service import indeed_service
            result = await indeed_service.test_connection()
            indeed_connected = result["success"]
        except Exception as e:
            indeed_error = str(e)
    
    services["indeed"] = ServiceStatus(
        service="indeed",
        configured=indeed_configured,
        connected=indeed_connected,
        last_tested=datetime.utcnow() if indeed_configured else None,
        error=indeed_error
    )
    
    # Check ATS
    ats_configured = bool(settings.chrome_executable_path)
    ats_connected = False
    ats_error = None
    
    if ats_configured:
        try:
            from ..services.ats_service import ats_service
            result = await ats_service.test_ats_connection()
            ats_connected = result["success"]
        except Exception as e:
            ats_error = str(e)
    
    services["ats"] = ServiceStatus(
        service="ats",
        configured=ats_configured,
        connected=ats_connected,
        last_tested=datetime.utcnow() if ats_configured else None,
        error=ats_error
    )
    
    return services

@router.post("/test/{service}")
async def test_service(service: str, credentials: Optional[Dict[str, Any]] = None):
    """Test connection to specific service"""
    try:
        result = await test_service_connection(service, credentials or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service test error: {str(e)}")

async def test_service_connection(service: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
    """Test connection to external service"""
    service = service.lower()
    
    if service == "overleaf":
        from ..services.overleaf_service import overleaf_service
        return await overleaf_service.list_projects()
    
    elif service == "linkedin":
        from ..services.linkedin_service import linkedin_service
        return await linkedin_service.test_connection()
    
    elif service == "indeed":
        from ..services.indeed_service import indeed_service
        return await indeed_service.test_connection()
    
    elif service == "ats":
        from ..services.ats_service import ats_service
        return await ats_service.test_ats_connection()
    
    else:
        return {"success": False, "error": "Unknown service"}

@router.get("/chrome-profile")
async def get_chrome_profile_info():
    """Get Chrome profile information for ATS"""
    try:
        from ..services.ats_service import ats_service
        return await ats_service.get_chrome_profile_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chrome profile error: {str(e)}")

def log_event(event: dict):
    """Log event to JSONL file"""
    log_path = pathlib.Path("apps/backend/logs")
    log_path.mkdir(parents=True, exist_ok=True)
    
    event["timestamp"] = datetime.utcnow().isoformat()
    event["service"] = "auth"
    
    with open(log_path / "app.log", "a") as f:
        f.write(json.dumps(event) + "\n")
