# dashboard_section.py

import tkinter as tk
from tkinter import ttk
import psycopg2

class DashboardSection(tk.Frame):
    def __init__(self, master, conn):
        super().__init__(master)
        self.conn = conn
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text="Dashboard", font=("Helvetica", 24, 'bold'), bg='white')
        title.pack(pady=20)

        stats_frame = tk.Frame(self, bg='white')
        stats_frame.pack(pady=10)

        self.asset_count_label = self.create_stat_box(stats_frame, "Total Assets", 0)
        self.user_count_label = self.create_stat_box(stats_frame, "Total Users", 0)
        self.assignment_count_label = self.create_stat_box(stats_frame, "Total Assignments", 0)

        self.update_stats()

    def create_stat_box(self, parent, title, count):
        frame = tk.Frame(parent, bg="#f0f0f0", padx=20, pady=10, bd=1, relief="solid")
        frame.pack(side=tk.LEFT, padx=10)

        label_title = tk.Label(frame, text=title, font=("Helvetica", 14), bg="#f0f0f0")
        label_title.pack()

        label_count = tk.Label(frame, text=str(count), font=("Helvetica", 22, "bold"), bg="#f0f0f0", fg="blue")
        label_count.pack()

        return label_count

    def update_stats(self):
        try:
            cur = self.conn.cursor()

            cur.execute("SELECT COUNT(*) FROM assets")
            asset_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM users")
            user_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM assignments")
            assignment_count = cur.fetchone()[0]

            self.asset_count_label.config(text=str(asset_count))
            self.user_count_label.config(text=str(user_count))
            self.assignment_count_label.config(text=str(assignment_count))

            cur.close()
        except Exception as e:
            print("Error fetching stats:", e)
