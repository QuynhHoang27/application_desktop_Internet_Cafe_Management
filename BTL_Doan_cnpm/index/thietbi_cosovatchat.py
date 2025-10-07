import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import mysql.connector

class thietbi_cosovatchat(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(thietbi_cosovatchat, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_tb_csvc.ui', self)
        self.tb_tb_csvc.setColumnCount(6)
        self.tb_tb_csvc.setHorizontalHeaderLabels(["Mã thiết bị", "Mã máy","Tên thiết bị","Giá trị", "Trạng thái","Phân Loại"])
        self.tb_tb_csvc.setColumnWidth(0,100)
        self.tb_tb_csvc.setColumnWidth(1,150)
        self.tb_tb_csvc.setColumnWidth(2,150)
        self.tb_tb_csvc.setColumnWidth(3,150)
        self.tb_tb_csvc.setColumnWidth(4,150)
        self.tb_tb_csvc.setColumnWidth(5,150)
        self.tb_tb_csvc.cellClicked.connect(self.load_data_from_table)
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
        self.load_mamay()
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
            query = "SELECT * FROM quan_ly_tb_va_csvc"
            self.cursor.execute(query,)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_tb_csvc.setRowCount(len(data))
            self.tb_tb_csvc.setColumnCount(len(data[0]) if data else 6)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_tb_csvc.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_tb_csvc.currentRow()
        if click < 0:
            return  # Không có hàng nào được chọn
        ma_thiet_bi = self.tb_tb_csvc.item(click,0).text()
        ma_may = self.tb_tb_csvc.item(click, 1).text()
        ten_thiet_bi = self.tb_tb_csvc.item(click, 2).text()
        gia_tri =  self.tb_tb_csvc.item(click,3).text()
        trang_thai = self.tb_tb_csvc.item(click,4).text()
        phan_loai = self.tb_tb_csvc.item(click,5).text()

        # Hiển thị dữ liệu lên các ô nhập
        self.txt_ma_tb.setText(ma_thiet_bi)
        self.txt_ten.setText(ten_thiet_bi)
        self.cbb_mamay.setCurrentText(ma_may)
        self.txt_gia_tri.setText(gia_tri)
        self.cbb_trangthai.setCurrentText(trang_thai)
        self.cbb_phanloai.setCurrentText(phan_loai)
    # Tạo mã tự động
    def tao_tu_dong_mathietbi(self):

        query = "SELECT MAX(ma_thiet_bi) FROM quan_ly_tb_va_csvc"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("MTC", ""))  
            ma_moi = f"MTC{so+1:03d}"           
            return ma_moi
        else:
            return "MTC001"  
    def load_mamay(self):
        try: 
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='qly_quan_net'
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT ma_may FROM quan_ly_may")
            data = self.cursor.fetchall()
            self.cbb_mamay.clear()
            for (ma_may,) in data:
                self.cbb_mamay.addItem(str(ma_may))
            self.cursor.close()
            self.conn.close()
        except mysql.connector.Error as e:
            print(f"Lỗi khi load thông tin: {e}")
    # def load_ma_tb(self):
    #     try: 
    #         self.conn = mysql.connector.connect(
    #             host='localhost',
    #             user='root',
    #             password='',
    #             database='qly_quan_net'
    #         )
    #         self.cursor = self.conn.cursor()
    #         self.cursor.execute("SELECT ma_thiet_bi FROM quan_ly_tb_va_csvc")
    #         data = self.cursor.fetchall()
    #         self.cbb_ma_tb.clear()
    #         for (ma_thiet_bi,) in data:
    #             self.cbb_ma_tb.addItem(str(ma_thiet_bi))
    #         self.cursor.close()
    #         self.conn.close()
    #     except mysql.connector.Error as e:
    #         print(f"Lỗi khi load thông tin: {e}")
    def them(self):
        ma_thiet_bi = self.tao_tu_dong_mathietbi()
        ma_may = self.cbb_mamay.currentText().strip()
        ten_thiet_bi = self.txt_ten.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        phan_loai = self.cbb_phanloai.currentText().strip()
        try:
            gia_tri = float(self.txt_gia_tri.text().strip())
            if gia_tri <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá trị phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá trị phải là số nguyên không âm!")
            return  
        if not (ma_may and ten_thiet_bi and gia_tri and trang_thai and phan_loai ):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
  
        if phan_loai == "Thiết bị":
            if not regex.match(r'^Thiết bị[\p{L}\p{N}\s]*$',ten_thiet_bi):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên thiết bị phải bắt đầu bằng 'Thiết bị: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        else:
            if not regex.match(r'^Cơ sở vật chất[\p{L}\p{N}\s]*$',ten_thiet_bi):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên phải bắt đầu bằng 'Cơ sở vật chất: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        try:
            query = """
            INSERT INTO quan_ly_tb_va_csvc (ma_thiet_bi, ma_may, ten_thiet_bi, gia_tri, trang_thai, phan_loai)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (ma_thiet_bi, ma_may, ten_thiet_bi, gia_tri, trang_thai, phan_loai)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            QMessageBox.information(self, "Thành Công", "Thêm thông tin thiết bị thành công!!!!")

            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm thiết bị: {e}")
    
    def xoa(self):
        ma_thiet_bi = self.txt_ma_tb.text().strip()
        #kiem tra
        if not ma_thiet_bi:
            QMessageBox.warning(self,"Lỗi", "Vui lòng chọn thiết bị cần xóa!!!")
            return
        try:
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa thiết bị này không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_tb_va_csvc WHERE ma_thiet_bi = %s"
                self.cursor.execute(query,(ma_thiet_bi,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa : {e}")
    def update(self):
        ma_thiet_bi = self.txt_ma_tb.text().strip()
        ma_may = self.cbb_mamay.currentText().strip()
        ten_thiet_bi = self.txt_ten.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        phan_loai = self.cbb_phanloai.currentText().strip()
        gia_tri = self.txt_gia_tri.text().strip()
        if not (ma_may and ten_thiet_bi and trang_thai and phan_loai and gia_tri):
            QMessageBox.warning(self,"Lỗi","Vui lòng điền đầy đủ thông tin")
            return
        try:
            gia_tri = float(self.txt_gia_tri.text().strip())
            if gia_tri <= 0:
                QMessageBox.warning(self, "Lỗi", "Giá trị phải lớn hơn 0!")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá trị phải là số hợp lệ!")
            return       
        if phan_loai == "Thiết bị":
            if not regex.match(r'^Thiết bị[\p{L}\p{N}\s]*$',ten_thiet_bi):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên thiết bị phải bắt đầu bằng 'Thiết bị: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        else:
            if not regex.match(r'^Cơ sở vật chất[\p{L}\p{N}\s]*$',ten_thiet_bi):
                QMessageBox.warning(
                    self, 
                    "Lỗi",  
                    "Tên phải bắt đầu bằng 'Cơ sở vật chất: ' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
                )
                return
        try:
            query = """
            UPDATE quan_ly_tb_va_csvc
            SET ma_may = %s, ten_thiet_bi = %s, gia_tri = %s, trang_thai = %s, phan_loai = %s WHERE ma_thiet_bi = %s
            """
            values = (ma_may, ten_thiet_bi, gia_tri, trang_thai, phan_loai, ma_thiet_bi)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thành Công","Cập nhập dữ liệu thành công")
            if hasattr(self,"loaddata"):
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
            SELECT * FROM quan_ly_tb_va_csvc
            WHERE ma_thiet_bi LIKE %s OR ma_may LIKE %s OR ten_thiet_bi LIKE %s OR gia_tri LIKE %s OR trang_thai LIKE %s OR phan_loai LIKE %s
            """
            values = tuple(f"%{keyword}%" for _ in range(6))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_tb_csvc.setRowCount(0)
            self.clear_input()
            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_tb_csvc.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_tb_csvc.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def clear_input(self):
        self.txt_ma_tb.clear()
        self.txt_ma_tb.clear()
        self.txt_ten.clear()
        self.cbb_mamay.setCurrentIndex(0)
        self.txt_gia_tri.clear()
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
# thietbi_cosovatchat_form = thietbi_cosovatchat()
# widget.addWidget(thietbi_cosovatchat_form)
# widget.setCurrentWidget(thietbi_cosovatchat_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()