import sqlite3
import hashlib

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def add_user(username, password):
    """Adds a new user to the database with a hashed password."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # This error occurs if the username already exists
        return False
    finally:
        conn.close()

def check_user(username, password):
    """Checks if a user exists and the password is correct."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password_hash = c.fetchone()
    conn.close()
    if stored_password_hash:
        # Check if the hashed version of the entered password matches the stored hash
        return stored_password_hash[0] == hash_password(password)
    return False