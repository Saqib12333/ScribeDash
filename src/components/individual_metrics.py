"""
Individual Metrics dashboard component
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

def render_individual_metrics():
    """Render individual scribe metrics dashboard"""
    
    st.header("👤 Individual Scribe Metrics")
    st.markdown("Detailed performance analysis for individual scribes")
    
    # Scribe selector
    selected_scribe = render_scribe_selector()
    
    if selected_scribe and selected_scribe != "Select a scribe":
        # Individual metrics overview
        render_individual_overview(selected_scribe)
        
        st.markdown("---")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_efficiency_timeline(selected_scribe)
            render_workload_analysis(selected_scribe)
        
        with col2:
            render_provider_compatibility(selected_scribe)
            render_session_patterns(selected_scribe)
        
        # Detailed analysis
        st.markdown("---")
        render_detailed_performance(selected_scribe)
        
        # Goals and recommendations
        render_goals_recommendations(selected_scribe)
    
    else:
        st.info("👆 Please select a scribe to view their individual metrics")


def render_scribe_selector():
    """Render scribe selection interface"""
    dp = _get_dp()
    scribes_df = dp.get_scribe_performance() if dp else pd.DataFrame()
    teams_options = ["All Teams"]
    if not scribes_df.empty and 'Team Leader' in scribes_df.columns:
        teams_options += sorted(scribes_df['Team Leader'].dropna().unique().tolist())
    # Team filter
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_team = st.selectbox("Filter by Team", teams_options, key="individual_team_filter")
    
    # Get scribes list based on team selection
    scribes_list = ["Select a scribe"]
    if not scribes_df.empty:
        df = scribes_df.copy()
        if selected_team != "All Teams" and 'Team Leader' in df.columns:
            df = df[df['Team Leader'] == selected_team]
        if 'Scribe Name' in df.columns:
            scribes_list += sorted(df['Scribe Name'].dropna().unique().tolist())
    
    with col2:
        selected_scribe = st.selectbox(
            "Select Scribe",
            scribes_list,
            key="scribe_selector"
        )
    
    return selected_scribe


def render_individual_overview(scribe_name):
    """Render individual scribe overview metrics"""
    
    st.subheader(f"📊 {scribe_name} - Performance Overview")
    dp = _get_dp()
    eff = 0.0
    patients = 0
    avg_len = 0.0
    rating = 0.0
    if dp:
        s_df = dp.get_scribe_performance(scribe_name)
        if not s_df.empty:
            eff = float(s_df['Efficiency Score'].iloc[0]) if 'Efficiency Score' in s_df.columns else 0.0
            patients = int(s_df['Monthly Patients'].iloc[0]) if 'Monthly Patients' in s_df.columns else 0
            avg_len = float(s_df['Avg Session Length'].iloc[0]) if 'Avg Session Length' in s_df.columns else 0.0
            rating = float(s_df['Provider Rating'].iloc[0]) if 'Provider Rating' in s_df.columns else 0.0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Efficiency Score",
            value=f"{eff:.1f}%",
            delta="2.3% vs last month",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Monthly Patients",
            value=int(patients),
            delta="12 more",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Avg Session Length",
            value=f"{avg_len:.1f}h",
            delta="15min shorter",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Provider Rating",
            value=f"{rating:.1f}/5.0",
            delta="0.2 improvement",
            delta_color="normal"
        )


def render_efficiency_timeline(scribe_name):
    """Render efficiency timeline chart"""
    
    st.subheader("📈 Efficiency Timeline")
    
    # Sample data - replace with actual data
    dates = pd.date_range(start='2024-01-01', end='2024-08-31', freq='W')
    efficiency_scores = np.random.normal(90, 5, len(dates))
    efficiency_scores = np.clip(efficiency_scores, 70, 100)
    
    # Add some realistic trends
    trend = np.linspace(0, 8, len(dates))
    efficiency_scores += trend
    efficiency_scores = np.clip(efficiency_scores, 70, 100)
    
    df = pd.DataFrame({
        'Date': dates,
        'Efficiency': efficiency_scores
    })
    
    fig = px.line(
        df,
        x='Date',
        y='Efficiency',
        title=f"Weekly Efficiency Trends - {scribe_name}",
        markers=True
    )
    
    # Add average line
    avg_efficiency = efficiency_scores.mean()
    fig.add_hline(y=avg_efficiency, line_dash="dash", 
                  annotation_text=f"Average: {avg_efficiency:.1f}%")
    
    fig.update_layout(
        height=300,
        yaxis_title="Efficiency (%)",
        yaxis=dict(range=[70, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workload_analysis(scribe_name):
    """Render workload analysis chart"""
    
    st.subheader("⚖️ Daily Workload Pattern")
    
    # Sample data - replace with actual data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    patients_per_day = np.random.randint(8, 25, 7)
    hours_per_day = np.random.uniform(6, 10, 7)
    
    fig = go.Figure()
    
    # Add bars for patients
    fig.add_trace(go.Bar(
        x=days,
        y=patients_per_day,
        name='Patients',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    # Add line for hours
    fig.add_trace(go.Scatter(
        x=days,
        y=hours_per_day,
        mode='lines+markers',
        name='Hours Worked',
        line=dict(color='orange', width=3),
        yaxis='y2'
    ))
    
    # Update layout for dual y-axis
    fig.update_layout(
        title=f"Daily Workload - {scribe_name}",
        xaxis_title="Day of Week",
        yaxis=dict(title="Number of Patients", side="left"),
        yaxis2=dict(title="Hours Worked", side="right", overlaying="y"),
        height=300,
        legend=dict(x=0.01, y=0.99)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_provider_compatibility(scribe_name):
    """Render provider compatibility analysis"""
    
    st.subheader("🤝 Provider Compatibility")
    
    # Sample data - replace with actual data
    providers = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Davis']
    compatibility_scores = np.random.uniform(3.5, 5.0, len(providers))
    session_counts = np.random.randint(5, 30, len(providers))
    
    df = pd.DataFrame({
        'Provider': providers,
        'Rating': compatibility_scores,
        'Sessions': session_counts
    })
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x='Provider',
        y='Rating',
        size='Sessions',
        title=f"Provider Ratings - {scribe_name}",
        labels={'Rating': 'Provider Rating (1-5)'},
        size_max=50
    )
    
    fig.update_layout(
        height=300,
        yaxis=dict(range=[3, 5])
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_session_patterns(scribe_name):
    """Render session timing patterns"""
    
    st.subheader("🕐 Session Timing Patterns")
    
    # Sample data - replace with actual data
    hours = list(range(8, 20))  # 8 AM to 7 PM
    session_counts = np.random.poisson(3, len(hours))
    efficiency_by_hour = np.random.normal(90, 8, len(hours))
    efficiency_by_hour = np.clip(efficiency_by_hour, 70, 100)
    
    fig = go.Figure()
    
    # Add bars for session counts
    fig.add_trace(go.Bar(
        x=hours,
        y=session_counts,
        name='Sessions',
        marker_color='lightgreen',
        yaxis='y'
    ))
    
    # Add line for efficiency
    fig.add_trace(go.Scatter(
        x=hours,
        y=efficiency_by_hour,
        mode='lines+markers',
        name='Efficiency',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=f"Hourly Performance - {scribe_name}",
        xaxis_title="Hour of Day",
        yaxis=dict(title="Number of Sessions", side="left"),
        yaxis2=dict(title="Efficiency (%)", side="right", overlaying="y"),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_performance(scribe_name):
    """Render detailed performance metrics table"""
    
    st.subheader("📋 Detailed Performance Metrics")
    
    # Sample data - replace with actual data
    performance_data = pd.DataFrame({
        'Metric': [
            'Total Sessions This Month',
            'Average Session Duration',
            'Patient Documentation Rate',
            'Error Rate',
            'On-Time Start Rate',
            'Provider Feedback Score',
            'Training Completion Rate',
            'Weekend Availability',
            'Peak Hours Coverage',
            'Backup Coverage Provided'
        ],
        'Current Value': [
            '127 sessions',
            '3.2 hours',
            '98.5%',
            '1.2%',
            '96.8%',
            '4.7/5.0',
            '100%',
            '85%',
            '92%',
            '12 times'
        ],
        'Target': [
            '120+ sessions',
            '< 3.5 hours',
            '> 95%',
            '< 2%',
            '> 95%',
            '> 4.5',
            '100%',
            '> 80%',
            '> 90%',
            '10+ times'
        ],
        'Status': [
            '✅ Exceeded',
            '✅ Met',
            '✅ Exceeded',
            '✅ Met',
            '✅ Exceeded',
            '✅ Exceeded',
            '✅ Met',
            '✅ Exceeded',
            '✅ Exceeded',
            '✅ Exceeded'
        ]
    })
    
    st.dataframe(
        performance_data,
        use_container_width=True,
        hide_index=True
    )


def render_goals_recommendations(scribe_name):
    """Render goals and recommendations section"""
    
    st.subheader("🎯 Goals & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Current Goals")
        st.success("✅ Maintain 95%+ efficiency rate")
        st.success("✅ Complete advanced EHR training")
        st.info("🎯 Reduce average session time by 10%")
        st.info("🎯 Increase weekend availability to 90%")
        
        st.markdown("#### 🏆 Recent Achievements")
        st.success("🎉 Perfect attendance for 2 months")
        st.success("🎉 Highest provider rating in team")
        st.success("🎉 Completed specialty training")
    
    with col2:
        st.markdown("#### 💡 Recommendations")
        st.info("""
        **Efficiency Improvement:**
        - Practice keyboard shortcuts for faster documentation
        - Use templates for common procedures
        - Focus on peak performance hours (10 AM - 2 PM)
        """)
        
        st.warning("""
        **Areas for Development:**
        - Consider additional training in cardiology documentation
        - Work on maintaining consistency during late shifts
        - Explore mentoring opportunities for new scribes
        """)
        
        st.markdown("#### 📊 Performance Trend")
        trend_direction = "📈 Improving"
        st.success(f"**Overall Trend:** {trend_direction}")
        st.markdown("Consistent upward trajectory in all key metrics")
    
    # Action items
    st.markdown("#### ✅ Action Items")
    
    action_items = pd.DataFrame({
        'Priority': ['High', 'Medium', 'Low', 'Low'],
        'Action': [
            'Complete advanced cardiology module by end of month',
            'Schedule feedback session with Dr. Johnson',
            'Review and update personal workflow templates',
            'Consider taking on mentoring role for new hire'
        ],
        'Due Date': ['2024-09-30', '2024-09-15', '2024-10-15', '2024-11-01'],
        'Status': ['In Progress', 'Not Started', 'Not Started', 'Planning']
    })
    
    # Color code by priority
    def highlight_priority(row):
        if row['Priority'] == 'High':
            return ['background-color: #f8d7da'] * len(row)
        elif row['Priority'] == 'Medium':
            return ['background-color: #fff3cd'] * len(row)
        else:
            return ['background-color: #d4edda'] * len(row)
    
    st.dataframe(
        action_items,
        use_container_width=True,
        hide_index=True
    )
