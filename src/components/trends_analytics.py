"""
Trends and Analytics dashboard component
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def render_trends_analytics():
    """Render trends and analytics dashboard"""
    
    st.header("📈 Trends & Analytics")
    st.markdown("Historical analysis and predictive insights for strategic planning")
    
    # Time period selector
    time_period = render_time_period_selector()
    
    # Key trend indicators
    render_trend_indicators(time_period)
    
    st.markdown("---")
    
    # Main analytics sections
    col1, col2 = st.columns(2)
    
    with col1:
        render_performance_trends(time_period)
        render_workload_trends(time_period)
        render_efficiency_analysis(time_period)
    
    with col2:
        render_utilization_trends(time_period)
        render_growth_projections(time_period)
        render_seasonal_patterns(time_period)
    
    # Advanced analytics
    st.markdown("---")
    render_advanced_analytics(time_period)


def render_time_period_selector():
    """Render time period selection controls"""
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        time_period = st.selectbox(
            "Analysis Period",
            ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "Year to Date"],
            index=2,
            key="trends_time_period"
        )
    
    with col2:
        comparison_period = st.selectbox(
            "Compare With",
            ["Previous Period", "Same Period Last Year", "No Comparison"],
            key="comparison_period"
        )
    
    with col3:
        st.markdown("#### 📅 Analysis Focus")
        focus_areas = st.multiselect(
            "Select focus areas",
            ["Efficiency", "Workload", "Utilization", "Growth", "Seasonal Patterns"],
            default=["Efficiency", "Workload"],
            key="focus_areas"
        )
    
    return time_period


def render_trend_indicators(time_period):
    """Render key trend indicator cards"""
    
    st.subheader("📊 Key Trend Indicators")
    
    # Sample trend data - replace with actual calculations
    efficiency_trend = np.random.uniform(2, 8)
    workload_trend = np.random.uniform(-5, 15)
    utilization_trend = np.random.uniform(1, 6)
    satisfaction_trend = np.random.uniform(0.1, 0.5)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Efficiency Trend",
            value=f"{94.2}%",
            delta=f"+{efficiency_trend:.1f}% vs previous period",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Workload Growth",
            value=f"{2840}",
            delta=f"+{workload_trend:.1f}% patients",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Utilization Rate",
            value=f"{89.7}%",
            delta=f"+{utilization_trend:.1f}% improvement",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Satisfaction Score",
            value=f"{4.6}/5.0",
            delta=f"+{satisfaction_trend:.1f} rating increase",
            delta_color="normal"
        )


def render_performance_trends(time_period):
    """Render performance trends over time"""
    
    st.subheader("📈 Performance Trends")
    
    # Generate sample data based on time period
    if time_period == "Last 30 Days":
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        freq_label = "Daily"
    elif time_period == "Last 3 Months":
        dates = pd.date_range(end=datetime.now(), periods=12, freq='W')
        freq_label = "Weekly"
    elif time_period == "Last 6 Months":
        dates = pd.date_range(end=datetime.now(), periods=6, freq='ME')
        freq_label = "Monthly"
    else:
        dates = pd.date_range(end=datetime.now(), periods=12, freq='ME')
        freq_label = "Monthly"
    
    # Generate performance data with realistic trends
    base_efficiency = 85
    efficiency_trend = np.linspace(0, 10, len(dates))
    noise = np.random.normal(0, 2, len(dates))
    efficiency_scores = base_efficiency + efficiency_trend + noise
    efficiency_scores = np.clip(efficiency_scores, 70, 100)
    
    # Team-specific data
    haider_team = efficiency_scores + np.random.normal(-2, 1, len(dates))
    saqib_team = efficiency_scores + np.random.normal(2, 1, len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'Overall': efficiency_scores,
        'Haider Khan Team': np.clip(haider_team, 70, 100),
        'Saqib Sherwani Team': np.clip(saqib_team, 70, 100)
    })
    
    fig = px.line(
        df,
        x='Date',
        y=['Overall', 'Haider Khan Team', 'Saqib Sherwani Team'],
        title=f"{freq_label} Efficiency Trends",
        markers=True
    )
    
    fig.update_layout(
        height=300,
        yaxis_title="Efficiency (%)",
        legend_title="Teams"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workload_trends(time_period):
    """Render workload distribution trends"""
    
    st.subheader("⚖️ Workload Distribution Trends")
    
    # Sample workload data
    months = ['Apr', 'May', 'Jun', 'Jul', 'Aug']
    low_workload = [2, 1, 1, 1, 2]      # <70 patients
    med_workload = [8, 10, 12, 15, 18]   # 70-100 patients
    high_workload = [15, 18, 20, 18, 15] # 100+ patients
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=low_workload,
        name='Low Workload (<70)',
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        x=months,
        y=med_workload,
        name='Medium Workload (70-100)',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=months,
        y=high_workload,
        name='High Workload (100+)',
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title="Workload Distribution Over Time",
        xaxis_title="Month",
        yaxis_title="Number of Scribes",
        barmode='stack',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_analysis(time_period):
    """Render detailed efficiency analysis"""
    
    st.subheader("🎯 Efficiency Analysis")
    
    # Efficiency distribution analysis
    efficiency_ranges = ['60-70%', '70-80%', '80-90%', '90-95%', '95-100%']
    
    # Current period
    current_counts = [1, 4, 15, 12, 6]
    # Previous period (for comparison)
    previous_counts = [2, 6, 18, 10, 2]
    
    df = pd.DataFrame({
        'Efficiency Range': efficiency_ranges,
        'Current Period': current_counts,
        'Previous Period': previous_counts
    })
    
    fig = px.bar(
        df,
        x='Efficiency Range',
        y=['Current Period', 'Previous Period'],
        title="Efficiency Distribution Comparison",
        barmode='group'
    )
    
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)


def render_utilization_trends(time_period):
    """Render utilization trends and patterns"""
    
    st.subheader("📊 Utilization Trends")
    
    # Sample utilization data
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    peak_hours = [92, 94, 96, 93]    # 10 AM - 2 PM
    standard_hours = [85, 87, 89, 86] # 8-10 AM, 2-6 PM
    off_hours = [65, 68, 70, 67]     # Before 8 AM, After 6 PM
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=peak_hours,
        mode='lines+markers',
        name='Peak Hours (10AM-2PM)',
        line=dict(color='green', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=standard_hours,
        mode='lines+markers',
        name='Standard Hours',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=off_hours,
        mode='lines+markers',
        name='Off Hours',
        line=dict(color='orange', width=3)
    ))
    
    fig.update_layout(
        title="Utilization by Time Periods",
        xaxis_title="Week",
        yaxis_title="Utilization (%)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_growth_projections(time_period):
    """Render growth projections and forecasts"""
    
    st.subheader("📈 Growth Projections")
    
    # Historical and projected data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    historical = [2200, 2350, 2420, 2580, 2650, 2740, 2840, 2900, None, None, None, None]
    projected = [None, None, None, None, None, None, None, None, 3050, 3200, 3350, 3500]
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=months[:8],
        y=historical[:8],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue', width=3)
    ))
    
    # Projected data
    fig.add_trace(go.Scatter(
        x=months[7:],
        y=[historical[7]] + projected[8:],
        mode='lines+markers',
        name='Projected',
        line=dict(color='red', width=3, dash='dash')
    ))
    
    # Confidence interval
    upper_bound = [3100, 3280, 3450, 3650]
    lower_bound = [3000, 3120, 3250, 3350]
    
    fig.add_trace(go.Scatter(
        x=months[8:],
        y=upper_bound,
        mode='lines',
        name='Upper Bound',
        line=dict(color='red', width=1),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=months[8:],
        y=lower_bound,
        mode='lines',
        name='Lower Bound',
        line=dict(color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.1)',
        showlegend=False
    ))
    
    fig.update_layout(
        title="Patient Volume Growth Projection",
        xaxis_title="Month",
        yaxis_title="Total Patients",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_seasonal_patterns(time_period):
    """Render seasonal patterns and cyclical trends"""
    
    st.subheader("🌟 Seasonal Patterns")
    
    # Day of week patterns
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    activity_levels = [95, 98, 96, 94, 92, 78, 65]
    
    fig = px.bar(
        x=days,
        y=activity_levels,
        title="Weekly Activity Patterns",
        labels={'x': 'Day of Week', 'y': 'Activity Level (%)'},
        color=activity_levels,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=300, showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)


def render_advanced_analytics(time_period):
    """Render advanced analytics and insights"""
    
    st.subheader("🔬 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Statistical Analysis")
        
        # Performance correlation matrix
        correlation_data = pd.DataFrame({
            'Metric': ['Efficiency', 'Workload', 'Session Length', 'Provider Rating'],
            'Efficiency': [1.0, 0.15, -0.32, 0.78],
            'Workload': [0.15, 1.0, 0.45, 0.22],
            'Session Length': [-0.32, 0.45, 1.0, -0.18],
            'Provider Rating': [0.78, 0.22, -0.18, 1.0]
        })
        
        st.dataframe(
            correlation_data,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("#### 🎯 Key Insights")
        st.success("✅ Strong correlation between efficiency and provider rating (0.78)")
        st.info("📊 Optimal session length appears to be 3.2 hours")
        st.warning("⚠️ Workload increase may impact efficiency beyond 120 patients/month")
        
    with col2:
        st.markdown("#### 📈 Predictive Insights")
        
        # Forecasting summary
        forecast_data = pd.DataFrame({
            'Metric': ['Team Size', 'Monthly Patients', 'Avg Efficiency', 'Provider Coverage'],
            'Current': [38, 2840, 94.2, 42],
            'Projected (3M)': [42, 3200, 95.5, 46],
            'Confidence': ['95%', '88%', '92%', '90%']
        })
        
        st.dataframe(
            forecast_data,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("#### 🚀 Recommendations")
        st.info("""
        **Strategic Actions:**
        - Plan to hire 4 additional scribes by Q4
        - Implement efficiency training program
        - Expand provider network by 10%
        - Focus on weekend coverage improvement
        """)
        
        st.markdown("#### 📋 Risk Factors")
        st.error("🚨 High: Rapid growth may strain training capacity")
        st.warning("⚠️ Medium: Seasonal fluctuations in Q4")
        st.success("✅ Low: Current team performance stable")
    
    # Detailed trend analysis table
    st.markdown("#### 📋 Comprehensive Trend Analysis")
    
    trend_analysis = pd.DataFrame({
        'Metric': [
            'Overall Efficiency',
            'Team Haider Khan',
            'Team Saqib Sherwani',
            'Peak Hours Performance',
            'Weekend Coverage',
            'Provider Satisfaction',
            'Documentation Speed',
            'Error Rate',
            'Training Completion',
            'Turnover Rate'
        ],
        'Current Value': ['94.2%', '92.5%', '95.8%', '96.1%', '86.3%', '4.6/5.0', '2.8 min/doc', '1.2%', '98.5%', '2.1%'],
        'Trend (3M)': ['↗️ +5.2%', '↗️ +4.8%', '↗️ +3.1%', '↗️ +2.9%', '↗️ +8.2%', '↗️ +0.4', '↗️ -0.5 min', '↘️ -0.3%', '→ Stable', '↘️ -0.5%'],
        'Projection': ['96.8%', '95.1%', '97.2%', '97.5%', '89.1%', '4.8/5.0', '2.3 min/doc', '0.9%', '99.0%', '1.6%'],
        'Risk Level': ['Low', 'Low', 'Low', 'Medium', 'Medium', 'Low', 'Low', 'Low', 'Low', 'Low']
    })
    
    # Apply risk level styling
    def highlight_risk(row):
        risk = row['Risk Level']
        if risk == 'High':
            return ['', '', '', '', 'background-color: #f8d7da']
        elif risk == 'Medium':
            return ['', '', '', '', 'background-color: #fff3cd']
        else:
            return ['', '', '', '', 'background-color: #d4edda']
    
    st.dataframe(
        trend_analysis,
        use_container_width=True,
        hide_index=True
    )
