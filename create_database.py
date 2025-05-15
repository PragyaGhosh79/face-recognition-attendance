import sqlite3

conn = sqlite3.connect('Attendance.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Database initialized successfully.")
