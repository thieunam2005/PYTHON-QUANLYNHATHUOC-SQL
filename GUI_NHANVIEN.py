import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_employee_tab(parent):
    for widget in parent.winfo_children(): widget.destroy()
    parent.config(bg="white")

    tk.Label(parent, text="Quản lý nhân viên", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    columns = ("Mã", "Họ tên", "Giới tính", "Ngày sinh", "SĐT", "Địa chỉ")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load():
        tree.delete(*tree.get_children())
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT * FROM NHANVIEN")
            for row in cur.fetchall():
                tree.insert("", "end", values=tuple(str(col).strip("(),' ") for col in row))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def add():
        top = tk.Toplevel(); top.title("Thêm nhân viên"); top.geometry("300x350")
        fields = ["Mã", "Họ tên", "Giới tính", "Ngày sinh", "SĐT", "Địa chỉ"]
        vars = []
        for f in fields:
            tk.Label(top, text=f).pack(); v = tk.StringVar(); vars.append(v); tk.Entry(top, textvariable=v).pack()
        def save():
            vals = [v.get().strip() for v in vars]
            if not all(vals): return messagebox.showwarning("Thiếu", "Nhập đầy đủ thông tin")
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("INSERT INTO NHANVIEN VALUES (?, ?, ?, ?, ?, ?)", vals)
                cur.execute("INSERT INTO TAIKHOAN VALUES (?, '12345', N'employee', ?)", (vals[0], vals[0]))
                conn.commit(); conn.close()
                top.destroy(); load()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        tk.Button(top, text="Lưu", bg="green", fg="white", command=save).pack(pady=10)

    def delete():
        selected = tree.focus()
        if not selected: return messagebox.showwarning("Chọn", "Chọn dòng cần xóa")
        ma = tree.item(selected)['values'][0]
        if messagebox.askyesno("Xóa", f"Xóa nhân viên {ma}?"):
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("DELETE FROM TAIKHOAN WHERE maNhanVien=?", (ma,))
                cur.execute("DELETE FROM NHANVIEN WHERE maNhanVien=?", (ma,))
                conn.commit(); conn.close(); load()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def edit():
        selected = tree.focus()
        if not selected: return messagebox.showwarning("Chọn", "Chọn dòng để sửa")
        data = tree.item(selected)['values']
        top = tk.Toplevel(); top.title("Sửa nhân viên"); top.geometry("300x350")
        fields = ["Mã", "Họ tên", "Giới tính", "Ngày sinh", "SĐT", "Địa chỉ"]
        vars = []
        for i, f in enumerate(fields):
            tk.Label(top, text=f).pack(); v = tk.StringVar(value=data[i]); vars.append(v); tk.Entry(top, textvariable=v).pack()
        def update():
            vals = [v.get().strip() for v in vars]
            if not all(vals): return messagebox.showwarning("Thiếu", "Nhập đầy đủ thông tin")
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("""
                    UPDATE NHANVIEN SET hoTen=?, gioiTinh=?, ngaySinh=?, soDienThoai=?, diaChi=? WHERE maNhanVien=?
                """, (vals[1], vals[2], vals[3], vals[4], vals[5], vals[0]))
                conn.commit(); conn.close(); top.destroy(); load()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        tk.Button(top, text="Cập nhật", bg="#0d6efd", fg="white", command=update).pack(pady=10)

    btn_frame = tk.Frame(parent, bg="white")
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="➕ Thêm", command=add, bg="#198754", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", command=edit, bg="#ffc107").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xóa", command=delete, bg="#dc3545", fg="white").pack(side="left", padx=5)

    load()
