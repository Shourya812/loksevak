import sqlite3
import os

# Path of the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "loksahay.db")


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """Create all required database tables if they don't already exist."""
    
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'citizen'
        )
    """)

    # Civic reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            address TEXT,
            image_filename TEXT,
            status TEXT NOT NULL DEFAULT 'Submitted',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Insert some default categories
    default_categories = [
        "Road/Pothole",
        "Garbage",
        "Streetlight",
        "Water Supply",
        "Drainage",
        "Electricity",
        "Other"
    ]

    for category in default_categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,)
        )

    # Add image_filename column to existing databases
    cursor.execute("PRAGMA table_info(reports)")
    columns = [column["name"] for column in cursor.fetchall()]

    if "image_filename" not in columns:
        cursor.execute(
            "ALTER TABLE reports ADD COLUMN image_filename TEXT"
        )

    connection.commit()
    connection.close()


def add_user(name, email, password, role="citizen"):
    """Add a new user to the database."""
    
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password, role))

        connection.commit()
        user_id = cursor.lastrowid

        return user_id

    except sqlite3.IntegrityError:
        return None

    finally:
        connection.close()


def get_user_by_email(email):
    """Find a user using their email address."""
    
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    connection.close()

    return user


def add_report(
    user_id,
    title,
    category,
    description,
    latitude=None,
    longitude=None,
    address=None,
    image_filename=None
):
    """Add a civic issue report."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reports
        (user_id, title, category, description, latitude, longitude, address,image_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        category,
        description,
        latitude,
        longitude,
        address,
        image_filename
    ))

    connection.commit()
    report_id = cursor.lastrowid
    connection.close()

    return report_id


def get_all_reports():
    """Return all civic reports."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            reports.*,
            users.name AS reporter_name,
            users.email AS reporter_email
        FROM reports
        LEFT JOIN users ON reports.user_id = users.id
        ORDER BY reports.created_at DESC
    """)

    reports = cursor.fetchall()
    connection.close()

    return reports


def get_report_by_id(report_id):
    """Return a single civic report."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            reports.*,
            users.name AS reporter_name,
            users.email AS reporter_email
        FROM reports
        LEFT JOIN users ON reports.user_id = users.id
        WHERE reports.id = ?
    """, (report_id,))

    report = cursor.fetchone()
    connection.close()

    return report


def update_report_status(report_id, status):
    """Update the status of a civic report."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE reports
        SET status = ?
        WHERE id = ?
    """, (status, report_id))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated