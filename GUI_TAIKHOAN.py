import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_account_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT taiKhoan, matKhau, vaiTro FROM TAIKHOAN")
    accounts = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Quản lý tài khoản", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 5))

    list_frame = tk.Frame(frame, bg="white")
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(list_frame, bg="white")
    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg="white")
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def update_account(user, mk_var, role_var):
        new_password = mk_var.get().strip()
        new_role = role_var.get().strip()
        if len(new_password) < 5:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 5 ký tự.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE TAIKHOAN SET matKhau = ?, vaiTro = ? WHERE taiKhoan = ?
            """, (new_password, new_role, user))
            conn.commit()
            messagebox.showinfo("Thành công", f"Cập nhật tài khoản {user} thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    if not accounts:
        tk.Label(scrollable, text="Không có tài khoản nào.", bg="white", fg="gray", font=("Arial", 11)).pack(pady=20)
    else:
        for acc in accounts:
            acc_data = dict(zip(col_names, acc))
            row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=f"Tài khoản: {acc_data['taiKhoan']}", bg="#f9f9f9", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)

            sub = tk.Frame(row, bg="#f9f9f9")
            sub.pack(fill="x", padx=10, pady=5)

            tk.Label(sub, text="Mật khẩu:", bg="#f9f9f9").grid(row=0, column=0, sticky="w")
            mk_var = tk.StringVar(value=acc_data['matKhau'])
            tk.Entry(sub, textvariable=mk_var, width=20).grid(row=0, column=1, padx=5)

            tk.Label(sub, text="Vai trò:", bg="#f9f9f9").grid(row=0, column=2, padx=(15, 0))
            role_var = tk.StringVar(value=acc_data['vaiTro'])
            role_menu = ttk.Combobox(sub, textvariable=role_var, values=["admin", "employee"], state="readonly", width=15)
            role_menu.grid(row=0, column=3, padx=5)

            tk.Button(sub, text="Lưu", bg="blue", fg="white",
                      command=lambda user=acc_data['taiKhoan'], mv=mk_var, rv=role_var: update_account(user, mv, rv)).grid(row=0, column=4, padx=10)

    conn.close()
