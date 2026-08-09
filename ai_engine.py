def analyze_error(error_message):

    text = error_message.lower()

    if (
        "database" in text
        or "sql" in text
        or "connection" in text
    ):

        return {
            "type": "Database Error",
            "severity": "HIGH",
            "cause": "Database connection or query problem.",
            "solution": (
                "Check database connection, "
                "credentials, SQL query and database availability."
            )
        }

    elif (
        "timeout" in text
        or "timed out" in text
    ):

        return {
            "type": "Timeout Error",
            "severity": "HIGH",
            "cause": "The service did not respond within the expected time.",
            "solution": (
                "Check server response time, "
                "network connection and service availability."
            )
        }

    elif (
        "permission" in text
        or "access denied" in text
    ):

        return {
            "type": "Permission Error",
            "severity": "MEDIUM",
            "cause": "The application does not have required permissions.",
            "solution": (
                "Check file, folder or service permissions."
            )
        }

    elif (
        "module not found" in text
        or "importerror" in text
    ):

        return {
            "type": "Dependency Error",
            "severity": "HIGH",
            "cause": "Required Python package is missing.",
            "solution": (
                "Install the required dependency "
                "and verify requirements.txt."
            )
        }

    elif (
        "syntaxerror" in text
        or "syntax error" in text
    ):

        return {
            "type": "Syntax Error",
            "severity": "MEDIUM",
            "cause": "The source code contains invalid syntax.",
            "solution": (
                "Check brackets, indentation, quotes "
                "and Python syntax."
            )
        }

    elif (
        "memory" in text
        or "out of memory" in text
    ):

        return {
            "type": "Memory Error",
            "severity": "HIGH",
            "cause": "The application may be consuming too much memory.",
            "solution": (
                "Check memory usage and optimize "
                "large objects or processes."
            )
        }

    else:

        return {
            "type": "Unknown Error",
            "severity": "LOW",
            "cause": "The system could not identify a specific category.",
            "solution": (
                "Review the complete log and investigate "
                "the surrounding events."
            )
        }


def analyze_log(log_text):

    lines = log_text.splitlines()

    errors = []
    warnings = []
    infos = []

    for line in lines:

        lower_line = line.lower()

        if "error" in lower_line:

            errors.append(line)

        elif "warning" in lower_line or "warn" in lower_line:

            warnings.append(line)

        elif "info" in lower_line:

            infos.append(line)

    return {
        "total": len(lines),
        "errors": errors,
        "warnings": warnings,
        "infos": infos
    }