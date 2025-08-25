"""
ScribeDash utilities package initialization
"""

from .config import (
    load_config,
    get_page_config,
    get_sheets_config,
    get_dashboard_config,
    get_metrics_config,
    initialize_session_state
)

from .google_sheets import (
    GoogleSheetsConnector,
    get_sheets_connector,
    load_all_data,
    refresh_data,
    get_data_status
)

from .data_processor import (
    DataProcessor,
    process_data,
    calculate_kpis,
    get_trend_analysis
)

from .helpers import (
    format_number,
    format_duration,
    format_datetime,
    calculate_percentage_change,
    get_status_color,
    get_status_emoji,
    create_alerts,
    format_alert_message
)

from .styles import (
    get_custom_css,
    get_plotly_theme,
    apply_custom_styling,
    create_metric_card,
    create_alert_html,
    create_progress_bar,
    create_team_badge,
    create_performance_indicator
)

__all__ = [
    # Config utilities
    'load_config',
    'get_page_config',
    'get_sheets_config',
    'get_dashboard_config',
    'get_metrics_config',
    'initialize_session_state',
    
    # Google Sheets utilities
    'GoogleSheetsConnector',
    'get_sheets_connector',
    'load_all_data',
    'refresh_data',
    'get_data_status',
    
    # Data processing utilities
    'DataProcessor',
    'process_data',
    'calculate_kpis',
    'get_trend_analysis',
    
    # Helper utilities
    'format_number',
    'format_duration',
    'format_datetime',
    'calculate_percentage_change',
    'get_status_color',
    'get_status_emoji',
    'create_alerts',
    'format_alert_message',
    
    # Style utilities
    'get_custom_css',
    'get_plotly_theme',
    'apply_custom_styling',
    'create_metric_card',
    'create_alert_html',
    'create_progress_bar',
    'create_team_badge',
    'create_performance_indicator'
]
