-- Tạo csdl
CREATE DATABASE IF NOT EXISTS QuanLyBanHang
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE QuanLyBanHang;

-- Tạo bảng nhân viên
CREATE TABLE IF NOT EXISTS NhanVien (
	ma_nv INT AUTO_INCREMENT PRIMARY KEY,
    ten_nv VARCHAR(100) NOT NULL,
    gioitinh VARCHAR(10),
    dia_chi VARCHAR(255),
    sdt VARCHAR(20),
    chuc_vu VARCHAR(50)
);

-- Tạo bảng sản phẩm
CREATE TABLE IF NOT EXISTS SanPham (
	ma_sp INT AUTO_INCREMENT PRIMARY KEY,
    ten_sp VARCHAR(150) NOT NULL,
	loai_sp VARCHAR(50),
    mo_ta TEXT,
    gia DECIMAL(13,2) NOT NULL,
    so_luong_ton INT DEFAULT 0
);

-- Tạo bảng khách hàng
CREATE TABLE IF NOT EXISTS KhachHang (
    ma_kh INT AUTO_INCREMENT PRIMARY KEY,
    ten_kh VARCHAR(100) NOT NULL,
    dia_chi_kh VARCHAR(255),
    sdt_kh VARCHAR(20)
);

-- Tạo bảng hóa đơn
CREATE TABLE IF NOT EXISTS HoaDon (
    ma_hd INT AUTO_INCREMENT PRIMARY KEY,
    ma_kh INT,
    ma_nv INT,
    ngay_lap DATE NOT NULL,
    tong_tien DECIMAL(12,2) DEFAULT 0,
    FOREIGN KEY (ma_kh) REFERENCES KhachHang(ma_kh),
    FOREIGN KEY (ma_nv) REFERENCES NhanVien(ma_nv)
);

-- Tạo bảng chi tiết hóa đơn
CREATE TABLE IF NOT EXISTS ChiTietHoaDon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_hd INT,
    ma_sp INT,
    so_luong INT NOT NULL,
    don_gia DECIMAL(12,2) NOT NULL,
    thanhtien DECIMAL(12,2) GENERATED ALWAYS AS (so_luong * don_gia) STORED,
    FOREIGN KEY (ma_hd) REFERENCES HoaDon(ma_hd),
    FOREIGN KEY (ma_sp) REFERENCES SanPham(ma_sp)
);

-- Dữ liệu mẫu
INSERT INTO NhanVien (ten_nv, gioitinh, dia_chi, sdt, chuc_vu) VALUES
('Nguyễn Văn A', 'Nam', 'Hà Nội', '0905123456', 'Nhân viên bán hàng'),
('Trần Thị B', 'Nữ', 'TP.HCM', '0912345678', 'Kế toán'),
('Lê Văn C', 'Nam', 'Đà Nẵng', '0934567890', 'Quản lý');

INSERT INTO SanPham (ten_sp, loai_sp, mo_ta, gia, so_luong_ton) VALUES
('Điện thoại iPhone 15', 'Điện thoại', 'Hàng chính hãng Apple, bảo hành 12 tháng', 25000000, 10),
('Tai nghe Bluetooth', 'Phụ kiện', 'Kết nối không dây, pin 8 giờ', 550000, 50),
('Laptop Dell Inspiron', 'Laptop', 'Core i5, RAM 8GB, SSD 512GB', 18000000, 5),
('Sạc nhanh 20W', 'Phụ kiện', 'Sạc nhanh chuẩn PD cho iPhone', 250000, 100);

INSERT INTO KhachHang (ten_kh, dia_chi_kh, sdt_kh) VALUES
('Phạm Minh Tâm', 'Hải Phòng', '0988123123'),
('Nguyễn Thu Trang', 'Cần Thơ', '0977456789'),
('Lưu Đức Mạnh', 'Đà Nẵng', '0909888777');

INSERT INTO HoaDon (ma_kh, ma_nv, ngay_lap, tong_tien) VALUES
(1, 1, '2025-10-28', 25550000),
(2, 2, '2025-10-29', 18000000),
(3, 1, '2025-10-29', 30500000);

INSERT INTO ChiTietHoaDon (ma_hd, ma_sp, so_luong, don_gia) VALUES
(1, 1, 1, 25000000),  -- iPhone 15
(1, 2, 1, 550000),    -- Tai nghe
(2, 3, 1, 18000000),  -- Laptop Dell
(3, 1, 1, 25000000),  -- iPhone 15
(3, 4, 2, 250000);    -- 2 Sạc nhanh


SELECT * FROM NhanVien;
SELECT * FROM SanPham;
SELECT * FROM KhachHang;
SELECT * FROM HoaDon;
SELECT * FROM ChiTietHoaDon;