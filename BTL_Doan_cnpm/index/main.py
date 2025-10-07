from PyQt6.QtWidgets import QApplication, QStackedWidget
from dangnhap_admin import dangnhap_admin
# from dangnhap_user import dangnhap_user

app = QApplication([])
widget = QStackedWidget()

dangnhap_admin_form = dangnhap_admin()
widget.addWidget(dangnhap_admin_form)
# dangnhap_user_form = dangnhap_user()
# widget.addWidget(dangnhap_user_form)
widget.resize(1000, 760)
widget.setFixedSize(1000, 760) 
widget.show()
app.exec()