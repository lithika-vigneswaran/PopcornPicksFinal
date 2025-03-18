import sqlite3

# Initialize the database
def init_db():
    """
    Initialize the database and create the necessary tables.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    # Create users table with username as PRIMARY KEY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT NOT NULL
        );
    """)

    # Create recommendations table using username 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title TEXT NOT NULL,
            release_date TEXT,
            overview TEXT,
            username TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()

def add_user(username, password):
    """
    Adds a new user to the database.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?);
    """, (username, password))

    conn.commit()
    conn.close()

def user_exists(username):
    """
    Checks if a user exists in the 'users' table by username.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM users WHERE username = ?;
    """, (username,))
    user = cursor.fetchone()

    conn.close()
    return user is not None

def authenticate_user(username, password):
    """
    Authenticate user by checking the username and the password.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username FROM users WHERE username = ? AND password = ?;
    """, (username, password))
    
    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None


def save_recommendation(movie_title, release_date, overview, username):
    """
    Saves a movie recommendation for a user in the 'recommendations' table.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO recommendations (movie_title, release_date, overview, username)
        VALUES (?, ?, ?, ?);
    """, (movie_title, release_date, overview, username))
    print("I SAVED STUFF!")

    conn.commit()
    conn.close()


def get_user_recommendations(username):
    """
    Retrieves all saved movie recommendations for a specific user.
    """
    conn = sqlite3.connect("popcorn_picks.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT movie_title, release_date, overview
        FROM recommendations
        WHERE username = ?;
    """, (username,))

    recommendations = cursor.fetchall()
    print(f"OUR RECS: {recommendations}")
    conn.close()
    return recommendations


# Initialize the database by creating tables if they don't exist
init_db()
