"""
Sidebar navigation component for ScribeDash
"""

import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar():
    """Render the sidebar navigation and return selected page"""
    
    with st.sidebar:
        # Logo and title
        st.markdown(
            """
            <div style='text-align: center; padding: 20px;'>
                <h2>🏥 ScribeDash</h2>
                <p style='color: #666;'>Medical Scribing Dashboard</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation menu
        selected_page = option_menu(
            menu_title="Navigation",
            options=[
                "Executive Overview",
                "Team Performance", 
                "Individual Metrics",
                "Provider Analysis",
                "Real-Time Activity",
                "Trends & Analytics"
            ],
            icons=[
                "graph-up-arrow",
                "people-fill",
                "person-badge",
                "hospital",
                "clock",
                "bar-chart-line"
            ],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#1f77b4", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee"
                },
                "nav-link-selected": {"background-color": "#1f77b4"},
            }
        )
        
        st.markdown("---")
        
        # Quick stats or filters can go here
        st.markdown("### Quick Filters")
        
        # Date range selector
        date_range = st.selectbox(
            "Time Period",
            options=["Today", "This Week", "This Month", "Last Month", "Custom Range"],
            index=2
        )
        
        # Team filter
        team_filter = st.selectbox(
            "Team Leader",
            options=["All Teams", "Haider Khan", "Saqib Sherwani"],
            index=0
        )
        
        # Scribe filter (multiselect for individual analysis)
        if selected_page == "Individual Metrics":
            scribe_filter = st.multiselect(
                "Select Scribes",
                options=[
                    "Shivam Chauhan", "Sutirtha Chakraborty", "Ansika Negi",
                    "Prachi Sharma", "Prarthana Sinha Roy", "Akshita Pandey",
                    "Rohan Setia", "Nikhil Yadav", "Vaibhavi Mittal",
                    "Ayushi Singh", "Deepa Deepak", "Tenzin Wangmo"
                    # Add more scribes as needed
                ],
                default=[]
            )
        
        st.markdown("---")
        
        # Data refresh info
        st.markdown("### Data Status")
        if st.session_state.get('data_loaded'):
            st.success("✅ Connected to Google Sheets")
        else:
            st.warning("⚠️ Using sample data")
        st.info("🔄 Auto-refresh: 5 minutes")
        
        # Last update time
        import datetime
        last_update = datetime.datetime.now().strftime("%H:%M:%S")
        st.caption(f"Last updated: {last_update}")
        
        # Export options
        st.markdown("### Export Data")
        if st.button("📊 Export to Excel"):
            st.info("Excel export functionality coming soon!")
        
        if st.button("📋 Generate Report"):
            st.info("PDF report generation coming soon!")
    
    return selected_page
