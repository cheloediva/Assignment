# setup_tables.py

import psycopg2
from db_connect import connect

def create_tables_and_insert_users():
    conn = connect()
    if conn is None:
        print("❌ Failed to connect to database.")
        return

    cur = conn.cursor()

    try:
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(50)
            );
        """)

        # Create assets table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                purchase_date DATE,
                status VARCHAR(30)
            );
        """)

        # Create assignments table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id SERIAL PRIMARY KEY,
                asset_id INT REFERENCES assets(id),
                user_id INT REFERENCES users(id),
                date_assigned DATE
            );
        """)

        # Create login_users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(30)
            );
        """)

        # Insert sample login users
        cur.execute("""
            INSERT INTO login_users (username, password, role) VALUES
            ('admin', 'admin123', 'admin'),
            ('it_jane', 'jane456', 'it_officer'),
            ('staff_mike', 'mike789', 'staff')
            ON CONFLICT (username) DO NOTHING;
        """)

        conn.commit()
        print("✅ Tables created and sample login users inserted successfully.")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_tables_and_insert_users()
