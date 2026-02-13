import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os
# Create folder if it doesn't exist
if not os.path.exists("employee_photos"):
    os.makedirs("employee_photos")



from PIL import Image, ImageTk
from db_connect import connect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def show_users_section(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    parent_frame.configure(bg="white")

    photo_path_var = tk.StringVar()

    title = tk.Label(parent_frame, text="Employee Management", font=("Helvetica", 18, "bold"), bg="white", fg="#0b6fa4")
    title.pack(pady=10)

    # === Search Bar ===
    search_frame = tk.Frame(parent_frame, bg="white")
    search_frame.pack(padx=20, pady=(5, 10), fill="x")

    tk.Label(search_frame, text="Search by:", font=("Segoe UI", 11), bg="white").pack(side="left", padx=5)
    search_filter = ttk.Combobox(search_frame, values=["Name", "Gender", "Department", "Email", "Status"], state="readonly", font=("Segoe UI", 10))
    search_filter.set("Name")
    search_filter.pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), width=30)
    search_entry.pack(side="left", padx=5)

    def apply_search():
        key = search_filter.get().lower()
        value = search_entry.get().strip().lower()
        for row in tree.get_children():
            tree.delete(row)
        conn = connect()
        if conn:
            cur = conn.cursor()
            query = f"SELECT id, name, gender, department, email, status FROM users WHERE LOWER({key}) LIKE %s ORDER BY id ASC"
            cur.execute(query, (f"%{value}%",))
            for idx, row_data in enumerate(cur.fetchall()):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=row_data, tags=(tag,))
            cur.close()
            conn.close()

    def reset_search():
        search_entry.delete(0, tk.END)
        load_employees()

    tk.Button(search_frame, text="Search", command=apply_search, bg="#0b6fa4", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(search_frame, text="Reset", command=reset_search, bg="gray", fg="white", font=("Segoe UI", 10)).pack(side="left", padx=5)

    # === Form Fields ===
    form_frame = tk.Frame(parent_frame, bg="white")
    form_frame.pack(pady=10, padx=20)

    entries = {}
    row = 0

    tk.Label(form_frame, text="Name:", bg="white", font=("Segoe UI", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entries["name"] = tk.Entry(form_frame, font=("Segoe UI", 11), width=25)
    entries["name"].grid(row=row, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Gender:", bg="white", font=("Segoe UI", 11)).grid(row=row, column=2, sticky="e", padx=5, pady=5)
    entries["gender"] = ttk.Combobox(form_frame, values=["Male", "Female"], font=("Segoe UI", 11), state="readonly", width=22)
    entries["gender"].grid(row=row, column=3, padx=5, pady=5)

    row += 1
    tk.Label(form_frame, text="Department:", bg="white", font=("Segoe UI", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entries["department"] = tk.Entry(form_frame, font=("Segoe UI", 11), width=25)
    entries["department"].grid(row=row, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Email:", bg="white", font=("Segoe UI", 11)).grid(row=row, column=2, sticky="e", padx=5, pady=5)
    entries["email"] = tk.Entry(form_frame, font=("Segoe UI", 11), width=25)
    entries["email"].grid(row=row, column=3, padx=5, pady=5)

    row += 1
    tk.Label(form_frame, text="Status:", bg="white", font=("Segoe UI", 11)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entries["status"] = ttk.Combobox(form_frame, values=["Full Time", "Part Time"], font=("Segoe UI", 11), state="readonly", width=22)
    entries["status"].grid(row=row, column=1, padx=5, pady=5)

    # === Photo Upload ===
    photo_frame = tk.Frame(form_frame, bg="white")
    photo_frame.grid(row=row, column=2, columnspan=2, padx=5, pady=5)

    photo_label = tk.Label(photo_frame, text="No Photo", bg="#f0f0f0", width=20, height=7, relief="solid")
    photo_label.pack(padx=5, pady=5)

    def choose_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            photo_path_var.set(file_path)
            img = Image.open(file_path)
            img = img.resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            photo_label.configure(image=img_tk)
            photo_label.image = img_tk

    tk.Button(photo_frame, text="Choose Photo", command=choose_photo, bg="#0b6fa4", fg="white", font=("Segoe UI", 9)).pack()

    selected_id = None

    # === Buttons ===
    btn_frame = tk.Frame(parent_frame, bg="white")
    btn_frame.pack(pady=10)

    def clear_fields():
        nonlocal selected_id
        selected_id = None
        for widget in entries.values():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        photo_path_var.set("")
        photo_label.configure(image="", text="No Photo")

    def load_employees():
        for row in tree.get_children():
            tree.delete(row)
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, gender, department, email, status FROM users ORDER BY id ASC")
            for idx, row_data in enumerate(cur.fetchall()):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=row_data, tags=(tag,))
            cur.close()
            conn.close()

    def save_employee():
        data = {k: v.get().strip() for k, v in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return

        photo_filename = ""
        if photo_path_var.get():
            os.makedirs("employee_photos", exist_ok=True)
            photo_filename = f"employee_photos/{data['name'].replace(' ', '_')}.jpg"
            img = Image.open(photo_path_var.get())
            img.save(photo_filename)

        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, gender, department, email, status) VALUES (%s, %s, %s, %s, %s)",
                    (data["name"], data["gender"], data["department"], data["email"], data["status"]))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Added", "Employee added successfully.")
        clear_fields()
        load_employees()

    def update_employee():
        nonlocal selected_id
        if not selected_id:
            return
        data = {k: v.get().strip() for k, v in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return
        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name=%s, gender=%s, department=%s, email=%s, status=%s WHERE id=%s",
                    (data["name"], data["gender"], data["department"], data["email"], data["status"], selected_id))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Updated", "Employee updated successfully.")
        clear_fields()
        load_employees()

    def delete_employee():
        nonlocal selected_id
        if not selected_id:
            return
        confirm = messagebox.askyesno("Confirm", "Delete this employee?")
        if confirm:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=%s", (selected_id,))
            conn.commit()
            cur.close()
            conn.close()
            clear_fields()
            load_employees()

    def on_tree_select(event):
        nonlocal selected_id
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            selected_id = values[0]
            entries["name"].delete(0, tk.END)
            entries["name"].insert(0, values[1])
            entries["gender"].set(values[2])
            entries["department"].delete(0, tk.END)
            entries["department"].insert(0, values[3])
            entries["email"].delete(0, tk.END)
            entries["email"].insert(0, values[4])
            entries["status"].set(values[5])
            image_path = f"employee_photos/{values[1].replace(' ', '_')}.jpg"
            if os.path.exists(image_path):
                img = Image.open(image_path).resize((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                photo_label.configure(image=img_tk, text="")
                photo_label.image = img_tk
                photo_path_var.set(image_path)
            else:
                photo_label.configure(image="", text="No Photo")

    def export_to_excel():
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, gender, department, email, status FROM users ORDER BY id ASC")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            if rows:
                df = pd.DataFrame(rows, columns=["ID", "Name", "Gender", "Department", "Email", "Status"])
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
                if file_path:
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Exported", "✅ Exported to Excel successfully!")

    def export_to_pdf():
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, gender, department, email, status FROM users ORDER BY id ASC")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            if rows:
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
                if file_path:
                    c = canvas.Canvas(file_path, pagesize=letter)
                    y = 750
                    for row in rows:
                        line = " | ".join(str(val) for val in row)
                        c.drawString(30, y, line)
                        y -= 20
                    c.save()
                    messagebox.showinfo("Exported", "✅ Exported to PDF successfully!")

    ttk.Button(btn_frame, text="Save", command=save_employee).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Update", command=update_employee).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Delete", command=delete_employee).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Clear", command=clear_fields).grid(row=0, column=3, padx=5)
    ttk.Button(btn_frame, text="Export Excel", command=export_to_excel).grid(row=0, column=4, padx=5)
    ttk.Button(btn_frame, text="Export PDF", command=export_to_pdf).grid(row=0, column=5, padx=5)

    # === Treeview Table ===
    tree_frame = tk.Frame(parent_frame, bg="white")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree_scroll_y = tk.Scrollbar(tree_frame)
    tree_scroll_y.pack(side="right", fill="y")

    tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
    tree_scroll_x.pack(side="bottom", fill="x")

    cols = ("ID", "Name", "Gender", "Department", "Email", "Status")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    tree.tag_configure("evenrow", background="#f2f2f2")
    tree.tag_configure("oddrow", background="white")
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    tree.pack(fill="both", expand=True)

    load_employees()
