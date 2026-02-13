# register_user.py

import tkinter as tk
from tkinter import messagebox
from db_connect import connect

def save_user():
    name = entry_name.get()
    department = entry_department.get()

    if not name or not department:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, department) VALUES (%s, %s)", (name, department))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "User registered successfully!")
            entry_name.delete(0, tk.END)
            entry_department.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# GUI Window
window = tk.Tk()
window.title("Register User")
window.geometry("350x250")

tk.Label(window, text="Register New User", font=("Arial", 14)).pack(pady=10)

tk.Label(window, text="Full Name").pack(pady=5)
entry_name = tk.Entry(window, width=30)
entry_name.pack(pady=5)

tk.Label(window, text="Department").pack(pady=5)
entry_department = tk.Entry(window, width=30)
entry_department.pack(pady=5)

tk.Button(window, text="Save User", command=save_user).pack(pady=20)

window.mainloop()
