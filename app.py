import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from utils import EVENT_VALUES  # Make sure utils.py has your EVENT_VALUES dict

# --- Google Sheets Authentication ---
# Pull credentials securely from Streamlit's secret manager
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(st.secrets)
gc = gspread.authorize(creds)

# Connect to Google Sheet + tab
sh = gc.open("Energy Bonus Tracker")
worksheet = sh.worksheet("Master")

# --- UI Title ---
st.title("💰 Energy Bonus Tracker")

# === Input Section ===
staff_name = st.selectbox("Select Staff Member", ["Claudia", "Laura", "Anna", "Other"])
event_type = st.selectbox("Select Event Type", list(EVENT_VALUES.keys()))

# Quantity input depending on event
if event_type == "Extra Hour Work":
    quantity = st.number_input("How many hours?", min_value=0.0, step=0.5)
else:
    quantity = st.number_input("Number of occurrences?", min_value=0, step=1)

# Calculate values
unit_value = EVENT_VALUES[event_type]
total_value = quantity * unit_value

# --- Submit button ---
if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([timestamp, staff_name, event_type, quantity, unit_value, total_value])
    st.success(f"✅ Entry recorded! {staff_name} earned ${total_value:.2f}")

st.markdown("---")

# === Bonus Summary Section ===
st.header("📊 Bonus Summary")

# Get all records from the sheet
data = worksheet.get_all_records()

if data:  # only show if there’s data
    # Staff selector for summary
    all_staff = sorted({row['Staff Name'] for row in data})
    summary_name = st.selectbox("View bonus for", all_staff)

    # Totals
    positives = sum(row['Total Value'] for row in data if row['Staff Name'] == summary_name and row['Total Value'] > 0)
    negatives = sum(row['Total Value'] for row in data if row['Staff Name'] == summary_name and row['Total Value'] < 0)
    net = positives + negatives

    st.metric("Total Positive Contributions", f"${positives:.2f}")
    st.metric("Total Deductions", f"${negatives:.2f}")
    st.metric("Net Bonus", f"${net:.2f}")
else:
    st.info("No data recorded yet.")