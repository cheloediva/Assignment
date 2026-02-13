# db_connect.py

import psycopg2

def connect():
    try:
        connection = psycopg2.connect(
            dbname="ict_inventory_db",
            user="postgres",
            password="admin123",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL database successfully!")
        print("PostgreSQL version:", connection.server_version)
        return connection
    except Exception as e:
        print("Failed to connect to the database.")
        print("Error:", e)
        return None
