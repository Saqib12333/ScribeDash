"""
Debug version of main.py to identify the exact error
"""

import streamlit as st
import sys
from pathlib import Path

print("=== DEBUG MAIN START ===")

# Add current directory to path for imports
current_path = Path(__file__).parent / "src"
sys.path.insert(0, str(current_path))

print(f"Added to path: {current_path}")

try:
    print("Testing basic imports...")
    import logging
    print("✓ logging imported")
    
    print("Testing streamlit config...")
    st.set_page_config(
        page_title="ScribeDash Debug",
        page_icon="📊",
        layout="wide"
    )
    print("✓ streamlit config set")
    
    print("Testing basic streamlit elements...")
    st.title("🔍 ScribeDash Debug Mode")
    st.write("If you can see this, basic Streamlit is working.")
    
    print("Testing utils imports...")
    try:
        from utils import get_page_config
        print("✓ utils.get_page_config imported")
    except Exception as e:
        print(f"✗ Error importing utils.get_page_config: {e}")
        st.error(f"Error importing utils.get_page_config: {e}")
    
    try:
        from utils import initialize_session_state
        print("✓ utils.initialize_session_state imported")
    except Exception as e:
        print(f"✗ Error importing utils.initialize_session_state: {e}")
        st.error(f"Error importing utils.initialize_session_state: {e}")
    
    try:
        from utils import apply_custom_styling
        print("✓ utils.apply_custom_styling imported")
    except Exception as e:
        print(f"✗ Error importing utils.apply_custom_styling: {e}")
        st.error(f"Error importing utils.apply_custom_styling: {e}")
    
    try:
        from utils import load_all_data
        print("✓ utils.load_all_data imported")
    except Exception as e:
        print(f"✗ Error importing utils.load_all_data: {e}")
        st.error(f"Error importing utils.load_all_data: {e}")
    
    print("Testing components imports...")
    try:
        from components import sidebar
        print("✓ components.sidebar imported")
    except Exception as e:
        print(f"✗ Error importing components.sidebar: {e}")
        st.error(f"Error importing components.sidebar: {e}")
    
    try:
        from components import overview
        print("✓ components.overview imported")
    except Exception as e:
        print(f"✗ Error importing components.overview: {e}")
        st.error(f"Error importing components.overview: {e}")
    
    print("All imports tested!")
    st.success("All critical imports tested - check terminal for details")
    
    # Test data loading
    st.subheader("Testing Data Loading")
    try:
        print("Testing data loading...")
        from utils import load_all_data, get_data_status
        
        with st.spinner("Testing data load..."):
            raw_data = load_all_data()
            print(f"Data loaded: {len(raw_data)} sheets")
            st.success(f"Data loaded successfully: {len(raw_data)} sheets")
            
            for sheet_name, df in raw_data.items():
                st.write(f"**{sheet_name}**: {len(df)} rows")
                
    except Exception as e:
        print(f"✗ Error in data loading: {e}")
        st.error(f"Error in data loading: {e}")
        st.exception(e)
    
except Exception as e:
    print(f"✗ CRITICAL ERROR: {e}")
    st.error(f"Critical error: {e}")
    st.exception(e)

print("=== DEBUG MAIN END ===")
