# add_asset_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect
from datetime import datetime

def open_add_asset_form(parent_frame, refresh_callback):
    top = tk.Toplevel(parent_frame)
    top.title("Add New Asset")
    top.geometry("350x250")
    top.resizable(False, False)

    tk.Label(top, text="Asset Name:", font=("Segoe UI", 10)).pack(pady=5)
    name_entry = ttk.Entry(top, width=30)
    name_entry.pack()

    tk.Label(top, text="Category:", font=("Segoe UI", 10)).pack(pady=5)
    category_entry = ttk.Entry(top, width=30)
    category_entry.pack()

    tk.Label(top, text="Status:", font=("Segoe UI", 10)).pack(pady=5)
    status_entry = ttk.Entry(top, width=30)
    status_entry.pack()

    def save_asset():
        name = name_entry.get().strip()
        category = category_entry.get().strip()
        status = status_entry.get().strip()
        date_added = datetime.now().strftime('%Y-%m-%d')

        if not name or not category or not status:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO assets (name, category, status, date_added)
                VALUES (%s, %s, %s, %s)
            """, (name, category, status, date_added))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "✅ Asset added successfully.")
            top.destroy()
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Database Error", f"❌ Failed to save asset:\n{e}")

    ttk.Button(top, text="➕ Save Asset", command=save_asset).pack(pady=15)
