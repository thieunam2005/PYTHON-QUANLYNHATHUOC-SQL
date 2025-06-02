import tkinter as tk
from tkinter import messagebox
import pyodbc
from datetime import datetime


def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )


def show_statistics_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    tk.Label(parent, text="THỐNG KÊ NỔI BẬT", font=("Arial", 16, "bold"), bg="white", fg = "black").pack(pady=10)

    container = tk.Frame(parent, bg="white")
    container.pack(padx=20, pady=10, fill="both", expand=True)

    def add_block(title, content):
        frame = tk.Frame(container, bg="#f0f0f0", bd=2, relief="groove")
        frame.pack(fill="x", padx=5, pady=8)
        tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg="#f0f0f0", anchor="w").pack(anchor="w", padx=10, pady=5)
        tk.Label(frame, text=content, font=("Arial", 10), bg="#f0f0f0", justify="left", wraplength=800).pack(anchor="w", padx=20, pady=5)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT TOP 1 maKhachHang, tenKhachHang, soLanMua FROM KHACHHANG ORDER BY soLanMua DESC")
        kh = cursor.fetchone()
        if kh:
            add_block("Khách hàng mua nhiều nhất:", f"Mã: {kh.maKhachHang} | Tên: {kh.tenKhachHang} | Số lần mua: {kh.soLanMua}")
        else:
            add_block("Khách hàng mua nhiều nhất:", "Không có dữ liệu")

        cursor.execute("""
            SELECT SP.maSanPham, SP.tenSanPham,
                   ISNULL(SUM(NH.soLuong), 0) AS nhap,
                   ISNULL(SUM(B.soLuong), 0) AS ban
            FROM SANPHAM SP
            LEFT JOIN CT_PHIEUNHAP NH ON SP.maSanPham = NH.maSanPham
            LEFT JOIN CT_HOADON B ON SP.maSanPham = B.maSanPham
            GROUP BY SP.maSanPham, SP.tenSanPham
            HAVING ISNULL(SUM(NH.soLuong), 0) - ISNULL(SUM(B.soLuong), 0) < 20
        """)
        sps = cursor.fetchall()
        if sps:
            sp_lines = [f"{sp.maSanPham} | {sp.tenSanPham} | Còn: {sp.nhap - sp.ban}" for sp in sps]
            add_block("Sản phẩm sắp hết hàng:", "\n".join(sp_lines))
        else:
            add_block("Sản phẩm sắp hết hàng:", "Không có sản phẩm nào sắp hết")

        cursor.execute("SELECT TOP 1 maHoaDon, ngayLap, tongTien FROM HOADON ORDER BY tongTien DESC")
        hd = cursor.fetchone()
        if hd:
            ngay = hd.ngayLap if isinstance(hd.ngayLap, str) else hd.ngayLap.strftime('%Y-%m-%d')
            add_block("Hóa đơn có tổng tiền lớn nhất:", f"Mã: {hd.maHoaDon} | Ngày: {ngay} | Tổng: {int(hd.tongTien):,}đ")
        else:
            add_block("Hóa đơn có tổng tiền lớn nhất:", "Không có dữ liệu")

        cursor.execute("SELECT TOP 1 maPhieuNhap, ngayNhap, tongTien FROM PHIEUNHAP ORDER BY tongTien DESC")
        pn = cursor.fetchone()
        if pn:
            ngay = pn.ngayNhap if isinstance(pn.ngayNhap, str) else pn.ngayNhap.strftime('%Y-%m-%d')
            add_block("Phiếu nhập có tổng tiền lớn nhất:", f"Mã: {pn.maPhieuNhap} | Ngày: {ngay} | Tổng: {int(pn.tongTien):,}đ")
        else:
            add_block("Phiếu nhập có tổng tiền lớn nhất:", "Không có dữ liệu")

        cursor.execute("""
            SELECT SP.maSanPham, SP.tenSanPham, MIN(CT.hanSD) AS hanSDGanNhat
            FROM SANPHAM SP
            JOIN CT_PHIEUNHAP CT ON SP.maSanPham = CT.maSanPham
            WHERE CT.hanSD BETWEEN GETDATE() AND DATEADD(MONTH, 3, GETDATE())
            GROUP BY SP.maSanPham, SP.tenSanPham
        """)
        hsd = cursor.fetchall()
        if hsd:
            sp_lines = [
                f"{row.maSanPham} | {row.tenSanPham} | HSD gần nhất: {row.hanSDGanNhat if isinstance(row.hanSDGanNhat, str) else row.hanSDGanNhat.strftime('%Y-%m-%d')}"
                for row in hsd
            ]
            add_block("Sản phẩm sắp hết hạn (trong 3 tháng):", "\n".join(sp_lines))
        else:
            add_block("Sản phẩm sắp hết hạn (trong 3 tháng):", "Không có sản phẩm nào sắp hết hạn")


        conn.close()

    except Exception as e:
        messagebox.showerror("Lỗi thống kê", str(e))
