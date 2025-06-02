import tkinter as tk
from PIL import Image, ImageTk
from GUI_BANHANG import show_sale_tab
from GUI_SANPHAM_NV import show_product_tab_nv
from GUI_HOADON_NV import show_invoice_tab
from GUI_KHACHHANG import show_customer_tab
from GUI_LOGIN import main as login_main
from GUI_KHO import show_warehouse_tab

def show_frame_content(content_func):
    for widget in main_area.winfo_children():
        widget.destroy()
    content_func(main_area)

root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Giao diện Employee")
root.geometry("940x530")
root.configure(bg="white")


sidebar = tk.Frame(root, bg="#f7971e", width=500)
sidebar.pack(side="left", fill="y")

avatar_img = Image.open("profile-img/employee.png")
avatar_img = avatar_img.resize((60, 60))
avatar_photo = ImageTk.PhotoImage(avatar_img)
avatar_label = tk.Label(sidebar, image=avatar_photo, bg="white")
avatar_label.pack(pady=(20, 5))

tk.Label(sidebar, text="EMPLOYEE", bg="#f7971e", font=("Arial", 12, "bold")).pack()

menu_data = [
    ("Hóa đơn", "icon/bill.png"),
    ("Sản phẩm", "icon/product.png"),
    ("Bán hàng", "icon/cart.png"),
    ("Khách hàng", "icon/customer.png"),
    ("Kho", "icon/warehouse.png")
]

menu_icons = []
for text, icon_path in menu_data:
    icon = Image.open(icon_path).resize((30, 30))
    icon_tk = ImageTk.PhotoImage(icon)
    menu_icons.append(icon_tk)

    if text == "Bán hàng":
        cmd = lambda: show_frame_content(show_sale_tab)
    elif text == "Sản phẩm":
        cmd = lambda: show_frame_content(show_product_tab_nv)
    elif text == "Hóa đơn":
        cmd = lambda: show_frame_content(show_invoice_tab)
    elif text == "Khách hàng":
        cmd = lambda: show_frame_content(show_customer_tab)
    elif text == "Kho":
        cmd = lambda: show_frame_content(show_warehouse_tab)
    else:
        cmd = lambda: print(f"{text} chưa được gắn chức năng")

    btn = tk.Button(
        sidebar,
        text=text,
        image=icon_tk,
        compound="left",
        anchor="w",
        padx=10,
        font=("Arial", 11),
        bg="#f7971e",
        fg="black",
        bd=1,
        activebackground="#faaa3c",
        cursor="hand2",
        command=cmd
    )
    btn.pack(fill="x", pady=2)


logout_icon = Image.open("icon/logout.png").resize((20, 20))
logout_icon_tk = ImageTk.PhotoImage(logout_icon)
menu_icons.append(logout_icon_tk)

def logout():
    root.destroy()
    login_main()

logout_btn = tk.Button(
    sidebar,
    text="Đăng xuất",
    image=logout_icon_tk,
    compound="left",
    anchor="w",
    padx=10,
    font=("Arial", 11),
    bg="#f7971e",
    fg="black",
    bd=0,
    activebackground="#f7971e",
    cursor="hand2",
    command=logout
)
logout_btn.pack(side="bottom", pady=10, fill="x")


main_area = tk.Frame(root, bg="black")
main_area.pack(fill="both", expand=True)

center_frame = tk.Frame(main_area, bg="black")
center_frame.pack(expand=True)

logo_img = Image.open("img/logo.png")
logo_img = logo_img.resize((250, 100))
logo_photo = ImageTk.PhotoImage(logo_img)
tk.Label(center_frame, image=logo_photo, bg="black").pack(pady=(0, 10))

tk.Label(center_frame, text="-SẢN PHẨM CỦA NHÓM MẠNH NHẤT HUIT-", font=("Arial", 12), fg="#f7971e", bg="black").pack()

root.mainloop()
