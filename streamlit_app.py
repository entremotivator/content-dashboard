import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# File path for JSON storage
DATA_FILE = Path("events_data.json")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = []
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

def load_data():
    """Load data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def initialize_data_from_csv():
    """Initialize data from the provided CSV-like data"""
    initial_data = [
        {"Date": "2026-01-01", "Day Name": "Thursday", "Start Time": "9:00 AM", "End Time": "10:00 AM", "Event Name": "Sales Team Training", "Format": "Live Training", "Platform": "Zoom / Internal", "Focus / Notes": "Sales skills & strategy", "Completed": False},
        {"Date": "2026-01-02", "Day Name": "Friday", "Start Time": "12:00 PM", "End Time": "", "Event Name": "Futuristic Fridays", "Format": "Live Stream", "Platform": "Social Platforms", "Focus / Notes": "Future tech, AI trends", "Completed": False},
        {"Date": "2026-01-03", "Day Name": "Saturday", "Start Time": "Flexible", "End Time": "", "Event Name": "System Saturdays", "Format": "Short Video Tip", "Platform": "All Social Platforms", "Focus / Notes": "Systems & automation", "Completed": False},
        {"Date": "2026-01-04", "Day Name": "Sunday", "Start Time": "6:00 AM", "End Time": "", "Event Name": "AIVACEO Podcast", "Format": "Audio / Recorded", "Platform": "Podcast Platforms", "Focus / Notes": "Weekly AI discussion & insights", "Completed": False},
        {"Date": "2026-01-04", "Day Name": "Sunday", "Start Time": "2:00 PM", "End Time": "", "Event Name": "Promptology Tip", "Format": "Video", "Platform": "Social Media", "Focus / Notes": "Quick AI prompt education", "Completed": False},
        {"Date": "2026-01-05", "Day Name": "Monday", "Start Time": "9:00 AM", "End Time": "11:00 AM", "Event Name": "Real Estate & AI", "Format": "Live Audio", "Platform": "Clubhouse", "Focus / Notes": "AI applications in real estate", "Completed": False},
        {"Date": "2026-01-06", "Day Name": "Tuesday", "Start Time": "6:00 PM", "End Time": "8:00 PM", "Event Name": "AI Superheroes Class", "Format": "Live Class", "Platform": "Community Platform", "Focus / Notes": "Hands-on AI training", "Completed": False},
        {"Date": "2026-01-07", "Day Name": "Wednesday", "Start Time": "Flexible", "End Time": "", "Event Name": "AI Whiteboard Wednesday", "Format": "Educational Video", "Platform": "YouTube", "Focus / Notes": "Visual AI breakdowns & tutorials", "Completed": False},
    ]
    save_data(initial_data)
    return initial_data

# Load data
if not st.session_state.data:
    st.session_state.data = load_data()
    if not st.session_state.data:
        st.session_state.data = initialize_data_from_csv()

# App title and configuration
st.set_page_config(page_title="Events Dashboard", page_icon="📅", layout="wide")
st.title("📅 Events Calendar Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Select Option", ["Dashboard", "Create Event", "Manage Events", "Analytics"])

# Dashboard View
if menu == "Dashboard":
    st.header("📊 Events Overview")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    total_events = len(st.session_state.data)
    completed_events = sum(1 for event in st.session_state.data if event.get('Completed', False))
    pending_events = total_events - completed_events
    completion_rate = (completed_events / total_events * 100) if total_events > 0 else 0
    
    col1.metric("Total Events", total_events)
    col2.metric("Completed", completed_events)
    col3.metric("Pending", pending_events)
    col4.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    st.divider()
    
    # Filter options
    st.subheader("🔍 Filter Events")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Status", ["All", "Completed", "Pending"])
    with col2:
        event_names = ["All"] + sorted(list(set(event['Event Name'] for event in st.session_state.data)))
        event_filter = st.selectbox("Event Type", event_names)
    with col3:
        platforms = ["All"] + sorted(list(set(event['Platform'] for event in st.session_state.data)))
        platform_filter = st.selectbox("Platform", platforms)
    
    # Apply filters
    filtered_data = st.session_state.data.copy()
    
    if status_filter == "Completed":
        filtered_data = [e for e in filtered_data if e.get('Completed', False)]
    elif status_filter == "Pending":
        filtered_data = [e for e in filtered_data if not e.get('Completed', False)]
    
    if event_filter != "All":
        filtered_data = [e for e in filtered_data if e['Event Name'] == event_filter]
    
    if platform_filter != "All":
        filtered_data = [e for e in filtered_data if e['Platform'] == platform_filter]
    
    st.divider()
    st.subheader(f"📋 Events List ({len(filtered_data)} events)")
    
    # Display events with checkboxes
    if filtered_data:
        for idx, event in enumerate(filtered_data):
            # Find the original index in the full data
            original_idx = st.session_state.data.index(event)
            
            with st.expander(f"{'✅' if event.get('Completed', False) else '⏳'} {event['Date']} - {event['Event Name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Day:** {event['Day Name']}")
                    st.write(f"**Time:** {event['Start Time']} {f'- {event['End Time']}' if event['End Time'] else ''}")
                    st.write(f"**Format:** {event['Format']}")
                    st.write(f"**Platform:** {event['Platform']}")
                    st.write(f"**Focus:** {event['Focus / Notes']}")
                
                with col2:
                    # Checkbox to toggle completion
                    completed = st.checkbox(
                        "Completed",
                        value=event.get('Completed', False),
                        key=f"checkbox_{original_idx}"
                    )
                    
                    if completed != event.get('Completed', False):
                        st.session_state.data[original_idx]['Completed'] = completed
                        save_data(st.session_state.data)
                        st.rerun()
    else:
        st.info("No events match the selected filters.")

# Create Event
elif menu == "Create Event":
    st.header("➕ Create New Event")
    
    with st.form("create_event_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date")
            day_name = st.selectbox("Day Name", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            start_time = st.text_input("Start Time", placeholder="e.g., 9:00 AM")
            end_time = st.text_input("End Time (optional)", placeholder="e.g., 10:00 AM")
        
        with col2:
            event_name = st.text_input("Event Name", placeholder="e.g., Sales Team Training")
            format_type = st.text_input("Format", placeholder="e.g., Live Training")
            platform = st.text_input("Platform", placeholder="e.g., Zoom / Internal")
            focus_notes = st.text_area("Focus / Notes", placeholder="e.g., Sales skills & strategy")
        
        submitted = st.form_submit_button("Create Event")
        
        if submitted:
            if not event_name or not date:
                st.error("Please fill in at least Event Name and Date")
            else:
                new_event = {
                    "Date": str(date),
                    "Day Name": day_name,
                    "Start Time": start_time,
                    "End Time": end_time,
                    "Event Name": event_name,
                    "Format": format_type,
                    "Platform": platform,
                    "Focus / Notes": focus_notes,
                    "Completed": False
                }
                st.session_state.data.append(new_event)
                save_data(st.session_state.data)
                st.success(f"✅ Event '{event_name}' created successfully!")
                st.balloons()

# Manage Events
elif menu == "Manage Events":
    st.header("⚙️ Manage Events")
    
    if st.session_state.data:
        # Sort events by date
        sorted_data = sorted(st.session_state.data, key=lambda x: x['Date'])
        
        for idx, event in enumerate(sorted_data):
            original_idx = st.session_state.data.index(event)
            
            with st.expander(f"{event['Date']} - {event['Event Name']}"):
                # Edit form
                with st.form(f"edit_form_{original_idx}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_date = st.text_input("Date", value=event['Date'])
                        new_day = st.text_input("Day Name", value=event['Day Name'])
                        new_start = st.text_input("Start Time", value=event['Start Time'])
                        new_end = st.text_input("End Time", value=event['End Time'])
                    
                    with col2:
                        new_name = st.text_input("Event Name", value=event['Event Name'])
                        new_format = st.text_input("Format", value=event['Format'])
                        new_platform = st.text_input("Platform", value=event['Platform'])
                        new_focus = st.text_area("Focus / Notes", value=event['Focus / Notes'])
                    
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        update = st.form_submit_button("💾 Update Event", use_container_width=True)
                    with col_btn2:
                        delete = st.form_submit_button("🗑️ Delete Event", use_container_width=True, type="secondary")
                    
                    if update:
                        st.session_state.data[original_idx].update({
                            "Date": new_date,
                            "Day Name": new_day,
                            "Start Time": new_start,
                            "End Time": new_end,
                            "Event Name": new_name,
                            "Format": new_format,
                            "Platform": new_platform,
                            "Focus / Notes": new_focus
                        })
                        save_data(st.session_state.data)
                        st.success("✅ Event updated!")
                        st.rerun()
                    
                    if delete:
                        st.session_state.data.pop(original_idx)
                        save_data(st.session_state.data)
                        st.success("🗑️ Event deleted!")
                        st.rerun()
    else:
        st.info("No events available to manage.")

# Analytics
elif menu == "Analytics":
    st.header("📈 Analytics & Insights")
    
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        
        # Event completion by type
        st.subheader("Event Completion by Type")
        event_stats = df.groupby('Event Name')['Completed'].agg(['sum', 'count'])
        event_stats.columns = ['Completed', 'Total']
        event_stats['Completion Rate'] = (event_stats['Completed'] / event_stats['Total'] * 100).round(1)
        st.dataframe(event_stats, use_container_width=True)
        
        # Platform distribution
        st.subheader("Events by Platform")
        platform_counts = df['Platform'].value_counts()
        st.bar_chart(platform_counts)
        
        # Format distribution
        st.subheader("Events by Format")
        format_counts = df['Format'].value_counts()
        st.bar_chart(format_counts)
        
        # Download data
        st.divider()
        st.subheader("📥 Export Data")
        
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="events_data.csv",
                mime="text/csv"
            )
        
        with col2:
            json_str = json.dumps(st.session_state.data, indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name="events_data.json",
                mime="application/json"
            )
    else:
        st.info("No data available for analytics.")

# Footer
st.divider()
st.caption("Events Calendar Dashboard | Built with Streamlit")
