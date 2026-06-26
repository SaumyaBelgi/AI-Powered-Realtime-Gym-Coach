import sqlite3
import streamlit as st
from pathlib import Path

# Define the path to the SQLite database file. The data.db file acts as a persistent storage for user and exercise data, allowing the application to maintain state across sessions and restarts. The database is located three levels up from the current file's directory, ensuring that it is easily accessible while keeping the project structure organized.

_DB_PATH = str(Path(__file__).parent.parent.parent / "data.db")


@st.cache_resource    # The @st.cache_resource decorator is used to cache the database connection resource. This means that the connection will be created only once and reused across multiple calls, improving performance by avoiding the overhead of establishing a new connection each time the database is accessed. It also ensures that the connection is shared across different threads in a multi-threaded environment like Streamlit.
def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)    # streamlit runs in a multi-threaded environment, and SQLite connections are not thread-safe by default. Setting check_same_thread to False allows the connection to be shared across different threads, enabling concurrent access to the database without running into threading issues.


    conn.row_factory = sqlite3.Row    # by default, sqlite3 returns rows as tuples. Setting the row factory to sqlite3.Row allows us to access columns by name, making the code more readable and maintainable.
    return conn

# creating the two tables
def init_db() -> None:
    conn = _get_connection()

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id),
                exercise_name TEXT    NOT NULL,
                reps          INTEGER NOT NULL DEFAULT 0,
                sets          INTEGER NOT NULL DEFAULT 0,
                time          INTEGER NOT NULL DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

# fetching a particular user from the database based on their username
def get_user(username: str) -> sqlite3.Row:
    conn = _get_connection()

    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


# creating a new user in the database with the provided username. If the username already exists, it will raise an IntegrityError due to the UNIQUE constraint on the username column.
def create_user(username: str) -> sqlite3.Row:
    conn = _get_connection()
    
    with conn:
        conn.execute(
            "INSERT INTO users (username) VALUES (?)", (username,)
        )

    return get_user(username) 

# function to check if a user exists in the database based on their username. If user does not exist, it creates a new user with the provided username
def get_or_create_user(username: str) -> sqlite3.Row:
    user = get_user(username)

    if user is None:
        user = create_user(username)
    
    return user

# function to add a new exercise entry for a user. If an entry for the same exercise already exists for the user on the current date, it updates the existing entry by adding the new reps, sets, and time to the existing values. Otherwise, it creates a new entry in the exercises table.
def add_exercise(user_id, exercise_name, reps, sets, time):
    conn = _get_connection()

    with conn:
        existing = conn.execute("""
            SELECT * FROM exercises 
            WHERE user_id = ? AND exercise_name = ? AND Date('created_at') = Date('now')
        """, (user_id, exercise_name)).fetchone()

        if existing:
            conn.execute("""
                UPDATE exercises 
                SET reps = reps + ?, sets = sets + ?, time = time + ?
                WHERE id = ?
            """, (reps, sets, time, existing['id']))
        else:
            conn.execute("""
                INSERT INTO exercises (user_id, exercise_name, sets, reps, time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, exercise_name, sets, reps, time))

# function to retrieve all exercise entries for a specific user from the database. It fetches all rows from the exercises table where the user_id matches the provided user_id, allowing the application to display the user's exercise history.
def get_users_exercises(user_id):
    conn = _get_connection()

    return conn.execute("""
        SELECT * FROM exercises 
        WHERE user_id = ?
    """, (user_id,)).fetchall()