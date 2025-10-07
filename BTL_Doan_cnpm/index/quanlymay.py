from datetime import datetime
import os
import regex
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import mysql.connector
import qrcode
from PyQt6.QtWidgets import QInputDialog, QLabel, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap

class quanlymay(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(quanlymay, self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_qlmay.ui', self)
        self.btn_them.clicked.connect(self.them_may)
        self.tb_may.setColumnCount(4)
        self.tb_may.setHorizontalHeaderLabels(["Mã máy", "Tên", "Trạng thái","Mã phòng"])
        self.tb_may.setColumnWidth(0,80)
        self.tb_may.setColumnWidth(1,210)
        self.tb_may.setColumnWidth(2,210)
        self.tb_may.setColumnWidth(3,210)
        self.tb_may.cellClicked.connect(self.load_data_from_table)
        self.btn_xoa.clicked.connect(self.xoa)
        self.btn_capnhap.clicked.connect(self.update)
        self.btn_timkiem.clicked.connect(self.search)
        self.loaddata()
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_qlphong.clicked.connect(self.go_to_quanlyphong)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
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
            query = "SELECT * FROM quan_ly_may"
            self.cursor.execute(query)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_may.setRowCount(len(data))
            self.tb_may.setColumnCount(len(data[0]) if data else 4)
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_may.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        
            # self.clear_input()
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    # Tạo mã máy   tự động
    def tao_tu_dong_mamay(self):

        query = "SELECT MAX(ma_may) FROM quan_ly_may"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("MM", ""))  
            ma_moi = f"MM{so+1:03d}"           
            return ma_moi
        else:
            return "MM001"  
    def tao_tu_dong_mals(self):

        query = "SELECT MAX(ma_ls) FROM lich_su_thue"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("MLS", ""))  
            ma_moi = f"MLS{so+1:03d}"           
            return ma_moi
        else:
            return "MLS001"
    def them_may(self):
        ma_may = self.tao_tu_dong_mamay()
        ten_may = self.txt_ten_may.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        ma_phong = self.cbb_maphong.currentText().strip()
        if not (ten_may and trang_thai and ma_phong):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        # \p{L} lấy chi cái unicode, \p{N} lấy chữ số \s là khoàng trắng
        if not regex.match(r'^Máy[\p{L}\p{N}\s]*$', ten_may):
            QMessageBox.warning(
                self, 
                "Lỗi", 
                "Tên máy phải bắt đầu bằng 'Máy' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
            )
            return
        self.cursor.execute("SELECT * FROM quan_ly_may WHERE ten_may = %s", (ten_may,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Tên máy '{ten_may}' đã tồn tại, vui lòng nhập tên khác!")
            return
        try:
            query = """
            INSERT INTO quan_ly_may (ma_may, ten_may, trang_thai, ma_phong)
            VALUES (%s, %s, %s, %s)
            """
            values = (ma_may, ten_may, trang_thai, ma_phong)
            self.cursor.execute(query, values)
            self.conn.commit()
            
            QMessageBox.information(self, "Thành Công", "Thêm thông tin máy thành công!!!!")

            if hasattr(self, "loaddata"):
                self.loaddata()
            
            # Xoá dữ liệu trong ô nhập
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm máy: {e}")
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
    def xoa(self):
        ten_may = self.txt_ten_may.text().strip()
        #kiem tra
        if not ten_may:
            QMessageBox.warning(self,"Lỗi", "Vui lòng chọn máy cần xóa!!!")
            return
        try:
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa máy này không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM quan_ly_may WHERE ten_may = %s"
                self.cursor.execute(query,(ten_may,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa máy: {e}")
    # def update(self):
    #     ma_ls = self.tao_tu_dong_mals()
    #     ma_may = self.txt_mamay.text().strip()
    #     ten_may = self.txt_ten_may.text().strip()
    #     trang_thai = self.cbb_trangthai.currentText().strip()
    #     ma_phong = self.cbb_maphong.currentText().strip()
    #     thoi_gian_thue = datetime.now()
    #     if not (ten_may and trang_thai and ma_phong):
    #         QMessageBox.warning(self,"Lỗi","Vui lòng điền đầy đủ thông tin")
    #         return
    #     if not regex.match(r'^Máy[\p{L}\p{N}\s]*$', ten_may):
    #         QMessageBox.warning(
    #             self, 
    #             "Lỗi", 
    #             "Tên máy phải bắt đầu bằng 'Máy' và chỉ được chứa chữ cái (có dấu), số và khoảng trắng!"
    #         )
    #         return
    #     try:
    #         query_trangthai = "SELECT trang_thai FROM quan_ly_may WHERE ma_may = %s"
    #         self.cursor.execute(query_trangthai, (ma_may,))
    #         result_tt = self.cursor.fetchone()
    #         trang_thai_cu = result_tt[0] if result_tt else None
            
    #         query_dongia = "SELECT don_gia FROM quan_ly_phong WHERE ma_phong = %s"
    #         self.cursor.execute(query_dongia, (ma_phong,))
    #         result_dg = self.cursor.fetchone()
    #         don_gia = result_dg[0] if result_dg else None
    #         kiem_tra = """
    #         SELECT ma_may FROM quan_ly_may
    #         WHERE ten_may = %s AND ma_may <> %s
    #         """
    #         self.cursor.execute(kiem_tra,(ten_may,ma_may))
    #         result = self.cursor.fetchone()
    #         if result:
    #             QMessageBox.warning(self,"Lỗi","Tên máy đã tồn tại, vui lòng nhập tên khác")
    #             return
    #         query = """
    #         UPDATE quan_ly_may 
    #         SET ten_may = %s, trang_thai = %s, ma_phong = %s WHERE ma_may = %s
    #         """

    #         values = (ten_may, trang_thai, ma_phong, ma_may)
    #         self.cursor.execute(query, values)
    #         self.conn.commit()
    #         # Nếu trạng thái từ Không hoạt động -> Hoạt động thì insert vào lịch sử thuê
    #         if trang_thai_cu == "Không hoạt động" and trang_thai == "Đang hoạt động":
    #             query_add = """
    #             INSERT INTO lich_su_thue (ma_ls, ma_may, ma_phong, gia_tien, thoi_gian_thue)
    #             VALUES (%s, %s, %s, %s, %s)
    #             """
    #             self.cursor.execute(query_add, (ma_ls, ma_may, ma_phong,don_gia, thoi_gian_thue))
    #             self.conn.commit()
    #         QMessageBox.information(self, "Thành Công", "Cập nhập thông tin máy thành công!!!!")
    #         if hasattr(self, "loaddata"):
    #             self.loaddata()
            
    #         # Xoá dữ liệu trong ô nhập
    #         self.clear_input()

    #     except mysql.connector.Error as e:
    #         QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm máy: {e}")


    def update(self):
        ma_ls = self.tao_tu_dong_mals()
        ma_may = self.txt_mamay.text().strip()
        ten_may = self.txt_ten_may.text().strip()
        trang_thai = self.cbb_trangthai.currentText().strip()
        ma_phong = self.cbb_maphong.currentText().strip()
        thoi_gian_thue = datetime.now()

        if not (ten_may and trang_thai and ma_phong):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin")
            return

        try:
            # Lấy trạng thái cũ
            query_trangthai = "SELECT trang_thai FROM quan_ly_may WHERE ma_may = %s"
            self.cursor.execute(query_trangthai, (ma_may,))
            result_tt = self.cursor.fetchone()
            trang_thai_cu = result_tt[0] if result_tt else None

            # Lấy đơn giá + tên phòng
            query_dongia = """
                SELECT don_gia, ten_phong 
                FROM quan_ly_phong WHERE ma_phong = %s
            """
            self.cursor.execute(query_dongia, (ma_phong,))
            result_dg = self.cursor.fetchone()
            don_gia, ten_phong = result_dg if result_dg else (None, None)

            # Update thông tin máy
            query = """
            UPDATE quan_ly_may 
            SET ten_may = %s, trang_thai = %s, ma_phong = %s WHERE ma_may = %s
            """
            self.cursor.execute(query, (ten_may, trang_thai, ma_phong, ma_may))
            self.conn.commit()

            # Nếu chuyển từ Không hoạt động -> Đang hoạt động
            if trang_thai_cu == "Không hoạt động" and trang_thai == "Đang hoạt động":
                # Chọn phương thức thanh toán
                phuong_thuc, ok = QInputDialog.getItem(
                    self, "Phương thức thanh toán", "Chọn phương thức:", 
                    ["Tiền mặt", "Tài khoản"], 0, False
                )

                if not ok:
                    return

                if phuong_thuc == "Tiền mặt":
                    query_add = """
                    INSERT INTO lich_su_thue (ma_ls, ma_may, ma_phong, gia_tien, thoi_gian_thue, phuong_thuc)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(query_add, (ma_ls, ma_may, ma_phong, don_gia, thoi_gian_thue, phuong_thuc))
                    self.conn.commit()

                elif phuong_thuc == "Tài khoản":
                    # Tạo dữ liệu QR
                    qr_data = f"""
                    Thanh toán máy: {ten_may}
                    Phòng: {ten_phong}
                    Giá: {don_gia} VND
                    Thời gian: {thoi_gian_thue.strftime('%Y-%m-%d %H:%M:%S')}
                    Mã thuê: {ma_ls}
                    """
                    qr = qrcode.make(qr_data)
                    qr_filename = f"qr_{ma_ls}.png"
                    qr.save(qr_filename)

                    # Hiển thị QR cho user
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Quét QR để thanh toán")
                    layout = QVBoxLayout()

                    lbl_qr = QLabel()
                    pixmap = QPixmap(qr_filename)
                    lbl_qr.setPixmap(pixmap)
                    layout.addWidget(lbl_qr)

                    btn_done = QPushButton("Xác nhận đã thanh toán")
                    layout.addWidget(btn_done)
                    dialog.setLayout(layout)

                    def confirm_payment():
                        # Lưu vào DB khi đã thanh toán
                        query_add = """
                        INSERT INTO lich_su_thue (ma_ls, ma_may, ma_phong, gia_tien, thoi_gian_thue, phuong_thuc)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        self.cursor.execute(query_add, (ma_ls, ma_may, ma_phong, don_gia, thoi_gian_thue, phuong_thuc))
                        self.conn.commit()
                        os.remove(qr_filename)  # Xoá file QR
                        dialog.accept()
                        QMessageBox.information(self, "Thành công", "Thanh toán thành công!")

                    btn_done.clicked.connect(confirm_payment)
                    dialog.exec()

            QMessageBox.information(self, "Thành Công", "Cập nhật thông tin máy thành công!!!!")
            if hasattr(self, "loaddata"):
                self.loaddata()
            self.clear_input()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể cập nhật máy: {e}")

    def search(self):
        keyword = self.txt_timkiem.text().strip()
        if not keyword:
            self.loaddata()
            return
        try:
            query = """
            SELECT * FROM quan_ly_may
            WHERE ten_may LIKE %s OR trang_thai LIKE %s OR ma_phong LIKE %s
            """
            values = tuple(f"%{keyword}%" for _ in range(3))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_may.setRowCount(0)

            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_may.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_may.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_may.currentRow()
        if click < 0:
            return  # Không có hàng nào được chọn\
        ma_may = self.tb_may.item(click,0).text()
        ten_may = self.tb_may.item(click, 1).text()
        trang_thai = self.tb_may.item(click, 2).text()
        ma_phong =  self.tb_may.item(click,3).text()

        # Hiển thị dữ liệu lên các ô nhập
        self.txt_mamay.setText(ma_may)
        self.txt_ten_may.setText(ten_may)
        self.cbb_trangthai.setCurrentText(trang_thai)
        self.cbb_maphong.setCurrentText(ma_phong)

    # Xóa nội dung nhập
    def clear_input(self):
        self.txt_ten_may.clear()
        self.txt_mamay.clear()
        self.cbb_trangthai.setCurrentIndex(0)
        self.cbb_maphong.setCurrentIndex(0)
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
# # # #______________________________________________________________________#
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# quanlymay_form = quanlymay()
# widget.addWidget(quanlymay_form)
# widget.setCurrentWidget(quanlymay_form)

# widget.resize(1000, 760)
# widget.show()
# app.exec()