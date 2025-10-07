-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th8 19, 2025 lúc 08:30 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qly_quan_net`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `bao_cao_thong_ke`
--

CREATE TABLE `bao_cao_thong_ke` (
  `ma_bao_cao` int(11) NOT NULL,
  `loai_bao_cao` varchar(50) NOT NULL,
  `tong_so_khach` int(11) NOT NULL,
  `tong_doanh_thu` decimal(10,2) NOT NULL,
  `ngay_tao_bao_cao` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lich_su_dang_nhap`
--

CREATE TABLE `lich_su_dang_nhap` (
  `ma_lich_su` int(11) NOT NULL,
  `ma_tai_khoan` int(11) DEFAULT NULL,
  `ma_may` int(11) DEFAULT NULL,
  `thoi_gian_bat_dau` datetime DEFAULT NULL,
  `thoi_gian_ket_thuc` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_dich_vu`
--

CREATE TABLE `quan_ly_dich_vu` (
  `ma_dich_vu` int(11) NOT NULL,
  `ma_phong` int(11) NOT NULL,
  `loai_dich_vu` varchar(50) NOT NULL,
  `don_gia` decimal(10,2) NOT NULL,
  `trang_thai` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_may`
--

CREATE TABLE `quan_ly_may` (
  `ma_may` int(11) NOT NULL,
  `ten_may` varchar(50) NOT NULL,
  `trang_thai` varchar(50) NOT NULL,
  `ma_phong` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_nhan_vien`
--

CREATE TABLE `quan_ly_nhan_vien` (
  `ma_nhan_vien` int(11) NOT NULL,
  `ma_phong` int(11) NOT NULL,
  `ten_nhan_vien` varchar(50) NOT NULL,
  `so_dien_thoai` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `dia_chi` text NOT NULL,
  `chuc_vu` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_phong`
--

CREATE TABLE `quan_ly_phong` (
  `ma_phong` int(11) NOT NULL,
  `ten_phong` varchar(50) NOT NULL,
  `loai_phong` varchar(20) NOT NULL,
  `don_gia` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_tai_khoan_khach_hang`
--

CREATE TABLE `quan_ly_tai_khoan_khach_hang` (
  `ma_tai_khoan` int(11) NOT NULL,
  `ten_tai_khoan` varchar(50) NOT NULL,
  `mat_khau` varchar(255) NOT NULL,
  `so_du` decimal(10,2) NOT NULL,
  `trang_thai` varchar(50) NOT NULL,
  `ngay_tao` datetime NOT NULL,
  `ngay_cap_nhat` datetime NOT NULL,
  `so_dien_thoai` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `quan_ly_tb_va_csvc`
--

CREATE TABLE `quan_ly_tb_va_csvc` (
  `ma_thiet_bi` int(11) NOT NULL,
  `ma_may` int(11) NOT NULL,
  `ten_thiet_bi` varchar(50) NOT NULL,
  `gia_tri` decimal(10,2) NOT NULL,
  `trang_thai` varchar(50) NOT NULL,
  `phan_loai` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `bao_cao_thong_ke`
--
ALTER TABLE `bao_cao_thong_ke`
  ADD PRIMARY KEY (`ma_bao_cao`);

--
-- Chỉ mục cho bảng `lich_su_dang_nhap`
--
ALTER TABLE `lich_su_dang_nhap`
  ADD PRIMARY KEY (`ma_lich_su`),
  ADD KEY `ma_tai_khoan` (`ma_tai_khoan`,`thoi_gian_bat_dau`) USING BTREE,
  ADD KEY `ma_may` (`ma_may`,`thoi_gian_bat_dau`) USING BTREE;

--
-- Chỉ mục cho bảng `quan_ly_dich_vu`
--
ALTER TABLE `quan_ly_dich_vu`
  ADD PRIMARY KEY (`ma_dich_vu`),
  ADD KEY `ma_phong` (`ma_phong`);

--
-- Chỉ mục cho bảng `quan_ly_may`
--
ALTER TABLE `quan_ly_may`
  ADD PRIMARY KEY (`ma_may`),
  ADD KEY `ma_phong` (`ma_phong`);

--
-- Chỉ mục cho bảng `quan_ly_nhan_vien`
--
ALTER TABLE `quan_ly_nhan_vien`
  ADD PRIMARY KEY (`ma_nhan_vien`),
  ADD KEY `ma_phong` (`ma_phong`);

--
-- Chỉ mục cho bảng `quan_ly_phong`
--
ALTER TABLE `quan_ly_phong`
  ADD PRIMARY KEY (`ma_phong`);

--
-- Chỉ mục cho bảng `quan_ly_tai_khoan_khach_hang`
--
ALTER TABLE `quan_ly_tai_khoan_khach_hang`
  ADD PRIMARY KEY (`ma_tai_khoan`);

--
-- Chỉ mục cho bảng `quan_ly_tb_va_csvc`
--
ALTER TABLE `quan_ly_tb_va_csvc`
  ADD PRIMARY KEY (`ma_thiet_bi`),
  ADD KEY `ma_may` (`ma_may`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `lich_su_dang_nhap`
--
ALTER TABLE `lich_su_dang_nhap`
  MODIFY `ma_lich_su` int(11) NOT NULL AUTO_INCREMENT;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `lich_su_dang_nhap`
--
ALTER TABLE `lich_su_dang_nhap`
  ADD CONSTRAINT `lich_su_dang_nhap_ibfk_1` FOREIGN KEY (`ma_tai_khoan`) REFERENCES `quan_ly_tai_khoan_khach_hang` (`ma_tai_khoan`),
  ADD CONSTRAINT `lich_su_dang_nhap_ibfk_2` FOREIGN KEY (`ma_may`) REFERENCES `quan_ly_may` (`ma_may`);

--
-- Các ràng buộc cho bảng `quan_ly_dich_vu`
--
ALTER TABLE `quan_ly_dich_vu`
  ADD CONSTRAINT `quan_ly_dich_vu_ibfk_1` FOREIGN KEY (`ma_phong`) REFERENCES `quan_ly_phong` (`ma_phong`);

--
-- Các ràng buộc cho bảng `quan_ly_may`
--
ALTER TABLE `quan_ly_may`
  ADD CONSTRAINT `quan_ly_may_ibfk_1` FOREIGN KEY (`ma_phong`) REFERENCES `quan_ly_phong` (`ma_phong`);

--
-- Các ràng buộc cho bảng `quan_ly_nhan_vien`
--
ALTER TABLE `quan_ly_nhan_vien`
  ADD CONSTRAINT `quan_ly_nhan_vien_ibfk_1` FOREIGN KEY (`ma_phong`) REFERENCES `quan_ly_phong` (`ma_phong`);

--
-- Các ràng buộc cho bảng `quan_ly_tb_va_csvc`
--
ALTER TABLE `quan_ly_tb_va_csvc`
  ADD CONSTRAINT `quan_ly_tb_va_csvc_ibfk_1` FOREIGN KEY (`ma_may`) REFERENCES `quan_ly_may` (`ma_may`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
