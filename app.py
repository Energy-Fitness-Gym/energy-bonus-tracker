import streamlit as st
import gspread
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

# Display the title
st.title("💰 Energy Bonus Tracker")

# Example: Get all values from column A
names = worksheet.col_values(1)

# Show names in a simple list
st.subheader("Names in Column A:")
for name in names:
    st.write(name)