"""
Helper utilities for ScribeDash
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st


def format_number(value: float, format_type: str = 'auto') -> str:
    """Format numbers for display"""
    if pd.isna(value):
        return "N/A"
    
    if format_type == 'percentage':
        return f"{value:.1f}%"
    elif format_type == 'currency':
        return f"${value:,.2f}"
    elif format_type == 'integer':
        return f"{int(value):,}"
    elif format_type == 'decimal':
        return f"{value:.2f}"
    elif format_type == 'rating':
        return f"{value:.1f}/5.0"
    else:  # auto
        if value >= 1000:
            return f"{value:,.0f}"
        elif value >= 100:
            return f"{value:.0f}"
        else:
            return f"{value:.1f}"


def format_duration(hours: float) -> str:
    """Format duration in hours to human-readable format"""
    if pd.isna(hours):
        return "N/A"
    
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes}m"
    else:
        h = int(hours)
        m = int((hours - h) * 60)
        if m == 0:
            return f"{h}h"
        else:
            return f"{h}h {m}m"


def format_datetime(dt: datetime, format_type: str = 'short') -> str:
    """Format datetime for display"""
    if pd.isna(dt):
        return "N/A"
    
    if format_type == 'short':
        return dt.strftime('%H:%M')
    elif format_type == 'date':
        return dt.strftime('%Y-%m-%d')
    elif format_type == 'full':
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(dt)


def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values"""
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return 0.0
    
    return ((current - previous) / previous) * 100


def get_status_color(value: float, thresholds: Dict[str, float]) -> str:
    """Get status color based on value and thresholds"""
    if value >= thresholds.get('excellent', 95):
        return 'green'
    elif value >= thresholds.get('good', 85):
        return 'blue'
    elif value >= thresholds.get('fair', 75):
        return 'orange'
    else:
        return 'red'


def get_status_emoji(value: float, thresholds: Dict[str, float]) -> str:
    """Get status emoji based on value and thresholds"""
    if value >= thresholds.get('excellent', 95):
        return '🟢'
    elif value >= thresholds.get('good', 85):
        return '🔵'
    elif value >= thresholds.get('fair', 75):
        return '🟡'
    else:
        return '🔴'


def create_gauge_chart_data(value: float, min_val: float = 0, max_val: float = 100) -> Dict[str, Any]:
    """Create data structure for gauge charts"""
    return {
        'value': value,
        'min': min_val,
        'max': max_val,
        'ranges': [
            {'min': min_val, 'max': min_val + (max_val - min_val) * 0.6, 'color': 'red'},
            {'min': min_val + (max_val - min_val) * 0.6, 'max': min_val + (max_val - min_val) * 0.8, 'color': 'yellow'},
            {'min': min_val + (max_val - min_val) * 0.8, 'max': max_val, 'color': 'green'}
        ]
    }


def filter_dataframe_by_date(df: pd.DataFrame, date_column: str, 
                           start_date: Optional[datetime] = None, 
                           end_date: Optional[datetime] = None) -> pd.DataFrame:
    """Filter DataFrame by date range"""
    if df.empty or date_column not in df.columns:
        return df
    
    filtered_df = df.copy()
    
    # Convert date column to datetime if it's not already
    filtered_df[date_column] = pd.to_datetime(filtered_df[date_column], errors='coerce')
    
    if start_date:
        filtered_df = filtered_df[filtered_df[date_column] >= start_date]
    
    if end_date:
        filtered_df = filtered_df[filtered_df[date_column] <= end_date]
    
    return filtered_df


def filter_dataframe_by_team(df: pd.DataFrame, team_column: str, team_name: str) -> pd.DataFrame:
    """Filter DataFrame by team"""
    if df.empty or team_column not in df.columns or team_name == 'All Teams':
        return df
    
    return df[df[team_column] == team_name]


def calculate_moving_average(series: pd.Series, window: int = 7) -> pd.Series:
    """Calculate moving average for a series"""
    return series.rolling(window=window, min_periods=1).mean()


def detect_anomalies(series: pd.Series, threshold: float = 2.0) -> pd.Series:
    """Detect anomalies using z-score method"""
    z_scores = np.abs((series - series.mean()) / series.std())
    return z_scores > threshold


def generate_summary_stats(df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Dict[str, float]]:
    """Generate summary statistics for numeric columns"""
    summary = {}
    
    for col in numeric_columns:
        if col in df.columns:
            summary[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'count': df[col].count()
            }
    
    return summary


def create_performance_bins(values: pd.Series, bins: int = 5) -> pd.Series:
    """Create performance bins for categorization"""
    return pd.cut(values, bins=bins, labels=['Low', 'Below Average', 'Average', 'Above Average', 'High'])


def calculate_correlation_matrix(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Calculate correlation matrix for specified columns"""
    numeric_df = df[columns].select_dtypes(include=[np.number])
    return numeric_df.corr()


def export_to_csv(df: pd.DataFrame, filename: str) -> bytes:
    """Export DataFrame to CSV format"""
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(data_dict: Dict[str, pd.DataFrame], filename: str) -> bytes:
    """Export multiple DataFrames to Excel with multiple sheets"""
    import io
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output.getvalue()


def create_download_link(data: bytes, filename: str, file_type: str) -> str:
    """Create download link for data"""
    import base64
    
    b64 = base64.b64encode(data).decode()
    
    if file_type == 'csv':
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    elif file_type == 'excel':
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel</a>'
    else:
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download File</a>'
    
    return href


def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate data quality and return report"""
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.astype(str).to_dict()
    }
    
    # Calculate missing percentage
    report['missing_percentage'] = {
        col: (count / len(df)) * 100 
        for col, count in report['missing_values'].items()
    }
    
    return report


def get_time_period_filter(period: str) -> Tuple[datetime, datetime]:
    """Get start and end dates for time period filter"""
    end_date = datetime.now()
    
    if period == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    elif period == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif period == "Last 3 Months":
        start_date = end_date - timedelta(days=90)
    elif period == "Last 6 Months":
        start_date = end_date - timedelta(days=180)
    elif period == "Last Year":
        start_date = end_date - timedelta(days=365)
    elif period == "Year to Date":
        start_date = datetime(end_date.year, 1, 1)
    else:
        start_date = end_date - timedelta(days=30)  # Default to last 30 days
    
    return start_date, end_date


def create_alerts(data: Dict[str, Any], thresholds: Dict[str, float]) -> List[Dict[str, str]]:
    """Create alerts based on data and thresholds"""
    alerts = []
    
    # Efficiency alerts
    if 'avg_efficiency' in data and data['avg_efficiency'] < thresholds.get('efficiency_min', 90):
        alerts.append({
            'type': 'warning',
            'message': f"Average efficiency ({data['avg_efficiency']:.1f}%) below target",
            'priority': 'medium'
        })
    
    # Utilization alerts
    if 'utilization_rate' in data and data['utilization_rate'] < thresholds.get('utilization_min', 80):
        alerts.append({
            'type': 'warning',
            'message': f"Utilization rate ({data['utilization_rate']:.1f}%) below target",
            'priority': 'medium'
        })
    
    # Session alerts
    if 'active_sessions' in data and data['active_sessions'] > thresholds.get('max_sessions', 30):
        alerts.append({
            'type': 'error',
            'message': f"High session load ({data['active_sessions']} active sessions)",
            'priority': 'high'
        })
    
    return alerts


def format_alert_message(alert: Dict[str, str]) -> str:
    """Format alert message for display"""
    icons = {
        'error': '🚨',
        'warning': '⚠️',
        'info': 'ℹ️',
        'success': '✅'
    }
    
    icon = icons.get(alert['type'], '📢')
    timestamp = datetime.now().strftime('%H:%M')
    
    return f"{icon} **{timestamp}** - {alert['message']}"
