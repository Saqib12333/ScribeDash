"""
Test version of ScribeDash main app to debug startup issues
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
current_path = Path(__file__).parent / "src"
sys.path.insert(0, str(current_path))

st.title("ScribeDash Debug Test")
st.write("If you see this, basic Streamlit is working")

try:
    st.write("Testing imports...")
    
    # Test individual imports
    from components import sidebar
    st.success("✅ Sidebar import successful")
    
    from components import overview
    st.success("✅ Overview import successful")
    
    from utils import load_all_data
    st.success("✅ Utils import successful")
    
    # Test data loading
    st.write("Testing data loading...")
    raw_data = load_all_data()
    st.success(f"✅ Data loaded successfully: {len(raw_data)} sheets")
    
    # Show sheet names
    st.write("Available sheets:")
    for sheet_name, df in raw_data.items():
        st.write(f"- {sheet_name}: {len(df)} rows")
    
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.exception(e)
