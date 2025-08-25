"""
ScribeDash - Real-time Medical Scribing Dashboard
Main application entry point
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from components import sidebar
from components import overview, team_performance, individual_metrics
from components import provider_analysis, realtime_activity, trends_analytics
from utils import (
    get_page_config, initialize_session_state, apply_custom_styling,
    load_all_data, process_data, get_data_status
)


def main():
    """Main application function"""
    
    # Configure page
    st.set_page_config(**get_page_config())
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom styling
    apply_custom_styling()
    
    # Header
    st.title("📊 ScribeDash - Medical Scribing Operations")
    st.markdown("Real-time dashboard for monitoring scribe performance and operations")
    
    # Data loading and status
    with st.spinner("Loading data..."):
        if not st.session_state.get('data_loaded', False):
            try:
                # Load data from Google Sheets
                raw_data = load_all_data()
                
                # Process data
                data_processor = process_data(raw_data)
                
                # Store in session state
                st.session_state.data_processor = data_processor
                st.session_state.raw_data = raw_data
                st.session_state.data_loaded = True
                st.session_state.last_update = get_data_status()['last_update']
                
            except Exception as e:
                st.error(f"Failed to load data: {str(e)}")
                st.info("Using sample data for demonstration purposes.")
                st.session_state.data_loaded = False
    
    # Show data status
    data_status = get_data_status()
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        if st.session_state.get('data_loaded', False):
            st.success(f"✅ Data connected - {data_status['status']}")
        else:
            st.warning("⚠️ Using sample data")
    
    with status_col2:
        st.info(f"📊 Last update: {data_status['last_update']}")
    
    with status_col3:
        if st.button("🔄 Refresh Data"):
            st.session_state.data_loaded = False
            st.rerun()
    
    # Render sidebar
    current_page = sidebar.render_sidebar()
    
    # Update session state
    st.session_state.current_page = current_page
    
    # Render selected page
    try:
        if current_page == "Overview":
            overview.render_overview()
        elif current_page == "Team Performance":
            team_performance.render_team_performance()
        elif current_page == "Individual Metrics":
            individual_metrics.render_individual_metrics()
        elif current_page == "Provider Analysis":
            provider_analysis.render_provider_analysis()
        elif current_page == "Real-time Activity":
            realtime_activity.render_realtime_activity()
        elif current_page == "Trends & Analytics":
            trends_analytics.render_trends_analytics()
        else:
            st.error(f"Page '{current_page}' not found")
            
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.exception(e)  # Show full error for debugging
        st.info("Please check the configuration and try again.")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**ScribeDash** | Medical Scribing Operations")
    
    with col2:
        st.markdown(f"**Teams:** Haider Khan (18) | Saqib Sherwani (20)")
    
    with col3:
        st.markdown(f"**Last Updated:** {st.session_state.get('last_update', 'Never')}")


if __name__ == "__main__":
    main()
