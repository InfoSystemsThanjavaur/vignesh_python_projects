import sqlite3

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
# USERNAME must be unique
c.execute('''
          CREATE TABLE IF NOT EXISTS users
          (username TEXT PRIMARY KEY,
           password TEXT NOT NULL)
          ''')

print("Database and table created successfully.")

conn.commit()
conn.close()