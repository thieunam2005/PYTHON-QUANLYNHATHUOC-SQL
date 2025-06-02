import tkinter as tk
import pyodbc
from tkinter import ttk

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_login_history_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    tk.Label(parent, text="LỊCH SỬ ĐĂNG NHẬP", font=("Arial", 16, "bold"), fg="black", bg="white").pack(pady=10)

    columns = ("id", "taiKhoan", "thoiGian")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    tree.heading("id", text="STT")
    tree.heading("taiKhoan", text="Tài khoản")
    tree.heading("thoiGian", text="Thời gian đăng nhập")

    tree.column("id", width=50)
    tree.column("taiKhoan", width=150)
    tree.column("thoiGian", width=200)

    tree.pack(fill="both", expand=True, padx=20, pady=10)


    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, taiKhoan, thoiGian FROM LICHSU_DANGNHAP ORDER BY thoiGian DESC")
        rows = cursor.fetchall()
        for row in rows:
            id_val, username, time_val = row
            time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
            tree.insert("", "end", values=(id_val, username, time_str))

        conn.close()
    except Exception as e:
        tk.Label(parent, text="Không thể tải dữ liệu: " + str(e), fg="red", bg="white").pack()

