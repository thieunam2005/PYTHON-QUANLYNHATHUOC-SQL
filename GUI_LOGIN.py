import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import pyodbc
import datetime


def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"  
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def toggle_password():
    if show_password.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

def insert_lichsu_dangnhap(tai_khoan):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO LICHSU_DANGNHAP (taiKhoan, thoiGian) VALUES (?, ?)",
            (tai_khoan, datetime.datetime.now())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Ghi lịch sử đăng nhập thất bại:", e)

def sign_in():
    username = entry_email.get().strip()
    password = entry_password.get().strip()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT taiKhoan, matKhau, vaiTro FROM TAIKHOAN WHERE taiKhoan = ? AND matKhau = ?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            taiKhoan, matKhau, vaiTro = result
            insert_lichsu_dangnhap(taiKhoan)
            root.destroy()
            if vaiTro.lower() == "admin":
                import GUI_ADMIN
            elif vaiTro.lower() == "employee":
                import GUI_EMPLOYEE
            else:
                messagebox.showerror("Lỗi", f"Không xác định vai trò: {vaiTro}")
        else:
            messagebox.showerror("Đăng nhập thất bại", "Tài khoản hoặc mật khẩu không đúng.")
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", str(e))

def main():
    global root, entry_email, entry_password, show_password
    root = tk.Tk()
    root.title("Đăng nhập")
    root.geometry("300x400")
    root.configure(bg="black")
    root.resizable(False, False)

    logo_img = Image.open("img/logo.png")
    logo_img = logo_img.resize((90, 30))
    logo_tk = ImageTk.PhotoImage(logo_img)
    tk.Label(root, image=logo_tk, bg="black").pack(pady=(30, 10))

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.pack(pady=10)

    tk.Label(frame, text="ĐĂNG NHẬP", font=("Helvetica", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 20))
    tk.Label(frame, text="Tài khoản:", bg="white").grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    tk.Label(frame, text="Mật khẩu:", bg="white").grid(row=3, column=0, sticky="w")
    entry_password = tk.Entry(frame, width=30, show="*")
    entry_password.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    show_password = tk.BooleanVar()
    tk.Checkbutton(frame, text="Hiển thị mật khẩu", variable=show_password, command=toggle_password, bg="white").grid(row=5, column=0, columnspan=2, sticky="w")

    tk.Button(frame, text="Đăng nhập", bg="black", fg="white", width=25, pady=5, command=sign_in).grid(row=7, column=0, columnspan=2, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
