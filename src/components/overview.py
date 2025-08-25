"""
Executive Overview dashboard component
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Access processed data via session state
def _get_dp():
    return st.session_state.get('data_processor', None)


def render_overview():
    """Render the executive overview dashboard"""
    
    st.header("📊 Executive Overview")
    st.markdown("High-level performance metrics and key insights")
    
    # Key Metrics Cards
    render_key_metrics()
    
    st.markdown("---")
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        render_team_comparison()
        render_monthly_trends()
    
    with col2:
        render_performance_distribution()
        render_utilization_overview()
    
    # Recent activity summary
    st.markdown("---")
    render_recent_activity()


def render_key_metrics():
    """Render key performance indicator cards"""
    dp = _get_dp()
    metrics = dp.get_summary_stats() if dp else {}
    total_scribes = int(metrics.get('total_scribes') or 0)
    active_providers = int(metrics.get('total_providers') or 0)
    monthly_patients = int(metrics.get('total_monthly_patients') or 0)
    avg_efficiency = float(metrics.get('avg_efficiency') or 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Scribes",
            value=total_scribes,
            delta="2 new this month",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Active Providers", 
            value=active_providers,
            delta="3 added",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Patients This Month",
            value=f"{monthly_patients:,}",
            delta="12.5% vs last month",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Avg Efficiency",
            value=f"{avg_efficiency}%",
            delta="2.1% improvement",
            delta_color="normal"
        )


def render_team_comparison():
    """Render team performance comparison chart"""
    
    st.subheader("Team Performance Comparison")
    dp = _get_dp()
    if not dp:
        st.info("Data not loaded yet.")
        return
    team_comp = dp.get_team_comparison()
    if not team_comp:
        st.info("No team comparison data.")
        return
    # Build dataframe from dict of dicts
    df = pd.DataFrame(team_comp)
    # Expected keys: 'Efficiency Score', 'Monthly Patients', 'Provider Rating'
    # They were suffixed with _Team_Avg earlier for individual rows; here groupby produced plain names
    df = df.T.reset_index().rename(columns={'index': 'Team Leader'})
    df = df.rename(columns={
        'Efficiency Score': 'Avg Efficiency',
        'Monthly Patients': 'Patient Count',
        'Provider Rating': 'Avg Provider Rating'
    })
    team_data = df[['Team Leader', 'Avg Efficiency', 'Patient Count']]
    
    # Create bar chart
    fig = px.bar(
        team_data,
        x='Team Leader',
        y='Avg Efficiency',
        color='Team Leader',
        title="Average Team Efficiency",
        color_discrete_map={
            'Haider Khan': '#1f77b4',
            'Saqib Sherwani': '#ff7f0e'
        }
    )
    
    fig.update_layout(
        showlegend=False,
        height=300,
        yaxis_title="Efficiency (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_monthly_trends():
    """Render monthly performance trends"""
    
    st.subheader("Monthly Patient Count Trends")
    dp = _get_dp()
    if not dp:
        st.info("Data not loaded yet.")
        return
    sessions = dp.processed_data.get('sessions') if hasattr(dp, 'processed_data') else None
    if sessions is None or sessions.empty:
        st.info("No session data to show trends.")
        return
    # Aggregate monthly patient counts by team leader if available via scribe mapping
    scribes = dp.processed_data.get('scribes')
    if scribes is not None and not scribes.empty and 'Scribe Name' in scribes.columns and 'Team Leader' in scribes.columns:
        # Map scribe to team
        scribe_to_team = dict(zip(scribes['Scribe Name'], scribes['Team Leader']))
        if 'Scribe' in sessions.columns:
            sessions = sessions.copy()
            sessions['Team Leader'] = sessions['Scribe'].map(scribe_to_team)
    # Build monthly sum by team
    if 'Team Leader' in sessions.columns:
        monthly = sessions.groupby(['Month', 'Team Leader'])['Patient Count'].sum().reset_index()
        fig = px.line(
            monthly,
            x='Month',
            y='Patient Count',
            color='Team Leader',
            title="Monthly Patient Count by Team",
            markers=True
        )
    else:
        monthly = sessions.groupby('Month')['Patient Count'].sum().reset_index()
        fig = px.line(
            monthly,
            x='Month',
            y='Patient Count',
            title="Monthly Patient Count",
            markers=True
        )
    fig.update_layout(
        title="Monthly Patient Count by Team",
        xaxis_title="Month",
        yaxis_title="Patient Count",
        height=300,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_performance_distribution():
    """Render scribe performance distribution"""
    
    st.subheader("Scribe Performance Distribution")
    dp = _get_dp()
    if not dp:
        st.info("Data not loaded yet.")
        return
    scribes = dp.get_scribe_performance()
    if scribes is None or scribes.empty or 'Efficiency Score' not in scribes.columns:
        st.info("No efficiency data available.")
        return
    fig = px.histogram(
        scribes,
        x='Efficiency Score',
        nbins=15,
        title="Efficiency Score Distribution",
        labels={'x': 'Efficiency Score (%)', 'y': 'Number of Scribes'}
    )
    
    fig.update_layout(
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_utilization_overview():
    """Render utilization overview chart"""
    
    st.subheader("Resource Utilization")
    dp = _get_dp()
    if not dp:
        st.info("Data not loaded yet.")
        return
    scribes = dp.get_scribe_performance()
    if scribes is None or scribes.empty or 'Monthly Patients' not in scribes.columns:
        st.info("No utilization data available.")
        return
    # Categorize workload using processor's logic
    category_col = 'Workload Category' if 'Workload Category' in scribes.columns else None
    if not category_col:
        # Fallback: derive categories quickly
        def _cat(p):
            if pd.isna(p):
                return 'Unknown'
            return 'High (>100)' if p >= 100 else ('Medium (70-99)' if p >= 70 else 'Low (<70)')
        scribes = scribes.copy()
        scribes['Workload Category'] = scribes['Monthly Patients'].apply(_cat)
        category_col = 'Workload Category'
    counts = scribes[category_col].value_counts().reset_index()
    counts.columns = ['Category', 'Count']
    fig = px.pie(
        counts,
        values='Count',
        names='Category',
        title="Scribe Utilization Categories",
        color_discrete_sequence=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']
    )
    
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)


def render_recent_activity():
    """Render recent activity summary"""
    
    st.subheader("📋 Recent Activity Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Today's Highlights")
        st.success("✅ 95% attendance rate")
        st.info("📊 1,247 patients processed")
        st.warning("⚠️ 3 providers need backup coverage")
        
    with col2:
        st.markdown("#### Alerts & Notifications")
        st.error("🚨 Dr. Smith's session ended early")
        st.info("💡 New provider onboarding: Dr. Johnson")
        st.success("🎉 Monthly target achieved 3 days early")
    
    # Recent activity table
    st.markdown("#### Recent Provider Sessions")
    dp = _get_dp()
    sessions = dp.processed_data.get('sessions') if dp else None
    if sessions is None or sessions.empty:
        st.info("No recent sessions available.")
        return
    # Build a simple recent list from available columns
    df = sessions.copy()
    # Prefer Date and Start Time/End Time if present
    if 'Date' in df.columns:
        df = df.sort_values(by='Date', ascending=False)
    df = df.head(10)
    out = pd.DataFrame({
        'Date': df.get('Date'),
        'Scribe': df.get('Scribe'),
        'Provider': df.get('Provider'),
        'Patients': df.get('Patient Count'),
        'Duration (h)': df.get('Duration_Hours')
    })
    st.dataframe(out, use_container_width=True, hide_index=True)
