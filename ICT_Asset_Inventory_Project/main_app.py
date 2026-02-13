import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connect import connect
from users_section import show_users_section
from assets_section import show_assets_section
from assignments_section import show_assignments_section
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import csv

# === Global Styles ===
BG_COLOR = "#f4f6f8"
SIDEBAR_COLOR = "#1f2a38"
BTN_COLOR = "#273447"
TEXT_COLOR = "#ffffff"
CARD_COLOR = "#ffffff"
FONT_HEADER = ("Segoe UI", 18, "bold")
FONT_NORMAL = ("Segoe UI", 11)

main_area = None
is_dark_mode = False

# === Theme Toggle ===
def toggle_dark_mode():
    global BG_COLOR, BTN_COLOR, TEXT_COLOR, is_dark_mode
    is_dark_mode = not is_dark_mode
    if is_dark_mode:
        BG_COLOR = "#1c1c2b"
        BTN_COLOR = "#2e2e48"
        TEXT_COLOR = "#e6e6e6"
    else:
        BG_COLOR = "#f4f6f8"
        BTN_COLOR = "#273447"
        TEXT_COLOR = "#ffffff"
    launch_app(refresh=True)

# === Clear Main UI ===
def clear_main_area():
    for widget in main_area.winfo_children():
        widget.destroy()

# === DASHBOARD ===
def show_dashboard():
    clear_main_area()

    conn = connect()
    cur = conn.cursor()

    now = datetime.datetime.now()
    greeting = f"Welcome, Chelsea 👋 | {now.strftime('%A, %d %B %Y')}"
    tk.Label(main_area, text=greeting, font=FONT_NORMAL, bg=BG_COLOR, anchor="w").pack(anchor="w", padx=20, pady=10)

    # === Database Fetching ===
    cur.execute("SELECT COUNT(*) FROM assets")
    total_assets = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Assigned'")
    assigned = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Available'")
    available = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Maintenance'")
    maintenance = cur.fetchone()[0]

    cur.execute("SELECT category, COUNT(*) FROM assets GROUP BY category")
    category_data = cur.fetchall()

    cur.execute("SELECT name, status, purchase_date FROM assets ORDER BY purchase_date DESC LIMIT 5")
    recent_assets = cur.fetchall()

    cur.execute("SELECT TO_CHAR(purchase_date, 'YYYY-MM') AS month, COUNT(*) FROM assets GROUP BY month ORDER BY month")
    monthly_data = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assignments")
    total_assignments = cur.fetchone()[0]

    cur.close()
    conn.close()

    # === Card Stats ===
    card_container = tk.Frame(main_area, bg=BG_COLOR)
    card_container.pack(padx=20, pady=(5, 15), fill="x")

    def card(title, count, bg):
        card_frame = tk.Frame(card_container, bg=bg, width=200, height=90)
        card_frame.pack_propagate(False)
        card_frame.pack(side="left", padx=10)
        tk.Label(card_frame, text=title, bg=bg, fg="white", font=("Segoe UI", 10)).pack(anchor="w", padx=10)
        tk.Label(card_frame, text=str(count), bg=bg, fg="white", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=10)

    card("Total Assets", total_assets, "#2c3e50")
    card("Assigned", assigned, "#2980b9")
    card("Available", available, "#27ae60")
    card("Maintenance", maintenance, "#e67e22")

    # === Alerts ===
    if maintenance > 0 or available <= 1:
        alert_frame = tk.Frame(main_area, bg=BG_COLOR)
        alert_frame.pack(anchor="w", padx=20)
        if maintenance > 0:
            tk.Label(alert_frame, text=f"⚠️ {maintenance} asset(s) under maintenance", font=FONT_NORMAL, fg="red", bg=BG_COLOR).pack(anchor="w")
        if available <= 1:
            tk.Label(alert_frame, text=f"⚠️ Low stock: Only {available} available", font=FONT_NORMAL, fg="orange", bg=BG_COLOR).pack(anchor="w")

    # === Charts ===
    chart_container = tk.Frame(main_area, bg=BG_COLOR)
    chart_container.pack(padx=20, pady=10, fill="both", expand=True)

    # Pie chart
    fig = Figure(figsize=(3.5, 3), dpi=100)
    ax = fig.add_subplot(111)
    if category_data:
        labels = [x[0] for x in category_data]
        sizes = [x[1] for x in category_data]
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title("Asset Categories")
    canvas = FigureCanvasTkAgg(fig, master=chart_container)
    canvas.draw()
    canvas.get_tk_widget().pack(side="left", padx=5)

    # Line chart
    if monthly_data:
        fig2 = Figure(figsize=(4.5, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        months = [x[0] for x in monthly_data]
        counts = [x[1] for x in monthly_data]
        ax2.plot(months, counts, marker="o")
        ax2.set_title("Monthly Asset Growth")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Assets")
        canvas2 = FigureCanvasTkAgg(fig2, master=chart_container)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", padx=5)

    # === Recent Activity ===
    recent_label = tk.Label(main_area, text="Recent Assets", font=FONT_HEADER, bg=BG_COLOR)
    recent_label.pack(anchor="w", padx=20, pady=(10, 0))

    for asset in recent_assets:
        activity = f"{asset[0]} | {asset[1]} | {asset[2]}"
        tk.Label(main_area, text=activity, font=FONT_NORMAL, bg=BG_COLOR).pack(anchor="w", padx=25)

    # === System Info Footer ===
    footer = tk.Label(main_area, text=f"Users: {total_users} | Assignments: {total_assignments}",
                      font=("Segoe UI", 10, "italic"), bg=BG_COLOR)
    footer.pack(side="bottom", pady=10)

# === Export CSV ===
def export_summary():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if not file_path:
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, status, purchase_date FROM assets")
    rows = cur.fetchall()
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Category", "Status", "Purchase Date"])
        writer.writerows(rows)
    cur.close()
    conn.close()
    messagebox.showinfo("Export", "Summary exported successfully ✅")

# === MAIN APP ===
def launch_app(refresh=False):
    global main_area
    if refresh:
        for widget in tk._default_root.winfo_children():
            widget.destroy()

    root = tk.Tk()
    root.title("ICT Asset Inventory System")
    root.geometry("1180x700")
    root.configure(bg=BG_COLOR)

    sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=200)
    sidebar.pack(side="left", fill="y")

    main_area = tk.Frame(root, bg=BG_COLOR)
    main_area.pack(side="right", expand=True, fill="both")

    def add_button(text, command):
        return tk.Button(
            sidebar, text=text, font=FONT_NORMAL, bg=BTN_COLOR, fg=TEXT_COLOR,
            activebackground="#1abc9c", activeforeground="white",
            relief="flat", padx=15, pady=10, anchor="w", command=command
        )

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            root.destroy()

    tk.Label(sidebar, text="☰ Menu", bg=SIDEBAR_COLOR, fg=TEXT_COLOR, font=FONT_HEADER).pack(pady=15)
    add_button("🏠 Dashboard", show_dashboard).pack(fill="x")
    add_button("👤 Employees", lambda: (clear_main_area(), show_users_section(main_area))).pack(fill="x")
    add_button("📦 Assets", lambda: (clear_main_area(), show_assets_section(main_area))).pack(fill="x")
    add_button("📋 Assignments", lambda: (clear_main_area(), show_assignments_section(main_area))).pack(fill="x")
    add_button("🌙 Toggle Dark Mode", toggle_dark_mode).pack(fill="x", pady=10)
    add_button("🚪 Logout", logout).pack(side="bottom", fill="x", pady=15)

    show_dashboard()
    root.mainloop()

# === RUN ===
if __name__ == "__main__":
    launch_app()
