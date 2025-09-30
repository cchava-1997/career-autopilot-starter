"""
Configuration settings for Career Autopilot
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Career Autopilot"
    app_version: str = "0.1.0"
    app_env: str = Field(default="development", env="APP_ENV")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database
    database_url: str = Field(default="sqlite:///./data/app.db", env="DATABASE_URL")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        env="CORS_ORIGINS"
    )
    
    # File paths
    tracker_path: str = Field(
        default="/Users/ptg/Documents/career_autopilot_tracker.xlsx",
        env="TRACKER_PATH"
    )
    apply_pack_dir: str = Field(default="./data/applications", env="APPLY_PACK_DIR")
    resume_dir: str = Field(default="./data/resumes", env="RESUME_DIR")
    
    # Overleaf API
    overleaf_api_key: Optional[str] = Field(default=None, env="OVERLEAF_API_KEY")
    overleaf_base_url: str = Field(default="https://www.overleaf.com", env="OVERLEAF_BASE_URL")
    overleaf_project_po: Optional[str] = Field(default=None, env="OVERLEAF_PROJECT_PO")
    overleaf_project_pm: Optional[str] = Field(default=None, env="OVERLEAF_PROJECT_PM")
    overleaf_project_tpm: Optional[str] = Field(default=None, env="OVERLEAF_PROJECT_TPM")
    
    # LinkedIn
    linkedin_email: Optional[str] = Field(default=None, env="LINKEDIN_EMAIL")
    linkedin_password: Optional[str] = Field(default=None, env="LINKEDIN_PASSWORD")
    linkedin_session_cookie: Optional[str] = Field(default=None, env="LINKEDIN_SESSION_COOKIE")
    
    # Indeed
    indeed_email: Optional[str] = Field(default=None, env="INDEED_EMAIL")
    indeed_password: Optional[str] = Field(default=None, env="INDEED_PASSWORD")
    
    # Chrome/ATS Configuration
    chrome_profile_path: str = Field(
        default="/Users/ptg/Library/Application Support/Google/Chrome/Default",
        env="CHROME_PROFILE_PATH"
    )
    chrome_user_data_dir: str = Field(
        default="/Users/ptg/Library/Application Support/Google/Chrome",
        env="CHROME_USER_DATA_DIR"
    )
    chrome_executable_path: str = Field(
        default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        env="CHROME_EXECUTABLE_PATH"
    )
    ats_headless_mode: bool = Field(default=False, env="ATS_HEADLESS_MODE")
    ats_timeout: int = Field(default=30000, env="ATS_TIMEOUT")
    ats_wait_for_navigation: bool = Field(default=True, env="ATS_WAIT_FOR_NAVIGATION")
    
    # Email Configuration
    smtp_host: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    email_from: Optional[str] = Field(default=None, env="EMAIL_FROM")
    email_to: Optional[str] = Field(default=None, env="EMAIL_TO")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")
    jwt_secret_key: str = Field(default="your-jwt-secret-key-change-this", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        Path(self.apply_pack_dir).mkdir(parents=True, exist_ok=True)
        Path(self.resume_dir).mkdir(parents=True, exist_ok=True)
        Path("data").mkdir(parents=True, exist_ok=True)
        Path("apps/backend/logs").mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
