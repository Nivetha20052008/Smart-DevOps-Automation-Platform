import streamlit as st
import time
import requests
import socket

from database import (
    create_database,
    save_deployment,
    save_log_analysis,
    save_system_monitoring
)

from auth import login_page
from errors import show_error_analyzer
from history import show_history
from ai_engine import analyze_log
from monitor import get_system_health


# =================================================
# CONFIGURATION
# =================================================

st.set_page_config(
    page_title="Smart DevOps Automation Platform",
    page_icon="🚀",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:5000"


# =================================================
# DATABASE
# =================================================

create_database()


# =================================================
# SESSION STATE
# =================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "email" not in st.session_state:
    st.session_state.email = ""


# =================================================
# API FUNCTION
# =================================================

def get_device_data(device_name):

    try:

        response = requests.get(
            f"{API_BASE_URL}/api/monitor/{device_name}",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None


# =================================================
# LOGIN
# =================================================

if not st.session_state.logged_in:

    login_page()

    st.stop()


# =================================================
# SIDEBAR
# =================================================

st.sidebar.title("🚀 Smart DevOps")

st.sidebar.write(
    f"Welcome, {st.session_state.username}"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Log Analyzer",
        "AI Error Analyzer",
        "CI/CD Monitor",
        "Health Check",
        "Recovery",
        "Deployment History"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""
    st.session_state.email = ""

    st.rerun()


# =================================================
# DASHBOARD
# =================================================

if page == "Dashboard":

    st.title(
        "Smart DevOps Automation Platform"
    )

    st.write(
        "Real-time monitoring, analysis and automation dashboard."
    )

    st.divider()

    st.subheader("🖥️ Device Monitoring")

    device_name = st.text_input(
        "Device Name",
        value=socket.gethostname()
    )

    device_data = get_device_data(
        device_name
    )

    if device_data:

        st.success(
            f"🟢 {device_name} is connected"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "CPU Usage",
                f"{device_data['cpu']}%"
            )

        with col2:

            st.metric(
                "Memory Usage",
                f"{device_data['memory']}%"
            )

        with col3:

            st.metric(
                "Disk Usage",
                f"{device_data['disk']}%"
            )

        with col4:

            st.metric(
                "System Status",
                device_data["status"]
            )

        st.caption(
            f"Last updated: {device_data['updated_at']}"
        )

    else:

        st.warning(
            "Device is not connected to the monitoring server."
        )

        st.info(
            "Start api.py and agent.py to connect this device."
        )

    st.divider()

    # -------------------------------------------------
    # DEVOPS OVERVIEW
    # -------------------------------------------------

    st.subheader("📊 DevOps Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Build Status",
            "SUCCESS"
        )

    with col2:

        st.metric(
            "Application",
            "ONLINE"
        )

    with col3:

        st.metric(
            "Errors",
            "0"
        )

    with col4:

        st.metric(
            "Deployments",
            "0"
        )

    st.divider()

    # -------------------------------------------------
    # PLATFORM MODULES
    # -------------------------------------------------

    st.subheader("Platform Modules")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            "📄 Log Analyzer\n\n"
            "Analyze application logs and identify "
            "errors and warnings."
        )

    with c2:

        st.info(
            "🤖 AI Error Analyzer\n\n"
            "Identify possible causes and recommended "
            "solutions."
        )

    with c3:

        st.info(
            "🔄 CI/CD Monitor\n\n"
            "Monitor build and deployment status."
        )

    c4, c5, c6 = st.columns(3)

    with c4:

        st.success(
            "❤️ Health Check\n\n"
            "Monitor CPU, memory and system health."
        )

    with c5:

        st.warning(
            "🛠 Recovery\n\n"
            "Perform controlled recovery actions."
        )

    with c6:

        st.success(
            "📜 Deployment History\n\n"
            "View previous deployment activity."
        )

    # -------------------------------------------------
    # AUTO REFRESH
    # -------------------------------------------------

    time.sleep(5)

    st.rerun()


# =================================================
# LOG ANALYZER
# =================================================

elif page == "Log Analyzer":

    st.header("Log Analyzer")

    uploaded_file = st.file_uploader(
        "Upload a log file",
        type=["txt", "log"]
    )

    log_text = st.text_area(
        "Or paste log content",
        height=250
    )

    if st.button(
        "Analyze Log",
        use_container_width=True
    ):

        content = ""

        if uploaded_file:

            content = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

        elif log_text.strip():

            content = log_text

        else:

            st.warning(
                "Please upload a log file or paste log content."
            )

            st.stop()

        result = analyze_log(content)

        total = result["total"]

        errors_count = len(
            result["errors"]
        )

        warnings_count = len(
            result["warnings"]
        )

        infos_count = len(
            result["infos"]
        )

        save_log_analysis(
            st.session_state.user_id,
            total,
            errors_count,
            warnings_count,
            infos_count
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Lines",
                total
            )

        with col2:

            st.metric(
                "Errors",
                errors_count
            )

        with col3:

            st.metric(
                "Warnings",
                warnings_count
            )

        with col4:

            st.metric(
                "Info",
                infos_count
            )

        if result["errors"]:

            st.subheader(
                "Detected Errors"
            )

            for error in result["errors"]:

                st.error(error)

        if result["warnings"]:

            st.subheader(
                "Detected Warnings"
            )

            for warning in result["warnings"]:

                st.warning(warning)

        st.success(
            "Log analysis completed and saved."
        )


# =================================================
# AI ERROR ANALYZER
# =================================================

elif page == "AI Error Analyzer":

    show_error_analyzer(
        st.session_state.user_id
    )


# =================================================
# CI/CD MONITOR
# =================================================

elif page == "CI/CD Monitor":

    st.header("CI/CD Monitor")

    st.write(
        "Monitor the current application build status."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Build",
            "SUCCESS"
        )

    with col2:

        st.metric(
            "Branch",
            "main"
        )

    with col3:

        st.metric(
            "Pipeline",
            "ACTIVE"
        )

    st.divider()

    st.subheader(
        "Latest Pipeline"
    )

    st.success(
        "Build #001 completed successfully."
    )

    st.write(
        "Environment: Production"
    )

    st.write(
        "Status: SUCCESS"
    )


# =================================================
# HEALTH CHECK
# =================================================

elif page == "Health Check":

    st.header(
        "System Health Check"
    )

    health = get_system_health()

    save_system_monitoring(
        st.session_state.user_id,
        health["cpu"],
        health["memory"],
        health["disk"],
        health["status"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "CPU Usage",
            f"{health['cpu']}%"
        )

    with col2:

        st.metric(
            "Memory Usage",
            f"{health['memory']}%"
        )

    with col3:

        st.metric(
            "Disk Usage",
            f"{health['disk']}%"
        )

    with col4:

        st.metric(
            "Status",
            health["status"]
        )

    st.caption(
        f"Last checked: {health['checked_at']}"
    )

    st.divider()

    if health["status"] == "HEALTHY":

        st.success(
            "🟢 CPU, memory and disk usage are normal."
        )

    elif health["status"] == "WARNING":

        st.warning(
            "🟡 One or more system resources are high."
        )

    else:

        st.error(
            "🔴 Critical system resource usage detected."
        )

    time.sleep(5)

    st.rerun()


# =================================================
# RECOVERY
# =================================================

elif page == "Recovery":

    st.header(
        "Recovery Center"
    )

    st.write(
        "Perform controlled recovery actions."
    )

    st.warning(
        "Recovery actions in this demo are simulated. "
        "No operating-system services are modified."
    )

    action = st.selectbox(
        "Select Recovery Action",
        [
            "Restart Application",
            "Clear Temporary Cache",
            "Retry Failed Operation"
        ]
    )

    if st.button(
        "Execute Recovery",
        use_container_width=True
    ):

        with st.spinner(
            "Performing recovery..."
        ):

            time.sleep(2)

        st.success(
            f"{action} completed successfully."
        )


# =================================================
# DEPLOYMENT HISTORY
# =================================================

elif page == "Deployment History":

    st.header(
        "Deployment History"
    )

    project_name = st.text_input(
        "Project Name",
        value="Smart DevOps"
    )

    environment = st.selectbox(
        "Environment",
        [
            "Development",
            "Testing",
            "Production"
        ]
    )

    status = st.selectbox(
        "Deployment Status",
        [
            "SUCCESS",
            "FAILED",
            "PENDING"
        ]
    )

    if st.button(
        "Record Deployment",
        use_container_width=True
    ):

        save_deployment(
            st.session_state.user_id,
            project_name,
            environment,
            status
        )

        st.success(
            "Deployment recorded successfully."
        )

    st.divider()

    show_history(
        st.session_state.user_id
    )