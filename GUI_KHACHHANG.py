import tkinter as tk
from tkinter import messagebox
import pyodbc
import random

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_customer_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Danh sách khách hàng", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 0))

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

    def delete_customer(ma):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KHACHHANG WHERE maKhachHang = ?", ma)
        conn.commit()
        conn.close()
        show_customer_tab(parent)

    def open_edit_popup(cus):
        popup = tk.Toplevel()
        popup.title("Chỉnh sửa khách hàng")
        popup.geometry("300x250")

        ten_var = tk.StringVar(value=cus['tenKhachHang'])
        sdt_var = tk.StringVar(value=cus['soDienThoai'])
        slm_var = tk.StringVar(value=str(cus['soLanMua']))

        tk.Label(popup, text="Tên khách hàng:").pack()
        tk.Entry(popup, textvariable=ten_var).pack()

        tk.Label(popup, text="Số điện thoại:").pack()
        tk.Entry(popup, textvariable=sdt_var).pack()

        tk.Label(popup, text="Số lần mua hàng:").pack()
        tk.Entry(popup, textvariable=slm_var).pack()

        def save_edit():
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE KHACHHANG SET tenKhachHang = ?, soDienThoai = ?, soLanMua = ?
                    WHERE maKhachHang = ?
                """, (ten_var.get(), sdt_var.get(), int(slm_var.get()), cus['maKhachHang']))
                conn.commit()
                popup.destroy()
                show_customer_tab(parent)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
            finally:
                conn.close()

        tk.Button(popup, text="Lưu", bg="blue", fg="white", command=save_edit).pack(pady=10)

    def open_add_popup():
        popup = tk.Toplevel()
        popup.title("Thêm khách hàng")
        popup.geometry("300x250")

        ten_var = tk.StringVar()
        sdt_var = tk.StringVar()

        tk.Label(popup, text="Tên khách hàng:").pack()
        tk.Entry(popup, textvariable=ten_var).pack()

        tk.Label(popup, text="Số điện thoại:").pack()
        tk.Entry(popup, textvariable=sdt_var).pack()

        def save_add():
            try:
                conn = get_connection()
                cursor = conn.cursor()
                ma = "KH" + str(random.randint(10000, 99999))
                cursor.execute(
                "INSERT INTO KHACHHANG (maKhachHang, tenKhachHang, gioiTinh, soDienThoai, soLanMua) VALUES (?, ?, N'Nam', ?, 0)",
                (ma, ten_var.get(), sdt_var.get())
                )

                conn.commit()
                popup.destroy()
                show_customer_tab(parent)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
            finally:
                conn.close()

        tk.Button(popup, text="Thêm", bg="green", fg="white", command=save_add).pack(pady=10)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT maKhachHang, tenKhachHang, soDienThoai, soLanMua FROM KHACHHANG")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()

    for row_data in rows:
        cus = dict(zip(col_names, row_data))
        row = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
        row.pack(fill="x", pady=5)

        info = f"Tên: {cus['tenKhachHang']}\nMã: {cus['maKhachHang']}\nSĐT: {cus['soDienThoai']}\nSL mua: {cus['soLanMua']}"
        tk.Label(row, text=info, bg="#f9f9f9", justify="left", font=("Arial", 10)).pack(side="left", padx=10)

        tk.Button(row, text="Sửa", bg="blue", fg="white", command=lambda c=cus: open_edit_popup(c)).pack(side="right", padx=5)
        tk.Button(row, text="Xóa", bg="red", fg="white", command=lambda m=cus['maKhachHang']: delete_customer(m)).pack(side="right", padx=5)

    tk.Button(frame, text="Thêm khách hàng", bg="green", fg="white", font=("Arial", 10), command=open_add_popup).pack(pady=10)
