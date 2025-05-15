# Mood of the Queue

A simple internal tool for tracking and visualizing the mood of the customer support ticket queue throughout the day.

## Features

- **Log Moods**: Select a mood (😊 Happy, 😠 Angry, 😕 Confused, 🎉 Excited) and add optional notes
- **Visualize Moods**: See a bar chart of mood counts for the current day
- **Historical Data**: View mood trends over time

## Setup Instructions

### Prerequisites

- Python 3.7+
- A Google account
- Google Cloud project with Sheets API enabled

### Step 1: Set up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API and Google Drive API
4. Create a service account
5. Download the JSON key file for the service account
6. Rename the JSON key to `credentials.json` and place it in a folder named `credentials` in the project directory

### Step 2: Install Dependencies

```bash
pip install streamlit pandas gspread oauth2client plotly
```

### Step 3: Run the App

```bash
streamlit run app.py
```

The app will automatically create a new Google Sheet named "Mood_Queue" on first run.

## Usage

1. Select a mood from the radio buttons
2. Add an optional note about what's happening
3. Click "Submit" to log the entry
4. View the mood distribution for today in the chart
5. Expand "View Historical Data" to see trends over time

## Time Spent

~30 minutes, as per the task requirements