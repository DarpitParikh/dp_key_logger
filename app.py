import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
import threading
from keylogger import KeyLogger, HAS_PYNPUT

# Page configuration
st.set_page_config(
    page_title="Keylogger Monitor",
    page_icon="⌨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .log-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        max-height: 400px;
        overflow-y: auto;
    }
    h1 {
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'keylogger' not in st.session_state:
    st.session_state.keylogger = KeyLogger()
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Check for environment issues
if not HAS_PYNPUT:
    st.error("❌ **System Error: X Server Not Available**")
    st.info(
        "The keylogger requires an X server to run on Linux systems. "
        "This error typically occurs in headless environments (containers, remote servers, SSH sessions). "
        "\n\n**Solutions:**\n"
        "1. Run this application on a desktop/GUI system\n"
        "2. Set up a virtual display (e.g., Xvfb)\n"
        "3. Use the keylogger on Windows or macOS where no X server is required"
    )
    st.warning(f"**Technical Details:** {st.session_state.keylogger.import_error}")
    st.stop()

# Header
st.title("⌨️ Keylogger Monitor")
st.markdown("*Educational Purpose Only - Monitor keyboard activity in real-time*")
st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Start/Stop buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.is_running):
            st.session_state.keylogger.start()
            st.session_state.is_running = True
            st.success("Logging started!")
            st.rerun()
    
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.is_running):
            st.session_state.keylogger.stop()
            st.session_state.is_running = False
            st.warning("Logging stopped!")
            st.rerun()
    
    st.markdown("---")
    
    # Clear logs
    if st.button("🗑️ Clear Logs"):
        st.session_state.keylogger.clear_logs()
        st.session_state.logs = []
        st.info("Logs cleared!")
        st.rerun()
    
    # Save logs
    if st.button("💾 Save Logs"):
        filename = st.session_state.keylogger.save_logs()
        if filename:
            st.success(f"Logs saved to {filename}")
        else:
            st.warning("No logs to save!")
    
    st.markdown("---")
    
    # Status indicator
    st.subheader("Status")
    if st.session_state.is_running:
        st.markdown("🟢 **Active**")
    else:
        st.markdown("🔴 **Inactive**")
    
    # Auto-refresh toggle
    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    if auto_refresh:
        st.markdown("*Refreshing every 2 seconds...*")

# Main content area
col1, col2, col3, col4 = st.columns(4)

# Get current logs
current_logs = st.session_state.keylogger.get_logs()
st.session_state.logs = current_logs

# Statistics
with col1:
    st.markdown("""
        <div class="stat-box">
            <h2>{}</h2>
            <p>Total Keys</p>
        </div>
    """.format(len(current_logs)), unsafe_allow_html=True)

with col2:
    special_keys = sum(1 for log in current_logs if log.get('type') == 'special')
    st.markdown("""
        <div class="stat-box">
            <h2>{}</h2>
            <p>Special Keys</p>
        </div>
    """.format(special_keys), unsafe_allow_html=True)

with col3:
    regular_keys = sum(1 for log in current_logs if log.get('type') == 'regular')
    st.markdown("""
        <div class="stat-box">
            <h2>{}</h2>
            <p>Regular Keys</p>
        </div>
    """.format(regular_keys), unsafe_allow_html=True)

with col4:
    sessions = len(set(log.get('session', 0) for log in current_logs))
    st.markdown("""
        <div class="stat-box">
            <h2>{}</h2>
            <p>Sessions</p>
        </div>
    """.format(sessions), unsafe_allow_html=True)

st.markdown("---")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 Live Logs", "📊 Analytics", "📁 History"])

with tab1:
    st.subheader("Recent Keystrokes")
    
    if current_logs:
        # Display last 50 logs
        recent_logs = current_logs[-50:]
        
        # Create a formatted display
        log_df = pd.DataFrame(recent_logs)
        
        # Format the dataframe
        if not log_df.empty:
            display_df = log_df[['timestamp', 'key', 'type']].copy()
            display_df.columns = ['Time', 'Key', 'Type']
            display_df['Time'] = pd.to_datetime(display_df['Time']).dt.strftime('%H:%M:%S')
            
            # Style the dataframe
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
        
        # Show raw text reconstruction
        st.subheader("Reconstructed Text")
        text = st.session_state.keylogger.get_text()
        st.text_area("", value=text, height=150, disabled=True)
    else:
        st.info("No logs yet. Start the keylogger to begin monitoring.")

with tab2:
    st.subheader("Key Statistics")
    
    if current_logs:
        # Key frequency analysis
        key_counts = {}
        for log in current_logs:
            key = log.get('key', '')
            key_counts[key] = key_counts.get(key, 0) + 1
        
        # Sort by frequency
        sorted_keys = sorted(key_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        if sorted_keys:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top 20 Most Pressed Keys**")
                freq_df = pd.DataFrame(sorted_keys, columns=['Key', 'Count'])
                st.bar_chart(freq_df.set_index('Key'))
            
            with col2:
                st.markdown("**Key Distribution**")
                type_counts = {}
                for log in current_logs:
                    log_type = log.get('type', 'unknown')
                    type_counts[log_type] = type_counts.get(log_type, 0) + 1
                
                type_df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Count'])
                st.bar_chart(type_df.set_index('Type'))
        
        # Timeline
        st.markdown("**Activity Timeline**")
        if len(current_logs) > 0:
            timeline_df = pd.DataFrame(current_logs)
            timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
            timeline_df['minute'] = timeline_df['timestamp'].dt.floor('Min')
            activity = timeline_df.groupby('minute').size().reset_index(name='keys')
            
            if not activity.empty:
                st.line_chart(activity.set_index('minute'))
    else:
        st.info("Start logging to see analytics.")

with tab3:
    st.subheader("Saved Log Files")
    
    # List saved log files
    logs_dir = Path("logs")
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("keylog_*.json"), reverse=True)
        
        if log_files:
            for log_file in log_files[:10]:  # Show last 10 files
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(log_file.name)
                with col2:
                    size = log_file.stat().st_size
                    st.text(f"{size/1024:.2f} KB")
                with col3:
                    if st.button("View", key=log_file.name):
                        with open(log_file, 'r') as f:
                            data = json.load(f)
                            st.json(data)
        else:
            st.info("No saved log files yet.")
    else:
        st.info("No logs directory found.")

# Auto-refresh
if auto_refresh and st.session_state.is_running:
    import time
    time.sleep(2)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "⚠️ <b>Warning:</b> Use this tool responsibly and only on systems you own or have permission to monitor."
    "</div>",
    unsafe_allow_html=True
)
