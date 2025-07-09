import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(
    page_title="IT Project Tracker",
    page_icon="🧩",
    layout="wide"
)

# Load Excel file
EXCEL_FILE = "IT_Project_Task_Planning_Form.xlsx"

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

df = load_data(EXCEL_FILE)

st.title("🧩 IT Project Task Tracker System")

# Show current tasks
st.subheader("📌 Current Task Table")
st.dataframe(df, use_container_width=True)

# Add new task
st.markdown("### ➕ Add New Task")
with st.form("task_form"):
    title = st.text_input("Task Title")
    requester = st.text_input("Project Owner / Requester")
    manager = st.text_input("Project Manager / Assigned Staff")
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("Target Completion Date", value=datetime.today())
    objective = st.text_area("Project / Task Objectives")
    scope = st.text_area("Scope of Work")
    resources = st.text_area("Resources Required")
    status = st.selectbox("Status", ["In Progress", "Completed", "Overdue"])

    submitted = st.form_submit_button("Add Task")
    if submitted:
        new_task = {
            "Task Title": title,
            "Project Owner / Requester": requester,
            "Project Manager / Assigned Staff": manager,
            "Start Date": start_date,
            "Target Completion Date": end_date,
            "Project / Task Objectives": objective,
            "Scope of Work": scope,
            "Resources Required": resources,
            "Status": status
        }
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        st.success("✅ Task added successfully!")

# Gantt Chart
st.subheader("📊 Project Timeline (Gantt Chart)")
fig = px.timeline(
    df,
    x_start="Start Date",
    x_end="Target Completion Date",
    y="Task Title",
    color="Status",
    color_discrete_map={
        "In Progress": "blue",
        "Completed": "green",
        "Overdue": "red"
    }
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# Download button
st.subheader("📥 Download Updated File")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
output = io.BytesIO()
df.to_excel(output, index=False, engine='openpyxl')
st.download_button(
    label="Download Updated Excel",
    data=output.getvalue(),
    file_name=f"Project_Tracker_{timestamp}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
