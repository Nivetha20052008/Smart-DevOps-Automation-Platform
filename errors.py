import streamlit as st

from ai_engine import analyze_error
from database import save_error


def show_error_analyzer(user_id):

    st.header("AI Error Analyzer")

    st.write(
        "Enter an application error and the system "
        "will identify the possible cause and solution."
    )

    error_message = st.text_area(
        "Paste Error Message",
        height=180,
        placeholder=(
            "Example: Database connection timeout..."
        )
    )

    if st.button(
        "Analyze Error",
        use_container_width=True
    ):

        if not error_message.strip():

            st.warning(
                "Please enter an error message."
            )

            return

        result = analyze_error(
            error_message
        )

        st.subheader("Analysis Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Error Type",
                result["type"]
            )

        with col2:

            st.metric(
                "Severity",
                result["severity"]
            )

        st.info(
            f"Possible Cause: {result['cause']}"
        )

        st.success(
            f"Recommended Solution: {result['solution']}"
        )

        save_error(
            user_id,
            result["type"],
            error_message,
            result["severity"],
            result["solution"]
        )

        st.success(
            "Analysis saved to your history."
        )