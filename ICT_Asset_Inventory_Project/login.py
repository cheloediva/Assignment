import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db_connect import connect
import main_app  # This launches the dashboard after login

def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    role = role_var.get()

    if not username or not password:
        messagebox.showwarning("Input Required", "Please fill in all fields.")
        return

    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM login_users WHERE username = %s AND password = %s", (username, password))
            result = cur.fetchone()

            if result:
                messagebox.showinfo("Login Success", f"Welcome, {username} ({role})!")
                window.destroy()
                main_app.launch_app()  # Call the main app launcher
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showerror("Connection Error", "Could not connect to the database.")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Feature under development.")

# ───────────────────── UI Layout ─────────────────────
window = tk.Tk()
window.title("ICT Asset Inventory - Login")
window.geometry("800x500")
window.resizable(True, True)

# Load background image
try:
    bg_image = Image.open("background.jpg")  # Use a nice, wide image
    bg_image = bg_image.resize((800, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except:
    window.configure(bg="#e0f7fa")  # fallback color

# Login form frame
form_frame = tk.Frame(window, bg="white", bd=2, relief="ridge")
form_frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=340)

tk.Label(form_frame, text="🔐 Sign In", font=("Segoe UI", 18, "bold"), bg="white", fg="#0b6fa4").pack(pady=(20, 10))

tk.Label(form_frame, text="Username", bg="white", anchor="w", font=("Segoe UI", 11)).pack(pady=(5, 0), padx=30, fill="x")
entry_username = tk.Entry(form_frame, font=("Segoe UI", 11))
entry_username.pack(padx=30, fill="x")

tk.Label(form_frame, text="Password", bg="white", anchor="w", font=("Segoe UI", 11)).pack(pady=(10, 0), padx=30, fill="x")
entry_password = tk.Entry(form_frame, font=("Segoe UI", 11), show="*")
entry_password.pack(padx=30, fill="x")

tk.Label(form_frame, text="Login as", bg="white", anchor="w", font=("Segoe UI", 11)).pack(pady=(10, 0), padx=30, fill="x")
role_var = tk.StringVar()
role_combo = ttk.Combobox(form_frame, textvariable=role_var, font=("Segoe UI", 11), state="readonly")
role_combo['values'] = ("Admin", "Employee")
role_combo.current(0)
role_combo.pack(padx=30, fill="x", pady=(0, 10))

login_button = tk.Button(form_frame, text="Login", bg="#0b6fa4", fg="white",
                         font=("Segoe UI", 11, "bold"), padx=10, pady=5,
                         command=login)
login_button.pack(pady=(10, 5))

# Forgot password link
forgot = tk.Label(form_frame, text="Forgot Password?", fg="blue", bg="white", cursor="hand2",
                  font=("Segoe UI", 10, "underline"))
forgot.pack()
forgot.bind("<Button-1>", lambda e: forgot_password())

window.mainloop()
