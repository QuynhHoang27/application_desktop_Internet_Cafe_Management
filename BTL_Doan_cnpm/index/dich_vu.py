import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import mysql.connector

class dich_vu(QMainWindow):
    def __init__(self, ten_tai_khoan):
        super(dich_vu, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_dichvu.ui', self)
        self.tb_dichvu.setColumnCount(6)
        self.tb_dichvu.setHorizontalHeaderLabels(["Mã dịch vụ", "Mã phòng","Tên dịch vụ","Loại dịch vụ","Đơn giá", "Trạng thái"])
        self.tb_dichvu.setColumnWidth(0,100)
        self.tb_dichvu.setColumnWidth(1,150)
        self.tb_dichvu.setColumnWidth(2,150)
        self.tb_dichvu.setColumnWidth(3,150)
        self.tb_dichvu.setColumnWidth(4,150)
        self.tb_dichvu.setColumnWidth(5,150)
        self.tb_dichvu.cellClicked.connect(self.load_data_from_table)
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
        self.loaddata()
        self.load_maphong()
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
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
            query = "SELECT * FROM quan_ly_dich_vu"
            self.cursor.execute(query,)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_dichvu.setRowCount(len(data))
            self.tb_dichvu.setColumnCount(len(data[0]) if data else 6)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_dichvu.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_dichvu.currentRow()
        if click < 0:
            return 
        ma_dich_vu = self.tb_dichvu.item(click,0).text()
        ma_phong = self.tb_dichvu.item(click,1).text()
        ten_dich_vu = self.tb_dichvu.item(click,2).text()
        loai_dich_vu = self.tb_dichvu.item(click,3).text()
        don_gia = self.tb_dichvu.item(click,4).text()
        trang_thai = self.tb_dichvu.item(click,5).text()

        # Hiển thị dữ liệu lên các ô nhập
        self.txt_madichvu.setText(ma_dich_vu)
        self.txt_ten.setText(ten_dich_vu)
        self.cbb_maphong.setCurrentText(ma_phong)
        self.cbb_phanloai.setCurrentText(loai_dich_vu)
        self.txt_gia_tri.setText(don_gia)
        self.cbb_trangthai.setCurrentText(trang_thai)
    def tao_tu_dong_madichvu(self):
        query = "SELECT MAX(ma_dich_vu) FROM quan_ly_dich_vu"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("DV", ""))  
            ma_moi = f"DV{so+1:03d}"           
            return ma_moi
        else:
            return "DV001"
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
        ma_dich_vu = self.tao_tu_dong_madichvu()
        ma_phong = self.cbb_maphong.currentText().strip()
        ten_dich_vu = self.txt_ten.text().strip()
        loai_dich_vu = self.cbb_phanloai.currentText().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        try:
            don_gia = float(self.txt_gia_tri.text().strip())
            if don_gia <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá trị phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá trị phải là số nguyên không âm!")
            return
        if not (ma_phong and ten_dich_vu and loai_dich_vu and trang_thai and don_gia):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền đầy đủ thông tin!!!!")
            return
        self.cursor.execute("SELECT * FROM quan_ly_dich_vu WHERE ten_dich_vu = %s", (ten_dich_vu,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Tên dịch vụ '{ten_dich_vu}' đã tồn tại, vui lòng nhập tên khác!")
            return
        if loai_dich_vu == "Đồ ăn":
            if not regex.match(r'^Đồ ăn: [\p{L}\p{N}\s]*$',ten_dich_vu):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên đồ ăn phải bắt đầu bằng 'Đồ ăn: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        elif loai_dich_vu == "Nước uống":
                if not regex.match(r'^Nước uống:[\p{L}\p{N}\s]*$',ten_dich_vu):
                    QMessageBox.warning(
                        self, 
                        "Lỗi",  
                        "Tên phải bắt đầu bằng 'Nước uống: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                    )
                    return
        else:                 
                if not regex.match(r'^Khác:[\p{L}\p{N}\s]*$',ten_dich_vu):
                    QMessageBox.warning(
                        self, 
                        "Lỗi",  
                        "Tên phải bắt đầu bằng 'Khác: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                    )
                    return
        try:
            query = """
            INSERT INTO quan_ly_dich_vu (ma_dich_vu, ma_phong, ten_dich_vu, loai_dich_vu, don_gia, trang_thai)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (ma_dich_vu, ma_phong, ten_dich_vu, loai_dich_vu, don_gia, trang_thai)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            QMessageBox.information(self, "Thành Công", "Thêm thông tin dịch vụ thành công!!!!")

            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm dịch vụ: {e}")
    def xoa(self):
        ten_dich_vu = self.txt_ten.text().strip()
        #kiem tra
        if not ten_dich_vu:
            QMessageBox.warning(self,"Lỗi", "Vui lòng chọn thông tin dịch vụ cần xóa!!!")
            return
        try:
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa thông tin này không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_dich_vu WHERE ten_dich_vu = %s"
                self.cursor.execute(query,(ten_dich_vu,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa : {e}")
    def update(self):
        ma_dich_vu = self.txt_madichvu.text().strip()
        ma_phong = self.cbb_maphong.currentText().strip()
        ten_dich_vu = self.txt_ten.text().strip()
        loai_dich_vu = self.cbb_phanloai.currentText().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        try:
            don_gia = float(self.txt_gia_tri.text().strip())
            if don_gia <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá trị phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá trị phải là số nguyên không âm!")
            return
        if not (ma_phong and ten_dich_vu and loai_dich_vu and trang_thai and don_gia):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền đầy đủ thông tin!!!!")
            return
        if loai_dich_vu == "Đồ ăn":
            if not regex.match(r'^Đồ ăn:[\p{L}\p{N}\s]*$',ten_dich_vu):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên đồ ăn phải bắt đầu bằng 'Đồ ăn: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        elif loai_dich_vu == "Nước uống":
            if not regex.match(r'^Nước uống:[\p{L}\p{N}\s]*$',ten_dich_vu):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên phải bắt đầu bằng 'Nước uống: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        else:                 
            if not regex.match(r'^Khác:[\p{L}\p{N}\s]*$',ten_dich_vu):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên phải bắt đầu bằng 'Khác: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        try:
            kiem_tra = """
            SELECT ma_dich_vu FROM quan_ly_dich_vu
            WHERE ten_dich_vu = %s AND ma_dich_vu <> %s
            """
            self.cursor.execute(kiem_tra,(ten_dich_vu, ma_dich_vu))
            result = self.cursor.fetchone()
            if result:
                QMessageBox.warning(self,"Lỗi","Tên dịch vụ này đã tồn tại")
                return
            query = """
            UPDATE quan_ly_dich_vu
            SET ma_phong = %s, ten_dich_vu = %s, loai_dich_vu = %s,don_gia = %s, trang_thai = %s WHERE ma_dich_vu = %s
            """
            values = (ma_phong, ten_dich_vu, loai_dich_vu, don_gia, trang_thai, ma_dich_vu)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành Công","Cập nhập dữ liệu thành công")
            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm dịch vụ: {e}")
    def search(self):
        keyword = self.txt_timkiem.text().strip()
        if not keyword:
            self.loaddata()
            return
        try:
            query = """
            SELECT * FROM quan_ly_dich_vu
            WHERE ma_dich_vu LIKE %s OR ma_phong LIKE %s OR ten_dich_vu LIKE %s OR loai_dich_vu LIKE %s OR don_gia LIKE %s OR trang_thai LIKE %s
            """
            values = tuple(f"%{keyword}%" for _ in range(6))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_dichvu.setRowCount(0)
            self.clear_input()
            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_dichvu.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_dichvu.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def clear_input(self):
        self.txt_ten.clear()
        self.cbb_maphong.setCurrentIndex(0)
        self.txt_gia_tri.clear()
        self.txt_madichvu.clear()
        self.cbb_trangthai.setCurrentIndex(0)
        self.cbb_phanloai.setCurrentIndex(0)
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
# dich_vu_form = dich_vu()
# widget.addWidget(dich_vu_form)
# widget.setCurrentWidget(dich_vu_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()