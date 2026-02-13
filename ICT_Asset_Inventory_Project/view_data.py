# view_assets.py

import tkinter as tk
from tkinter import ttk
from db_connect import connect

def show_assets():
    conn = connect()
    if not conn:
        print("❌ Failed to connect to the database.")
        return

    cur = conn.cursor()
    cur.execute("SELECT id, name, category, purchase_date, status FROM assets")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Create a new popup window
    window = tk.Toplevel()
    window.title("📋 All Assets")
    window.geometry("700x400")

    tk.Label(window, text="📋 Asset List", font=("Arial", 14, "bold")).pack(pady=10)

    # Scrollable text area
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    text_area = tk.Text(frame, wrap=tk.NONE)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, command=text_area.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area.config(yscrollcommand=scrollbar.set)

    # Insert asset records into text area
    for row in rows:
        text_area.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Purchased: {row[3]} | Status: {row[4]}\n")

    text_area.config(state=tk.DISABLED)  # Make it read-only
