# GUI_BANHANG.py - Giao diện bán hàng cải tiến
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import random

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_sale_tab(parent):
    for w in parent.winfo_children(): w.destroy()
    parent.config(bg="white")

    tk.Label(parent, text="Giao diện bán hàng", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=10)

    main_frame = tk.Frame(parent, bg="white")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)


    left_frame = tk.LabelFrame(main_frame, text="Danh sách sản phẩm", bg="white", padx=10, pady=10)
    left_frame.pack(side="left", fill="both", expand=True)

    product_tree = ttk.Treeview(left_frame, columns=("Mã", "Tên", "Giá", "Tồn"), show="headings", height=15)
    for col in ("Mã", "Tên", "Giá", "Tồn"):
        product_tree.heading(col, text=col)
        product_tree.column(col, width=100)
    product_tree.pack(fill="both", expand=True)

    def load_products():
        product_tree.delete(*product_tree.get_children())
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT maSanPham, tenSanPham, giaSanPham, tonKho FROM SANPHAM")
            for row in cur.fetchall():
                ma = row.maSanPham
                ten = row.tenSanPham
                gia = row.giaSanPham
                ton = int(row.tonKho) if row.tonKho is not None else 0
                product_tree.insert("", "end", values=(ma, ten, gia, ton))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # GIỎ HÀNG
    right_frame = tk.LabelFrame(main_frame, text="Giỏ hàng", bg="white", padx=10, pady=10)
    right_frame.pack(side="right", fill="both", expand=True)

    cart_tree = ttk.Treeview(right_frame, columns=("Mã", "Tên", "Giá", "SL", "Tổng"), show="headings", height=12)
    for col in ("Mã", "Tên", "Giá", "SL", "Tổng"):
        cart_tree.heading(col, text=col)
        cart_tree.column(col, width=90)
    cart_tree.pack(fill="both", expand=True)

    qty_frame = tk.Frame(right_frame, bg="white"); qty_frame.pack(pady=5)
    tk.Label(qty_frame, text="Số lượng:", bg="white").pack(side="left")
    qty_var = tk.IntVar(value=1)
    tk.Spinbox(qty_frame, from_=1, to=100, textvariable=qty_var, width=5).pack(side="left")

    cart = []

    def add_to_cart():
        selected = product_tree.focus()
        if not selected:
            return messagebox.showwarning("Chọn sản phẩm", "Vui lòng chọn sản phẩm để thêm")
        item = product_tree.item(selected)['values']
        ma, ten, gia, ton = item[:4]
        sl = qty_var.get()
        if sl > int(str(ton).replace(",", "")):
            return messagebox.showwarning("Tồn kho không đủ", f"Tồn kho chỉ còn {ton}")
        tong = int(str(gia).replace(",", "")) * sl
        cart.append((ma, ten, gia, sl, tong))
        cart_tree.insert("", "end", values=(ma, ten, gia, sl, tong))

    def clear_cart():
        cart.clear()
        cart_tree.delete(*cart_tree.get_children())

    # CHỌN KHÁCH HÀNG
    customer_frame = tk.Frame(right_frame, bg="white"); customer_frame.pack(pady=5)
    tk.Label(customer_frame, text="Khách hàng:", bg="white").pack(side="left")
    customer_cb = ttk.Combobox(customer_frame, state="readonly"); customer_cb.pack(side="left")

    def load_customers():
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT maKhachHang, tenKhachHang FROM KHACHHANG")
            result = cur.fetchall()
            customers = [f"{row[0]} - {row[1]}" for row in result]
            customer_cb['values'] = customers
            if customers: customer_cb.current(0)
            conn.close()
        except:
            pass

    load_customers()

    def thanh_toan():
        if not cart:
            return messagebox.showwarning("Trống", "Giỏ hàng đang trống")
        try:
            conn = get_connection(); cur = conn.cursor()
            total = sum(row[4] for row in cart)
            ma_khach = customer_cb.get().split(' - ')[0] if customer_cb.get() else None

            cur.execute("""
                SELECT TOP 1 T.maNhanVien
                FROM LICHSU_DANGNHAP L
                JOIN TAIKHOAN T ON L.taiKhoan = T.taiKhoan
                ORDER BY L.thoiGian DESC
            """)
            row = cur.fetchone()
            ma_nv = row[0] if row else None

            ma_hd = f"HD{random.randint(10000000, 99999999)}"
            cur.execute("INSERT INTO HOADON(maHoaDon, ngayLap, tongTien, maKhachHang, maNhanVien) VALUES(?, GETDATE(), ?, ?, ?)",
                        (ma_hd, total, ma_khach, ma_nv))

            for sp in cart:
                cur.execute("INSERT INTO CT_HOADON(maHoaDon, maSanPham, soLuong, thanhTien) VALUES (?, ?, ?, ?)",
                            (ma_hd, sp[0], sp[3], sp[4]))
                cur.execute("UPDATE SANPHAM SET tonKho = tonKho - ? WHERE maSanPham = ?", (sp[3], sp[0]))

            if ma_khach:
                cur.execute("UPDATE KHACHHANG SET soLanMua = soLanMua + 1 WHERE maKhachHang = ?", (ma_khach,))
            conn.commit(); conn.close()
            messagebox.showinfo("Thành công", "Đã thanh toán hoá đơn")
            clear_cart()
            load_products()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    btn_frame = tk.Frame(right_frame, bg="white"); btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="➕ Thêm vào giỏ", command=add_to_cart, bg="#198754", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🧹 Xoá giỏ", command=clear_cart, bg="#ffc107").pack(side="left", padx=5)
    tk.Button(btn_frame, text="💵 Thanh toán", command=thanh_toan, bg="#0d6efd", fg="white").pack(side="left", padx=5)

    load_products()
