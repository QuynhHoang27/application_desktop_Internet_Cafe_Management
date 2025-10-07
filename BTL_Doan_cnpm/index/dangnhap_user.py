from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import mysql.connector
class dangnhap_user(QMainWindow):
    def __init__(self):
        super(dangnhap_user,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_dangnhap_user.ui',self)
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
        mat_khau = self.txt_mat_khau.text().strip()
        # Kiểm tra nhập đủ thông tin
        if not ten_tai_khoan or not mat_khau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        # Truy vấn kiểm tra đăng nhập
        query = "SELECT * FROM quan_ly_tai_khoan_khach_hang WHERE ten_tai_khoan = %s AND mat_khau = %s"
        self.cursor.execute(query, (ten_tai_khoan, mat_khau))
        test = self.cursor.fetchone()
        if test:
            self.start_time = datetime.now()
            QMessageBox.information(self, "Login output", "Đăng nhập thành công")
            from trangchu_user import trangchu_user
            self.trangchu_user_form = trangchu_user(ten_tai_khoan)
            self.trangchu_user_form .show()
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
# #Phần xử lí code
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
dangnhap_user_form= dangnhap_user()
widget.addWidget(dangnhap_user_form)
widget.setCurrentWidget(dangnhap_user_form)
widget.resize(1000,760)
widget.show()
app.exec()