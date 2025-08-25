"""
Team Performance dashboard component
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

def render_team_performance():
    """Render team performance analysis dashboard"""
    
    st.header("👥 Team Performance Analysis")
    st.markdown("Detailed performance metrics by team and individual scribes")
    
    # Team selector (dynamic from data)
    dp = _get_dp()
    teams = ["All Teams"]
    if dp and hasattr(dp, 'processed_data'):
        scribes = dp.processed_data.get('scribes')
        if scribes is not None and not scribes.empty and 'Team Leader' in scribes.columns:
            teams = ["All Teams"] + sorted(scribes['Team Leader'].dropna().unique().tolist())
    selected_team = st.selectbox("Select Team", teams, key="team_selector")
    
    # Performance metrics overview
    render_team_metrics(selected_team)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_efficiency_trends(selected_team)
        render_workload_distribution(selected_team)
    
    with col2:
        render_performance_rankings(selected_team)
        render_attendance_patterns(selected_team)
    
    # Detailed team comparison
    st.markdown("---")
    render_detailed_comparison()


def render_team_metrics(selected_team):
    """Render team-specific performance metrics"""
    
    st.subheader(f"📊 {selected_team} Metrics")
    dp = _get_dp()
    team_size = 0
    avg_efficiency = 0.0
    total_patients = 0
    avg_hours = 0.0
    if dp and hasattr(dp, 'processed_data'):
        scribes = dp.processed_data.get('scribes')
        sessions = dp.processed_data.get('sessions')
        if scribes is not None and not scribes.empty:
            df = scribes.copy()
            if selected_team != "All Teams" and 'Team Leader' in df.columns:
                df = df[df['Team Leader'] == selected_team]
            team_size = len(df)
            if 'Efficiency Score' in df.columns:
                avg_efficiency = float(df['Efficiency Score'].mean())
            if 'Monthly Patients' in df.columns:
                total_patients = int(df['Monthly Patients'].sum())
            if sessions is not None and not sessions.empty and 'Duration_Hours' in sessions.columns:
                if selected_team != "All Teams" and 'Scribe' in sessions.columns and 'Scribe Name' in scribes.columns:
                    scribe_to_team = dict(zip(scribes['Scribe Name'], scribes['Team Leader']))
                    s_df = sessions.copy()
                    s_df['Team Leader'] = s_df['Scribe'].map(scribe_to_team)
                    s_df = s_df[s_df['Team Leader'] == selected_team]
                else:
                    s_df = sessions
                avg_hours = float(s_df['Duration_Hours'].mean() or 0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Team Size",
            value=team_size,
            delta="Active scribes"
        )
    
    with col2:
        st.metric(
            label="Avg Efficiency",
            value=f"{avg_efficiency}%",
            delta="2.1% vs last month",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Monthly Patients",
            value=f"{total_patients:,}",
            delta="8.3% increase",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Avg Hours/Day",
            value=f"{avg_hours}h",
            delta="0.5h more",
            delta_color="normal"
        )


def render_efficiency_trends(selected_team):
    """Render efficiency trends over time"""
    
    st.subheader("📈 Efficiency Trends")
    dp = _get_dp()
    if not dp or not hasattr(dp, 'processed_data'):
        st.info("Data not loaded yet.")
        return
    sessions = dp.processed_data.get('sessions')
    if sessions is None or sessions.empty:
        st.info("No session data available.")
        return
    scribes = dp.processed_data.get('scribes')
    s_df = sessions.copy()
    if selected_team != "All Teams" and scribes is not None and not scribes.empty and 'Scribe' in s_df.columns and 'Scribe Name' in scribes.columns:
        scribe_to_team = dict(zip(scribes['Scribe Name'], scribes['Team Leader']))
        s_df['Team Leader'] = s_df['Scribe'].map(scribe_to_team)
        s_df = s_df[s_df['Team Leader'] == selected_team]
    # Use Session Rating as proxy for efficiency over months
    if 'Session Rating' not in s_df.columns or 'Month' not in s_df.columns:
        st.info("Insufficient data to compute trends.")
        return
    df = s_df.groupby('Month')['Session Rating'].mean().reset_index().rename(columns={'Session Rating': 'Efficiency'})
    fig = px.line(df, x='Month', y='Efficiency', title=f"Efficiency Trends - {selected_team}", markers=True)
    
    fig.update_layout(
        height=300,
        yaxis_title="Efficiency (%)",
        yaxis=dict(range=[80, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workload_distribution(selected_team):
    """Render workload distribution chart"""
    
    st.subheader("⚖️ Workload Distribution")
    dp = _get_dp()
    if not dp or not hasattr(dp, 'processed_data'):
        st.info("Data not loaded yet.")
        return
    scribes = dp.processed_data.get('scribes')
    if scribes is None or scribes.empty or 'Monthly Patients' not in scribes.columns:
        st.info("No workload data available.")
        return
    df = scribes.copy()
    if selected_team != "All Teams" and 'Team Leader' in df.columns:
        df = df[df['Team Leader'] == selected_team]
    # Bin patient counts
    bins = [-1, 50, 75, 100, 125, np.inf]
    labels = ['0-50', '51-75', '76-100', '101-125', '126+']
    df['Range'] = pd.cut(df['Monthly Patients'], bins=bins, labels=labels)
    counts = df['Range'].value_counts().reindex(labels, fill_value=0)
    fig = px.bar(x=counts.index, y=counts.values, title="Patients per Scribe Distribution", labels={'x': 'Patients per Month', 'y': 'Number of Scribes'})
    
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)


def render_performance_rankings(selected_team):
    """Render top performer rankings"""
    
    st.subheader("🏆 Top Performers")
    dp = _get_dp()
    if not dp or not hasattr(dp, 'processed_data'):
        st.info("Data not loaded yet.")
        return
    scribes = dp.processed_data.get('scribes')
    if scribes is None or scribes.empty:
        st.info("No scribe data available.")
        return
    df = scribes.copy()
    if selected_team != "All Teams" and 'Team Leader' in df.columns:
        df = df[df['Team Leader'] == selected_team]
    # Keep top 5 by efficiency
    cols = [c for c in ['Scribe Name', 'Efficiency Score', 'Monthly Patients'] if c in df.columns]
    df = df[cols].dropna().sort_values(by='Efficiency Score', ascending=False).head(5)
    df = df.rename(columns={'Scribe Name': 'Scribe', 'Efficiency Score': 'Efficiency (%)', 'Monthly Patients': 'Patients'})
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Efficiency (%)': st.column_config.ProgressColumn(
                'Efficiency (%)',
                help="Efficiency percentage",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )
        }
    )


def render_attendance_patterns(selected_team):
    """Render attendance patterns"""
    
    st.subheader("📅 Attendance Patterns")
    dp = _get_dp()
    if not dp or not hasattr(dp, 'processed_data'):
        st.info("Data not loaded yet.")
        return
    scribes = dp.processed_data.get('scribes')
    if scribes is None or scribes.empty or 'Attendance Rate' not in scribes.columns:
        st.info("No attendance data available.")
        return
    df = scribes.copy()
    if selected_team != "All Teams" and 'Team Leader' in df.columns:
        df = df[df['Team Leader'] == selected_team]
    fig = px.histogram(df, x='Attendance Rate', nbins=10, title='Attendance Rate Distribution', labels={'x': 'Attendance Rate (%)', 'y': 'Scribes'})
    
    fig.update_layout(
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_comparison():
    """Render detailed team comparison table"""
    
    st.subheader("📋 Detailed Team Comparison")
    
    # Sample data - replace with actual data
    comparison_data = pd.DataFrame({
        'Metric': [
            'Team Size',
            'Avg Efficiency (%)',
            'Total Patients',
            'Avg Patients/Scribe',
            'Avg Hours/Day',
            'Attendance Rate (%)',
            'Provider Coverage',
            'Peak Hours Efficiency',
            'Weekend Coverage (%)',
            'Training Hours/Month'
        ],
        'Haider Khan Team': [
            18, 92.5, 1420, 79, 8.2, 94.5, 21, 89.8, 85, 12
        ],
        'Saqib Sherwani Team': [
            20, 95.8, 1420, 71, 8.5, 96.2, 21, 93.2, 87, 15
        ],
        'Difference': [
            '+2', '+3.3%', '0', '-8', '+0.3h', '+1.7%', '0', '+3.4%', '+2%', '+3h'
        ]
    })
    
    # Apply styling to highlight differences
    def highlight_better_performance(row):
        if row.name in [1, 4, 5, 7, 8, 9]:  # Metrics where higher is better
            if '+' in str(row['Difference']):
                return ['', '', 'background-color: #d4edda', 'background-color: #d4edda']
            elif '-' in str(row['Difference']):
                return ['', 'background-color: #d4edda', '', 'background-color: #f8d7da']
        return ['', '', '', '']
    
    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Performance insights
    st.markdown("#### 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Saqib Sherwani Team Strengths:**
        - Higher efficiency rate (95.8% vs 92.5%)
        - Better attendance (96.2% vs 94.5%)
        - More training hours per month
        """)
    
    with col2:
        st.info("""
        **Haider Khan Team Strengths:**
        - More patients per scribe (79 vs 71)
        - Balanced workload distribution
        - Consistent performance trends
        """)
    
    st.success("""
    **Overall Assessment:** Both teams are performing excellently with complementary strengths. 
    Consider cross-team knowledge sharing to leverage best practices from both teams.
    """)
