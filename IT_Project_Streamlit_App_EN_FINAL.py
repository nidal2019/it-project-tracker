
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import io

# Load data from Excel file
df = pd.read_excel("IT_Project_Task_Planning_Form.xlsx")
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['Target Completion Date'] = pd.to_datetime(df['Target Completion Date'], errors='coerce')

# Compute status and alerts
today = datetime.today()
df['Status'] = df['Target Completion Date'].apply(
    lambda d: 'Done' if d < today - timedelta(days=1)
    else 'In Progress' if d >= today - timedelta(days=3)
    else 'Pending'
)

df['Deadline Alert'] = df['Target Completion Date'].apply(
    lambda d: '⚠️ Due Soon' if today <= d <= today + timedelta(days=3) else ''
)

# Streamlit UI
st.set_page_config(page_title="IT Project Task Tracker", layout="wide")
st.title("📋 IT Project Task Tracker System")

# Display task table
st.subheader("📌 Current Task Table")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Add new task
st.subheader("➕ Add New Task")
with st.form("new_task_form"):
    title = st.text_input("Task Title")
    owner = st.text_input("Project Owner / Requestor")
    manager = st.text_input("Project Manager / Assigned Staff")
    start = st.date_input("Start Date")
    end = st.date_input("Target Completion Date")
    objective = st.text_area("Project / Task Objectives")
    scope = st.text_area("Scope of Work")
    resources = st.text_area("Resources Required")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        new_row = {
            'Project/Task Title': title,
            'Project Owner / Requestor': owner,
            'Project Manager / Assigned Staff': manager,
            'Start Date': pd.to_datetime(start),
            'Target Completion Date': pd.to_datetime(end),
            'Project / Task Objectives': objective,
            'Scope of Work': scope,
            'Resources Required': resources,
            'Status': 'Pending',
            'Deadline Alert': '⚠️ Due Soon' if (end - today.date()).days <= 3 else ''
        }
        edited_df = pd.concat([edited_df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("✅ Task added successfully!")

# Gantt chart
st.subheader("📊 Project Timeline (Gantt Chart)")
fig = px.timeline(
    edited_df,
    x_start="Start Date",
    x_end="Target Completion Date",
    y="Project/Task Title",
    color="Status",
    title="Task Timeline",
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# Create Excel file in memory for download
st.subheader("📥 Download Updated File")
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    edited_df.to_excel(writer, index=False)
excel_data = output.getvalue()

st.download_button(
    label="📁 Download Excel",
    data=excel_data,
    file_name="IT_Project_Tasks_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
