# Events Calendar Dashboard

A full-featured Streamlit application for managing events with JSON storage and Google Sheets integration.

## Features

✅ **Dashboard View**
- Overview statistics (total, completed, pending events)
- Filter by status, event type, and platform
- Toggle completion checkboxes directly

✅ **CRUD Operations**
- **Create**: Add new events with all details
- **Read**: View events in organized lists
- **Update**: Edit existing event information
- **Delete**: Remove events from the calendar

✅ **Analytics**
- Event completion rates by type
- Platform and format distribution charts
- Export data as CSV or JSON

✅ **Google Sheets Integration**
- Manual import/export functionality
- CSV format compatible with Google Sheets
- Instructions for API-based auto-sync

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the main app:
```bash
streamlit run streamlit_app.py
```

3. For Google Sheets sync:
```bash
streamlit run google_sheets_sync.py
```

## Usage

### Main Dashboard
- Navigate using the sidebar menu
- Use filters to find specific events
- Click checkboxes to mark events as completed

### Creating Events
- Go to "Create Event" in the sidebar
- Fill in the event details
- Click "Create Event" to save

### Managing Events
- Go to "Manage Events" to edit or delete
- Update event details and save
- Delete events you no longer need

### Google Sheets Sync
- Export data as CSV to paste into Google Sheets
- Import data from Google Sheets by copying CSV
- Set up API credentials for automatic sync

## Data Storage

Events are stored in `events_data.json` in the following format:
```json
{
  "Date": "2026-01-01",
  "Day Name": "Thursday",
  "Start Time": "9:00 AM",
  "End Time": "10:00 AM",
  "Event Name": "Sales Team Training",
  "Format": "Live Training",
  "Platform": "Zoom / Internal",
  "Focus / Notes": "Sales skills & strategy",
  "Completed": false
}
```

## Google Sheets Integration

Your Google Sheet URL:
https://docs.google.com/spreadsheets/d/1402OLAiU93ttbknkjFpZom75pGcDKD59Gez_31BJ6kg/edit

To enable auto-sync:
1. Set up Google Cloud credentials
2. Enable Google Sheets API
3. Upload credentials.json in the sync page
4. Share your sheet with the service account email

## Support

For issues or questions, refer to the Streamlit documentation:
https://docs.streamlit.io/
