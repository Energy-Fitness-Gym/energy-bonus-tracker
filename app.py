import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Use credentials stored securely in Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(creds_dict)
gc = gspread.authorize(creds)

# Connect to Google Sheet
sh = gc.open("Energy Bonus Tracker")
worksheet = sh.worksheet("Master")

st.title("💰 Energy Bonus Tracker")

# === Input Section ===
staff_name = st.selectbox("Select Staff Member", ["Claudia", "Laura", "Anna", "Other"])
event_type = st.selectbox("Select Event Type", list(EVENT_VALUES.keys()))

# Determine input method
if event_type == "Extra Hour Work":
    quantity = st.number_input("How many hours?", min_value=0.0, step=0.5)
elif event_type in ["Late to Shift", "Missed Meeting", "Safety Violation", "Saved the Day", "Led Showcase", "Increased Enroll"]:
    quantity = st.number_input("Number of occurrences?", min_value=0, step=1)
else:
    quantity = 1

# Calculate value
unit_value = EVENT_VALUES[event_type]
total_value = quantity * unit_value

if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row([timestamp, staff_name, event_type, quantity, unit_value, total_value])
    st.success(f"Entry recorded! {staff_name} earned ${total_value:.2f}")

st.markdown("---")

# === Bonus Summary Section ===
st.header("📊 Bonus Summary")

# Fetch all rows
data = worksheet.get_all_records()

# Staff selection
summary_name = st.selectbox("View bonus for", sorted({row['Staff Name'] for row in data}))

# Calculate totals
positives = sum(row['Total Value'] for row in data if row['Staff Name'] == summary_name and row['Total Value'] > 0)
negatives = sum(row['Total Value'] for row in data if row['Staff Name'] == summary_name and row['Total Value'] < 0)
net = positives + negatives

st.metric("Total Positive Contributions", f"${positives:.2f}")
st.metric("Total Deductions", f"${negatives:.2f}")
st.metric("Net Bonus", f"${net:.2f}")