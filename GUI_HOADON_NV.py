import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_invoice_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Quản lý hóa đơn", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 5))


    filter_frame = tk.Frame(frame, bg="white")
    filter_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(filter_frame, text="Khách hàng:", bg="white").pack(side="left")
    customer_var = tk.StringVar()
    customer_entry = ttk.Entry(filter_frame, textvariable=customer_var, width=20)
    customer_entry.pack(side="left", padx=5)

    tk.Label(filter_frame, text="Từ ngày (yyyy-mm-dd):", bg="white").pack(side="left")
    from_date_var = tk.StringVar()
    from_date_entry = ttk.Entry(filter_frame, textvariable=from_date_var, width=15)
    from_date_entry.pack(side="left", padx=5)

    tk.Label(filter_frame, text="Đến ngày:", bg="white").pack(side="left")
    to_date_var = tk.StringVar()
    to_date_entry = ttk.Entry(filter_frame, textvariable=to_date_var, width=15)
    to_date_entry.pack(side="left", padx=5)

    tk.Button(filter_frame, text="Lọc", command=lambda: render_table(customer_var.get(), from_date_var.get(), to_date_var.get())).pack(side="left", padx=10)

    canvas = tk.Canvas(frame, bg="white")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg="white")

    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_table(customer_filter="", from_date="", to_date=""):
        for widget in scrollable.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM HOADON WHERE 1=1"
        params = []

        if customer_filter:
            query += " AND maKhachHang LIKE ?"
            params.append(f"%{customer_filter}%")

        if from_date:
            query += " AND ngayLap >= ?"
            params.append(from_date)

        if to_date:
            query += " AND ngayLap <= ?"
            params.append(to_date)

        query += " ORDER BY ngayLap DESC"
        cursor.execute(query, params)
        invoices = cursor.fetchall()

        for invoice in invoices:
            ma = invoice.maHoaDon
            ngay_obj = invoice.ngayLap
            ngay = ngay_obj if isinstance(ngay_obj, str) else ngay_obj.strftime("%Y-%m-%d")
            kh = invoice.maKhachHang

  
            cursor.execute("SELECT hoTen FROM NHANVIEN WHERE maNhanVien=?", invoice.maNhanVien)
            nv_row = cursor.fetchone()
            ten_nv = nv_row.hoTen if nv_row else "Không rõ"

            if kh:
                cursor.execute("SELECT tenKhachHang, soLanMua FROM KHACHHANG WHERE maKhachHang=?", kh)
                row = cursor.fetchone()
                if row:
                    ten_kh, so_lan_mua = row
                else:
                    ten_kh = "Không rõ"
                    so_lan_mua = 0
            else:
                ten_kh = "Khách lẻ"
                so_lan_mua = 0

            cursor.execute("""
                SELECT s.tenSanPham, cth.soLuong, s.giaSanPham, cth.thanhTien
                FROM CT_HOADON cth
                JOIN SANPHAM s ON cth.maSanPham = s.maSanPham
                WHERE cth.maHoaDon = ?
            """, ma)
            chi_tiet = cursor.fetchall()

            tong_tien = sum(row.thanhTien for row in chi_tiet)
            so_sp = len(chi_tiet)

    
            row_frame = tk.Frame(scrollable, bg="#f9f9f9", bd=1, relief="solid", pady=5)
            row_frame.pack(fill="x", pady=5, padx=10)

            info = (
                f"Mã HĐ: {ma} | Ngày: {ngay} | "
                f"KH: {kh or '---'} - {ten_kh} | Nhân viên: {ten_nv} | "
                f"Số lần mua: {so_lan_mua} | Số SP: {so_sp} | Tổng: {int(tong_tien)}đ"
            )
            tk.Label(row_frame, text=info, font=("Arial", 10, "bold"), bg="#f9f9f9", anchor="w", justify="left").pack(anchor="w", padx=10, pady=(0, 5))

   
            tree = ttk.Treeview(row_frame, columns=("Tên sản phẩm", "Số lượng", "Giá", "Thành tiền"), show="headings")
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=150)
            for row in chi_tiet:
                tree.insert("", "end", values=(row.tenSanPham, row.soLuong, row.giaSanPham, row.thanhTien))
            tree.pack(fill="x", padx=10, pady=5)

        conn.close()

    render_table()
