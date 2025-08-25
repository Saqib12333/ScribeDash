"""
Real-time Activity dashboard component
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def render_realtime_activity():
    """Render real-time activity dashboard"""
    
    st.header("⚡ Real-time Activity Monitor")
    st.markdown("Live tracking of current sessions and activities")
    
    # Auto-refresh controls
    render_refresh_controls()
    
    # Current status overview
    render_current_status()
    
    st.markdown("---")
    
    # Live activity sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_active_sessions()
        render_recent_completions()
    
    with col2:
        render_live_metrics()
        render_alerts_notifications()
    
    # Real-time charts
    st.markdown("---")
    render_realtime_charts()


def render_refresh_controls():
    """Render auto-refresh and manual refresh controls"""
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        auto_refresh = st.checkbox(
            "Auto-refresh (30 seconds)",
            value=True,
            key="auto_refresh_toggle"
        )
        
        if auto_refresh:
            st.markdown("🔄 **Live data** - Updates automatically")
        else:
            st.markdown("⏸️ **Static view** - Manual refresh required")
    
    with col2:
        if st.button("🔄 Refresh Now", type="primary"):
            st.rerun()
    
    with col3:
        last_update = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"**Last Update:** {last_update}")


def render_current_status():
    """Render current system status overview"""
    
    st.subheader("📊 Current Status")
    
    # Sample real-time data - replace with actual data
    active_sessions = np.random.randint(15, 25)
    pending_starts = np.random.randint(2, 8)
    completed_today = np.random.randint(45, 65)
    alerts_count = np.random.randint(0, 5)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Sessions",
            value=active_sessions,
            delta=f"{np.random.randint(-3, 4)} vs 1h ago"
        )
    
    with col2:
        st.metric(
            label="Pending Starts",
            value=pending_starts,
            delta=f"{np.random.randint(-2, 3)} waiting"
        )
    
    with col3:
        st.metric(
            label="Completed Today",
            value=completed_today,
            delta=f"{np.random.randint(5, 15)} since midnight"
        )
    
    with col4:
        if alerts_count > 0:
            st.metric(
                label="Active Alerts",
                value=alerts_count,
                delta="⚠️ Attention needed",
                delta_color="inverse"
            )
        else:
            st.metric(
                label="System Status",
                value="✅ All Clear",
                delta="No alerts"
            )


def render_active_sessions():
    """Render currently active sessions table"""
    
    st.subheader("🟢 Active Sessions")
    
    # Sample active sessions data - replace with actual data
    current_time = datetime.now()
    
    active_sessions_data = []
    scribes = ['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Rohan Setia', 'Muskan Gupta', 
               'Anmol Agarwal', 'Shreya Jain', 'Deepa Deepak', 'Vineet Kumar']
    providers = ['Dr. Mark Basham', 'Amanda DeBois', 'Melanie Arrington', 'Dr. Sarah Johnson', 
                'Alison Blake', 'Dr. Michael Chen', 'Nikki Kelly', 'Dr. Emily Davis', 'Dr. Lisa Rodriguez']
    
    num_active = min(len(scribes), len(providers), np.random.randint(8, 16))
    
    for i in range(num_active):
        start_time = current_time - timedelta(minutes=np.random.randint(30, 300))
        duration = current_time - start_time
        
        active_sessions_data.append({
            'Scribe': np.random.choice(scribes),
            'Provider': np.random.choice(providers),
            'Start Time': start_time.strftime('%H:%M'),
            'Duration': f"{duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m",
            'Patients': np.random.randint(1, 8),
            'Status': np.random.choice(['Active', 'Break', 'Documentation'], p=[0.7, 0.15, 0.15])
        })
    
    df = pd.DataFrame(active_sessions_data)
    
    # Apply status-based styling
    def highlight_status(row):
        if row['Status'] == 'Active':
            return ['background-color: #d4edda'] * len(row)
        elif row['Status'] == 'Break':
            return ['background-color: #fff3cd'] * len(row)
        elif row['Status'] == 'Documentation':
            return ['background-color: #d1ecf1'] * len(row)
        return [''] * len(row)
    
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No active sessions at the moment")


def render_recent_completions():
    """Render recently completed sessions"""
    
    st.subheader("✅ Recent Completions")
    
    # Sample recent completions data
    current_time = datetime.now()
    
    recent_completions = []
    scribes = ['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Rohan Setia', 'Muskan Gupta']
    providers = ['Dr. Mark Basham', 'Amanda DeBois', 'Melanie Arrington', 'Dr. Sarah Johnson', 'Alison Blake']
    
    for i in range(5):
        end_time = current_time - timedelta(minutes=np.random.randint(5, 120))
        session_duration = np.random.uniform(1.5, 4.5)
        
        recent_completions.append({
            'Scribe': np.random.choice(scribes),
            'Provider': np.random.choice(providers),
            'End Time': end_time.strftime('%H:%M'),
            'Duration': f"{session_duration:.1f}h",
            'Patients': np.random.randint(3, 15),
            'Rating': f"{np.random.uniform(4.2, 5.0):.1f}/5.0"
        })
    
    df = pd.DataFrame(recent_completions)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Rating': st.column_config.ProgressColumn(
                'Rating',
                help="Session rating",
                min_value=0,
                max_value=5,
                format="%.1f/5.0"
            )
        }
    )


def render_live_metrics():
    """Render live performance metrics"""
    
    st.subheader("📈 Live Metrics")
    
    # Current hour metrics
    current_hour = datetime.now().hour
    
    # Sample metrics
    hourly_efficiency = np.random.uniform(88, 96)
    patients_this_hour = np.random.randint(8, 25)
    avg_session_length = np.random.uniform(2.2, 3.8)
    
    st.metric(
        label="Current Hour Efficiency",
        value=f"{hourly_efficiency:.1f}%",
        delta=f"{np.random.uniform(-2, 3):.1f}% vs last hour"
    )
    
    st.metric(
        label="Patients This Hour",
        value=patients_this_hour,
        delta=f"{np.random.randint(-5, 8)} vs last hour"
    )
    
    st.metric(
        label="Avg Session Length",
        value=f"{avg_session_length:.1f}h",
        delta=f"{np.random.uniform(-0.5, 0.3):.1f}h vs target"
    )
    
    # System health indicators
    st.markdown("#### 🔧 System Health")
    
    system_metrics = {
        "EHR Connection": "🟢 Online",
        "Data Sync": "🟢 Active",
        "Backup Systems": "🟢 Ready",
        "API Status": "🟢 Operational"
    }
    
    for metric, status in system_metrics.items():
        st.markdown(f"**{metric}:** {status}")


def render_alerts_notifications():
    """Render active alerts and notifications"""
    
    st.subheader("🚨 Alerts & Notifications")
    
    # Sample alerts - replace with actual data
    alerts = []
    
    # Generate random alerts
    alert_types = [
        ("⚠️", "Dr. Johnson's session running 30min over", "warning"),
        ("🔴", "Backup needed for Dr. Smith", "error"), 
        ("🟡", "Peak hours approaching - 3 scribes needed", "warning"),
        ("🔵", "New provider onboarding scheduled", "info"),
        ("🟢", "Monthly targets 95% achieved", "success")
    ]
    
    # Randomly select 2-4 alerts
    num_alerts = np.random.randint(2, 5)
    selected_alerts = np.random.choice(len(alert_types), size=num_alerts, replace=False)
    
    for i in selected_alerts:
        icon, message, alert_type = alert_types[i]
        timestamp = (datetime.now() - timedelta(minutes=np.random.randint(1, 60))).strftime('%H:%M')
        
        if alert_type == "error":
            st.error(f"{icon} **{timestamp}** - {message}")
        elif alert_type == "warning":
            st.warning(f"{icon} **{timestamp}** - {message}")
        elif alert_type == "info":
            st.info(f"{icon} **{timestamp}** - {message}")
        elif alert_type == "success":
            st.success(f"{icon} **{timestamp}** - {message}")
    
    if num_alerts == 0:
        st.success("🟢 No active alerts - All systems normal")


def render_realtime_charts():
    """Render real-time activity charts"""
    
    st.subheader("📊 Real-time Activity Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly activity chart
        st.markdown("#### Hourly Activity (Today)")
        
        current_hour = datetime.now().hour
        hours = list(range(max(0, current_hour - 8), min(24, current_hour + 2)))
        
        # Generate realistic activity data
        activity_counts = []
        for hour in hours:
            if 8 <= hour <= 18:  # Business hours
                base_activity = np.random.poisson(8)
                if 10 <= hour <= 14:  # Peak hours
                    base_activity += np.random.poisson(5)
            else:
                base_activity = np.random.poisson(2)
            activity_counts.append(base_activity)
        
        fig = px.bar(
            x=hours,
            y=activity_counts,
            title="Sessions Started by Hour",
            labels={'x': 'Hour', 'y': 'Sessions Started'},
            color=activity_counts,
            color_continuous_scale='viridis'
        )
        
        # Highlight current hour
        fig.add_vline(x=current_hour, line_dash="dash", line_color="red", 
                      annotation_text="Current Hour")
        
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Live efficiency gauge
        st.markdown("#### Current System Efficiency")
        
        current_efficiency = np.random.uniform(85, 98)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_efficiency,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Efficiency %"},
            delta = {'reference': 92, 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 85], 'color': "yellow"},
                    {'range': [85, 95], 'color': "lightgreen"},
                    {'range': [95, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Activity timeline
    st.markdown("#### Recent Activity Timeline")
    
    # Generate timeline data for the last 4 hours
    timeline_data = []
    current_time = datetime.now()
    
    for i in range(20):  # Last 20 events
        event_time = current_time - timedelta(minutes=np.random.randint(5, 240))
        event_types = ['Session Start', 'Session End', 'Break Start', 'Break End', 'Provider Change']
        event_type = np.random.choice(event_types)
        scribe = np.random.choice(['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Rohan Setia', 'Muskan Gupta'])
        
        timeline_data.append({
            'Time': event_time,
            'Event': event_type,
            'Scribe': scribe,
            'Display_Time': event_time.strftime('%H:%M')
        })
    
    # Sort by time (most recent first)
    timeline_data.sort(key=lambda x: x['Time'], reverse=True)
    
    # Create timeline visualization
    df_timeline = pd.DataFrame(timeline_data[:10])  # Show last 10 events
    
    # Color mapping for events
    color_map = {
        'Session Start': '#28a745',
        'Session End': '#dc3545',
        'Break Start': '#ffc107',
        'Break End': '#17a2b8',
        'Provider Change': '#6f42c1'
    }
    
    df_timeline['Color'] = df_timeline['Event'].map(color_map)
    
    fig = px.scatter(
        df_timeline,
        x='Display_Time',
        y='Scribe',
        color='Event',
        title="Recent Activity Timeline",
        color_discrete_map=color_map,
        size_max=15
    )
    
    fig.update_layout(
        height=300,
        xaxis_title="Time",
        yaxis_title="Scribe"
    )
    
    st.plotly_chart(fig, use_container_width=True)
