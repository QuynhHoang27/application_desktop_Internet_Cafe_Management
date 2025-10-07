from datetime import datetime
from io import BytesIO
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import mysql.connector
import qrcode
from PyQt6.QtGui import QPixmap
class trangchu_user(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(trangchu_user,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_dichvu_nguoidung.ui',self)
        self.ten_tai_khoan = ten_tai_khoan
        self.lb_tentk.setText(f"Xin chào, {self.ten_tai_khoan}")
        self.btn_doan.clicked.connect(self.go_to_ds_doan)
        self.btn_nuoc.clicked.connect(self.go_to_ds_nuoc)
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qly_quan_net'
        )
        self.cursor = self.conn.cursor()
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
        self.btn_dangxuat.clicked.connect(self.go_to_dangnhap)
        self.btn_napthem.clicked.connect(self.nap_tien)

        # Gọi hàm load số dư + thời gian
        self.load_tai_khoan()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cap_nhat_thoi_gian)
        self.timer.start(60000)

    def load_tai_khoan(self):
        """Lấy số dư và tính thời gian còn lại"""
        query = "SELECT so_du FROM quan_ly_tai_khoan_khach_hang WHERE ten_tai_khoan = %s"
        self.cursor.execute(query, (self.ten_tai_khoan,))
        result = self.cursor.fetchone()

        if result:
            so_du = float(result[0])

            thoi_gian_gio = so_du / 10  

            # Chuyển sang giờ và phút để hiển thị đẹp hơn
            gio = int(thoi_gian_gio)
            phut = int((thoi_gian_gio - gio) * 60)

            # Hiển thị lên label
            self.lb_tienconlai.setText(f"{so_du:.0f} VNĐ")
            self.lb_thoigianconlai.setText(f"{gio} giờ {phut} phút")
        else:
            self.lb_tienconlai.setText("Số dư: 0 VNĐ")
            self.lb_thoigianconlai.setText("Thời gian còn: 0 giờ 0 phút")
    def cap_nhat_thoi_gian(self):
        """Cập nhật số dư và thời gian còn lại mỗi phút"""
        query = "SELECT so_du FROM quan_ly_tai_khoan_khach_hang WHERE ten_tai_khoan = %s"
        self.cursor.execute(query, (self.ten_tai_khoan,))
        result = self.cursor.fetchone()

        if result:
            so_du = float(result[0])
            so_du -= 0.1666   # trừ 1 phút (10 VND = 1 giờ)

            if so_du <= 0:
                so_du = 0
                QMessageBox.warning(self, "Hết giờ", "Tài khoản đã hết thời gian sử dụng!")
                self.timer.stop()
                self.go_to_home()

            # Cập nhật lại DB
            sql_update = "UPDATE quan_ly_tai_khoan_khach_hang SET so_du = %s WHERE ten_tai_khoan = %s"
            self.cursor.execute(sql_update, (so_du, self.ten_tai_khoan))
            self.conn.commit()

            # Hiển thị lại trên giao diện
            thoi_gian_gio = so_du / 10
            gio = int(thoi_gian_gio)
            phut = int((thoi_gian_gio - gio) * 60)

            self.lb_tienconlai.setText(f"{so_du:.0f} VNĐ")
            self.lb_thoigianconlai.setText(f"{gio} giờ {phut} phút")
    def tao_tu_dong_manap(self):
        query = "SELECT MAX(CAST(SUBSTRING(ma_nap, 4) AS UNSIGNED)) FROM lich_su_nap WHERE ma_nap LIKE 'MN%'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            so = int(result[0])
            return f"MN{so+1:03d}"
        else:
            return "MN001"
    def nap_tien(self):
        ma_nap = self.tao_tu_dong_manap()
        so_tien, ok = QInputDialog.getDouble(self, "Nạp tiền", "Nhập số tiền nạp (VNĐ):", decimals=0, min=1)
        if not ok:
            return

        # Bước 2: Chọn ngân hàng
        bank_urls = {
            "Vietcombank": "https://vcb.com.vn/payment?so_tien={so_tien}&maGD={ma_hd}",
            "Techcombank": "https://techcombank.com.vn/payment?amount={so_tien}&maGD={ma_hd}",
            "BIDV": "https://bidv.com.vn/payment?amount={so_tien}&maGD={ma_hd}",
            "VietinBank": "https://vietinbank.vn/payment?so_tien={so_tien}&maGD={ma_hd}",
            "MBBank": "https://mbbank.com.vn/payment?amount={so_tien}&maGD={ma_hd}",
            "Agribank": "https://agribank.com.vn/payment?so_tien={so_tien}&maGD={ma_hd}",
            "ACB": "https://acb.com.vn/payment?so_tien={so_tien}&maGD={ma_hd}",
        }

        bank, ok = QInputDialog.getItem(
            self, "Chọn ngân hàng", "Ngân hàng:", list(bank_urls.keys()), 0, False
        )
        if not ok:
            return

        # Bước 3: Sinh URL QR
        ma_hd = datetime.now().strftime('%Y%m%d%H%M%S')  # Mã giao dịch tạm
        qr_url = bank_urls[bank].format(so_tien=so_tien, ma_hd=ma_hd)
        qr_img = qrcode.make(qr_url)

        # Hiển thị QR
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "PNG")

        qr_label = QLabel()
        qr_label.setPixmap(pixmap)
        qr_label.setScaledContents(True)
        qr_label.setFixedSize(250, 250)

        dialog = QDialog(self)
        dialog.setWindowTitle("Quét mã QR để nạp tiền")
        vbox = QVBoxLayout(dialog)
        vbox.addWidget(QLabel(f"Số tiền nạp: {so_tien} VND"))
        vbox.addWidget(QLabel(f"Ngân hàng: {bank}"))
        vbox.addWidget(qr_label)

        # Khi người dùng xác nhận đã nạp
        btn_ok = QPushButton("Xác nhận đã nạp")
        def confirm_nap():
            thoi_gian_nap = datetime.now()

            # Cập nhật số dư tài khoản
            query = "UPDATE quan_ly_tai_khoan_khach_hang SET so_du = so_du + %s WHERE ten_tai_khoan = %s"
            self.cursor.execute(query, (so_tien, self.ten_tai_khoan))
            self.conn.commit()

            # Lưu lịch sử nạp tiền
            sql_insert = """
                INSERT INTO lich_su_nap (ma_nap,ten_tai_khoan, thoi_gian_nap, so_tien_nap)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql_insert, (ma_nap, self.ten_tai_khoan, thoi_gian_nap, so_tien))
            self.conn.commit()

            QMessageBox.information(self, "Thành công", f"Đã nạp {so_tien:.0f} VNĐ vào tài khoản!")
            self.load_tai_khoan()  # Cập nhật số dư trên giao diện
            dialog.accept()

        btn_ok.clicked.connect(confirm_nap)
        vbox.addWidget(btn_ok)

        dialog.exec()
    def go_to_ds_doan(self):
        from ds_doan_user import ds_doan
        self.ds_doan_form = ds_doan(self.ten_tai_khoan)
        self.ds_doan_form.show()
        self.hide()
    def go_to_ds_nuoc(self):
        from ds_nuoc import ds_nuoc
        self.ds_nuoc_form = ds_nuoc(self.ten_tai_khoan)
        self.ds_nuoc_form.show()
        self.hide()
    def go_to_dangnhap(self):
    # Dừng trừ giờ khi đăng xuất
        if hasattr(self, "timer"):
            self.timer.stop()

        from dangnhap_user import dangnhap_user
        self.dangnhap_user_form = dangnhap_user()
        self.dangnhap_user_form.show()
        self.hide()