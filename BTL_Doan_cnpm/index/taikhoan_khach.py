import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from datetime import datetime
import sys
import mysql.connector
import qrcode
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QLabel, QPushButton,QComboBox
from PyQt6.QtGui import QPixmap
import os
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import QUrl
import os
# phần code cần thêm/trích vào file chính PyQt của bạn
import uuid
import socket
import threading
import time
import os
import requests  # pip install requests
from PyQt6.QtCore import QTimer, QUrl

# import module server (file server_for_qr.py)
class taikhoan_khach(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(taikhoan_khach, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_taikhoan.ui', self)
        self.btn_them.clicked.connect(self.them)
        self.tb_taikhoan.setColumnCount(8)
        self.tb_taikhoan.setHorizontalHeaderLabels(["Mã tài khoản", "Tên tài khoản","Mật khẩu","Số dư","Trạng thái", "Ngày tạo","Ngày cập nhật","Số điện thoại"])
        self.tb_taikhoan.setColumnWidth(0,100)
        self.tb_taikhoan.setColumnWidth(1,130)
        self.tb_taikhoan.setColumnWidth(2,130)
        self.tb_taikhoan.setColumnWidth(3,130)
        self.tb_taikhoan.setColumnWidth(4,130)
        self.tb_taikhoan.setColumnWidth(5,130)
        self.tb_taikhoan.setColumnWidth(6,130)
        self.tb_taikhoan.setColumnWidth(7,130)
        self.tb_taikhoan.cellClicked.connect(self.load_data_from_table)
        self.btn_xoa.clicked.connect(self.xoa)
        self.btn_capnhap.clicked.connect(self.update)
        self.btn_timkiem.clicked.connect(self.search)
        self.btn_napthem.clicked.connect(self.nap_them)
        self.loaddata()
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.tb_taikhoan.cellClicked.connect(self.load_data_from_table)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_qlphong.clicked.connect(self.go_to_quanlyphong)
        self.btn_lichsu_tk.clicked.connect(self.go_to_lich_su)
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
        self.ten_tai_khoan = ten_tai_khoan
        self.lb_tentaikhoan.setText(f"Xin chào, {self.ten_tai_khoan}")
        self.setStyleSheet("""

            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 6px;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: 1px solid #dee2e6;
            }
        """)

        self.conn = mysql.connector.connect(
             host='localhost',
            user='root',
            password='',
            database='qly_quan_net'
        )
        self.cursor = self.conn.cursor()
    def loaddata(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='qly_quan_net'
            )
            self.cursor = self.conn.cursor()
            query = "SELECT * FROM quan_ly_tai_khoan_khach_hang"
            self.cursor.execute(query,)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_taikhoan.setRowCount(len(data))
            self.tb_taikhoan.setColumnCount(len(data[0]) if data else 8)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            # self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def tao_tu_dong_ma(self):
        query = "SELECT MAX(ma_tai_khoan) FROM quan_ly_tai_khoan_khach_hang"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("TK", ""))  
            ma_moi = f"TK{so+1:03d}"           
            return ma_moi
        else:
            return "TK001"
    def tao_tu_dong_ma_ls(self):
        query = "SELECT MAX(ma_lich_su) FROM lich_su_cap_nhat"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("LSCN", ""))  
            ma_moi = f"LSCN{so+1:03d}"           
            return ma_moi
        else:
            return "LSCN001"
    def load_data_from_table(self):
        click = self.tb_taikhoan.currentRow()
        if click <0:
            return
        ma_tai_khoan = self.tb_taikhoan.item(click,0).text()
        ten_tai_khoan = self.tb_taikhoan.item(click,1).text()
        mat_khau = self.tb_taikhoan.item(click,2).text()
        so_du = self.tb_taikhoan.item(click,3).text()
        trang_thai = self.tb_taikhoan.item(click,4).text()
        so_dien_thoai = self.tb_taikhoan.item(click,7).text()
        # Hiển thị dữ liệu lên các ô nhập
        self.txt_matk.setText(ma_tai_khoan)
        self.txt_ten.setText(ten_tai_khoan)
        self.txt_matkhau.setText(mat_khau)
        self.txt_sodu.setText(so_du)
        self.cbb_trangthai.setCurrentText(trang_thai)
        self.txt_sdt.setText(so_dien_thoai)
    def them(self):
        ma_tai_khoan = self.tao_tu_dong_ma()
        ten_tai_khoan = self.txt_ten.text().strip()
        mat_khau = self.txt_matkhau.text().strip()
        # so_du = self.txt_sodu.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        ngay_tao = datetime.now()
        ngay_cap_nhat = datetime.now()
        so_dien_thoai = self.txt_sdt.text().strip()
        if not (ten_tai_khoan and mat_khau and so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền thông tin như lưu ý")
            return
        if not regex.match(r'[\p{L}\p{N}\s]*$',ten_tai_khoan):
            QMessageBox.warning(self,"Lỗi, Lưu ý","Tên tài khoản chỉ chứa chữ cái có dấu, số và khoảng trắng")
            return
        self.cursor.execute("SELECT * FROM quan_ly_tai_khoan_khach_hang WHERE ten_tai_khoan = %s", (ten_tai_khoan,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Tên tài khoản '{ten_tai_khoan}' đã tồn tại, vui lòng nhập tên khác!")
            return
        if not regex.match(r'^[A-Za-z0-9\s@._-]*$',mat_khau):
            QMessageBox.warning(self,"Lỗi, Lưu ý","Mật khẩu chỉ chứa chữ cái không dấu, số và khoảng trắng ")
            return
        if not regex.match(r'^0\d{9}$',so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Số điện thoại phải được bắt đầu bằng số 0 và có 10 chữ số!!!")
            return
        # if so_du == "":
        #     so_du = 0
        # else:
        #     try:
        #         so_du = float(self.txt_sodu.text().strip())
        #         if so_du < 0:
        #             QMessageBox.warning(self, "Lỗi", "Giá trị phải là giá trị không âm!")
        #             return
        #     except ValueError:
        #         QMessageBox.warning(self, "Lỗi", "Giá trị phải là số nguyên không âm!")
        #         return
        try:
            query = """
            INSERT INTO quan_ly_tai_khoan_khach_hang (ma_tai_khoan, ten_tai_khoan, mat_khau, so_du, trang_thai, ngay_tao, ngay_cap_nhat, so_dien_thoai)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (ma_tai_khoan, ten_tai_khoan, mat_khau, 0, trang_thai, ngay_tao, ngay_cap_nhat,so_dien_thoai)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành công","Thêm thông tin thành công")
            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm thông tin: {e}")
    def xoa(self):
        ten_tai_khoan = self.txt_ten.text().strip()
        if not ten_tai_khoan:
            QMessageBox.warning(self,"Lỗi","Hãy chọn thông tin tài khoản bạn muốn xóa")
            return
        try:
            reply = QMessageBox.question(self,"Xác nhận xóa","Bạn có chắc chắn muốn xóa thông tin này hay không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_tai_khoan_khach_hang WHERE ten_tai_khoan = %s"
                self.cursor.execute(query,(ten_tai_khoan,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa : {e}")
    
    def update(self):
        ma_lich_su = self.tao_tu_dong_ma_ls()
        ma_tai_khoan = self.txt_matk.text().strip()
        ten_tai_khoan = self.txt_ten.text().strip()
        mat_khau  = self.txt_matkhau.text().strip()
        so_du = self.txt_sodu.text().strip()
        so_dien_thoai = self.txt_sdt.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        ngay_cap_nhat = datetime.now()
        if not ( ten_tai_khoan and mat_khau and so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền thông tin như lưu ý")
            return
        if not regex.match(r'^[A-Za-z0-9\s@._-]*$',mat_khau):
            QMessageBox.warning(self,"Lỗi, Lưu ý","Mật khẩu chỉ chứa chữ cái không dấu, số và khoảng trắng ")
            return
        if not regex.match(r'^0\d{9}$',so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Số điện thoại phải được bắt đầu bằng số 0 và có 10 chữ số!!!")
            return
        try:
            # lấy ngày_tao 
            query_ngaytao = """
            SELECT ngay_tao 
            FROM quan_ly_tai_khoan_khach_hang 
            WHERE ma_tai_khoan = %s
            """
            self.cursor.execute(query_ngaytao, (ma_tai_khoan,))
            result_ngaytao = self.cursor.fetchone()
            if result_ngaytao:
                ngay_tao = result_ngaytao[0]
            kiem_tra = """
            SELECT ma_tai_khoan FROM quan_ly_tai_khoan_khach_hang
            WHERE ten_tai_khoan = %s AND ma_tai_khoan <> %s
            """
            self.cursor.execute(kiem_tra, (ten_tai_khoan,ma_tai_khoan))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self,"Lỗi","Tên tài khoản đã tồn tại vui lòng nhập tên tài khoản khác")
                return
            query = """
            UPDATE quan_ly_tai_khoan_khach_hang 
            SET mat_khau = %s, trang_thai = %s, ngay_cap_nhat = %s, so_dien_thoai = %s WHERE ma_tai_khoan = %s
            """
            values = (mat_khau, trang_thai, ngay_cap_nhat, so_dien_thoai,ma_tai_khoan)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành công","Cập nhật thông tin thành công")
            # thêm dữ liệu vào bảng ls
            query = """
            INSERT INTO lich_su_cap_nhat (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau, so_du, trang_thai, ngay_tao, ngay_cap_nhat, so_dien_thoai)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau, so_du, trang_thai, ngay_tao, ngay_cap_nhat,so_dien_thoai)
            self.cursor.execute(query,values)
            self.conn.commit()
            if hasattr(self, "loaddata"):
                self.loaddata()
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể cập nhập: {e}")
    def search(self):
        keyword = self.txt_timkiem.text().strip()
        if not keyword:
            self.loaddata()
            return
        try:
            query = """
            SELECT * FROM quan_ly_tai_khoan_khach_hang
            WHERE ma_tai_khoan LIKE %s OR ten_tai_khoan LIKE %s OR mat_khau LIKE %s OR so_du LIKE %s OR trang_thai LIKE %s OR ngay_tao LIKE %s OR ngay_cap_nhat LIKE %s OR so_dien_thoai LIKE %s 
            """ 
            values = tuple(f"%{keyword}%" for _ in range(8))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_taikhoan.setRowCount(0)
            self.clear_input()
            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_taikhoan.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def tao_tu_dong_manap(self):
        query = "SELECT MAX(CAST(SUBSTRING(ma_nap, 4) AS UNSIGNED)) FROM lich_su_nap WHERE ma_nap LIKE 'MN%'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            so = int(result[0])
            return f"MN{so+1:03d}"
        else:
            return "MN001"

    def nap_them(self):
        ma_nap = self.tao_tu_dong_manap()
        ma_lich_su = self.tao_tu_dong_ma_ls()
        ten_tai_khoan = self.txt_ten.text().strip()
        thoi_gian_nap = datetime.now()
        so_tien_nap = self.txt_sotiennap.text().strip()

        if not ten_tai_khoan or not so_tien_nap:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền tên tài khoản và số tiền nạp")
            return

        try:
            so_tien_nap = float(so_tien_nap)
            if so_tien_nap <= 0:
                QMessageBox.warning(self, "Lỗi", "Số tiền nạp phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số tiền nạp phải là số hợp lệ!")
            return

        payment_methods = ["Tiền mặt", "Thanh toán Online"]
        phuong_thuc, ok = QInputDialog.getItem(
            self, "Chọn phương thức thanh toán", "Phương thức:", payment_methods, 0, False
        )
        if not ok:
            return

        try:
            query_taikhoan = """
                SELECT ma_tai_khoan, mat_khau, so_du, trang_thai, ngay_tao, so_dien_thoai
                FROM quan_ly_tai_khoan_khach_hang
                WHERE ten_tai_khoan = %s
            """
            self.cursor.execute(query_taikhoan, (ten_tai_khoan,))
            result = self.cursor.fetchone()
            if not result:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy tài khoản này trong hệ thống!")
                return

            ma_tai_khoan, mat_khau, so_du, trang_thai, ngay_tao, so_dien_thoai = result
            so_du = float(so_du if so_du else 0)
            so_du_moi = so_du + so_tien_nap

            #  TIỀN MẶT 
            if phuong_thuc == "Tiền mặt":
                self.cursor.execute("""
                    UPDATE quan_ly_tai_khoan_khach_hang
                    SET so_du = %s, ngay_cap_nhat = %s
                    WHERE ten_tai_khoan = %s
                """, (so_du_moi, thoi_gian_nap, ten_tai_khoan))
                self.conn.commit()

                self.cursor.execute("""
                    INSERT INTO lich_su_nap (ma_nap, ten_tai_khoan, thoi_gian_nap, so_tien_nap)
                    VALUES (%s, %s, %s, %s)
                """, (ma_nap, ten_tai_khoan, thoi_gian_nap, so_tien_nap))
                self.conn.commit()

                self.cursor.execute("""
                    INSERT INTO lich_su_cap_nhat (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau,
                                                so_du, trang_thai, ngay_tao, ngay_cap_nhat, so_dien_thoai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau,
                    so_du_moi, trang_thai, ngay_tao, thoi_gian_nap, so_dien_thoai))
                self.conn.commit()

                QMessageBox.information(self, "Thành công",
                                        f"Nạp tiền mặt thành công {so_tien_nap}.\nSố dư mới: {so_du_moi}")

            #  ONLINE 
            else:
                bank_urls = {
                    "Vietcombank": "https://www.vietcombank.com.vn/",
                    "Techcombank": "https://www.techcombank.com.vn/",
                    "BIDV": "https://www.bidv.com.vn/",
                    "VietinBank": "https://www.vietinbank.vn/",
                    "MBBank": "https://www.mbbank.com.vn/",
                    "Agribank": "https://www.agribank.com.vn/",
                    "ACB": "https://www.acb.com.vn/"
                }

                dialog = QDialog(self)
                dialog.setWindowTitle("Thanh toán Online")
                layout = QVBoxLayout(dialog)

                lbl_bank = QLabel("Chọn ngân hàng:")
                cbb_bank = QComboBox()
                cbb_bank.addItems(bank_urls.keys())
                layout.addWidget(lbl_bank)
                layout.addWidget(cbb_bank)

                lbl_qr = QLabel()
                layout.addWidget(lbl_qr)

                def generate_qr():
                    selected_bank = cbb_bank.currentText()
                    bank_url = bank_urls[selected_bank]

                    # QR chứa luôn link mở ngân hàng + tham số giả lập
                    data_qr = f"{bank_url}?maNap={ma_nap}&taiKhoan={ten_tai_khoan}&soTien={so_tien_nap}"
                    img = qrcode.make(data_qr)
                    img_path = f"qr_{ma_nap}.png"
                    img.save(img_path)

                    pix = QPixmap(img_path)
                    lbl_qr.setPixmap(pix.scaled(300, 300))

                # sinh QR ban đầu
                generate_qr()
                cbb_bank.currentIndexChanged.connect(generate_qr)

                #  Hàm hoàn tất 
                def finish_payment():
                    try:
                        self.cursor.execute("""
                            UPDATE quan_ly_tai_khoan_khach_hang
                            SET so_du = %s, ngay_cap_nhat = %s
                            WHERE ten_tai_khoan = %s
                        """, (so_du_moi, thoi_gian_nap, ten_tai_khoan))
                        self.conn.commit()

                        self.cursor.execute("""
                            INSERT INTO lich_su_nap (ma_nap, ten_tai_khoan, thoi_gian_nap, so_tien_nap)
                            VALUES (%s, %s, %s, %s)
                        """, (ma_nap, ten_tai_khoan, thoi_gian_nap, so_tien_nap))
                        self.conn.commit()

                        self.cursor.execute("""
                            INSERT INTO lich_su_cap_nhat (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau,
                                                        so_du, trang_thai, ngay_tao, ngay_cap_nhat, so_dien_thoai)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (ma_lich_su, ma_tai_khoan, ten_tai_khoan, mat_khau,
                            so_du_moi, trang_thai, ngay_tao, thoi_gian_nap, so_dien_thoai))
                        self.conn.commit()

                        QMessageBox.information(dialog, "Thành công",
                            f"Thanh toán online qua {cbb_bank.currentText()} thành công {so_tien_nap}.\nSố dư mới: {so_du_moi}"
                        )

                        img_path = f"qr_{ma_nap}.png"
                        if os.path.exists(img_path):
                            os.remove(img_path)
                        dialog.accept()
                    except Exception as e:
                        QMessageBox.critical(dialog, "Lỗi", f"Không thể hoàn tất: {e}")

                #  Nút hoàn tất thủ công 
                btn_finish = QPushButton("Hoàn tất thanh toán")
                btn_finish.clicked.connect(finish_payment)
                layout.addWidget(btn_finish)

                btn_cancel = QPushButton("Hủy")
                btn_cancel.clicked.connect(dialog.reject)
                layout.addWidget(btn_cancel)

                dialog.exec()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể nạp thêm: {e}")

        if hasattr(self, "loaddata"):
            self.loaddata()
        self.clear_input()


    def clear_input(self):
        self.txt_ten.clear()
        self.txt_matkhau.clear()
        self.txt_matk.clear()
        self.txt_sdt.clear()
        self.txt_sodu.clear()
        self.txt_sotiennap.clear()
        self.cbb_trangthai.setCurrentIndex(0)
    # chuyển form  
    def go_to_quanlyphong(self):
        from quanlyphong import quanlyphong
        self.quanlyphong_form = quanlyphong(self.ten_tai_khoan)
        self.quanlyphong_form.show()
        self.hide()
    def go_to_quanlymay(self):
        from quanlymay import quanlymay
        self.quanlymay_form = quanlymay(self.ten_tai_khoan)
        self.quanlymay_form.show()
        self.hide()
    def go_to_tbcsvc(self):
        from thietbi_cosovatchat import thietbi_cosovatchat
        self.thietbi_cosovatchat_form = thietbi_cosovatchat(self.ten_tai_khoan)
        self.thietbi_cosovatchat_form.show()
        self.hide()
    def go_to_dichvu(self):
        from dich_vu import dich_vu
        self.dich_vu_form = dich_vu(self.ten_tai_khoan)
        self.dich_vu_form.show()
        self.hide()
    def go_to_nhanvien(self):
        from nhan_vien import nhan_vien
        self.nhan_vien_form = nhan_vien(self.ten_tai_khoan)
        self.nhan_vien_form.show()
        self.hide()
    def go_to_taikhoankhach(self):
        from taikhoan_khach import taikhoan_khach
        self.taikhoan_khach_form = taikhoan_khach(self.ten_tai_khoan)
        self.taikhoan_khach_form.show()
        self.hide()
    def go_to_taikhoannhanvien(self):
        from taikhoan_nhanvien import taikhoan_nhanvien
        self.taikhoan_nhanvien_form = taikhoan_nhanvien(self.ten_tai_khoan)
        self.taikhoan_nhanvien_form.show()
        self.hide()
    def go_to_logout(self):
        from dangnhap_admin import dangnhap_admin
        self.dangnhap_admin_form = dangnhap_admin()
        self.dangnhap_admin_form.show()
        self.hide()
    def go_to_trangchu_admin(self):
        from trangchu_admin import trangchu_admin
        self.trangchu_admin_form = trangchu_admin(self.ten_tai_khoan)
        self.trangchu_admin_form.show()
        self.hide()
    def go_to_lich_su(self):
        from lich_su_cap_nhat_nap_them import lich_su_cap_nhat_nap_them
        self.lich_su_form = lich_su_cap_nhat_nap_them(self.ten_tai_khoan)
        self.lich_su_form.show()
        self.hide()
# # #______________________________________________________________________#
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# taikhoan_khach_form = taikhoan_khach()
# widget.addWidget(taikhoan_khach_form)
# widget.setCurrentWidget(taikhoan_khach_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()
    