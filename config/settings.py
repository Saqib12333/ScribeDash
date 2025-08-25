"""
Configuration settings for ScribeDash application
"""

import os
from typing import List, Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Sheets Configuration
    google_sheets_id: str = "17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c"
    google_credentials_path: str = "config/credentials.json"
    
    # Dashboard Settings
    refresh_interval: int = 300  # 5 minutes
    cache_ttl: int = 600  # 10 minutes
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # UI Configuration
    default_theme: str = "light"
    show_raw_data: bool = False
    enable_exports: bool = True
    page_title: str = "ScribeDash - Medical Scribing Dashboard"
    page_icon: str = "🏥"
    
    # Performance Settings
    max_cache_size: int = 100
    api_timeout: int = 30
    retry_attempts: int = 3
    rate_limit_delay: float = 1.0
    
    # Dashboard Features
    enable_realtime_updates: bool = True
    enable_notifications: bool = True
    enable_analytics: bool = True
    enable_forecasting: bool = True
    
    # Security Settings
    session_timeout: int = 3600  # 1 hour
    require_auth: bool = False
    allowed_domains: str = "*"
    
    # Deployment Settings
    port: int = 8501
    host: str = "0.0.0.0"
    workers: int = 1
    
    # Company Information
    company_name: str = "Medical Scribing Company"
    team_leaders: List[str] = ["Haider Khan", "Saqib Sherwani"]
    business_hours_start: str = "08:00"
    business_hours_end: str = "18:00"
    timezone: str = "America/Chicago"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Sheet configuration
SHEET_CONFIGS = {
    "dataset": {
        "name": "Dataset",
        "key_columns": ["Name", "TEAM LEADER", "PROVIDER", "CLIENT"],
        "cache_duration": 3600  # 1 hour
    },
    "patient_count": {
        "name": "Patient Count",
        "key_columns": ["Current Primary", "Provider", "Client", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "July", "August"],
        "cache_duration": 1800  # 30 minutes
    },
    "utilization": {
        "name": "Utilization",
        "key_columns": ["Name", "Team", "Utilization Rate"],
        "cache_duration": 900  # 15 minutes
    },
    "august": {
        "name": "August",
        "key_columns": ["Name", "Lead", "Date", "Primary", "Task", "Provider Covered"],
        "cache_duration": 300  # 5 minutes
    },
    "july": {
        "name": "July",
        "key_columns": ["Name", "Lead", "Date", "Primary", "Task", "Provider Covered"],
        "cache_duration": 1800  # 30 minutes
    }
}


# Metrics configuration
METRICS_CONFIG = {
    "efficiency_threshold": 0.8,
    "utilization_target": 0.85,
    "quality_threshold": 4.0,
    "response_time_target": 24,  # hours
    "availability_target": 0.95
}


# Chart and visualization settings
CHART_CONFIG = {
    "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    "team_colors": {
        "Haider Khan": "#1f77b4",
        "Saqib Sherwani": "#ff7f0e"
    },
    "chart_height": 400,
    "chart_width": 800,
    "font_family": "Arial, sans-serif"
}


# Dashboard layout configuration
LAYOUT_CONFIG = {
    "sidebar_width": 300,
    "main_content_padding": "1rem",
    "card_spacing": "1rem",
    "header_height": "80px"
}
