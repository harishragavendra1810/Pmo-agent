"""Configuration module for PMO Agent."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # JIRA Configuration
    jira_server: Optional[str] = None
    jira_username: Optional[str] = None
    jira_api_token: Optional[str] = None
    jira_enabled: bool = False
    
    # Smartsheet Configuration
    smartsheet_api_token: Optional[str] = None
    smartsheet_enabled: bool = False
    
    # Excel Configuration
    excel_output_path: str = "./outputs/"
    
    # Agent Configuration
    log_level: str = "INFO"
    debug_mode: bool = False
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
