import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=DATABASE_QLTHUOC;"
        "Trusted_Connection=yes;"
    )

def show_product_tab(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    parent.config(bg="white")
    tk.Label(parent, text="Quản lý sản phẩm", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    filter_frame = tk.Frame(parent, bg="white")
    filter_frame.pack(fill="x", padx=20, pady=5)

    tk.Label(filter_frame, text="Tìm kiếm:", bg="white").pack(side="left")
    search_entry = tk.Entry(filter_frame)
    search_entry.pack(side="left", padx=5)

    filter_category = ttk.Combobox(filter_frame, values=["Tất cả", "Kê toa", "Không kê toa"], state="readonly")
    filter_category.current(0)
    filter_category.pack(side="left", padx=5)

    product_list = ttk.Treeview(parent, columns=("Mã", "Tên", "Giá", "Kê toa"), show="headings")
    for col, text in zip(("Mã", "Tên", "Giá", "Kê toa"), ("Mã SP", "Tên SP", "Giá", "Kê toa")):
        product_list.heading(col, text=text)
        product_list.column(col, width=100)
    product_list.pack(fill="both", expand=True, padx=20, pady=10)

    def apply_filter():
        keyword = search_entry.get().lower()
        require_prescription = filter_category.get()
        for item in product_list.get_children():
            product_list.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT maSanPham, tenSanPham, giaSanPham, thuocCanKeToa FROM SANPHAM"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                if keyword in row.tenSanPham.lower():
                    if require_prescription == "Tất cả" or \
                       (require_prescription == "Kê toa" and row.thuocCanKeToa == 'Có') or \
                       (require_prescription == "Không kê toa" and row.thuocCanKeToa == 'Không'):
                        product_list.insert("", "end", values=(row.maSanPham, row.tenSanPham, row.giaSanPham, row.thuocCanKeToa))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def show_add_form():
        def save():
            try:
                msp, tsp, gsp, dmuc, ktoa = entry_ma.get(), entry_ten.get(), int(entry_gia.get()), entry_dmuc.get(), cb_ketoa.get()
                if not msp.startswith("SP"):
                    raise ValueError("Mã sản phẩm phải bắt đầu bằng 'SP'")
                if not all([msp, tsp, dmuc, ktoa]):
                    raise ValueError("Thiếu thông tin")
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO SANPHAM(maSanPham, tenSanPham, giaSanPham, thuocCanKeToa, danhMuc, tonKho)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (msp, tsp, gsp, ktoa, dmuc, 0)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã thêm sản phẩm")
                top.destroy()
                apply_filter()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        top = Toplevel()
        top.title("Thêm sản phẩm")
        top.geometry("300x300")
        entry_ma = tk.Entry(top)
        entry_ten = tk.Entry(top)
        entry_gia = tk.Entry(top)
        entry_dmuc = tk.Entry(top)
        cb_ketoa = ttk.Combobox(top, values=["Có", "Không"], state="readonly")

        for text, widget in zip(("Mã SP", "Tên SP", "Giá", "Danh mục", "Kê toa"), (entry_ma, entry_ten, entry_gia, entry_dmuc, cb_ketoa)):
            tk.Label(top, text=text).pack()
            widget.pack(fill="x", padx=10, pady=3)

        tk.Button(top, text="Lưu", command=save, bg="#4caf50", fg="white").pack(pady=10)

    def show_edit_form():
        selected = product_list.focus()
        if not selected:
            messagebox.showwarning("Chọn sản phẩm", "Vui lòng chọn sản phẩm để sửa")
            return
        values = product_list.item(selected)['values']
        msp = values[0]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM SANPHAM WHERE maSanPham=?", (msp,))
            row = cur.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            return

        top = Toplevel()
        top.title("Sửa sản phẩm")
        top.geometry("400x750")
        tk.Label(top, text="Mã SP").pack()
        entry_ma = tk.Entry(top)
        entry_ma.insert(0, row.maSanPham)
        entry_ma.config(state="readonly")
        entry_ma.pack(fill="x", padx=10, pady=2)

        fields = []
        labels_fields = [
            ("Tên SP", row.tenSanPham), ("Giá", row.giaSanPham), ("Danh mục", row.danhMuc),
            ("Dạng bào chế", row.dangBaoChe), ("Quy cách", row.quyCach), ("Thành phần", row.thanhPhan),
            ("Chỉ định", row.chiDinh), ("Chống chỉ định", row.chongChiDinh), ("Nhà SX", row.nhaSanXuat),
            ("Nước SX", row.nuocSanXuat), ("Xuất xứ", row.xuatXu), ("Kê toa", row.thuocCanKeToa),
            ("Mô tả", row.moTa), ("Đối tượng SD", row.doiTuongSuDung), ("Lưu ý", row.luuY)
        ]

        for label, val in labels_fields:
            tk.Label(top, text=label).pack()
            ent = tk.Entry(top)
            ent.insert(0, str(val) if val is not None else "")
            ent.pack(fill="x", padx=10, pady=2)
            fields.append(ent)

        def update():
            try:
                data = [f.get() for f in fields]
                data[1] = int(data[1])
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE SANPHAM SET
                        tenSanPham=?, giaSanPham=?, danhMuc=?, dangBaoChe=?, quyCach=?, thanhPhan=?,
                        chiDinh=?, chongChiDinh=?, nhaSanXuat=?, nuocSanXuat=?, xuatXu=?, thuocCanKeToa=?,
                        moTa=?, doiTuongSuDung=?, luuY=?
                    WHERE maSanPham=?""", (*data, msp))
                conn.commit()
                conn.close()
                top.destroy()
                apply_filter()
                messagebox.showinfo("Cập nhật", "Đã cập nhật sản phẩm.")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        tk.Button(top, text="Cập nhật", command=update, bg="#ffc107", fg="black").pack(pady=10)

    def show_view_form():
        selected = product_list.focus()
        if not selected:
            messagebox.showwarning("Chọn sản phẩm", "Vui lòng chọn sản phẩm để xem chi tiết")
            return
        values = product_list.item(selected)['values']
        msp = values[0]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM SANPHAM WHERE maSanPham=?", (msp,))
            row = cur.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            return

        top = Toplevel()
        top.title(f"Chi tiết sản phẩm {msp}")
        top.geometry("420x500")
        top.resizable(False, False)

        canvas = tk.Canvas(top)
        scrollbar = ttk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        fields = [
            ("Mã SP", row.maSanPham), ("Tên SP", row.tenSanPham), ("Giá", row.giaSanPham),
            ("Danh mục", row.danhMuc), ("Dạng bào chế", row.dangBaoChe), ("Quy cách", row.quyCach),
            ("Thành phần", row.thanhPhan), ("Chỉ định", row.chiDinh), ("Chống chỉ định", row.chongChiDinh),
            ("Nhà SX", row.nhaSanXuat), ("Nước SX", row.nuocSanXuat), ("Xuất xứ", row.xuatXu),
            ("Thuốc kê toa", row.thuocCanKeToa), ("Mô tả", row.moTa),
            ("Đối tượng sử dụng", row.doiTuongSuDung), ("Lưu ý", row.luuY),
            ("Tồn kho", row.tonKho)
        ]

        for label, val in fields:
            tk.Label(scroll_frame, text=label + ":", font=("Arial", 10, "bold"), anchor="w").pack(anchor="w", padx=10, pady=(8, 0))
            tk.Label(scroll_frame, text=str(val) if val is not None else "(trống)", anchor="w", bg="white", wraplength=380, justify="left").pack(fill="x", padx=10)


    def show_delete_form():
        selected = product_list.focus()
        if not selected:
            messagebox.showwarning("Chọn sản phẩm", "Vui lòng chọn sản phẩm để xoá")
            return
        ma = product_list.item(selected)['values'][0]
        if not messagebox.askyesno("Xoá", f"Xoá sản phẩm {ma}?"):
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM SANPHAM WHERE maSanPham=?", (ma,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Xoá", f"Đã xoá sản phẩm {ma}")
            apply_filter()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    btn_frame = tk.Frame(filter_frame, bg="white")
    btn_frame.pack(side="right")
    tk.Button(btn_frame, text="➕ Thêm", bg="#28a745", fg="white", command=show_add_form).pack(side="left", padx=5)
    tk.Button(btn_frame, text="✏️ Sửa", bg="#ffc107", fg="black", command=show_edit_form).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Xoá", bg="#dc3545", fg="white", command=show_delete_form).pack(side="left", padx=5)
    tk.Button(btn_frame, text="🔍 Xem", bg="#0d6efd", fg="white", command=show_view_form).pack(side="left", padx=5)

    apply_filter()
