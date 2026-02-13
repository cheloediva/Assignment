import tkinter as tk 
from tkinter import ttk, messagebox
from db_connect import connect

def show_assignments_section(main_area):
    for widget in main_area.winfo_children():
        widget.destroy()

    title = tk.Label(
        main_area,
        text="📋 Assignment Records",
        font=("Helvetica", 16, "bold"),
        bg="#f0f2f5"
    )
    title.pack(pady=10)

    # ----- Add Assignment Form -----
    form_frame = tk.Frame(main_area, bg="#f0f2f5")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Select User:", bg="#f0f2f5").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    user_combo = ttk.Combobox(form_frame, state="readonly", width=25)
    user_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Select Asset:", bg="#f0f2f5").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    asset_combo = ttk.Combobox(form_frame, state="readonly", width=25)
    asset_combo.grid(row=0, column=3, padx=5, pady=5)

    def refresh_dropdowns():
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM users")
        users = cur.fetchall()
        user_combo["values"] = [f"{u[0]} - {u[1]}" for u in users]

        cur.execute("SELECT id, name FROM assets WHERE status = 'Available'")
        assets = cur.fetchall()
        asset_combo["values"] = [f"{a[0]} - {a[1]}" for a in assets]

        cur.close()
        conn.close()

    refresh_dropdowns()

    def add_assignment():
        user_sel = user_combo.get()
        asset_sel = asset_combo.get()

        if not user_sel or not asset_sel:
            messagebox.showwarning("Missing Info", "Please select both user and asset.")
            return

        user_id = int(user_sel.split(" - ")[0])
        asset_id = int(asset_sel.split(" - ")[0])

        try:
            conn = connect()
            cur = conn.cursor()

            # Add assignment
            cur.execute(
                "INSERT INTO assignments (asset_id, user_id, date_assigned) VALUES (%s, %s, CURRENT_DATE)",
                (asset_id, user_id)
            )

            # Update asset status
            cur.execute("UPDATE assets SET status = 'Assigned' WHERE id = %s", (asset_id,))
            conn.commit()

            cur.close()
            conn.close()

            messagebox.showinfo("Success", "Assignment added successfully.")
            user_combo.set("")
            asset_combo.set("")
            refresh_dropdowns()
            load_assignments()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add assignment:\n{e}")

    add_btn = tk.Button(form_frame, text="➕ Add Assignment", bg="#4CAF50", fg="white", command=add_assignment)
    add_btn.grid(row=0, column=4, padx=10, pady=5)

    # ----- Treeview -----
    columns = ("Assignment ID", "Assigned To", "Asset Name", "Date Assigned")
    tree = ttk.Treeview(main_area, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(pady=20, fill="both", expand=True)

    def load_assignments():
        for row in tree.get_children():
            tree.delete(row)

        conn = connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                a.id AS assignment_id,
                u.name AS assigned_to,
                s.name AS asset_name,
                a.date_assigned
            FROM assignments a
            JOIN users u ON a.user_id = u.id
            JOIN assets s ON a.asset_id = s.id
            ORDER BY a.id;
        """)
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

        cur.close()
        conn.close()

    load_assignments()

    # ----- Delete Assignment -----
    def delete_assignment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an assignment to delete.")
            return

        item = tree.item(selected)
        assignment_id = item["values"][0]
        asset_name = item["values"][2]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Assignment ID {assignment_id}?")
        if not confirm:
            return

        try:
            conn = connect()
            cur = conn.cursor()

            cur.execute("SELECT id FROM assets WHERE name = %s", (asset_name,))
            asset_id = cur.fetchone()[0]

            cur.execute("DELETE FROM assignments WHERE id = %s", (assignment_id,))
            cur.execute("UPDATE assets SET status = 'Available' WHERE id = %s", (asset_id,))
            conn.commit()

            cur.close()
            conn.close()

            messagebox.showinfo("Deleted", f"Assignment {assignment_id} deleted.")
            load_assignments()
            refresh_dropdowns()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete assignment:\n{e}")

    delete_btn = tk.Button(main_area, text="🗑️ Delete Assignment", command=delete_assignment, bg="#dc3545", fg="white")
    delete_btn.pack(pady=5)
