"""
Provider Analysis dashboard component
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

def render_provider_analysis():
    """Render provider analysis dashboard"""
    
    st.header("🩺 Provider Analysis")
    st.markdown("Insights into provider preferences, assignments, and performance metrics")
    
    # Provider selector and filters
    selected_provider = render_provider_selector()
    
    if selected_provider and selected_provider != "Select a provider":
        # Provider overview
        render_provider_overview(selected_provider)
        
        st.markdown("---")
        
        # Analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_scribe_assignments(selected_provider)
            render_session_patterns(selected_provider)
        
        with col2:
            render_performance_metrics(selected_provider)
            render_speciality_analysis(selected_provider)
        
        # Detailed insights
        st.markdown("---")
        render_provider_insights(selected_provider)
    
    else:
        # Show overall provider analytics
        render_overall_provider_analytics()


def render_provider_selector():
    """Render provider selection interface"""
    dp = _get_dp()
    providers = ["Select a provider"]
    if dp and hasattr(dp, 'processed_data'):
        pv = dp.processed_data.get('providers')
        if pv is not None and not pv.empty and 'Provider' in pv.columns:
            providers += sorted(pv['Provider'].dropna().unique().tolist())
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_provider = st.selectbox(
            "Select Provider",
            providers,
            key="provider_selector"
        )
    
    with col2:
        if selected_provider != "Select a provider":
            specialty_filter = st.selectbox(
                "Filter by Specialty",
                ["All", "Internal Medicine", "Family Medicine", "Cardiology", "Orthopedics", "Emergency Medicine"],
                key="specialty_filter"
            )
    
    return selected_provider


def render_provider_overview(provider_name):
    """Render provider overview metrics"""
    
    st.subheader(f"📊 {provider_name} - Overview")
    dp = _get_dp()
    assigned_scribes = 0
    avg_session_length = 0.0
    monthly_patients = 0
    satisfaction_score = 0.0
    if dp and hasattr(dp, 'processed_data'):
        pv = dp.processed_data.get('providers')
        if pv is not None and not pv.empty and 'Provider' in pv.columns:
            row = pv[pv['Provider'] == provider_name]
            if not row.empty:
                monthly_patients = int(row['Patient Count_sum'].iloc[0]) if 'Patient Count_sum' in row.columns else int(row['Patient Count_mean'].iloc[0]) if 'Patient Count_mean' in row.columns else 0
                avg_session_length = float(row['Avg Session Duration_mean'].iloc[0]) if 'Avg Session Duration_mean' in row.columns else 0.0
        # Estimate assigned_scribes from sessions mapping if available
        sessions = dp.processed_data.get('sessions')
        if sessions is not None and not sessions.empty and 'Provider' in sessions.columns and 'Scribe' in sessions.columns:
            assigned_scribes = sessions[sessions['Provider'] == provider_name]['Scribe'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Assigned Scribes",
            value=assigned_scribes,
            delta="1 new this month"
        )
    
    with col2:
        st.metric(
            label="Avg Session Length",
            value=f"{avg_session_length:.1f}h",
            delta="20min shorter",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Monthly Patients",
            value=int(monthly_patients),
            delta="15% increase",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Satisfaction Score",
            value=f"{satisfaction_score:.1f}/5.0",
            delta="0.3 improvement",
            delta_color="normal"
        )


def render_scribe_assignments(provider_name):
    """Render scribe assignment analysis"""
    
    st.subheader("👥 Scribe Assignment History")
    
    # Sample data - replace with actual data
    scribes = ['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Rohan Setia']
    sessions = np.random.randint(10, 50, len(scribes))
    avg_ratings = np.random.uniform(4.0, 5.0, len(scribes))
    
    df = pd.DataFrame({
        'Scribe': scribes,
        'Sessions': sessions,
        'Avg Rating': avg_ratings
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='Sessions',
        y='Scribe',
        orientation='h',
        title=f"Sessions by Scribe - {provider_name}",
        color='Avg Rating',
        color_continuous_scale='viridis',
        text='Sessions'
    )
    
    fig.update_layout(
        height=300,
        xaxis_title="Number of Sessions"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_session_patterns(provider_name):
    """Render session timing and pattern analysis"""
    
    st.subheader("📅 Session Patterns")
    
    # Sample data - replace with actual data
    hours = list(range(8, 18))  # 8 AM to 5 PM
    sessions_by_hour = np.random.poisson(2, len(hours))
    
    # Create more realistic pattern (peak hours)
    peak_hours = [9, 10, 11, 14, 15, 16]
    for hour in peak_hours:
        if hour in hours:
            idx = hours.index(hour)
            sessions_by_hour[idx] += np.random.randint(2, 5)
    
    fig = px.bar(
        x=hours,
        y=sessions_by_hour,
        title=f"Daily Session Distribution - {provider_name}",
        labels={'x': 'Hour of Day', 'y': 'Average Sessions'},
        color=sessions_by_hour,
        color_continuous_scale='blues'
    )
    
    fig.update_layout(
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_performance_metrics(provider_name):
    """Render provider performance metrics"""
    
    st.subheader("📈 Performance Trends")
    
    # Sample data - replace with actual data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    patient_counts = np.random.randint(80, 150, len(months))
    efficiency_scores = np.random.uniform(85, 98, len(months))
    
    fig = go.Figure()
    
    # Add patient count bars
    fig.add_trace(go.Bar(
        x=months,
        y=patient_counts,
        name='Patient Count',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    # Add efficiency line
    fig.add_trace(go.Scatter(
        x=months,
        y=efficiency_scores,
        mode='lines+markers',
        name='Efficiency Score',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=f"Monthly Performance - {provider_name}",
        xaxis_title="Month",
        yaxis=dict(title="Patient Count", side="left"),
        yaxis2=dict(title="Efficiency Score (%)", side="right", overlaying="y"),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_speciality_analysis(provider_name):
    """Render specialty/procedure analysis"""
    
    st.subheader("🔬 Procedure Complexity")
    
    # Sample data - replace with actual data
    procedures = ['Routine Checkup', 'Diagnostic', 'Follow-up', 'Emergency', 'Consultation']
    counts = np.random.randint(5, 30, len(procedures))
    avg_duration = np.random.uniform(15, 60, len(procedures))
    
    df = pd.DataFrame({
        'Procedure': procedures,
        'Count': counts,
        'Avg Duration (min)': avg_duration
    })
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x='Procedure',
        y='Avg Duration (min)',
        size='Count',
        title=f"Procedure Analysis - {provider_name}",
        size_max=50,
        color='Count',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)


def render_provider_insights(provider_name):
    """Render detailed provider insights"""
    
    st.subheader("💡 Provider Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Performance Summary")
        
        # Performance metrics table
        performance_data = pd.DataFrame({
            'Metric': [
                'Documentation Accuracy',
                'Session Efficiency',
                'Scribe Satisfaction',
                'Patient Throughput',
                'EHR Utilization',
                'Communication Score'
            ],
            'Score': ['96.8%', '94.2%', '4.7/5.0', '125%', '92.1%', '4.8/5.0'],
            'Trend': ['↗️ +2.1%', '↗️ +1.8%', '↗️ +0.2', '↗️ +8%', '↘️ -0.5%', '→ Stable']
        })
        
        st.dataframe(
            performance_data,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("#### 🎯 Optimization Opportunities")
        st.info("""
        **Scribe Utilization:**
        - Peak efficiency with Nikhil Yadav (98.5%)
        - Consider pairing with newer scribes for training
        - Optimal session length: 3.2 hours
        """)
        
    with col2:
        st.markdown("#### 📋 Recent Activity")
        
        recent_activity = pd.DataFrame({
            'Date': ['Aug 15', 'Aug 14', 'Aug 13', 'Aug 12', 'Aug 11'],
            'Scribe': ['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Nikhil Yadav', 'Rohan Setia'],
            'Patients': [18, 15, 22, 20, 16],
            'Duration': ['4.2h', '3.8h', '4.5h', '4.1h', '3.9h'],
            'Rating': ['5.0', '4.8', '4.9', '5.0', '4.7']
        })
        
        st.dataframe(
            recent_activity,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("#### 🔄 Recommendations")
        st.success("""
        **Best Practices:**
        - Continue partnership with top-rated scribes
        - Schedule complex cases during peak hours (10-2 PM)
        - Maintain current documentation workflow
        """)
        
        st.warning("""
        **Areas for Improvement:**
        - EHR utilization slightly below target
        - Consider template optimization
        - Review documentation shortcuts
        """)


def render_overall_provider_analytics():
    """Render overall provider analytics when no specific provider is selected"""
    
    st.info("👆 Select a provider above to view detailed analysis, or explore overall provider insights below")
    
    st.subheader("🏥 Overall Provider Analytics")
    
    # Provider summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    dp = _get_dp()
    total_providers = 0
    active_sessions_today = 0
    avg_satisfaction = 0.0
    coverage_rate = 0.0
    if dp and hasattr(dp, 'processed_data'):
        pv = dp.processed_data.get('providers')
        if pv is not None and not pv.empty and 'Provider' in pv.columns:
            total_providers = pv['Provider'].nunique()
            avg_satisfaction = float(pv['Consistency_Score'].mean()) if 'Consistency_Score' in pv.columns else 0.0
        sessions = dp.processed_data.get('sessions')
        if sessions is not None and not sessions.empty:
            active_sessions_today = int(sessions['Patient Count'].sum()) if 'Patient Count' in sessions.columns else 0
    with col1:
        st.metric(label="Total Providers", value=total_providers, delta="")
    
    with col2:
        st.metric(label="Patients in Data", value=active_sessions_today, delta="")
    
    with col3:
        st.metric(label="Avg Consistency", value=f"{avg_satisfaction:.1f}%", delta="")
    
    with col4:
        st.metric(label="Coverage Rate", value=f"{coverage_rate:.1f}%", delta="")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Provider specialty distribution
        st.subheader("🏥 Provider Specialties")
        
        specialties = ['Internal Medicine', 'Family Medicine', 'Cardiology', 'Orthopedics', 'Emergency Medicine', 'Other']
        counts = [12, 8, 6, 5, 4, 7]
        
        fig = px.pie(
            values=counts,
            names=specialties,
            title="Provider Distribution by Specialty"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Session volume by provider
        st.subheader("📊 Top Providers by Volume")
        
        top_providers = ['Dr. Mark Basham', 'Dr. Sarah Johnson', 'Amanda DeBois', 'Dr. Michael Chen', 'Melanie Arrington']
        session_counts = [156, 142, 138, 134, 129]
        
        fig = px.bar(
            x=session_counts,
            y=top_providers,
            orientation='h',
            title="Monthly Session Counts",
            labels={'x': 'Sessions', 'y': 'Provider'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Provider performance table
    st.subheader("📋 Provider Performance Summary")
    
    provider_summary = pd.DataFrame({
        'Provider': ['Dr. Mark Basham', 'Amanda DeBois', 'Melanie Arrington', 'Dr. Sarah Johnson', 'Alison Blake'],
        'Specialty': ['Internal Medicine', 'Family Medicine', 'Cardiology', 'Emergency Medicine', 'Orthopedics'],
        'Sessions': [156, 138, 129, 142, 121],
        'Avg Rating': [4.8, 4.7, 4.9, 4.6, 4.8],
        'Preferred Scribes': [3, 2, 4, 3, 2],
        'Efficiency': ['96.2%', '94.8%', '97.1%', '93.5%', '95.9%']
    })
    
    st.dataframe(
        provider_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Avg Rating': st.column_config.ProgressColumn(
                'Avg Rating',
                help="Provider satisfaction rating",
                min_value=0,
                max_value=5,
                format="%.1f"
            ),
            'Efficiency': st.column_config.ProgressColumn(
                'Efficiency',
                help="Documentation efficiency",
                min_value=0,
                max_value=100,
                format="%s"
            )
        }
    )
