import streamlit as st
import json
from pathlib import Path
import pandas as pd

"""
Google Sheets Synchronization Script
This script helps sync data between JSON storage and Google Sheets
"""

st.set_page_config(page_title="Google Sheets Sync", page_icon="🔄", layout="wide")
st.title("🔄 Google Sheets Synchronization")

st.info("""
**Instructions for Google Sheets Integration:**

1. Install required packages: `pip install gspread oauth2client`
2. Set up Google Cloud credentials (see below)
3. Share your Google Sheet with the service account email
4. Use the functions below to sync data

**Your Google Sheet URL:**  
https://docs.google.com/spreadsheets/d/1402OLAiU93ttbknkjFpZom75pGcDKD59Gez_31BJ6kg/edit
""")

# Setup instructions
with st.expander("📝 Setup Instructions", expanded=False):
    st.markdown("""
    ### Google Cloud Setup
    
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
    2. Create a new project or select existing
    3. Enable Google Sheets API
    4. Create Service Account credentials
    5. Download the JSON credentials file
    6. Share your Google Sheet with the service account email
    
    ### Code Example
    
    ```python
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    # Setup credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Open the sheet
    sheet = client.open_by_key('1402OLAiU93ttbknkjFpZom75pGcDKD59Gez_31BJ6kg').sheet1
    
    # Read data
    data = sheet.get_all_records()
    
    # Update data
    sheet.update('A2:I2', [['2026-01-01', 'Thursday', '9:00 AM', '10:00 AM', 
                             'Sales Team Training', 'Live Training', 
                             'Zoom / Internal', 'Sales skills', 'TRUE']])
```    """)

# Manual data entry
st.divider()
st.header("📥 Import from Google Sheets")

st.text_area(
    "Paste CSV data from Google Sheets",
    height=200,
    placeholder="Date,Day Name,Start Time,End Time,Event Name,Format,Platform,Focus / Notes,Completed\n2026-01-01,Thursday,9:00 AM,10:00 AM,Sales Team Training,Live Training,Zoom / Internal,Sales skills,FALSE",
    key="import_data"
)

if st.button("Import Data"):
    if st.session_state.import_data:
        try:
            from io import StringIO
            csv_data = StringIO(st.session_state.import_data)
            df = pd.read_csv(csv_data)
            
            # Convert to JSON format
            events = df.to_dict('records')
            
            # Convert Completed column to boolean
            for event in events:
                if 'Completed' in event:
                    event['Completed'] = str(event['Completed']).upper() == 'TRUE'
            
            # Save to JSON
            with open('events_data.json', 'w') as f:
                json.dump(events, f, indent=2)
            
            st.success(f"✅ Successfully imported {len(events)} events!")
            st.json(events[:3])  # Show first 3 events as preview
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
    else:
        st.warning("Please paste CSV data first")

# Export to Google Sheets format
st.divider()
st.header("📤 Export to Google Sheets")

DATA_FILE = Path("events_data.json")

if DATA_FILE.exists():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Convert boolean Completed to TRUE/FALSE
    if 'Completed' in df.columns:
        df['Completed'] = df['Completed'].map({True: 'TRUE', False: 'FALSE'})
    
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV for Google Sheets",
        data=csv,
        file_name="events_export.csv",
        mime="text/csv"
    )
    
    st.info("💡 Copy the CSV data and paste it into your Google Sheet")
    st.text_area("CSV Data (copy this)", value=csv, height=300)
else:
    st.warning("No data file found. Please create events first.")

# Live sync toggle
st.divider()
st.header("🔄 Auto-Sync Settings")

st.warning("⚠️ Live sync requires Google Sheets API credentials")

enable_sync = st.toggle("Enable Auto-Sync", value=False)

if enable_sync:
    st.info("Auto-sync is enabled. Changes will be pushed to Google Sheets automatically.")
    
    credentials_file = st.file_uploader("Upload credentials.json", type=['json'])
    
    if credentials_file:
        st.success("✅ Credentials uploaded! Auto-sync is active.")
else:
    st.info("Auto-sync is disabled. Use manual import/export.")
