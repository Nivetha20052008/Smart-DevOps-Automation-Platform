import streamlit as st
import time
import requests

from database import (
    create_database,
    save_deployment,
    save_log_analysis
)

from auth import login_page
from errors import show_error_analyzer
from history import show_history
from ai_engine import analyze_log
from monitor import get_system_health


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Smart DevOps Automation Platform",
    page_icon="🚀",
    layout="wide"
)


# -------------------------------------------------
# DATABASE
# -------------------------------------------------

create_database()


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "email" not in st.session_state:
    st.session_state.email = ""


# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------

if not st.session_state.logged_in:

    login_page()

    st.stop()


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

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


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------

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
        "Real-time monitoring, analysis and "
        "automation dashboard."
    )

    st.divider()


    # -------------------------------------------------
    # CONNECT YOUR DEVICE
    # -------------------------------------------------

    st.subheader("🖥️ Connect Your Device")

    st.write(
        "To monitor CPU, memory and disk usage "
        "of your computer, install the Smart DevOps Agent."
    )

    connect_col1, connect_col2 = st.columns([2, 1])

    with connect_col1:

        st.markdown(
            """
            ### 📥 How to connect this computer

            **Step 1:** Download the Smart DevOps Agent.

            **Step 2:** Install the downloaded application.

            **Step 3:** The Agent will run in the background.

            **Step 4:** Wait approximately 30–60 seconds.

            **Step 5:** Refresh this dashboard.

            Your device will automatically appear under
            **Connected Devices**.
            """
        )

    with connect_col2:

        st.markdown("### 🚀 Agent")

        st.link_button(
            "📥 Download Smart DevOps Agent",
            "https://github.com/Nivetha20052008/Smart-DevOps-Automation-Platform/releases/download/v1.0.0/SmartDevOpsAgentSetup.exe",
            use_container_width=True
        )

        st.caption(
            "Windows Agent • Version 1.0.0"
        )

        st.link_button(
            "📦 View Release",
            "https://github.com/Nivetha20052008/Smart-DevOps-Automation-Platform/releases/tag/v1.0.0",
            use_container_width=True
        )


    st.info(
        "💡 The Agent must be installed on the computer "
        "you want to monitor. Opening the website alone "
        "cannot read that computer's CPU, memory or disk usage."
    )

    st.divider()


    # -------------------------------------------------
    # CONNECTED DEVICE MONITORING
    # -------------------------------------------------

    st.subheader("🖥️ Connected Devices")

    MONITOR_API = (
        "https://smart-devops-api.onrender.com/api/monitor"
    )

    try:

        response = requests.get(
            MONITOR_API,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            devices = result.get(
                "devices",
                []
            )

            if devices:

                for device in devices:

                    st.markdown(
                        f"### 💻 {device['device_name']}"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "CPU Usage",
                            f"{device['cpu']}%"
                        )

                    with col2:

                        st.metric(
                            "Memory Usage",
                            f"{device['memory']}%"
                        )

                    with col3:

                        st.metric(
                            "Disk Usage",
                            f"{device['disk']}%"
                        )

                    with col4:

                        st.metric(
                            "Status",
                            device["status"]
                        )


                    if device["status"] == "HEALTHY":

                        st.success(
                            "🟢 Device is healthy."
                        )

                    elif device["status"] == "WARNING":

                        st.warning(
                            "🟡 Device resource usage is high."
                        )

                    else:

                        st.error(
                            "🔴 Critical resource usage detected."
                        )


                    st.caption(
                        f"Last updated: "
                        f"{device['updated_at']}"
                    )

                    st.divider()

            else:

                st.info(
                    "No devices are currently connected. "
                    "Install the Smart DevOps Agent above "
                    "to connect this computer."
                )

        else:

            st.error(
                f"Monitoring API error: "
                f"{response.status_code}"
            )

    except requests.RequestException:

        st.warning(
            "Monitoring server is currently unavailable."
        )


    # -------------------------------------------------
    # LOCAL SYSTEM HEALTH
    # -------------------------------------------------

    st.subheader("🔴 Live System Monitoring")

    health = get_system_health()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if health["status"] == "HEALTHY":

            st.metric(
                "Application",
                "ONLINE",
                "Healthy"
            )

        elif health["status"] == "WARNING":

            st.metric(
                "Application",
                "WARNING",
                "Check system"
            )

        else:

            st.metric(
                "Application",
                "CRITICAL",
                "Immediate attention"
            )


    with col2:

        st.metric(
            "CPU Usage",
            f"{health['cpu']}%"
        )


    with col3:

        st.metric(
            "Memory Usage",
            f"{health['memory']}%"
        )


    with col4:

        st.metric(
            "Disk Usage",
            f"{health['disk']}%"
        )


    st.caption(
        f"Last checked: {health['checked_at']}"
    )


    # -------------------------------------------------
    # HEALTH MESSAGE
    # -------------------------------------------------

    if health["status"] == "HEALTHY":

        st.success(
            "🟢 System is healthy and operating normally."
        )

    elif health["status"] == "WARNING":

        st.warning(
            "🟡 System resource usage is getting high."
        )

    else:

        st.error(
            "🔴 Critical resource usage detected."
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
            "View your previous deployment activity."
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
        "Monitor the latest GitHub Actions workflow status."
    )

    GITHUB_API_URL = (
        "https://api.github.com/repos/"
        "Nivetha20052008/"
        "Smart-DevOps-Automation-Platform/"
        "actions/runs"
    )

    try:

        response = requests.get(
            GITHUB_API_URL,
            headers={
                "Accept": "application/vnd.github+json"
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            workflow_runs = data.get(
                "workflow_runs",
                []
            )

            if workflow_runs:

                latest_run = workflow_runs[0]

                status = latest_run.get(
                    "status",
                    "unknown"
                )

                conclusion = latest_run.get(
                    "conclusion"
                )

                branch = latest_run.get(
                    "head_branch",
                    "unknown"
                )

                run_number = latest_run.get(
                    "run_number",
                    "unknown"
                )

                workflow_name = latest_run.get(
                    "name",
                    "GitHub Actions"
                )

                created_at = latest_run.get(
                    "created_at",
                    "unknown"
                )

                updated_at = latest_run.get(
                    "updated_at",
                    "unknown"
                )


                # ---------------------------------
                # BUILD STATUS
                # ---------------------------------

                if status == "completed":

                    if conclusion == "success":

                        build_status = "SUCCESS"

                    elif conclusion == "failure":

                        build_status = "FAILED"

                    else:

                        build_status = (
                            conclusion.upper()
                            if conclusion
                            else "UNKNOWN"
                        )

                else:

                    build_status = (
                        status.upper()
                    )


                # ---------------------------------
                # STATUS CARDS
                # ---------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Build",
                        build_status
                    )

                with col2:

                    st.metric(
                        "Branch",
                        branch
                    )

                with col3:

                    st.metric(
                        "Pipeline",
                        status.upper()
                    )


                st.divider()


                # ---------------------------------
                # LATEST WORKFLOW
                # ---------------------------------

                st.subheader(
                    "Latest Pipeline"
                )

                st.write(
                    f"**Workflow:** {workflow_name}"
                )

                st.write(
                    f"**Run:** #{run_number}"
                )

                st.write(
                    f"**Branch:** {branch}"
                )

                st.write(
                    f"**Status:** {status.upper()}"
                )

                st.write(
                    f"**Conclusion:** "
                    f"{conclusion or 'Running'}"
                )

                st.write(
                    f"**Created:** {created_at}"
                )

                st.write(
                    f"**Updated:** {updated_at}"
                )


                # ---------------------------------
                # RESULT MESSAGE
                # ---------------------------------

                if conclusion == "success":

                    st.success(
                        "🟢 GitHub Actions build "
                        "completed successfully."
                    )

                elif conclusion == "failure":

                    st.error(
                        "🔴 GitHub Actions build failed."
                    )

                elif status in [
                    "queued",
                    "in_progress"
                ]:

                    st.warning(
                        "🟡 GitHub Actions workflow "
                        "is currently running."
                    )

                else:

                    st.info(
                        "ℹ️ Workflow status is "
                        "currently unavailable."
                    )

            else:

                st.info(
                    "No GitHub Actions workflow runs found."
                )

        else:

            st.error(
                "Unable to access GitHub Actions API."
            )

            st.write(
                f"GitHub API Status: "
                f"{response.status_code}"
            )

    except requests.RequestException as error:

        st.error(
            "Unable to connect to GitHub."
        )

        st.write(
            str(error)
        )


# =================================================
# HEALTH CHECK
# =================================================

elif page == "Health Check":

    st.header(
        "System Health Check"
    )

    health = get_system_health()

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