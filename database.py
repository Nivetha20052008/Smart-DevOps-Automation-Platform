import sqlite3
import bcrypt
from datetime import datetime


DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Deployment history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deployment_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            environment TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Error history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            error_type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL,
            solution TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Log history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_lines INTEGER NOT NULL,
            errors INTEGER NOT NULL,
            warnings INTEGER NOT NULL,
            infos INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Real-time system monitoring history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            status TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def check_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def register_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users
            (name, email, password, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Email already registered."

    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    user_id, name, email, hashed_password = user

    if check_password(password, hashed_password):
        return {
            "id": user_id,
            "name": name,
            "email": email
        }

    return None


def get_user_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()

    return count


def save_deployment(user_id, project_name, environment, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO deployment_history
        (user_id, project_name, environment, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        project_name,
        environment,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_error(user_id, error_type, message, severity, solution):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO error_history
        (user_id, error_type, message, severity, solution, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        error_type,
        message,
        severity,
        solution,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_log_analysis(
    user_id,
    total_lines,
    errors,
    warnings,
    infos
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO log_history
        (user_id, total_lines, errors, warnings, infos, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        total_lines,
        errors,
        warnings,
        infos,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_system_monitoring(
    user_id,
    cpu,
    memory,
    disk,
    status
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO system_monitoring
        (user_id, cpu, memory, disk, status, checked_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        cpu,
        memory,
        disk,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_system_monitoring_history(user_id, limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cpu, memory, disk, status, checked_at
        FROM system_monitoring
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    data = cursor.fetchall()

    conn.close()

    return data


def get_deployment_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT project_name, environment, status, created_at
        FROM deployment_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_error_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT error_type, message, severity, solution, created_at
        FROM error_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_log_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total_lines, errors, warnings, infos, created_at
        FROM log_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data