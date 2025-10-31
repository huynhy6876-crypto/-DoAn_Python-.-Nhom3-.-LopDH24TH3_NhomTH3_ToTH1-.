import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import random
import os

# ====================== KẾT NỐI MySQL ======================
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="QuanLyBanHang"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi CSDL", f"Không kết nối được: {err}")
        return None

# ====================== CĂN GIỮA CỬA SỔ ======================
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# ====================== FORM ĐĂNG NHẬP ======================
def create_login_window():
    global login_window, entry_user, entry_pass

    # === TẠO CỬA SỔ ===
    login_window = tk.Tk()
    login_window.title("Đăng Nhập - POS System")
    login_window.configure(bg="#ffffff")
    login_window.resizable(False, False)

    # === CĂN GIỮA TRƯỚC KHI THÊM WIDGET ===
    center_window(login_window, 500, 400)
    login_window.geometry("500x400")

    # === TIÊU ĐỀ ===
    tk.Label(
        login_window,
        text="ĐĂNG NHẬP",
        font=("Time New Roman", 28, "bold"),
        bg="#ffffff",
        fg="#2c3e50"
    ).pack(pady=(50, 25))

    # === FRAME CHỨA FORM (DÙNG PACK THUẦN) ===
    form_frame = tk.Frame(login_window, bg="#ffffff")
    form_frame.pack(pady=(0, 20))

    # --- Tên đăng nhập ---
    tk.Label(
        form_frame,
        text="Tên đăng nhập",
        font=("Time New Roman", 12),
        bg="#ffffff",
        fg="#34495e"
    ).pack(anchor="w", padx=80, pady=(0, 5))

    entry_user = tk.Entry(
        form_frame,
        font=("Time New Roman", 13),
        width=28,
        relief="solid",
        bd=1,
        highlightthickness=2,
        highlightcolor="#3498db"
    )
    entry_user.pack(pady=(0, 15), ipady=10, padx=80)
    entry_user.focus()

    # --- Mật khẩu ---
    tk.Label(
        form_frame,
        text="Mật khẩu",
        font=("Time New Roman", 12),
        bg="#ffffff",
        fg="#34495e"
    ).pack(anchor="w", padx=80, pady=(0, 5))

    entry_pass = tk.Entry(
        form_frame,
        font=("Time New Roman", 13),
        width=28,
        show="*",
        relief="solid",
        bd=1,
        highlightthickness=2,
        highlightcolor="#3498db"
    )
    entry_pass.pack(pady=(0, 35), ipady=10, padx=80)

    # === HÀM ĐĂNG NHẬP (ĐỊNH NGHĨA TRƯỚC) ===
    def check_login():
        username = entry_user.get().strip()
        password = entry_pass.get()

        if not username or not password:
            messagebox.showwarning("Thiếu", "Vui lòng nhập đầy đủ!")
            return

        if username == "NYCT" and password == "782823":
            messagebox.showinfo("Thành công", f"Chào {username}!")
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")

    # === NÚT ĐĂNG NHẬP (SAU KHI HÀM ĐÃ ĐƯỢC ĐỊNH NGHĨA) ===
    btn_login = tk.Button(
        login_window,
        text="ĐĂNG NHẬP",
        font=("Time New Roman", 14, "bold"),
        bg="#27ae60",
        fg="white",
        width=25,
        height=2,
        relief="flat",
        cursor="hand2",
        command=check_login
    )
    btn_login.pack(pady=10)

    # Hover effect
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#219653"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#27ae60"))

    # === HIỆU ỨNG FOCUS ===
    def focus_in(e, ent): ent.config(highlightcolor="#2980b9")
    def focus_out(e, ent): ent.config(highlightcolor="#3498db")
    for ent in (entry_user, entry_pass):
        ent.bind("<FocusIn>", lambda e, ent=ent: focus_in(e, ent))
        ent.bind("<FocusOut>", lambda e, ent=ent: focus_out(e, ent))

    # === ENTER = ĐĂNG NHẬP ===
    entry_pass.bind("<Return>", lambda e: check_login())
    entry_user.bind("<Return>", lambda e: entry_pass.focus())

    # === FOOTER ===
    tk.Label(
        login_window,
        text="© 2025 Hệ thống quản lý bán hàng",
        font=("Time New Roman", 9),
        bg="#ffffff",
        fg="#95a5a6"
    ).pack(side="bottom", pady=20)

    login_window.mainloop()
    


# ====================== FORM CHÍNH ======================
def open_main_window():
    main = tk.Tk()
    main.title("HỆ THỐNG QUẢN LÝ BÁN HÀNG")
    main.geometry("900x550")
    center_window(main, 900, 550)
    main.configure(bg="#f8f9fa")

    tk.Label(main, text="HỆ THỐNG QUẢN LÝ BÁN HÀNG", font=("Time New Roman", 24, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(pady=40)
    tk.Label(main, text="Chào mừng bạn đến với hệ thống POS!", font=("Time New Roman", 14), bg="#f8f9fa", fg="#34495e").pack(pady=10)

    btn_style = {"font": ("Time New Roman", 14, "bold"), "width": 30, "height": 2, "fg": "white"}

    tk.Button(main, text="BÁN HÀNG", bg="#27ae60", command=lambda: open_sales_window(main), **btn_style).pack(pady=15)
    tk.Button(main, text="QUẢN LÝ NHÂN VIÊN", bg="#3498db", command=lambda: open_crud_window(main, "NhanVien", ["ma_nv", "ten_nv", "gioitinh", "dia_chi", "sdt", "chuc_vu"], ["Mã NV", "Họ tên", "Giới tính", "Địa chỉ", "SĐT", "Chức vụ"]), **btn_style).pack(pady=10)
    tk.Button(main, text="QUẢN LÝ SẢN PHẨM", bg="#e67e22", command=lambda: open_crud_window(main, "SanPham", ["ma_sp", "ten_sp", "loai_sp", "mo_ta", "gia", "so_luong_ton"], ["Mã SP", "Tên SP", "Loại", "Mô tả", "Giá", "Tồn kho"]), **btn_style).pack(pady=10)
    tk.Button(main, text="QUẢN LÝ KHÁCH HÀNG", bg="#9b59b6", command=lambda: open_crud_window(main, "KhachHang", ["ma_kh", "ten_kh", "dia_chi_kh", "sdt_kh"], ["Mã KH", "Tên KH", "Địa chỉ", "SĐT"]), **btn_style).pack(pady=10)

    main.mainloop()

# ====================== CRUD CHUNG (NHÂN VIÊN, SẢN PHẨM, KHÁCH HÀNG) ======================
def open_crud_window(prev, table, cols, labels):
    prev.destroy()
    win = tk.Tk()
    win.title(f"QUẢN LÝ {table.upper()}")
    win.geometry("1100x700")
    center_window(win, 1100, 700)
    win.configure(bg="#f0f2f5")

    tk.Label(win, text=f"QUẢN LÝ {table.upper()}", font=("Time New Roman", 24, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=15)

    # Form nhập
    form = tk.LabelFrame(win, text=" THÔNG TIN ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    form.pack(pady=10, padx=20, fill="x")

    entries = {}
    for i, label in enumerate(labels):
        tk.Label(form, text=label + ":", bg="white").grid(row=i//2, column=(i%2)*2, padx=10, pady=8, sticky="w")
        if label == "Mã NV" or label == "Mã SP" or label == "Mã KH":
            e = tk.Entry(form, width=15, state="readonly")
        elif label == "Giới tính":
            var = tk.StringVar(value="Nam")
            tk.Radiobutton(form, text="Nam", variable=var, value="Nam", bg="white").grid(row=i//2, column=(i%2)*2+1, sticky="w")
            tk.Radiobutton(form, text="Nữ", variable=var, value="Nữ", bg="white").grid(row=i//2, column=(i%2)*2+1, padx=60, sticky="w")
            entries[label] = var
            continue
        elif label == "Chức vụ":
            e = ttk.Combobox(form, values=["Trưởng phòng", "Phó phòng", "Nhân viên", "Kế toán", "Lái xe"], state="readonly")
            e.set("Nhân viên")
        elif label == "Tồn kho":
            e = tk.Entry(form, width=15)
            e.insert(0, "0")
        else:
            e = tk.Entry(form, width=30 if "tên" in label.lower() or "địa chỉ" in label.lower() else 20)
        e.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=8)
        entries[label] = e

    # Bảng
    tree = ttk.Treeview(win, columns=cols, show="headings", height=15)
    for col in cols:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    def load_data():
        for i in tree.get_children(): tree.delete(i)
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table}")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

    def them():
        values = []
        for label in labels:
            if label in ["Mã NV", "Mã SP", "Mã KH"]: continue
            val = entries[label].get() if hasattr(entries[label], "get") else entries[label].get()
            values.append(val.strip() if isinstance(val, str) else val)
        if not values[0]: return messagebox.showwarning("Lỗi", "Nhập tên!")
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            placeholders = ",".join(["%s"] * len(values))
            cur.execute(f"INSERT INTO {table} ({','.join(cols[1:])}) VALUES ({placeholders})", values)
            conn.commit(); conn.close()
            load_data(); clear_form()

    def clear_form():
        for label, e in entries.items():
            if label not in ["Mã NV", "Mã SP", "Mã KH"]:
                if hasattr(e, "delete"): e.delete(0, tk.END)
                elif hasattr(e, "set"): e.set("Nam" if "Giới tính" in label else "Nhân viên" if "Chức vụ" in label else "0")

    btn_frame = tk.Frame(win, bg="#f0f2f5")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="THÊM", bg="#27ae60", fg="white", command=them, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="LÀM MỚI", bg="#95a5a6", fg="white", command=clear_form, width=15).pack(side="left", padx=10)
    tk.Button(btn_frame, text="QUAY LẠI", bg="#e74c3c", fg="white", command=lambda: [win.destroy(), open_main_window()], width=15).pack(side="right", padx=20)

    load_data()
    win.mainloop()

# ====================== BÁN HÀNG ======================
def open_sales_window(prev):
    prev.destroy()
    root = tk.Tk()
    root.title("BÁN HÀNG - POS")
    root.geometry("1350x750")
    center_window(root, 1350, 750)
    root.configure(bg="#f0f2f5")

    tk.Label(root, text="GIAO DIỆN BÁN HÀNG", font=("Time New Roman", 26, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=15)

    # Thông tin hóa đơn
    info_frame = tk.LabelFrame(root, text=" THÔNG TIN HÓA ĐƠN ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    info_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(info_frame, text="Mã HD:", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    ma_hd = f"HD{datetime.now().strftime('%Y%m%d')}{random.randint(100,999)}"
    tk.Label(info_frame, text=ma_hd, font=("Time New Roman", 12, "bold"), bg="white", fg="#e74c3c").grid(row=0, column=1, sticky="w")

    tk.Label(info_frame, text="Nhân viên:", bg="white").grid(row=0, column=2, padx=20, sticky="w")
    cbb_nv = ttk.Combobox(info_frame, width=30, state="readonly")
    cbb_nv.grid(row=0, column=3, padx=10)

    tk.Label(info_frame, text="Khách hàng:", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    cbb_kh = ttk.Combobox(info_frame, width=30, state="readonly")
    cbb_kh.grid(row=1, column=1, padx=10)

    def load_nvk():
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT ma_nv, ten_nv FROM NhanVien")
            cbb_nv['values'] = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
            cur.execute("SELECT ma_kh, ten_kh FROM KhachHang")
            cbb_kh['values'] = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
            if cbb_nv['values']: cbb_nv.current(0)
            if cbb_kh['values']: cbb_kh.current(0)
            conn.close()
    load_nvk()

    # Chọn sản phẩm
    sp_frame = tk.LabelFrame(root, text=" CHỌN SẢN PHẨM ", font=("Time New Roman", 14, "bold"), bg="white", bd=2)
    sp_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(sp_frame, text="Tên SP:", bg="white").grid(row=0, column=0, padx=10, pady=8)
    cbb_sp = ttk.Combobox(sp_frame, width=50, state="readonly")
    cbb_sp.grid(row=0, column=1, padx=10)

    tk.Label(sp_frame, text="SL:", bg="white").grid(row=0, column=2, padx=10)
    entry_sl = tk.Entry(sp_frame, width=8)
    entry_sl.grid(row=0, column=3, padx=10)
    entry_sl.insert(0, "1")

    def load_sp():
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT ma_sp, ten_sp, gia, so_luong_ton FROM SanPham WHERE so_luong_ton > 0")
            rows = cur.fetchall()
            cbb_sp['values'] = [f"{r[0]} - {r[1]} | Giá: {r[2]:,.0f} | Tồn: {r[3]}" for r in rows]
            conn.close()
    load_sp()

    # Bảng giỏ hàng
    cols = ("STT", "Tên SP", "SL", "Đơn giá", "Thành tiền")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
    for i, c in enumerate(cols):
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=100 if i==0 else 220)
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    total = 0
    cart = []

    def add_sp():
        nonlocal total
        sel = cbb_sp.current()
        if sel == -1: return messagebox.showwarning("Lỗi", "Chọn sản phẩm!")
        try:
            sl = int(entry_sl.get())
            if sl <= 0: raise ValueError
        except: return messagebox.showwarning("Lỗi", "Số lượng phải > 0!")

        sp = cbb_sp['values'][sel].split(" | ")
        ma_sp = int(sp[0].split(" - ")[0])
        ten_sp = sp[0].split(" - ", 1)[1]
        gia = float(sp[1].split(": ")[1].replace(",", ""))
        ton = int(sp[2].split(": ")[1])
        if sl > ton: return messagebox.showwarning("Lỗi", f"Chỉ còn {ton} sản phẩm!")

        sub = gia * sl
        total += sub
        cart.append({"ma_sp": ma_sp, "ten": ten_sp, "sl": sl, "gia": gia, "sub": sub})
        tree.insert("", "end", values=(len(cart), ten_sp, sl, f"{gia:,.0f}", f"{sub:,.0f}"))
        lbl_total.config(text=f"TỔNG TIỀN: {total:,.0f} VND")
        entry_sl.delete(0, tk.END); entry_sl.insert(0, "1"); load_sp()

    tk.Button(sp_frame, text="THÊM VÀO GIỎ", bg="#3498db", fg="white", command=add_sp).grid(row=0, column=4, padx=20)

    lbl_total = tk.Label(root, text="TỔNG TIỀN: 0 VND", font=("Time New Roman", 18, "bold"), bg="#f0f2f5", fg="#e74c3c")
    lbl_total.pack(pady=10)

    def pay():
        if not cart: return messagebox.showwarning("Rỗng", "Chưa có sản phẩm!")
        nv = cbb_nv.get().split(" - ")[0]
        kh = cbb_kh.get().split(" - ")[0]

        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO HoaDon (ma_kh, ma_nv, ngay_lap, tong_tien) VALUES (%s,%s,%s,%s)",
                        (kh, nv, datetime.now().date(), total))
            hd_id = cur.lastrowid
            for item in cart:
                cur.execute("INSERT INTO ChiTietHoaDon (ma_hd, ma_sp, so_luong, don_gia) VALUES (%s,%s,%s,%s)",
                            (hd_id, item["ma_sp"], item["sl"], item["gia"]))
                cur.execute("UPDATE SanPham SET so_luong_ton = so_luong_ton - %s WHERE ma_sp = %s",
                            (item["sl"], item["ma_sp"]))
            conn.commit(); conn.close()

        messagebox.showinfo("THÀNH CÔNG", f"Thanh toán {total:,.0f} VND\nMã HD: {ma_hd}")
        print_invoice(ma_hd, cart, total, cbb_nv.get(), cbb_kh.get())
        reset()

    def reset():
        nonlocal total, cart
        cart.clear(); tree.delete(*tree.get_children())
        total = 0; lbl_total.config(text="TỔNG TIỀN: 0 VND")
        load_sp()

    def print_invoice(ma_hd, items, tot, nv, kh):
        fn = f"HOADON_{ma_hd}.txt"
        with open(fn, "w", encoding="utf-8") as f:
            f.write("═" * 65 + "\n")
            f.write("           HÓA ĐƠN BÁN HÀNG and\n")
            f.write("═" * 65 + "\n")
            f.write(f"Mã HD: {ma_hd} | {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Nhân viên: {nv} | Khách hàng: {kh}\n")
            f.write("─" * 65 + "\n")
            f.write(f"{'STT':<4} {'Tên SP':<30} {'SL':>4} {'Giá':>12} {'Thành tiền':>12}\n")
            f.write("─" * 65 + "\n")
            for i, it in enumerate(items, 1):
                f.write(f"{i:<4} {it['ten']:<30} {it['sl']:>4} {it['gia']:>12,.0f} {it['sub']:>12,.0f}\n")
            f.write("─" * 65 + "\n")
            f.write(f"{'TỔNG TIỀN':>51} {tot:>12,.0f} VND\n")
            f.write("═" * 65 + "\n")
            f.write("           CẢM ƠN QUÝ KHÁCH!\n")
        if os.name == 'nt':
            os.startfile(fn, "print")

    btn_f = tk.Frame(root, bg="#f0f2f5")
    btn_f.pack(pady=20)
    tk.Button(btn_f, text="THANH TOÁN & IN", font=("Time New Roman", 14, "bold"), bg="#27ae60", fg="white", width=22, height=2, command=pay).pack(side="right", padx=40)
    tk.Button(btn_f, text="LÀM MỚI", bg="#95a5a6", fg="white", command=reset, width=15).pack(side="left", padx=20)
    tk.Button(btn_f, text="QUAY LẠI", bg="#e74c3c", fg="white", command=lambda: [root.destroy(), open_main_window()], width=15).pack(side="left", padx=20)

    root.mainloop()

# ====================== CHẠY CHƯƠNG TRÌNH ======================
if __name__ == "__main__":
    create_login_window()