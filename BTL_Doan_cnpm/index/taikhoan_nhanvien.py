from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import mysql.connector
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from datetime import datetime, timedelta
class taikhoan_nhanvien(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(taikhoan_nhanvien,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_tk_nhanvien.ui',self)
        self.tb_tk_nhanvien.setColumnCount(3)
        self.tb_tk_nhanvien.setHorizontalHeaderLabels(["Mã tài khoản", "Tên tài khoản", "Mật khẩu"])
        self.tb_tk_nhanvien.setColumnWidth(0,120)
        self.tb_tk_nhanvien.setColumnWidth(1,300)
        self.tb_tk_nhanvien.setColumnWidth(2,300)
        self.tb_tk_nhanvien.cellClicked.connect(self.load_data_from_table)
        self.btn_xoa.clicked.connect(self.xoa)
        self.txt_timkiem.setPlaceholderText("Tìm kiếm")
        self.btn_capnhap.clicked.connect(self.update)
        self.btn_timkiem.clicked.connect(self.search)
        self.btn_them.clicked.connect(self.them)
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
            query = "SELECT ma_tai_khoan, ten_tai_khoan, mat_khau_tai_khoan FROM tai_khoan_nhan_vien"
            self.cursor.execute(query,)
            # self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Hiển thị dữ liệu lên table
            self.tb_tk_nhanvien.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_tk_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

            self.clear_input()
        
        except mysql.connector.Error as e:
            print(f"Lỗi MySQL: {e}")
    def load_data_from_table(self):
        click = self.tb_tk_nhanvien.currentRow()
        if click < 0:
            return  # Không có hàng nào được chọn
        ma_tai_khoan = self.tb_tk_nhanvien.item(click,0).text()
        ten_tai_khoan = self.tb_tk_nhanvien.item(click, 1).text()
        mat_khau_tai_khoan = self.tb_tk_nhanvien.item(click, 2).text()

        # Hiển thị dữ liệu lên các ô nhập
        self.txt_matk.setText(ma_tai_khoan)
        self.txt_ten.setText(ten_tai_khoan)
        self.txt_matkhau.setText(mat_khau_tai_khoan)
    def tao_tu_dong_ma(self):
        query = "SELECT MAX(ma_tai_khoan) FROM tai_khoan_nhan_vien"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("TKNV", ""))  
            ma_moi = f"TKNV{so+1:03d}"           
            return ma_moi
        else:
            return "TKNV001"  
    def send_otp(self, to_email):
        """Gửi OTP xác nhận đến email"""
        import random, smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from datetime import datetime, timedelta

        # Tạo OTP và thời gian hết hạn 2 phút
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expiry = datetime.now() + timedelta(minutes=2)

        subject = "Xác nhận đăng ký tài khoản"
        body = f"Mã xác nhận của bạn là: {self.otp_code}\nMã này có hiệu lực trong 2 phút."

        msg = MIMEMultipart()
        msg["From"] = "hoangquynfh@gmail.com"  # Gmail gửi đi
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("hoangquynfh@gmail.com", "tiht ywya lyvz pfdt")  
            server.sendmail("hoangquynfh@gmail.com", to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Mail", f"Gửi mail thất bại: {e}")
            return False


    def them(self):
        ma_tai_khoan = self.tao_tu_dong_ma()
        ten_tai_khoan = self.txt_ten.text().strip()
        mat_khau_tai_khoan = self.txt_matkhau.text().strip()

        # Kiểm tra nhập đủ thông tin
        if not ten_tai_khoan or not mat_khau_tai_khoan:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not ten_tai_khoan.endswith("@gmail.com"):
            QMessageBox.warning(self, "Lỗi", "Tên tài khoản phải có đuôi @gmail.com")
            return

        self.cursor.execute("SELECT * FROM tai_khoan_nhan_vien WHERE ten_tai_khoan = %s", (ten_tai_khoan,))
        result = self.cursor.fetchone()
        if result:
            QMessageBox.warning(self, "Lỗi", f"Tên '{ten_tai_khoan}' đã tồn tại, vui lòng nhập tên khác!")
            return

        # Gửi OTP tới email nhân viên
        if not self.send_otp(ten_tai_khoan):
            return

        # Nhập OTP do người dùng nhận
        user_otp, ok = QInputDialog.getText(self, "Xác nhận OTP", "Nhập mã OTP đã gửi đến email:")
        if not ok:
            QMessageBox.warning(self, "Huỷ", "Bạn đã huỷ xác nhận OTP")
            return

        # Kiểm tra OTP hợp lệ
        from datetime import datetime
        if datetime.now() > self.otp_expiry:
            QMessageBox.critical(self, "Lỗi OTP", "Mã OTP đã hết hạn, vui lòng thử lại!")
            return

        if user_otp != self.otp_code:
            QMessageBox.critical(self, "Sai OTP", "Mã OTP không đúng!")
            return

        # Thêm tài khoản vào DB (mật khẩu do người dùng nhập)
        try:
            query = """
            INSERT INTO tai_khoan_nhan_vien (ma_tai_khoan, ten_tai_khoan, mat_khau_tai_khoan)
            VALUES (%s, %s, %s)
            """
            values = (ma_tai_khoan, ten_tai_khoan, mat_khau_tai_khoan)
            self.cursor.execute(query, values)
            self.conn.commit()

            QMessageBox.information(self, "Thành Công", "Thêm thông tin thành công!!!!")
            if hasattr(self, "loaddata"):
                self.loaddata()

            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thêm: {e}")

    def xoa(self):
        ten_tai_khoan = self.txt_ten.text().strip()
        #kiểm tra
        if not ten_tai_khoan:
            QMessageBox.warning(self,"Lỗi","Vui lòng chọn tài khoản cần xóa!!!!")
            return
        try:
            reply = QMessageBox.question(
                self,
                "Xác nhận xóa",
                "Bạn có chắc chắn muốn xóa tài khoản này không ?",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                query = "DELETE FROM tai_khoan_nhan_vien WHERE ten_tai_khoan = %s"
                self.cursor.execute(query,(ten_tai_khoan,))
                self.conn.commit()
                self.clear_input()
                if hasattr(self, "loaddata"):
                    self.loaddata()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể xóa : {e}")
    def update(self):
        ma_tai_khoan = self.txt_matk.text().strip()
        ten_tai_khoan = self.txt_ten.text().strip()
        mat_khau_tai_khoan = self.txt_matkhau.text().strip()
        if not ten_tai_khoan or not mat_khau_tai_khoan:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return 
        if not ten_tai_khoan.endswith("@gmail.com"):
            QMessageBox.warning(self,"Lỗi","Tên tài khoản phải có đuôi @gmail.com")
            return

        try: 
            kiem_tra_ten_phong = """
            SELECT ma_tai_khoan FROM tai_khoan_nhan_vien
            WHERE ten_tai_khoan = %s AND ma_tai_khoan <> %s
            """
            self.cursor.execute(kiem_tra_ten_phong, (ten_tai_khoan, ma_tai_khoan))
            result = self.cursor.fetchone()

            if result:
                QMessageBox.warning(self, "Lỗi", "Tài khoản này đã tồn tại, vui lòng nhập tên khác!")
                return

            query = """
            UPDATE tai_khoan_nhan_vien
            SET ten_tai_khoan = %s, mat_khau_tai_khoan = %s WHERE ma_tai_khoan = %s
            """
            values = (ten_tai_khoan,mat_khau_tai_khoan,ma_tai_khoan)
            self.cursor.execute(query,values)
            self.conn.commit()
            QMessageBox.information(self,"Thông báo","Cập nhập thông tin thành công")
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
            SELECT * FROM tai_khoan_nhan_vien
            WHERE ten_tai_khoan LIKE %s OR mat_khau_tai_khoan LIKE %s OR ma_tai_khoan LIKE %s
            """
            values = tuple(f"%{keyword}%" for _ in range(3))
            self.cursor.execute(query, values)
            data = self.cursor.fetchall()
            self.tb_tk_nhanvien.setRowCount(0)

            # Hiển thị kết quả tìm kiếm lên bảng
            for row_idx, row_data in enumerate(data):
                self.tb_tk_nhanvien.insertRow(row_idx)
                for col_idx, cell_data in enumerate(row_data):
                    self.tb_tk_nhanvien.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
            self.clear_input()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi MySQL: {e}")
    def clear_input(self):
        self.txt_ten.clear()
        self.txt_matkhau.clear()
        self.txt_matk.clear()
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
# taikhoan_nhanvien_form = taikhoan_nhanvien()
# widget.addWidget(taikhoan_nhanvien_form)
# widget.setCurrentWidget(taikhoan_nhanvien_form)
# widget.resize(1000,760)
# widget.show()
# app.exec()