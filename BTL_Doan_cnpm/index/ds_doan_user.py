from functools import partial
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import mysql.connector
import qrcode
from PyQt6.QtGui import QPixmap
from io import BytesIO
from datetime import datetime
class ds_doan(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(ds_doan,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_ds_doan.ui',self)
        self.loadata()
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qly_quan_net'
        )
        self.cursor = self.conn.cursor() 
        self.btn_thanhtoan.clicked.connect(self.thanh_toan)
        self.gio_hang = []
        self.ten_tai_khoan = ten_tai_khoan
        self.lb_tentk.setText(f"Xin chào, {self.ten_tai_khoan}")
        self.btn_back.clicked.connect(self.go_to_home)
        self.btn_napthem.clicked.connect(self.nap_tien)
        self.resize(1000, 760)
        self.setFixedSize(1000, 760) 
        self.btn_dangxuat.clicked.connect(self.go_to_dangnhap)
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
    def loadata(self, ten_dich_vu=None):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qly_quan_net'
        )
        self.cursor = self.conn.cursor()
        old_widget = self.scrollArea.widget()
        if old_widget:
            old_widget.deleteLater()

        # Truy vấn SQL
        if ten_dich_vu:
            sql = "SELECT ma_dich_vu, ten_dich_vu, loai_dich_vu, don_gia, trang_thai FROM quan_ly_dich_vu WHERE ten_dich_vu LIKE 'Đồ ăn:%'"
            value = f"%{ten_dich_vu}%"
            self.cursor.execute(sql, (value,))
        else:
            sql = "SELECT ma_dich_vu, ten_dich_vu, loai_dich_vu, don_gia, trang_thai FROM quan_ly_dich_vu WHERE ten_dich_vu LIKE 'Đồ ăn:%'"
            self.cursor.execute(sql)

        items = self.cursor.fetchall()

        # Widget chứa danh sách
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        for item in items:
            ma_dich_vu,ten_dich_vu, loai_dich_vu, don_gia, trang_thai = item

            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setSpacing(15)
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_widget.setStyleSheet("""
                QWidget {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #fafafa;
                }
            """)

            # Thông tin dịch vụ
            vbox = QVBoxLayout()
            label_name = QLabel(ten_dich_vu)
            label_name.setStyleSheet("font-size: 16px; font-weight: bold; border:none;")
            label_madv = QLabel(f"Mã DV: {ma_dich_vu}")
            label_madv.setStyleSheet("border:none;")
            label_detail = QLabel(f"Loại: {loai_dich_vu} | Giá: {don_gia} | Trạng thái: {trang_thai}")
            label_detail.setStyleSheet("border:none;")
            vbox.addWidget(label_name)
            vbox.addWidget(label_madv)
            vbox.addWidget(label_detail)

            # Nút đặt hàng
            btn_order = QPushButton("Đặt hàng")
            btn_order.setStyleSheet("font-size: 16px; border-radius:12px; padding: 6px; background-color:#6c63ff; color:white;")
            btn_order.setFixedSize(80, 28)
            btn_order.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn_order.clicked.connect(partial(self.them_vao_gio, ma_dich_vu, ten_dich_vu, don_gia))

            # Thêm vào layout
            item_layout.addLayout(vbox)
            item_layout.addWidget(btn_order)

            layout.addWidget(item_widget)

        layout.addStretch()
        self.scrollArea.setWidget(content_widget)
    def them_vao_gio(self, ma_dich_vu, ten_dich_vu, don_gia):
        """Thêm sản phẩm vào giỏ hàng tạm"""
        # kiểm tra nếu đã có thì tăng số lượng
        for sp in self.gio_hang:
            if sp["ma_dich_vu"] == ma_dich_vu:
                sp["so_luong"] += 1
                break
        else:
            self.gio_hang.append({
                "ma_dich_vu": ma_dich_vu,
                "ten_dich_vu": ten_dich_vu,
                "don_gia": don_gia,
                "so_luong": 1
            })
        QMessageBox.information(self, "Thông báo", f"Đã thêm {ten_dich_vu} vào giỏ hàng!")
        self.cap_nhat_bang_giohang()

    def cap_nhat_bang_giohang(self):
        """Hiển thị giỏ hàng lên bảng tb_ds"""
        self.tb_ds.setRowCount(len(self.gio_hang))
        self.tb_ds.setColumnCount(5)  # thêm cột "Xóa"
        self.tb_ds.setHorizontalHeaderLabels(["Mã", "Tên", "Số lượng", "Thành tiền", "Thao tác"])
        self.tb_ds.setColumnWidth(0, 80)
        self.tb_ds.setColumnWidth(1, 120)
        self.tb_ds.setColumnWidth(2, 80)
        self.tb_ds.setColumnWidth(3, 100)
        self.tb_ds.setColumnWidth(4, 80)

        tong_tien = 0
        for row, sp in enumerate(self.gio_hang):
            thanh_tien = sp["so_luong"] * float(sp["don_gia"])
            self.tb_ds.setItem(row, 0, QTableWidgetItem(str(sp["ma_dich_vu"])))
            self.tb_ds.setItem(row, 1, QTableWidgetItem(sp["ten_dich_vu"]))
            self.tb_ds.setItem(row, 2, QTableWidgetItem(str(sp["so_luong"])))
            self.tb_ds.setItem(row, 3, QTableWidgetItem(str(thanh_tien)))

            # Nút Xóa
            btn_xoa = QPushButton("Xóa")
            btn_xoa.setStyleSheet("background-color: red; color: white; border-radius:6px;")
            btn_xoa.clicked.connect(partial(self.xoa_san_pham, sp["ma_dich_vu"]))
            self.tb_ds.setCellWidget(row, 4, btn_xoa)

            tong_tien += thanh_tien

        # nếu có QLabel hiển thị tổng tiền
        if hasattr(self, "lblTongTien"):
            self.lblTongTien.setText(f"Tổng: {tong_tien} VNĐ")


    def xoa_san_pham(self, ma_dich_vu):
        """Xóa sản phẩm khỏi giỏ hàng"""
        self.gio_hang = [sp for sp in self.gio_hang if sp["ma_dich_vu"] != ma_dich_vu]
        self.cap_nhat_bang_giohang()

    def thanh_toan(self):
        if not self.gio_hang:
            QMessageBox.warning(self, "Lỗi", "Giỏ hàng đang trống!")
            return

        tong_tien = sum(sp["so_luong"] * float(sp["don_gia"]) for sp in self.gio_hang)
        ma_hd = datetime.now().strftime('%Y%m%d%H%M%S')

        # --- Danh sách ngân hàng ---
        bank_urls = {
            "Vietcombank": "https://vcb.com.vn/payment?so_tien={so_tien}&maHD={ma_hd}",
            "Techcombank": "https://techcombank.com.vn/payment?amount={so_tien}&invoice={ma_hd}",
            "BIDV": "https://bidv.com.vn/payment?amount={so_tien}&order={ma_hd}",
            "VietinBank": "https://vietinbank.vn/payment?so_tien={so_tien}&maGD={ma_hd}",
            "MBBank": "https://mbbank.com.vn/payment?amount={so_tien}&bill={ma_hd}",
            "Agribank": "https://agribank.com.vn/payment?so_tien={so_tien}&maHD={ma_hd}",
            "ACB": "https://acb.com.vn/payment?so_tien={so_tien}&maHD={ma_hd}",
        }

        # Chọn ngân hàng
        bank, ok = QInputDialog.getItem(
            self, "Chọn ngân hàng", "Ngân hàng:", list(bank_urls.keys()), 0, False
        )
        if not ok:
            return

        # Sinh URL cho QR
        qr_url = bank_urls[bank].format(so_tien=tong_tien, ma_hd=ma_hd)
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
        dialog.setWindowTitle("Quét mã QR để thanh toán")
        vbox = QVBoxLayout(dialog)
        vbox.addWidget(QLabel(f"Số tiền cần thanh toán: {tong_tien} VND"))
        vbox.addWidget(QLabel(f"Ngân hàng: {bank}"))
        vbox.addWidget(qr_label)

        btn_ok = QPushButton("Xác nhận đã thanh toán")
        btn_ok.clicked.connect(lambda: (self.luu_lich_su(f"QR-{bank}"), dialog.accept()))
        vbox.addWidget(btn_ok)

        dialog.exec()
    def tao_tu_dong_ma(self):

        query = "SELECT MAX(ma_lich_su_dich_vu) FROM lich_su_dich_vu"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            chuoi_ma = result[0]
            so = int(chuoi_ma.replace("LSDV", ""))  
            ma_moi = f"LSDV{so+1:03d}"           
            return ma_moi
        else:
            return "LSDV001"  
    def luu_lich_su(self, phuong_thuc):
        """Lưu lịch sử thanh toán vào database"""
        tong_tien = sum(sp["so_luong"] * float(sp["don_gia"]) for sp in self.gio_hang)
        thoi_gian = datetime.now()

        for sp in self.gio_hang:
            ma_lich_su_dich_vu = self.tao_tu_dong_ma()  

            sql = """
                INSERT INTO lich_su_dich_vu(ma_lich_su_dich_vu, ten_tai_khoan, ten_dich_vu, gia_tien, phuong_thuc, ngay_mua)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (
                ma_lich_su_dich_vu,
                self.ten_tai_khoan,
                sp["ten_dich_vu"],
                sp["so_luong"] * float(sp["don_gia"]),
                phuong_thuc,
                thoi_gian
            )
            self.cursor.execute(sql, val)
            self.conn.commit()

        self.gio_hang.clear()
        self.cap_nhat_bang_giohang()
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

    def go_to_home(self):
        from trangchu_user import trangchu_user
        self.trangchu_user_form = trangchu_user(self.ten_tai_khoan)
        self.trangchu_user_form.show()
        self.hide()
    def go_to_dangnhap(self):
    # Dừng trừ giờ khi đăng xuất
        if hasattr(self, "timer"):
            self.timer.stop()
        from dangnhap_user import dangnhap_user
        self.dangnhap_user_form = dangnhap_user()
        self.dangnhap_user_form.show()
        self.hide()
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# ds_doan_form = ds_doan()
# widget.addWidget(ds_doan_form)
# widget.setCurrentWidget(ds_doan_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()



