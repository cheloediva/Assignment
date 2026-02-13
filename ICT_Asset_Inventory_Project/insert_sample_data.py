from db_connect import connect

def insert_sample_data():
    conn = connect()
    cursor = conn.cursor()

    # Insert sample users
    cursor.execute("""
    INSERT INTO users (name, department) VALUES
    ('Alice Mwaura', 'IT'),
    ('Brian Otieno', 'Finance'),
    ('Cynthia Mwikali', 'HR'),
    ('David Kariuki', 'Procurement'),
    ('Esther Njeri', 'IT'),
    ('Felix Kimani', 'Marketing'),
    ('Grace Achieng', 'HR'),
    ('Henry Maina', 'Finance'),
    ('Irene Wambui', 'Admin'),
    ('James Ouma', 'IT');
    """)

    # Insert sample assets
    cursor.execute("""
    INSERT INTO assets (name, category, purchase_date, status) VALUES
    ('Dell XPS 15', 'Laptop', '2023-03-01', 'Available'),
    ('HP LaserJet Pro', 'Printer', '2022-10-15', 'Assigned'),
    ('Cisco Router 2900', 'Router', '2021-09-20', 'Maintenance'),
    ('Lenovo ThinkPad', 'Laptop', '2023-05-10', 'Available'),
    ('Epson L3150', 'Printer', '2022-07-01', 'Assigned'),
    ('Samsung Galaxy Tab A7', 'Tablet', '2023-01-11', 'Available'),
    ('TP-Link Archer C7', 'Router', '2021-11-05', 'Available'),
    ('MacBook Air M1', 'Laptop', '2022-12-25', 'Assigned'),
    ('Canon PIXMA G3411', 'Printer', '2021-05-08', 'Available'),
    ('Asus ZenBook 14', 'Laptop', '2023-06-17', 'Assigned');
    """)

    # Insert sample assignments
    cursor.execute("""
    INSERT INTO assignments (asset_id, user_id, date_assigned) VALUES
    (2, 1, '2023-06-01'),
    (5, 3, '2023-08-15'),
    (8, 2, '2024-01-10'),
    (10, 4, '2023-11-05'),
    (1, 5, '2023-09-22');
    """)

    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully.")

insert_sample_data()
