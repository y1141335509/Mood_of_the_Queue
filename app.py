import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import plotly.express as px
import os
import json

st.set_page_config(
    page_title="Mood of the Queue",
    page_icon="💙",
    layout="wide"
)

st.title("💙 Mood of the Queue")
st.write("Designed to keep track of the emotion of patients throughout the day.")

def setup_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    credentials_path = './credentials/credentials.json'
    credentials = None
    if not os.path.exists(credentials_path):
        credentials_dict = json.loads(st.secrets['GOOGLE_CREDENTIALS'])
        if not credentials_dict:
            st.error(f"Credentials file not found at: {credentials_path}")
            return None
        else:
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    
    client = gspread.authorize(credentials)
    
    spreadsheet_id = "1b6qfnwGHmYmj9-Rg4KSmPhUzHGSh51RWLMOsEvCCMYE"
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    sheet = spreadsheet.sheet1
    values = sheet.get_all_values()
    
    if not values or values[0] != ["timestamp", "mood", "note"]:
        sheet.clear()
        sheet.append_row(["timestamp", "mood", "note"])
        st.success("Sheet initialized with headers: timestamp, mood, note")
    
    return sheet

def add_record(sheet, mood, note):
    if sheet is None:
        return False
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    sheet.append_row([timestamp, mood, note])    
    msg = "Mood " + str(mood) + " added with note: " + str(note) + " at " + str(timestamp)
    st.success(msg)
    return True

def get_data(sheet):
    if sheet is None:
        return pd.DataFrame()
    
    values = sheet.get_all_values()     
    if not values or len(values) <= 1:  
        return pd.DataFrame(columns=["timestamp", "mood", "note"])
    
    headers = values[0] 

    if headers != ["timestamp", "mood", "note"]:
        st.warning(f"Unexpected headers in sheet: {headers}")

    data_rows = values[1:]   
    df = pd.DataFrame(data_rows, columns=["timestamp", "mood", "note"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])      
    df['date'] = df['timestamp'].dt.date         

    return df

sheet = setup_google_sheet()


################################ Streamlit App Layout ################################
st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Log a Mood")
    
    moods = ["😊 Happy", "😠 Angry", "😕 Confused", "🎉 Excited"]
    mood = st.selectbox("Select your current mood:", moods)
    note = st.text_area("Add a short note (optional):", height=200)
    
    if st.button("Submit", type="primary"):
        if sheet is not None:
            success = add_record(sheet, mood, note)
            if success:
                st.success("✅ Mood logged successfully!")  
                note = ""   
        else:
            st.error("Failed to connect to Google Sheets. Check the credentials please.")

df = get_data(sheet)

with col2:
    st.subheader("Mood Visualization of Today")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if df.empty:
        st.info("No data available yet. Start logging moods!")
    else:
        today = datetime.now().date()
        today_df = df[df['date'] == today]
        
        if today_df.empty:
            st.info("No moods logged for today yet.")
        else:
            mood_counts = today_df['mood'].value_counts().reset_index()
            mood_counts.columns = ['Mood', 'Count']
            
            fig = px.bar(
                mood_counts, 
                x='Mood', 
                y='Count', 
                title=f'Mood Distribution for {today}',
                color='Mood',
                color_discrete_map={
                    "😊 Happy": "green",
                    "😠 Angry": "red",
                    "😕 Confused": "yellow",
                    "🎉 Excited": "blue"
                }
            )
            
            fig.update_layout(
                xaxis_title="Mood",
                yaxis_title="Count",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")

if not df.empty:
    st.subheader("Historical Data")
    
    with st.expander("View Historical Data"):
        daily_counts = df.groupby(['date', 'mood']).size().reset_index(name='count')
        
        fig2 = px.bar(
            daily_counts,
            x='date',
            y='count',
            color='mood',
            title='Mood Trends Over Time',
            color_discrete_map={
                "😊 Happy": "green",
                "😠 Angry": "red",
                "😕 Confused": "yellow",
                "🎉 Excited": "blue"
            }
        )
        
        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Built by Yinghai | [GitHub](https://github.com/y1141335509/Mood_of_the_Queue)")