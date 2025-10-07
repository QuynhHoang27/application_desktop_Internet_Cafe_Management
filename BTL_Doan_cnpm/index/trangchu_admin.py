from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
import sys
import mysql.connector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
class trangchu_admin(QMainWindow):
    def __init__(self,ten_tai_khoan):
        super(trangchu_admin,self).__init__()
        uic.loadUi('/Users/hoangquynh/BTL_DOAN_CNPM/interface/interface_trangchu_admin.ui',self)
        self.hien_thi_thong_ke()
        self.btn_qlmay.clicked.connect(self.go_to_quanlymay)
        self.btn_tbcsvc.clicked.connect(self.go_to_tbcsvc)
        self.btn_dichvu.clicked.connect(self.go_to_dichvu)
        self.btn_nhanvien.clicked.connect(self.go_to_nhanvien)
        self.btn_tk.clicked.connect(self.go_to_taikhoankhach)
        self.btn_tknhanvien.clicked.connect(self.go_to_taikhoannhanvien)
        self.btn_dangxuat.clicked.connect(self.go_to_logout)
        self.btn_trangchu.clicked.connect(self.go_to_trangchu_admin)
        self.btn_qlphong.clicked.connect(self.go_to_quanlyphong)
        self.btn_doanhthutong.clicked.connect(self.go_to_bao_cao)
        self.btn_doanhthu_nap.clicked.connect(self.go_to_bao_cao)
        self.btn_doanhthu_thuephong.clicked.connect(self.go_to_bao_cao)
        self.btn_doanhthu_dichvu.clicked.connect(self.go_to_bao_cao)
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


        self.hien_thi_thong_ke()
        self.resize(1000, 760)
        self.setFixedSize(1000, 760)
        self.ten_tai_khoan = ten_tai_khoan
        self.lb_tentaikhoan.setText(f"Xin chào, {self.ten_tai_khoan}")

    def hien_thi_thong_ke(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='qly_quan_net'
            )
            self.cursor = self.conn.cursor()

            # Doanh thu từ nạp
            self.cursor.execute("SELECT SUM(so_tien_nap) FROM lich_su_nap")
            doanh_thu_nap = self.cursor.fetchone()[0] or 0
            self.cursor.execute("SELECT SUM(gia_tien) FROM lich_su_dich_vu")
            doanh_thu_dich_vu = self.cursor.fetchone()[0] or 0
            # Doanh thu từ thuê máy
            self.cursor.execute("SELECT SUM(gia_tien) FROM lich_su_thue")
            doanh_thu_thue = self.cursor.fetchone()[0] or 0

            # Tổng doanh thu
            doanh_thu = doanh_thu_nap + doanh_thu_thue + doanh_thu_dich_vu

            # Tài khoản nạp nhiều tiền nhất
            self.cursor.execute("""
                SELECT ten_tai_khoan, SUM(so_tien_nap) as tong_nap
                FROM lich_su_nap
                GROUP BY ten_tai_khoan
                ORDER BY tong_nap DESC
                LIMIT 3
            """)
            results = self.cursor.fetchall()

            if results:
                # Ghép top 3 lại thành 1 chuỗi
                top_text = " | ".join([f"{row[0]}: {row[1]:,.0f} VNĐ" for row in results])
            else:
                top_text = "Không có dữ liệu"
            # máy theo trạng thái
            self.cursor.execute("SELECT COUNT(*) FROM quan_ly_may WHERE trang_thai = 'Đang hoạt động'")
            may_hd = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM quan_ly_may WHERE trang_thai = 'Không hoạt động'")
            may_khd = self.cursor.fetchone()[0]


            # Hiển thị
            self.btn_doanhthutong.setText(f" Doanh thu tổng: {doanh_thu:,.0f} VNĐ")
            self.btn_doanhthu_nap.setText(f"Doanh thu nạp: {doanh_thu_nap:,.0F} VNĐ")
            self.btn_doanhthu_thuephong.setText(f"Doanh thu thuê phòng: {doanh_thu_thue:,.0F} VNĐ")
            self.btn_mayhd.setText(f" Máy hoạt động: {may_hd}")
            self.btn_maykhd.setText(f" Máy không hoạt động: {may_khd}")
            self.btn_doanhthu_dichvu.setText(f" Doanh thu dịch vụ: {doanh_thu_dich_vu}")
            self.lb_tkmax.setText(f"Top 3 tài khoản nạp nhiều nhất: {top_text}")


            # Vẽ biểu đồ cột doanh thu
            barset = QBarSet("Doanh thu")
            barset.append([doanh_thu_nap, doanh_thu_thue, doanh_thu_dich_vu])

            series = QBarSeries()
            series.append(barset)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Thống kê doanh thu theo nguồn")
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            categories = ["Nạp tiền", "Thuê máy","Dịch vụ"]
            axisX = QBarCategoryAxis()
            axisX.append(categories)
            chart.addAxis(axisX, QtCore.Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axisX)

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

            layout = QVBoxLayout()
            layout.addWidget(chart_view)
            self.frame_bieudo.setLayout(layout) 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi MySQL", f"Không thể thống kê: {e}")
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
    def go_to_phong(self):
        from quanlyphong import quanlyphong
        self.quanlyphong_form = quanlyphong(self.ten_tai_khoan)
        self.quanlyphong_form.show()
        self.hide()
    def go_to_bao_cao(self):
        from baocao_thongke import baocao_thongke
        self.baocao_thongke_form = baocao_thongke(self.ten_tai_khoan)
        self.baocao_thongke_form.show()
        self.hide()
# # #______________________________________________________________________#
# app = QApplication(sys.argv)
# widget = QtWidgets.QStackedWidget()
# trangchu_admin_form = trangchu_admin()
# widget.addWidget(trangchu_admin_form)
# widget.setCurrentWidget(trangchu_admin_form)
# widget.resize(1000, 760)
# widget.show()
# app.exec()
