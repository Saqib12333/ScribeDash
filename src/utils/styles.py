"""
Custom CSS styles for ScribeDash
"""

def get_custom_css() -> str:
    """Get custom CSS styles for the dashboard"""
    return """
    <style>
    /* Main app styling */
    .main {
        padding-top: 1rem;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Status indicators */
    .status-excellent {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-good {
        color: #17a2b8;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-danger {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Table styling */
    .dataframe {
        border: none !important;
    }
    
    .dataframe th {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        border: 1px solid #dee2e6 !important;
    }
    
    /* Alert styling */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0.375rem;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0.375rem;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0.375rem;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0.375rem;
    }
    
    /* Progress bars */
    .progress {
        height: 1rem;
        background-color: #e9ecef;
        border-radius: 0.375rem;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        transition: width 0.3s ease;
    }
    
    /* Button styling */
    .btn-primary {
        background: linear-gradient(90deg, #1f77b4, #17a2b8);
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Navigation styling */
    .nav-pills .nav-link {
        border-radius: 6px;
        margin: 0 0.25rem;
        transition: all 0.2s ease;
    }
    
    .nav-pills .nav-link.active {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #1f77b4;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            margin: 0.25rem 0;
            padding: 0.75rem;
        }
        
        .chart-container {
            padding: 0.75rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    header {
        visibility: hidden;
    }
    
    /* Custom footer */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.875rem;
        border-top: 1px solid #dee2e6;
        z-index: 999;
    }
    
    /* Performance indicators */
    .performance-excellent {
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .performance-good {
        background: linear-gradient(90deg, #17a2b8, #6f42c1);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .performance-fair {
        background: linear-gradient(90deg, #ffc107, #fd7e14);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .performance-poor {
        background: linear-gradient(90deg, #dc3545, #e83e8c);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Notification badges */
    .notification-badge {
        background: #dc3545;
        color: white;
        border-radius: 50%;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: bold;
        position: absolute;
        top: -8px;
        right: -8px;
        min-width: 20px;
        text-align: center;
    }
    
    /* Data quality indicators */
    .data-quality-high {
        color: #28a745;
        font-weight: bold;
    }
    
    .data-quality-medium {
        color: #ffc107;
        font-weight: bold;
    }
    
    .data-quality-low {
        color: #dc3545;
        font-weight: bold;
    }
    
    /* Team badges */
    .team-haider {
        background: linear-gradient(90deg, #1f77b4, #17a2b8);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .team-saqib {
        background: linear-gradient(90deg, #ff7f0e, #fd7e14);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Real-time indicators */
    .realtime-active {
        color: #28a745;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .realtime-inactive {
        color: #6c757d;
    }
    
    /* Chart legends */
    .chart-legend {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.875rem;
    }
    
    /* Trend arrows */
    .trend-up {
        color: #28a745;
        font-weight: bold;
    }
    
    .trend-down {
        color: #dc3545;
        font-weight: bold;
    }
    
    .trend-stable {
        color: #6c757d;
        font-weight: bold;
    }
    </style>
    """


def get_plotly_theme() -> dict:
    """Get Plotly theme configuration"""
    return {
        'layout': {
            'colorway': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
            'font': {'family': 'Inter, sans-serif', 'size': 12},
            'title': {'font': {'size': 16, 'color': '#2c3e50'}},
            'xaxis': {'gridcolor': '#ecf0f1', 'linecolor': '#bdc3c7'},
            'yaxis': {'gridcolor': '#ecf0f1', 'linecolor': '#bdc3c7'},
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white'
        }
    }


def apply_custom_styling():
    """Apply custom CSS styling to the app"""
    import streamlit as st
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def create_metric_card(title: str, value: str, delta: str = None, 
                      delta_color: str = "normal") -> str:
    """Create HTML for a metric card"""
    delta_html = ""
    if delta:
        color_class = {
            "normal": "trend-up",
            "inverse": "trend-down",
            "off": "trend-stable"
        }.get(delta_color, "trend-stable")
        
        delta_html = f'<div class="{color_class}">{delta}</div>'
    
    return f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #2c3e50; font-size: 1.2rem;">{title}</h3>
        <div style="font-size: 2rem; font-weight: bold; color: #1f77b4; margin: 0.5rem 0;">
            {value}
        </div>
        {delta_html}
    </div>
    """


def create_alert_html(message: str, alert_type: str = "info") -> str:
    """Create HTML for alerts"""
    return f'<div class="alert-{alert_type}">{message}</div>'


def create_progress_bar(percentage: float, label: str = "") -> str:
    """Create HTML for progress bar"""
    return f"""
    <div style="margin: 1rem 0;">
        {f'<label style="font-weight: 500; margin-bottom: 0.5rem; display: block;">{label}</label>' if label else ''}
        <div class="progress">
            <div class="progress-bar" style="width: {percentage}%"></div>
        </div>
        <small style="color: #6c757d;">{percentage:.1f}%</small>
    </div>
    """


def create_team_badge(team_name: str) -> str:
    """Create HTML for team badge"""
    if "Haider" in team_name:
        return f'<span class="team-haider">{team_name}</span>'
    elif "Saqib" in team_name:
        return f'<span class="team-saqib">{team_name}</span>'
    else:
        return f'<span class="badge badge-secondary">{team_name}</span>'


def create_performance_indicator(score: float) -> str:
    """Create HTML for performance indicator"""
    if score >= 95:
        return f'<span class="performance-excellent">{score:.1f}% Excellent</span>'
    elif score >= 85:
        return f'<span class="performance-good">{score:.1f}% Good</span>'
    elif score >= 75:
        return f'<span class="performance-fair">{score:.1f}% Fair</span>'
    else:
        return f'<span class="performance-poor">{score:.1f}% Needs Improvement</span>'
