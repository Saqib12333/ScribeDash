"""
Configuration utilities for ScribeDash
"""

import streamlit as st
from pathlib import Path
import json
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load application configuration"""
    config_path = Path(__file__).parent.parent.parent / "config" / "settings.py"
    
    # Default configuration
    default_config = {
        "app": {
            "title": "ScribeDash",
            "icon": "📊",
            "layout": "wide",
            "sidebar_state": "expanded"
        },
        "google_sheets": {
            "spreadsheet_id": "17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c",
            "cache_ttl": 300,
            "rate_limit": 60
        },
        "dashboard": {
            "auto_refresh": True,
            "refresh_interval": 30,
            "theme": "light"
        },
        "metrics": {
            "efficiency_target": 95,
            "utilization_target": 85,
            "rating_target": 4.5
        }
    }
    
    return default_config


def get_page_config() -> Dict[str, Any]:
    """Get Streamlit page configuration"""
    config = load_config()
    
    return {
        "page_title": config["app"]["title"],
        "page_icon": config["app"]["icon"],
        "layout": config["app"]["layout"],
        "initial_sidebar_state": config["app"]["sidebar_state"]
    }


def get_sheets_config() -> Dict[str, Any]:
    """Get Google Sheets configuration"""
    config = load_config()
    return config["google_sheets"]


def get_dashboard_config() -> Dict[str, Any]:
    """Get dashboard configuration"""
    config = load_config()
    return config["dashboard"]


def get_metrics_config() -> Dict[str, Any]:
    """Get metrics configuration"""
    config = load_config()
    return config["metrics"]


def save_user_preferences(preferences: Dict[str, Any]):
    """Save user preferences to session state"""
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
    
    st.session_state.user_preferences.update(preferences)


def get_user_preferences() -> Dict[str, Any]:
    """Get user preferences from session state"""
    return st.session_state.get('user_preferences', {})


def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        'current_page': 'Overview',
        'selected_team': 'All Teams',
        'selected_scribe': None,
        'selected_provider': None,
        'auto_refresh': True,
        'last_refresh': None,
        'data_loaded': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
