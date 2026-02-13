import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connect import connect
from datetime import datetime
import os
from PIL import Image, ImageTk

def show_assets_section(frame):
    frame.configure(bg="#f0f2f5")

    if not os.path.exists("asset_photos"):
        os.makedirs("asset_photos")

    selected_asset = {}
    photo_path_var = tk.StringVar()

    # Title
    title = tk.Label(frame, text="📦 Asset Management", font=("Helvetica", 16, "bold"), bg="#f0f2f5")
    title.pack(pady=10)

    # Top layout: Form + Preview
    top_frame = tk.Frame(frame, bg="#f0f2f5")
    top_frame.pack(padx=10, fill="x")

    form_frame = tk.Frame(top_frame, bg="#f0f2f5")
    form_frame.pack(side="left", padx=10, pady=5)

    preview_frame = tk.Frame(top_frame, bg="#f0f2f5")
    preview_frame.pack(side="right", padx=10)

    # Photo label
    image_label = tk.Label(preview_frame, text="No Image", bg="#dcdde1", width=18, height=10, relief="solid")
    image_label.pack(pady=5)

    def show_photo(path):
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((150, 120))
            img_tk = ImageTk.PhotoImage(img)
            image_label.configure(image=img_tk, text="")
            image_label.image = img_tk
        else:
            image_label.configure(image="", text="No Image")

    def clear_photo():
        image_label.configure(image="", text="No Image")
        image_label.image = None

    # === Form Fields ===
    tk.Label(form_frame, text="Name:", bg="#f0f2f5").grid(row=0, column=0, sticky="e")
    name_entry = ttk.Entry(form_frame, width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Category:", bg="#f0f2f5").grid(row=1, column=0, sticky="e")
    category_entry = ttk.Entry(form_frame, width=25)
    category_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Status:", bg="#f0f2f5").grid(row=2, column=0, sticky="e")
    status_entry = ttk.Entry(form_frame, width=25)
    status_entry.grid(row=2, column=1, padx=5, pady=5)

    def choose_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            photo_path_var.set(file_path)
            show_photo(file_path)

    ttk.Button(form_frame, text="Choose Photo", command=choose_photo).grid(row=3, columnspan=2, pady=5)

    # Search Bar
    search_var = tk.StringVar()
    search_entry = ttk.Entry(frame, textvariable=search_var, width=40)
    search_entry.pack(pady=5)
    search_entry.insert(0, "Search asset by name...")
    search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END))
    search_entry.bind("<KeyRelease>", lambda e: filter_assets())

    # Treeview
    columns = ("ID", "Name", "Category", "Status", "Purchase Date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=28)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#2c3e50", foreground="white")
    style.map("Treeview", background=[("selected", "#3498db")])

    tree.tag_configure("evenrow", background="#ecf0f1")
    tree.tag_configure("oddrow", background="white")

    # Tree Select
    def on_tree_select(event):
        selected = tree.focus()
        if selected:
            selected_asset.clear()
            selected_asset.update(dict(zip(columns, tree.item(selected)["values"])))
            enable_buttons()

            # Auto-fill form fields
            name_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            status_entry.delete(0, tk.END)
            name_entry.insert(0, selected_asset["Name"])
            category_entry.insert(0, selected_asset["Category"])
            status_entry.insert(0, selected_asset["Status"])

            img_path = f"asset_photos/{selected_asset['Name'].replace(' ', '_')}.jpg"
            show_photo(img_path)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def disable_buttons():
        edit_btn.config(state="disabled")
        delete_btn.config(state="disabled")

    def enable_buttons():
        edit_btn.config(state="normal")
        delete_btn.config(state="normal")

    # Load assets
    def load_assets():
        tree.delete(*tree.get_children())
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT id, name, category, status, purchase_date FROM assets ORDER BY id ASC")
        for idx, row in enumerate(cur.fetchall()):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            tree.insert("", "end", values=row, tags=(tag,))
        cur.close()
        conn.close()
        disable_buttons()
        clear_photo()

    def filter_assets():
        query = search_var.get().lower()
        for item in tree.get_children():
            values = tree.item(item)['values']
            name = str(values[1]).lower()
            tree.item(item, tags=("hidden",))
            if query in name:
                tree.item(item, tags=("visible",))
        tree.tag_configure("hidden", foreground="#f0f2f5")
        tree.tag_configure("visible", foreground="black")

    # CRUD Functions
    def save_asset():
        name = name_entry.get().strip()
        category = category_entry.get().strip()
        status = status_entry.get().strip()
        purchase_date = datetime.now().strftime('%Y-%m-%d')

        if not name or not category or not status:
            messagebox.showerror("Missing", "All fields are required")
            return

        # Save photo
        if photo_path_var.get():
            final_path = f"asset_photos/{name.replace(' ', '_')}.jpg"
            img = Image.open(photo_path_var.get())
            img.save(final_path)

        conn = connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO assets (name, category, status, purchase_date) VALUES (%s, %s, %s, %s)",
                    (name, category, status, purchase_date))
        conn.commit()
        cur.close()
        conn.close()
        load_assets()
        clear_fields()

    def update_asset():
        if not selected_asset:
            return
        name = name_entry.get().strip()
        category = category_entry.get().strip()
        status = status_entry.get().strip()

        if not name or not category or not status:
            messagebox.showerror("Missing", "All fields are required")
            return

        # Save photo
        if photo_path_var.get():
            final_path = f"asset_photos/{name.replace(' ', '_')}.jpg"
            img = Image.open(photo_path_var.get())
            img.save(final_path)

        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE assets SET name=%s, category=%s, status=%s WHERE id=%s",
                    (name, category, status, selected_asset["ID"]))
        conn.commit()
        cur.close()
        conn.close()
        load_assets()
        clear_fields()

    def delete_asset():
        if not selected_asset:
            return
        confirm = messagebox.askyesno("Confirm", "Delete this asset?")
        if confirm:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM assets WHERE id=%s", (selected_asset["ID"],))
            conn.commit()
            cur.close()
            conn.close()
            load_assets()
            clear_fields()

    def clear_fields():
        name_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        status_entry.delete(0, tk.END)
        photo_path_var.set("")
        clear_photo()
        selected_asset.clear()
        disable_buttons()

    # Buttons
    btn_frame = tk.Frame(frame, bg="#f0f2f5")
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="➕ Add Asset", command=save_asset).grid(row=0, column=0, padx=5)
    edit_btn = ttk.Button(btn_frame, text="✏️ Update Asset", command=update_asset, state="disabled")
    edit_btn.grid(row=0, column=1, padx=5)
    delete_btn = ttk.Button(btn_frame, text="🗑️ Delete Asset", command=delete_asset, state="disabled")
    delete_btn.grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Clear", command=clear_fields).grid(row=0, column=3, padx=5)

    load_assets()
