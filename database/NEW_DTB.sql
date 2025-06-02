CREATE DATABASE DATABASE_QLTHUOC
USE DATABASE_QLTHUOC

CREATE TABLE NHANVIEN (
    maNhanVien VARCHAR(10) NOT NULL PRIMARY KEY,
    hoTen NVARCHAR(100) NOT NULL,
    gioiTinh NVARCHAR(10) NOT NULL,
    ngaySinh DATE NOT NULL,
    soDienThoai VARCHAR(20) NOT NULL,
    diaChi NVARCHAR(255) NOT NULL,
	CONSTRAINT CHK_GioiTinh CHECK (gioiTinh IN (N'Nam', N'Nữ'))
);

CREATE TABLE NHACUNGCAP (
    maNCC VARCHAR(10) NOT NULL PRIMARY KEY,
    tenNCC NVARCHAR(100) NOT NULL,
    diaChi NVARCHAR(255),
    soDienThoai VARCHAR(20)
);

CREATE TABLE SANPHAM (
    maSanPham VARCHAR(10) NOT NULL PRIMARY KEY,
    tenSanPham NVARCHAR(255) NOT NULL,
    giaSanPham INT NOT NULL,
    danhMuc NVARCHAR(100) NOT NULL,
    dangBaoChe NVARCHAR(100),
    quyCach NVARCHAR(100),
    thanhPhan NVARCHAR(255),
    chiDinh NVARCHAR(255),
    chongChiDinh NVARCHAR(255),
    nhaSanXuat NVARCHAR(255),
    nuocSanXuat NVARCHAR(100),
    xuatXu NVARCHAR(100),
    thuocCanKeToa NVARCHAR(10) NOT NULL,
    moTa NVARCHAR(MAX),
    doiTuongSuDung NVARCHAR(100),
    luuY NVARCHAR(255),
	tonKho INT
);


CREATE TABLE KHACHHANG (
    maKhachHang VARCHAR(10) NOT NULL PRIMARY KEY,
    tenKhachHang NVARCHAR(100) NOT NULL,
    gioiTinh NVARCHAR(3) NOT NULL,
    soDienThoai VARCHAR(10),
    soLanMua INT,
	CONSTRAINT CHK_GioiTinhKH CHECK (gioiTinh IN (N'Nam', N'Nữ'))
);


CREATE TABLE HOADON (
    maHoaDon VARCHAR(10) NOT NULL PRIMARY KEY,
    ngayLap DATE NOT NULL,
    maKhachHang VARCHAR(10) NULL,
    tongTien INT NOT NULL,
	maNhanVien VARCHAR(10) NOT NULL,
    FOREIGN KEY (maKhachHang) REFERENCES KHACHHANG(maKhachHang),
	FOREIGN KEY (maNhanVien) REFERENCES NHANVIEN(maNhanVien)
);


CREATE TABLE CT_HOADON (
    maHoaDon VARCHAR(10) NOT NULL,
    maSanPham VARCHAR(10) NOT NULL,
    soLuong INT NOT NULL,
    thanhTien INT NOT NULL,
    PRIMARY KEY (maHoaDon, maSanPham),
    FOREIGN KEY (maHoaDon) REFERENCES HOADON(maHoaDon),
    FOREIGN KEY (maSanPham) REFERENCES SANPHAM(maSanPham),
	CONSTRAINT CHK_SoLuong CHECK (soLuong > 0),
    CONSTRAINT CHK_ThanhTien CHECK (thanhTien >= 0)
);


CREATE TABLE PHIEUNHAP (
    maPhieuNhap VARCHAR(10) NOT NULL PRIMARY KEY,
	ngayLap DATE NOT NULL,
    ngayNhap DATE NOT NULL,
    tongTien INT NOT NULL,
	trangThai nvarchar(20),
    maNCC VARCHAR(10) NOT NULL,
	maNhanVien VARCHAR(10) NOT NULL,
    FOREIGN KEY (maNCC) REFERENCES NHACUNGCAP(maNCC),
	FOREIGN KEY (maNhanVien) REFERENCES NHANVIEN(maNhanVien)
);


CREATE TABLE CT_PHIEUNHAP (
    maPhieuNhap VARCHAR(10) NOT NULL,
    maSanPham VARCHAR(10) NOT NULL,
    soLuong INT NOT NULL,
    donGia INT NOT NULL,
	hanSD date,
    PRIMARY KEY (maPhieuNhap, maSanPham),
    FOREIGN KEY (maPhieuNhap) REFERENCES PHIEUNHAP(maPhieuNhap),
    FOREIGN KEY (maSanPham) REFERENCES SANPHAM(maSanPham)
);



CREATE TABLE TAIKHOAN (
    taiKhoan VARCHAR(20) NOT NULL PRIMARY KEY,
    matKhau NVARCHAR(100) NOT NULL,
    vaiTro NVARCHAR(20) NOT NULL,
    maNhanVien VARCHAR(10) NOT NULL,
    FOREIGN KEY (maNhanVien) REFERENCES NHANVIEN(maNhanVien)
);

CREATE TABLE LICHSU_DANGNHAP (
    id INT NOT NULL IDENTITY PRIMARY KEY,
    taiKhoan VARCHAR(20) NULL,
    thoiGian DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (taiKhoan) REFERENCES TAIKHOAN(taiKhoan)
);

INSERT INTO NHANVIEN (maNhanVien, hoTen, gioiTinh, ngaySinh, soDienThoai, diaChi) VALUES
('NV001', N'Nguyễn Văn An', N'Nam', '1990-05-10', '0901122334', N'123 Đường Lê Lợi, Quận 1, TP.HCM'),
('NV002', N'Trần Thị Bình', N'Nữ', '1995-08-22', '0911223344', N'456 Đường Nguyễn Huệ, Quận 3, TP.HCM'),
('NV003', N'Lê Minh Châu', N'Nam', '1988-03-15', '0933445566', N'789 Đường Trần Hưng Đạo, Quận 5, TP.HCM');

INSERT INTO NHACUNGCAP (maNCC, tenNCC, diaChi, soDienThoai) VALUES
('NCC01', N'Công ty Dược phẩm Trường Thọ', N'123 Đường Phạm Ngũ Lão, Hà Nội', '0909123456'),
('NCC02', N'Công ty Dược Hậu Giang', N'456 Đường Lê Đại Hành, Cần Thơ', '0911222333'),
('NCC03', N'Công ty Dược Sài Gòn', N'789 Đường Võ Văn Tần, TP.HCM', '0933445777');

INSERT INTO SANPHAM (maSanPham, tenSanPham, giaSanPham, danhMuc, dangBaoChe, quyCach, thanhPhan, chiDinh, chongChiDinh, nhaSanXuat, nuocSanXuat, xuatXu, thuocCanKeToa, moTa, doiTuongSuDung, luuY, tonKho) VALUES
('SP001', N'Paracetamol 500mg', 25000, N'Thuốc giảm đau', N'Viên nén', N'Hộp 10 vỉ x 10 viên', N'Paracetamol', N'Giảm đau, hạ sốt', N'Không dùng cho người dị ứng Paracetamol', N'Trường Thọ', N'Việt Nam', N'Việt Nam', N'Không', N'Dùng cho các trường hợp cảm cúm, đau nhức', N'Người lớn', N'Không uống quá 4g/ngày',50),
('SP002', N'Amoxicillin 500mg', 40000, N'Thuốc kháng sinh', N'Viên nang', N'Hộp 10 vỉ x 10 viên', N'Amoxicillin', N'Nhiễm khuẩn đường hô hấp', N'Không dùng cho người dị ứng Penicillin', N'Dược Hậu Giang', N'Việt Nam', N'Việt Nam', N'Có', N'Kháng sinh phổ rộng', N'Mọi đối tượng', N'Cần có chỉ định bác sĩ',30),
('SP003', N'Vitamin C 1000mg', 15000, N'Thuốc bổ', N'Viên sủi', N'Hộp 10 viên', N'Vitamin C', N'Tăng cường sức đề kháng', N'Không dùng cho người bị sỏi thận', N'Sài Gòn Pharma', N'Việt Nam', N'Việt Nam', N'Không', N'Bổ sung Vitamin C', N'Người lớn và trẻ em', N'Uống sau bữa ăn',40);

INSERT INTO KHACHHANG (maKhachHang, tenKhachHang, gioiTinh, soDienThoai, soLanMua) VALUES
('KH001', N'Nguyễn Văn Hùng', N'Nam', '0912345678', 5),
('KH002', N'Trần Thị Mai', N'Nữ', '0934567890', 3),
('KHLE', N'Khách lẻ', N'Nam', NULL, 0); 

INSERT INTO TAIKHOAN (taiKhoan, matKhau, vaiTro, maNhanVien) VALUES
('admin1', '12345', N'admin', 'NV001'), 
('employee1', '12345', N'employee', 'NV002');

INSERT INTO PHIEUNHAP (maPhieuNhap, ngayLap, ngayNhap, tongTien, maNCC, maNhanVien, trangThai) VALUES
('PN001', '2025-05-20', '2025-05-21', 2500000, 'NCC01', 'NV001', N'Chưa xác nhận'),
('PN002', '2025-05-22', '2025-05-23', 6000000, 'NCC02', 'NV002', N'Chưa xác nhận'),
('PN003', '2025-05-24', '2025-05-25', 1500000, 'NCC03', 'NV003', N'Chưa xác nhận');

INSERT INTO CT_PHIEUNHAP (maPhieuNhap, maSanPham, soLuong, donGia, hanSD) VALUES
('PN001', 'SP001', 100, 25000, '2025-10-10'),
('PN001', 'SP002', 50, 40000, '2025-7-7'),
('PN002', 'SP002', 100, 40000, '2026-10-10'),
('PN002', 'SP003', 100, 15000, '2025-11-11'),
('PN003', 'SP001', 50, 25000, '2025-12-12'),
('PN003', 'SP003', 50, 15000,'2026-1-1');

INSERT INTO HOADON (maHoaDon, ngayLap, maKhachHang, tongTien, maNhanVien) VALUES
('HD001', '2025-05-25', 'KH001', 25000, 'NV001'),
('HD002', '2025-05-25', 'KH002', 55000, 'NV002'),
('HD003', '2025-05-25', NULL, 15000, 'NV003'); 

INSERT INTO CT_HOADON (maHoaDon, maSanPham, soLuong, thanhTien) VALUES
('HD001', 'SP001', 1, 25000),
('HD002', 'SP002', 1, 40000),
('HD002', 'SP003', 1, 15000),
('HD003', 'SP003', 1, 15000);

INSERT INTO LICHSU_DANGNHAP (taiKhoan, thoiGian) VALUES
('admin1', '2025-05-25 09:00:00'),
('employee1', '2025-05-25 10:00:00');

