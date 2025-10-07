import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import mysql.connector

class nhan_vien(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(nhan_vien, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_qlnhanvien.ui', self)
        self.tb_nhanvien.setColumnCount(7)
        self.tb_nhanvien.setHorizontalHeaderLabels(["Mã nhân viên", "Mã phòng","Tên nhân viên","Số điện thoại","Email", "Địa chỉ","Chức vụ"])
        self.tb_nhanvien.setColumnWidth(0,100)
        self.tb_nhanvien.setColumnWidth(1,130)
        self.tb_nhanvien.setColumnWidth(2,130)
        self.tb_nhanvien.setColumnWidth(3,130)
        self.tb_nhanvien.setColumnWidth(4,130)
        self.tb_nhanvien.setColumnWidth(5,130)
        self.tb_nhanvien.setColumnWidth(6,130)
        self.tb_nhanvien.cellClicked.connect(self.load_data_from_table)
        self.btn_xoa.clicked.connect(self.xoa)
        self.btn_capnhap.clicked.connect(self.update)
        self.btn_timkiem.clicked.connect(self.search)
        self.btn_them.clicked.connect(self.them)
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_qlphong.clicked.connect(self.go_to_quanlyphong)
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
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
        self.loaddata()
        self.load_maphong()
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
            query = "SELECT * FROM quan_ly_nhan_vien"
            self.cursor.execute(query,)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_nhanvien.setRowCount(len(data))
            self.tb_nhanvien.setColumnCount(len(data[0]) if data else 7)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_nhanvien.currentRow()
        if click < 0:
            return 
        ma_nhan_vien = self.tb_nhanvien.item(click,0).text()
        ma_phong = self.tb_nhanvien.item(click,1).text()
        ten_nhan_vien = self.tb_nhanvien.item(click,2).text()
        so_dien_thoai = self.tb_nhanvien.item(click,3).text()
        email = self.tb_nhanvien.item(click,4).text()
        dia_chi = self.tb_nhanvien.item(click,5).text()
        chu_vu = self.tb_nhanvien.item(click,6).text()
        # Hiển thị dữ liệu lên các ô nhập
        self.txt_manhanvien.setText(ma_nhan_vien)
        self.txt_ten.setText(ten_nhan_vien)
        self.cbb_maphong.setCurrentText(ma_phong)
        self.txt_sodienthoai.setText(so_dien_thoai)
        self.txt_mail.setText(email)
        self.txt_diachi.setText(dia_chi)
        self.cbb_chucvu.setCurrentText(chu_vu)
    
    def tao_tu_dong_manhanvien(self):
        query = "SELECT MAX(ma_nhan_vien) FROM quan_ly_nhan_vien"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("NV", ""))  
            ma_moi = f"NV{so+1:03d}"           
            return ma_moi
        else:
            return "NV001"
    def load_maphong(self):
        try: 
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='qly_quan_net'
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT ma_phong FROM quan_ly_phong")
            data = self.cursor.fetchall()
            self.cbb_maphong.clear()
            for (ma_phong,) in data:
                self.cbb_maphong.addItem(str(ma_phong))
            self.cursor.close()
            self.conn.close()
        except mysql.connector.Error as e:
            print(f"Lỗi khi load thông tin: {e}") 
    def them(self):
        ma_nhan_vien = self.tao_tu_dong_manhanvien()
        ma_phong = self.cbb_maphong.currentText().strip()
        ten_nhan_vien = self.txt_ten.text().strip()
        so_dien_thoai = self.txt_sodienthoai.text().strip()
        email = self.txt_mail.text().strip()
        dia_chi = self.txt_diachi.text().strip()
        chuc_vu = self.cbb_chucvu.currentText().strip()
        if not (ma_phong and ten_nhan_vien and so_dien_thoai and email and dia_chi and chuc_vu):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền đẩy đủ thông tin")
            return 
        if not regex.match(r'^0\d{9}$',so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Số điện thoại phải được bắt đầu bằng số 0 và có 10 chữ số")
            return
        
        if not regex.match(r'[\p{L}\s]*$',ten_nhan_vien):
            QMessageBox.warning(self, "Lỗi","Tên chỉ được chứa chữ cái (có dấu) và khoảng trắng!")
            return
        if not regex.match(r'[\p{L}\p{N}\s]*$',dia_chi):
            QMessageBox.warning(self, "Lỗi","Địa chỉ, chỉ được chứa chữ cái dấu, số và khoảng trắng!")
            return
        if not regex.match(r'^[A-Za-z0-9\s@._-]*$',email):
            QMessageBox.warning(self, "Lỗi","Email, chỉ được chứa chữ cái không dấu, số và khoảng trắng!")
            return
        if not email.endswith("@gmail.com"):
            QMessageBox.warning(self,"Lỗi","Địa chỉ mail phải có đuôi @gmail.com")
            return
        self.cursor.execute("SELECT * FROM quan_ly_nhan_vien WHERE email = %s",(email,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Email này '{email}' đã tồn tại, vui lòng nhập email khác!")
            return
        self.cursor.execute("SELECT * FROM quan_ly_nhan_vien WHERE so_dien_thoai = %s",(so_dien_thoai,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Số điện thoại '{so_dien_thoai}' đã tồn tại, vui lòng nhập số điện thoại khác!")
            return
        try:
            query = """
            INSERT INTO quan_ly_nhan_vien (ma_nhan_vien, ma_phong, ten_nhan_vien, so_dien_thoai, email, dia_chi, chuc_vu)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (ma_nhan_vien, ma_phong, ten_nhan_vien, so_dien_thoai, email, dia_chi, chuc_vu)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành công","Thêm thông tin nhân viên thành công")
            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm thông tin nhân viên: {e}")
    def xoa(self):
        so_dien_thoai = self.txt_sodienthoai.text().strip()
        if not so_dien_thoai:
            QMessageBox.warning(self,"Lỗi","Vui lòng chọn thông tin nhân viên cần xóa")
            return
        try:
            reply = QMessageBox.question(self,"Xác nhận xóa","Bạn có chắc chắn muốn xóa thông tin này hay không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_nhan_vien WHERE so_dien_thoai = %s"
                self.cursor.execute(query,(so_dien_thoai,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa : {e}")
    def update(self):
        ma_nhan_vien = self.txt_manhanvien.text().strip()
        ma_phong = self.cbb_maphong.currentText().strip()
        ten_nhan_vien = self.txt_ten.text().strip()
        so_dien_thoai = self.txt_sodienthoai.text().strip()
        email = self.txt_mail.text().strip()
        dia_chi = self.txt_diachi.text().strip()
        chuc_vu = self.cbb_chucvu.currentText().strip()
        if not (ma_phong and ten_nhan_vien and so_dien_thoai and email and dia_chi and chuc_vu):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền đẩy đủ thông tin")
            return 
        if not regex.match(r'^0\d{9}$',so_dien_thoai):
            QMessageBox.warning(self,"Lỗi","Số điện thoại phải được bắt đầu bằng số 0 và có 10 chữ số!!!")
            return
        if not regex.match(r'[\p{L}\s]*$',ten_nhan_vien):
            QMessageBox.warning(self, "Lỗi","Tên chỉ được chứa chữ cái (có dấu) và khoảng trắng!")
            return
        if not regex.match(r'[\p{L}\p{N}\s]*$',dia_chi):
            QMessageBox.warning(self, "Lỗi","Địa chỉ, chỉ được chứa chữ cái (có dấu), số và khoảng trắng!")
            return
        if not regex.match(r'^[A-Za-z0-9\s@._-]*$',email):
            QMessageBox.warning(self, "Lỗi","Email, chỉ được chứa chữ cái không dấu, số và khoảng trắng!")
            return
        if not email.endswith("@gmail.com"):
            QMessageBox.warning(self,"Lỗi","Địa chỉ mail phải có đuôi @gmail.com")
            return
        try:
            kiem_tra_sdt = """
            SELECT ma_nhan_vien FROM quan_ly_nhan_vien
            WHERE so_dien_thoai = %s AND ma_nhan_vien <> %s
            """
            self.cursor.execute(kiem_tra_sdt,(so_dien_thoai,ma_nhan_vien))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self,"Lỗi","Số điện thoại đã tồn tại vui lòng nhập số điện thoại khác")
                return
            kiem_tra_email = """
            SELECT ma_nhan_vien FROM quan_ly_nhan_vien
            WHERE email = %s AND ma_nhan_vien <> %s
            """
            self.cursor.execute(kiem_tra_email,(email,ma_nhan_vien))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self,"Lỗi","Email đã tồn tại vui lòng nhập Email khác")
                return
            query = """
            UPDATE quan_ly_nhan_vien
            SET ma_phong = %s, ten_nhan_vien = %s, so_dien_thoai = %s, email = %s, dia_chi = %s, chuc_vu = %s WHERE ma_nhan_vien = %s
            """
            values = (ma_phong, ten_nhan_vien, so_dien_thoai, email, dia_chi, chuc_vu, ma_nhan_vien)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành Công","Cập nhập dữ liệu thành công")
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
            SELECT * FROM quan_ly_nhan_vien
            WHERE ma_nhan_vien LIKE %s OR ma_phong LIKE %s OR ten_nhan_vien LIKE %s OR so_dien_thoai LIKE %s OR email LIKE %s OR dia_chi LIKE %s OR chuc_vu LIKE %s
            """
            values = tuple(f"%{keyword}%" for _ in range(7))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_nhanvien.setRowCount(0)
            self.clear_input()
            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_nhanvien.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def clear_input(self):
        self.txt_ten.clear()
        self.txt_manhanvien.clear()
        self.cbb_maphong.setCurrentIndex(0)
        self.txt_sodienthoai.clear()
        self.txt_mail.clear()
        self.txt_diachi.clear()
        self.cbb_chucvu.setCurrentIndex(0)
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
# # #______________________________________________________________________#
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# nhan_vien_form = nhan_vien()
# widget.addWidget(nhan_vien_form)
# widget.setCurrentWidget(nhan_vien_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()