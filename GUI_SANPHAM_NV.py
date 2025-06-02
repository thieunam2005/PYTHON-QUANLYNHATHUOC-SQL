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

def show_product_tab_nv(parent):
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




    btn_frame = tk.Frame(filter_frame, bg="white")
    btn_frame.pack(side="right")
    tk.Button(btn_frame, text="🔍 Xem", bg="#0d6efd", fg="white", command=show_view_form).pack(side="left", padx=5)

    apply_filter()
