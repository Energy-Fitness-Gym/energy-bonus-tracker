import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from utils import EVENT_VALUES

# Define the scope for Google Sheets access
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from secrets.toml with the proper scope
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

# Authorize gspread with those credentials
gc = gspread.authorize(credentials)

# Open your Google Sheet (must be shared with the service account email!)
spreadsheet = gc.open("Energy Bonus Tracker")
worksheet = spreadsheet.worksheet("Master")

# Load all data into a pandas DataFrame
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Display the title
st.title("💰 Energy Bonus Tracker")

# Define the manager code from secrets
MANAGER_CODE = st.secrets["manager_code"]

# Role selection
role = st.selectbox("Who are you?", ["Employee", "Manager"])

# Manager role
if role == "Manager":
    access_code = st.text_input("Enter manager access code:", type="password")
    if access_code != MANAGER_CODE:
        st.warning("Access denied. Please enter the correct code.")
        st.stop()
    else:
        st.subheader("All Submitted Bonuses")
        st.dataframe(df)

# Employee role
elif role == "Employee":
    name = st.text_input("Enter your name").strip().lower()
    if not name:
        st.stop()
    else:
        user_data = df[df["Name"].str.lower() == name]
        if user_data.empty:
            st.warning("No records found for this name.")
        else:
            st.subheader(f"Bonuses for {name.title()}")
            st.dataframe(user_data)