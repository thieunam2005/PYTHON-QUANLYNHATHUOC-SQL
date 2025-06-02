# GUI_PHIEUNHAP.py - Quản lý phiếu nhập thuốc
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
import uuid

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;")

def get_logged_in_employee():
    try:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            SELECT TOP 1 NV.maNhanVien FROM LICHSU_DANGNHAP L
            JOIN TAIKHOAN T ON L.taiKhoan = T.taiKhoan
            JOIN NHANVIEN NV ON T.maNhanVien = NV.maNhanVien
            ORDER BY L.thoiGian DESC
        """)
        row = cur.fetchone()
        return row.maNhanVien if row else None
    except:
        return None

def show_receipt_tab(parent):
    for widget in parent.winfo_children(): widget.destroy()

    frame = tk.Frame(parent, bg="white")
    frame.pack(fill="both", expand=True)

    left = tk.Frame(frame, bg="white")
    left.pack(side="left", fill="both", expand=True)
    right = tk.Frame(frame, bg="white", width=400)
    right.pack(side="right", fill="y")

    tk.Label(left, text="DANH SÁCH PHIẾU NHẬP", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    filter_frame = tk.Frame(left, bg="white")
    filter_frame.pack(pady=5)
    tk.Label(filter_frame, text="Từ:", bg="white").grid(row=0, column=0)
    tk.Label(filter_frame, text="Đến:", bg="white").grid(row=0, column=2)
    date_from = tk.Entry(filter_frame); date_from.grid(row=0, column=1)
    date_to = tk.Entry(filter_frame); date_to.grid(row=0, column=3)
    nv_filter = tk.StringVar(); cb_nv_filter = ttk.Combobox(filter_frame, textvariable=nv_filter, width=20)
    cb_nv_filter.grid(row=0, column=4, padx=5)
    tk.Button(filter_frame, text="Lọc", command=lambda: render(date_from.get(), date_to.get(), nv_filter.get())).grid(row=0, column=5)

    list_frame = tk.Frame(left, bg="white")
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)


    form = tk.LabelFrame(right, text="Tạo phiếu nhập", font=("Arial", 12), bg="white")
    form.pack(fill="both", expand=True, padx=10, pady=10)

    maPhieu = tk.StringVar(value=f"PN{str(uuid.uuid4())[:8]}")
    ngayLap = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    ngayNhap = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    maNCC = tk.StringVar()
    maNV = get_logged_in_employee()

    sp_chon = tk.StringVar()
    so_luong = tk.StringVar()
    don_gia = tk.StringVar()
    han_sd = tk.StringVar()
    sp_list = []

    tk.Label(form, text="Mã phiếu:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=maPhieu, state="readonly").pack(fill="x")
    tk.Label(form, text="Ngày lập:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=ngayLap).pack(fill="x")
    tk.Label(form, text="Ngày nhập:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=ngayNhap).pack(fill="x")
    cb_ncc = ttk.Combobox(form, textvariable=maNCC)
    tk.Label(form, text="Nhà cung cấp:", bg="white").pack(anchor="w")
    cb_ncc.pack(fill="x")

    ttk.Separator(form, orient="horizontal").pack(fill="x", pady=5)
    tk.Label(form, text="Thêm sản phẩm:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
    cb_sp = ttk.Combobox(form, textvariable=sp_chon)
    cb_sp.pack(fill="x")
    tk.Label(form, text="Số lượng:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=so_luong, width=10).pack(fill="x", padx=5, pady=2)
    tk.Label(form, text="Đơn giá:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=don_gia, width=10).pack(fill="x", padx=5, pady=2)
    tk.Label(form, text="Hạn SD:", bg="white").pack(anchor="w")
    tk.Entry(form, textvariable=han_sd, width=10).pack(fill="x", padx=5, pady=2)

    tree = ttk.Treeview(form, columns=("Mã", "Tên", "SL", "Giá", "HSD"), show="headings", height=4)
    for col in ("Mã", "Tên", "SL", "Giá", "HSD"):
        tree.heading(col, text=col)
        tree.column(col, width=80)
    tree.pack(pady=5)

    def add_sanpham():
        try:
            m, t = sp_chon.get().split(" - ", 1)
            sl = int(so_luong.get())
            gia = int(don_gia.get())
            hsd = han_sd.get()
            hsd_date = datetime.strptime(hsd, "%Y-%m-%d")
            if hsd_date <= datetime.now():
                messagebox.showwarning("Hạn sử dụng không hợp lệ", "Hạn sử dụng phải sau ngày hiện tại")
                return
            sp_list.append((m, t, sl, gia, hsd))
            tree.insert("", "end", values=(m, t, sl, gia, hsd))
            sp_chon.set(""); so_luong.set(""); don_gia.set(""); han_sd.set("")
        except:
            messagebox.showerror("Lỗi", "Thông tin sản phẩm không hợp lệ")

    def load_combobox():
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT maNCC, tenNCC FROM NHACUNGCAP")
        cb_ncc["values"] = [f"{m} - {t}" for m, t in cur.fetchall()]
        cur.execute("SELECT maSanPham, tenSanPham FROM SANPHAM")
        cb_sp["values"] = [f"{m} - {t}" for m, t in cur.fetchall()]
        cur.execute("SELECT maNhanVien FROM NHANVIEN")
        cb_nv_filter["values"] = [""] + [m for m, in cur.fetchall()]
        conn.close()

    def create_phieu():
        if not sp_list:
            return messagebox.showwarning("Thiếu sản phẩm", "Vui lòng thêm ít nhất một sản phẩm")
        try:
            tong = sum(sl * gia for _, _, sl, gia, _ in sp_list)
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""
                INSERT INTO PHIEUNHAP (maPhieuNhap, ngayLap, ngayNhap, tongTien, maNCC, maNhanVien, trangThai)
                VALUES (?, ?, ?, ?, ?, ?, N'chưa xác nhận')
            """, (maPhieu.get(), ngayLap.get(), ngayNhap.get(), tong, maNCC.get().split(" - ")[0], maNV))
            for m, _, sl, gia, hsd in sp_list:
                cur.execute("INSERT INTO CT_PHIEUNHAP VALUES (?, ?, ?, ?, ?)", (maPhieu.get(), m, sl, gia, hsd))
            conn.commit(); conn.close()
            messagebox.showinfo("Thành công", "Đã lưu phiếu nhập")
            render(); reset()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def reset():
        maPhieu.set(f"PN{str(uuid.uuid4())[:8]}")
        ngayLap.set(datetime.now().strftime("%Y-%m-%d"))
        ngayNhap.set(datetime.now().strftime("%Y-%m-%d"))
        maNCC.set(""); sp_chon.set("")
        so_luong.set(""); don_gia.set(""); han_sd.set("")
        sp_list.clear(); tree.delete(*tree.get_children())

    tk.Button(form, text="Thêm sản phẩm", command=add_sanpham, bg="#2196f3", fg="white").pack(fill="x")
    tk.Button(form, text="Tạo phiếu nhập", command=create_phieu, bg="#4caf50", fg="white").pack(pady=5, fill="x")
    tk.Button(form, text="Làm mới", command=reset).pack(pady=5, fill="x")

    def render(date_from_val="", date_to_val="", nv_ma=""):
        for w in list_frame.winfo_children(): w.destroy()
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            SELECT PN.maPhieuNhap, ngayLap, ngayNhap, tongTien, NV.hoTen, NCC.tenNCC, PN.trangThai
            FROM PHIEUNHAP PN
            JOIN NHANVIEN NV ON PN.maNhanVien = NV.maNhanVien
            JOIN NHACUNGCAP NCC ON PN.maNCC = NCC.maNCC
            WHERE (? = '' OR ngayLap >= ?) AND (? = '' OR ngayLap <= ?) AND (? = '' OR PN.maNhanVien = ?)
            ORDER BY ngayLap DESC
        """, date_from_val, date_from_val, date_to_val, date_to_val, nv_ma, nv_ma)
        rows = cur.fetchall()
        for ma, lap, nhap, tong, nv, ncc, trangThai in rows:
            box = tk.LabelFrame(list_frame, text=f"{ma} | {lap} - {nhap} | {ncc} | {nv} | Trạng thái: {trangThai} | Tổng: {tong:,}đ", bg="white")
            box.pack(fill="x", padx=5, pady=3)
            tv = ttk.Treeview(box, columns=("Mã", "Tên", "Số lượng", "Đơn giá", "Hạn SD"), show="headings", height=3)
            for c in tv["columns"]:
                tv.heading(c, text=c); tv.column(c, width=90, anchor="center")
            tv.pack(fill="x")
            cur2 = conn.cursor()
            cur2.execute("""
                SELECT CT.maSanPham, tenSanPham, soLuong, donGia, hanSD
                FROM CT_PHIEUNHAP CT JOIN SANPHAM SP ON CT.maSanPham = SP.maSanPham
                WHERE maPhieuNhap = ?
            """, ma)
            for ct in cur2.fetchall():
                ma, ten, sl, gia, hsd = ct
                tv.insert("", "end", values=(str(ma).strip(), str(ten).strip(), str(sl), f"{gia:,}đ", hsd.strftime('%Y-%m-%d') if hasattr(hsd, 'strftime') else str(hsd)))
        conn.close()

    load_combobox()
    render()
