import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_warehouse_tab(parent):
    for w in parent.winfo_children(): w.destroy()
    parent.config(bg="white")

    tk.Label(parent, text="Phiếu nhập chưa xác nhận", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    tree = ttk.Treeview(parent, columns=("Mã phiếu", "Ngày lập", "Nhà cung cấp", "Tổng tiền", "Trạng thái", "Người lập"), show="headings")
    for col in ("Mã phiếu", "Ngày lập", "Nhà cung cấp", "Tổng tiền", "Trạng thái", "Người lập"):
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    def load_data():
        tree.delete(*tree.get_children())
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""
                SELECT pn.maPhieuNhap, pn.ngayLap, ncc.tenNCC, pn.tongTien, pn.trangThai, nv.hoTen
                FROM PHIEUNHAP pn
                JOIN NHACUNGCAP ncc ON pn.maNCC = ncc.maNCC
                JOIN NHANVIEN nv ON pn.maNhanVien = nv.maNhanVien
                WHERE pn.trangThai = N'chưa xác nhận'
                ORDER BY pn.ngayLap DESC
            """)
            for row in cur.fetchall():
                tree.insert("", "end", values=tuple(str(col).strip("(),' ") for col in row))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def xac_nhan_phieu():
        selected = tree.focus()
        if not selected:
            return messagebox.showwarning("Chọn phiếu", "Vui lòng chọn một phiếu nhập để xác nhận")
        ma_pn = tree.item(selected)['values'][0]
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT maSanPham, soLuong FROM CT_PHIEUNHAP WHERE maPhieuNhap = ?", (ma_pn,))
            for ma_sp, so_luong in cur.fetchall():
                cur.execute("UPDATE SANPHAM SET tonKho = tonKho + ? WHERE maSanPham = ?", (so_luong, ma_sp))
            cur.execute("UPDATE PHIEUNHAP SET trangThai = N'đã xác nhận' WHERE maPhieuNhap = ?", (ma_pn,))
            conn.commit(); conn.close()
            messagebox.showinfo("Thành công", f"Phiếu {ma_pn} đã được xác nhận và cập nhật tồn kho.")
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    btn_frame = tk.Frame(parent, bg="white")
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="✅ Xác nhận phiếu", command=xac_nhan_phieu, bg="#198754", fg="white").pack()

    load_data()
