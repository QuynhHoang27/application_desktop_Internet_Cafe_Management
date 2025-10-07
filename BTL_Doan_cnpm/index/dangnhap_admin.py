from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import mysql.connector
class dangnhap_admin(QMainWindow):
    def __init__(self):
        super(dangnhap_admin,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/Interface_Dang_nhap.ui',self)
        self.txt_ten_tk.setPlaceholderText("Tên đăng nhập")
        self.txt_mat_khau.setPlaceholderText("Mật khẩu")
        self.btn_hien_thi_mk.setCheckable(True)
        self.btn_hien_thi_mk.setIcon(QIcon("/Users/hoangquynh/BTL_DOAN_CNPM/Icon & image/7787574_blind_eye_view_vision_magnifier_icon.ico"))
        self.btn_dangnhap.clicked.connect(self.login)
        self.btn_hien_thi_mk.toggled.connect(self.an_hien_mat_khau)
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qly_quan_net'
        )
        self.cursor = self.conn.cursor()
    def login(self):
        ten_tai_khoan = self.txt_ten_tk.text().strip()
        mat_khau_tai_khoan = self.txt_mat_khau.text().strip()
        # Kiểm tra nhập đủ thông tin
        if not ten_tai_khoan or not mat_khau_tai_khoan:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        if not ten_tai_khoan.endswith("@gmail.com"):
            QMessageBox.warning(self,"Lỗi","Tên tài khoản phải có đuôi @gmail.com")
            return
        # Truy vấn kiểm tra đăng nhập
        query = "SELECT * FROM tai_khoan_nhan_vien WHERE ten_tai_khoan = %s AND mat_khau_tai_khoan = %s"
        self.cursor.execute(query, (ten_tai_khoan, mat_khau_tai_khoan))
        test = self.cursor.fetchone()
        if test:
            QMessageBox.information(self, "Login output", "Đăng nhập thành công")
            from trangchu_admin import trangchu_admin
            self.trangchu_admin_form = trangchu_admin(ten_tai_khoan)
            self.trangchu_admin_form .show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login output", "Đăng nhập thất bại")

    def an_hien_mat_khau(self, checked):
        if checked:
            # Hiện mật khẩu
            self.txt_mat_khau.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_hien_thi_mk.setIcon(QIcon("/Users/hoangquynh/BTL_DOAN_CNPM/Icon & image/8324214_ui_essential_app_eye_watch_icon.ico"))
        else:
            # Ẩn mật khẩu
            self.txt_mat_khau.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_hien_thi_mk.setIcon(QIcon("/Users/hoangquynh/BTL_DOAN_CNPM/Icon & image/7787574_blind_eye_view_vision_magnifier_icon.ico"))

# # #______________________________________________________________________#
# # #Phần xử lí code
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# login_form = login_admin()
# widget.addWidget(login_form)
# widget.setCurrentWidget(login_form)
# #Chỉnh kích thước cố định của cửa sổ hiển thị
# widget.resize(1000,760)
# # widget.resize(1054,575)
# widget.show()
# app.exec()