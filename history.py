import streamlit as st
import pandas as pd

from database import (
    get_deployment_history,
    get_error_history,
    get_log_history
)


def show_history(user_id):

    st.header("Deployment & Activity History")

    tab1, tab2, tab3 = st.tabs([
        "Deployments",
        "Errors",
        "Log Analysis"
    ])

    # ---------------- DEPLOYMENT ----------------

    with tab1:

        data = get_deployment_history(user_id)

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Project",
                    "Environment",
                    "Status",
                    "Date"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No deployment history available."
            )

    # ---------------- ERRORS ----------------

    with tab2:

        data = get_error_history(user_id)

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Error Type",
                    "Message",
                    "Severity",
                    "Solution",
                    "Date"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No error history available."
            )

    # ---------------- LOGS ----------------

    with tab3:

        data = get_log_history(user_id)

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Total Lines",
                    "Errors",
                    "Warnings",
                    "Info",
                    "Date"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No log analysis history available."
            )