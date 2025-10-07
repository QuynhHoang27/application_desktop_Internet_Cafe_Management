import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from datetime import datetime
import sys
import mysql.connector

class lich_su_cap_nhat_nap_them(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(lich_su_cap_nhat_nap_them, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_lichsutaikhoan.ui', self)
        self.tb_taikhoan.setColumnCount(9)
        self.tb_taikhoan.setHorizontalHeaderLabels(["Mã lịch sử","Mã tài khoản", "Tên tài khoản","Mật khẩu","Số dư","Trạng thái", "Ngày tạo","Ngày cập nhật","Số điện thoại"])
        self.tb_taikhoan.setColumnWidth(0,100)
        self.tb_taikhoan.setColumnWidth(1,130)
        self.tb_taikhoan.setColumnWidth(2,130)
        self.tb_taikhoan.setColumnWidth(3,130)
        self.tb_taikhoan.setColumnWidth(4,130)
        self.tb_taikhoan.setColumnWidth(5,130)
        self.tb_taikhoan.setColumnWidth(6,130)
        self.tb_taikhoan.setColumnWidth(7,130)
        self.tb_taikhoan.setColumnWidth(7,130)
        self.tb_taikhoan_2.setColumnCount(4)
        self.tb_taikhoan_2.setHorizontalHeaderLabels(["Mã nạp","Tên tài khoản", "Thời gian nạp","Số tiền nạp"])
        self.tb_taikhoan_2.setColumnWidth(0,100)
        self.tb_taikhoan_2.setColumnWidth(1,130)
        self.tb_taikhoan_2.setColumnWidth(2,130)
        self.tb_taikhoan_2.setColumnWidth(3,130)
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_qlphong.clicked.connect(self.go_to_quanlyphong)
        self.btn_back.clicked.connect(self.go_to_taikhoankhach)
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
        self.loaddata()
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_timkiem.clicked.connect(self.search)
        self.tb_taikhoan.itemSelectionChanged.connect(self.hien_thi_chi_tiet_cap_nhat)
        self.tb_taikhoan_2.itemSelectionChanged.connect(self.hien_thi_chi_tiet_nap)
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
    def loaddata(self):
        try:
            # Tạo kết nối
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "qly_quan_net"
            )
            self.cursor = self.conn.cursor()
            query = "SELECT * FROM lich_su_cap_nhat"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            # Hiển thị dữ liệu lên table
            self.tb_taikhoan.setRowCount(len(data))
            self.tb_taikhoan.setColumnCount(len(data[0]) if data else 9)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            # bảng 2
            query = "SELECT * FROM lich_su_nap"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            # Hiển thị dữ liệu lên table
            self.tb_taikhoan_2.setRowCount(len(data))
            self.tb_taikhoan_2.setColumnCount(len(data[0]) if data else 4)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan_2.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            # Đóng kết nối
            self.cursor.close()
            self.conn.close()
            # self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def hien_thi_chi_tiet_cap_nhat(self):
        # Lấy dòng được chọn
        selected_items = self.tb_taikhoan.selectedItems()
        print("Selected items:", selected_items)  # Debug: In ra các item được chọn
        if selected_items:  # Kiểm tra xem có dòng nào được chọn không
            # Lấy dữ liệu từ dòng được chọn (giả sử mỗi dòng có 10 cột)
            row = selected_items[0].row()  # Lấy số dòng của item đầu tiên được chọn
            chi_tiet = []
            for col in range(self.tb_taikhoan.columnCount()):
                item = self.tb_taikhoan.item(row, col)
                if item:
                    chi_tiet.append(item.text())
                else:
                    chi_tiet.append("Không có dữ liệu")  # Thêm giá trị mặc định nếu item rỗng
            print("Chi tiết:", chi_tiet)  # Debug: In ra dữ liệu chi tiết
            
            # Xóa nội dung cũ
            self.tb_taikhoan_ls.clearContents()
            self.tb_taikhoan_ls.setRowCount(0)  # Xóa tất cả các hàng hiện tại

            # Đặt tiêu đề cột
            headers = ["Thông Tin", "Giá Trị"]
            self.tb_taikhoan_ls.setColumnCount(len(headers))
            self.tb_taikhoan_ls.setHorizontalHeaderLabels(headers)

            # Thêm dữ liệu vào bảng
            details = [
                # ("Chi Tiết Cập nhật", ""),
                ("Mã Lịch sử", chi_tiet[0]),
                ("Mã tài khoản", chi_tiet[1]),
                ("Tên tài khoản", chi_tiet[2]),
                ("Mật khẩu", chi_tiet[3]),
                ("Số dư", chi_tiet[4]),
                ("Trạng thái", chi_tiet[5]),
                ("Ngày tạo", chi_tiet[6]),
                ("Ngày cập nhật", chi_tiet[7]),
                ("Số điện thoại", chi_tiet[8]),
            ]

            self.tb_taikhoan_ls.setRowCount(len(details))  # Thêm số hàng tương ứng với dữ liệu

            for row, (label, value) in enumerate(details):
                self.tb_taikhoan_ls.setItem(row, 0, QTableWidgetItem(label))
                self.tb_taikhoan_ls.setItem(row, 1, QTableWidgetItem(value))
            self.tb_taikhoan_ls.setColumnWidth(0, 150)
            self.tb_taikhoan_ls.setColumnWidth(1, 200)
        else:
            print("Không có dòng nào được chọn")
            # Xóa nội dung cũ trong tb_taikhoan_ls nếu không có dòng được chọn
            self.tb_taikhoan_ls.clearContents()
            self.tb_taikhoan_ls.setRowCount(0)
    def hien_thi_chi_tiet_nap(self):
        # Lấy dòng được chọn
        selected_items = self.tb_taikhoan_2.selectedItems()
        print("Selected items:", selected_items) 
        if selected_items: 
            row = selected_items[0].row()  
            chi_tiet = []
            for col in range(self.tb_taikhoan_2.columnCount()):
                item = self.tb_taikhoan_2.item(row, col)
                if item:
                    chi_tiet.append(item.text())
                else:
                    chi_tiet.append("Không có dữ liệu")  
            print("Chi tiết:", chi_tiet)  
            
            # Xóa nội dung cũ
            self.tb_taikhoan_ls.clearContents()
            self.tb_taikhoan_ls.setRowCount(0)  

            # tiêu đề
            headers = ["Thông Tin", "Giá Trị"]
            self.tb_taikhoan_ls.setColumnCount(len(headers))
            self.tb_taikhoan_ls.setHorizontalHeaderLabels(headers)
            details = [
                # ("Chi Tiết nạp", ""),
                ("Mã nạp", chi_tiet[0]),
                ("Tên tài khoản", chi_tiet[1]),
                ("Thời gian nạp", chi_tiet[2]),
                ("Số tiền nạp", chi_tiet[3]),

            ]

            self.tb_taikhoan_ls.setRowCount(len(details)) 

            for row, (label, value) in enumerate(details):
                self.tb_taikhoan_ls.setItem(row, 0, QTableWidgetItem(label))
                self.tb_taikhoan_ls.setItem(row, 1, QTableWidgetItem(value))
            self.tb_taikhoan_ls.setColumnWidth(0, 150)
            self.tb_taikhoan_ls.setColumnWidth(1, 200)
        else:
            print("Không có dòng nào được chọn")
            # Xóa nội dung cũ trong tb_taikhoan_ls nếu không có dòng được chọn
            self.tb_taikhoan_ls.clearContents()
            self.tb_taikhoan_ls.setRowCount(0)
    def search(self):
        # Lấy dữ liệu từ ô tìm kiếm
        keyword = self.txt_timkiem.text().strip()

        # # Kiểm tra nếu ô tìm kiếm rỗng
        if not keyword:
            self.loaddata()
            return

        try:
            # Kết nối MySQL
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qly_quan_net"
            )
            self.cursor = self.conn.cursor()

            # Câu lệnh SQL tìm kiếm trên tất cả các cột
            query = """
            SELECT * FROM lich_su_cap_nhat
            WHERE  ma_lich_su LIKE %s OR ma_tai_khoan LIKE %s OR ten_tai_khoan LIKE %s OR mat_khau LIKE %s OR so_du LIKE %s OR trang_thai LIKE %s OR ngay_tao LIKE %s OR ngay_cap_nhat LIKE %s OR so_dien_thoai LIKE %s 
            """
            values = tuple(f"%{keyword}%" for _ in range(9)) 
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.tb_taikhoan.setRowCount(0)

            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_taikhoan.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            query = """
            SELECT * FROM lich_su_nap
            WHERE  ma_nap LIKE %s OR ten_tai_khoan LIKE %s OR thoi_gian_nap LIKE %s OR so_tien_nap LIKE %s 
            """
            values = tuple(f"%{keyword}%" for _ in range(4)) 
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()

            self.tb_taikhoan_2.setRowCount(0)

            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_taikhoan_2.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_taikhoan_2.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")

        finally:
            self.cursor.close()
            self.conn.close()

#####
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
# lich_su_cap_nhat_nap_them_form = lich_su_cap_nhat_nap_them()
# widget.addWidget(lich_su_cap_nhat_nap_them_form)
# widget.setCurrentWidget(lich_su_cap_nhat_nap_them_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()
    