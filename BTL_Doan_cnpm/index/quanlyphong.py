from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
class quanlyphong(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(quanlyphong,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_qlphong.ui',self)
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_xem_luxury.clicked.connect(self.go_to_phongluxury)
        self.btn_xem_vip.clicked.connect(self.go_to_phongvip)
        self.btn_xem_thuong.clicked.connect(self.go_to_phongthuong)
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

    def go_to_phongluxury(self):
        from quanlyphong_luxury import quanlyphong_luxury
        self.quanlyphong_luxury_form = quanlyphong_luxury(self.ten_tai_khoan)
        self.quanlyphong_luxury_form.show()
        self.hide()
    def go_to_phongvip(self):
        from quanlyphong_vip import quanlyphong_vip
        self.quanlyphong_vip_form = quanlyphong_vip(self.ten_tai_khoan)
        self.quanlyphong_vip_form.show()
        self.hide()
    def go_to_phongthuong(self):
        from quanlyphong_thuong import quanlyphong_thuong
        self.quanlyphong_thuong_form = quanlyphong_thuong(self.ten_tai_khoan)
        self.quanlyphong_thuong_form.show()
        self.hide()
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
