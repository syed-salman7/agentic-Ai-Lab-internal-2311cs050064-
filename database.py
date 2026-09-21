import sqlite3

DB_NAME = "college.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            marks INTEGER,
            city TEXT
        )
    """)

    # Insert sample data only if table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        students = [
            (1, "Rahul", "CSE", 85, "Hyderabad"),
            (2, "Priya", "ECE", 78, "Warangal"),
            (3, "Arjun", "CSE", 92, "Hyderabad"),
            (4, "Sneha", "EEE", 69, "Nizamabad"),
            (5, "Kiran", "CSE", 88, "Karimnagar"),
            (6, "Anjali", "ECE", 95, "Hyderabad")
        ]

        cursor.executemany("""
            INSERT INTO students
            (id, name, department, marks, city)
            VALUES (?, ?, ?, ?, ?)
        """, students)

    conn.commit()
    conn.close()


def get_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sql
        FROM sqlite_master
        WHERE type='table'
        AND name='students'
    """)

    schema = cursor.fetchone()[0]

    conn.close()

    return schema


def execute_query(sql):
    conn = sqlite3.connect(DB_NAME)

    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [description[0] for description in cursor.description]

        rows = cursor.fetchall()

        return columns, rows

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")