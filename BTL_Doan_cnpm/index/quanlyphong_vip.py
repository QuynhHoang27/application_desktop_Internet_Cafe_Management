import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import mysql.connector
import re

class quanlyphong_vip(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(quanlyphong_vip, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_qlphong_2.ui', self)
        self.btn_them.clicked.connect(self.them_phong)
        self.tb_phong_vip.setColumnCount(4)
        self.tb_phong_vip.setHorizontalHeaderLabels(["Mã", "Tên", "Loại phòng","Giá phòng"])
        self.tb_phong_vip.setColumnWidth(0,80)
        self.tb_phong_vip.setColumnWidth(1,210)
        self.tb_phong_vip.setColumnWidth(2,210)
        self.tb_phong_vip.setColumnWidth(3,210)
        self.tb_phong_vip.cellClicked.connect(self.load_data_from_table)
        self.btn_xoa.clicked.connect(self.xoa)
        self.btn_capnhap.clicked.connect(self.update)
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_timkiem.clicked.connect(self.search)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_back.clicked.connect(self.go_to_quanlyphong)
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
        self.ten_tai_khoan = ten_tai_khoan
        self.lb_tentaikhoan.setText(f"Xin chào, {self.ten_tai_khoan}")

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
            query = "SELECT * FROM quan_ly_phong WHERE loai_phong = %s"
            self.cursor.execute(query, ("VIP",))
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_phong_vip.setRowCount(len(data))
            self.tb_phong_vip.setColumnCount(len(data[0]) if data else 4)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_phong_vip.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    # Tạo mã phòng tự động
    def tao_tu_dong_maphong(self):
        query = "SELECT MAX(CAST(SUBSTRING(ma_phong, 4) AS UNSIGNED)) FROM quan_ly_phong WHERE ma_phong LIKE 'MPV%'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            so = int(result[0])
            return f"MPV{so+1:03d}"
        else:
            return "MPV001"
    def them_phong(self):
        ma_phong = self.tao_tu_dong_maphong()
        ten_phong = self.txt_ten_phong.text().strip()

        try:
            don_gia = float(self.txt_gia_phong.text().strip())
            if don_gia <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá phòng phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá phòng phải là số hợp lệ!")
            return       

        if not ten_phong:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        if not self.rb_loai_phong.isChecked():
            QMessageBox.warning(self, "Lỗi", "Vui lòng bấm chọn loại phòng")
            return                                              
        # \p{L} lấy chi cái unicode, \p{N} lấy chữ số \s là khoàng trắng
        if not regex.match(r'^[\p{L}\p{N}\s]+$', ten_phong):
            QMessageBox.warning(self, "Lỗi", "Tên phòng chỉ được chứa chữ cái (có dấu), số và khoảng trắng, không được có ký tự đặc biệt!")
            return

        self.cursor.execute("SELECT * FROM quan_ly_phong WHERE ten_phong = %s", (ten_phong,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Tên phòng '{ten_phong}' đã tồn tại, vui lòng nhập tên khác!")
            return
        try:
            query = """
            INSERT INTO quan_ly_phong (ma_phong, ten_phong, loai_phong, don_gia)
            VALUES (%s, %s, %s, %s)
            """
            values = (ma_phong, ten_phong, "VIP", don_gia)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            QMessageBox.information(self, "Thành Công", "Thêm thông tin phòng thành công!!!!")

            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm phòng: {e}")
    def xoa(self):
        ten_phong = self.txt_ten_phong.text().strip()
        #kiểm tra
        if not ten_phong:
            QMessageBox.warning(self,"Lỗi","Vui lòng chọn phòng cần xóa!!!!")
            return
        try:
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa phòng này không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_phong WHERE ten_phong = %s"
                self.cursor.execute(query,(ten_phong,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa phòng: {e}")
    def update(self):
        ma_phong = self.txt_maphong.text().strip()
        ten_phong = self.txt_ten_phong.text().strip()
        gia_phong = self.txt_gia_phong.text().strip()

        if not ten_phong or not gia_phong:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return 

        if not regex.match(r'^[\p{L}\p{N}\s]+$', ten_phong):
            QMessageBox.warning(self, "Lỗi", "Tên phòng chỉ được chứa chữ cái (có dấu), số và khoảng trắng, không được có ký tự đặc biệt!")
            return

        try:
            don_gia = float(self.txt_gia_phong.text().strip())
            if don_gia <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá phòng phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá phòng phải là số hợp lệ!")
            return       

        try:
            # Kiểm tra tên phòng có trùng không
            kiem_tra_ten_phong = """
            SELECT ma_phong FROM quan_ly_phong
            WHERE ten_phong = %s AND ma_phong <> %s
            """
            self.cursor.execute(kiem_tra_ten_phong, (ten_phong, ma_phong))
            result = self.cursor.fetchone()

            if result:
                QMessageBox.warning(self, "Lỗi", "Tên phòng này đã tồn tại, vui lòng nhập tên khác!")
                return

            # Cập nhật phòng
            query = """
            UPDATE quan_ly_phong
            SET ten_phong = %s, don_gia = %s
            WHERE ma_phong = %s
            """
            values = (ten_phong, don_gia, ma_phong)
            self.cursor.execute(query, values)
            self.conn.commit()
            QMessageBox.information(self, "Thông báo", "Cập nhật thông tin thành công")

            if hasattr(self, "loaddata"):
                self.loaddata()
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")

    def search(self):
        keyword = self.txt_timkiem.text().strip()
        if not keyword:
            self.loaddata()
            return
        try:
            query = """
            SELECT * FROM quan_ly_phong
            WHERE loai_phong = 'VIP' 
            AND (ten_phong LIKE %s OR don_gia LIKE %s)
            """
            values = tuple(f"%{keyword}%" for _ in range(2))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_phong_vip.setRowCount(0)

            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_phong_vip.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_phong_vip.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_phong_vip.currentRow()
        if click < 0:
            return  # Không có hàng nào được chọn
        ma_phong = self.tb_phong_vip.item(click,0).text()
        ten_phong = self.tb_phong_vip.item(click, 1).text()
        don_gia = self.tb_phong_vip.item(click, 3).text()
        # Hiển thị dữ liệu lên các ô nhập
        self.txt_maphong.setText(ma_phong)
        self.txt_ten_phong.setText(ten_phong)
        self.txt_gia_phong.setText(don_gia)

    # Xóa nội dung nhập
    def clear_input(self):
        self.txt_ten_phong.clear()
        self.txt_gia_phong.clear()
        self.txt_maphong.clear()
        self.rb_loai_phong.setChecked(False)
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
# quanlyphong_vip_form = quanlyphong_vip()
# widget.addWidget(quanlyphong_vip_form)
# widget.setCurrentWidget(quanlyphong_vip_form)

# widget.resize(1000, 760)
# widget.show()
# app.exec()
