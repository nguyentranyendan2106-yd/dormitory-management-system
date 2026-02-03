from PyQt5 import QtCore,QtGui,QtWidgets,uic
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mdb

#Cửa sổ login
class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w,self).__init__()
        uic.loadUi('login.ui',self)
        import Anh_rc
        self.login_dangnhap.clicked.connect(self.login)
        self.login_dangky.clicked.connect(self.reg_form)
    def reg_form(self):
        widget.setCurrentIndex(1)
    def login(self):
        try:
            un = self.login_tennguoidung.text()
            pw = self.login_matkhau.text()

            db = pymysql.connect(host="localhost", user="root", password="", database="login_app")
            query = db.cursor()

            query.execute("SELECT * FROM user_list WHERE username = %s AND password = %s", (un, pw))
            kt = query.fetchone()

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Login output")

            if kt:
                msg_box.setText("Login success")
                widget.setCurrentIndex(2)  # Chuyển sang cửa sổ login_success
            else:
                msg_box.setText("Login failed")

            # Áp dụng style để loại bỏ border-image
            msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                        border: none;
                        border-image: none;
                    }
                """)
            msg_box.exec()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối: {str(e)}")

#Cửa sổ register
class Reg_w(QMainWindow):
    def __init__(self):
        super(Reg_w,self).__init__()
        uic.loadUi('register.ui',self)
        import Anhdangky_rc
        self.reg_dangky.clicked.connect(self.reg)
    def reg(self):
        try:
            un = self.reg_tennguoidung.text()
            pw = self.dangky_matkhau.text()
            
            db = pymysql.connect(host="localhost", user="root", password="", database="login_app")
            query = db.cursor()

            query.execute("SELECT * FROM user_list WHERE username = %s AND password = %s", (un, pw))
            kt = query.fetchone()

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Register output")

            if kt:
                msg_box.setText("Tài khoản đã tồn tại")
            else:
                query.execute("insert into user_list values('"+un+"','"+pw+"')")
                db.commit()
                msg_box.setText("Đăng ký thành công")
                widget.setCurrentIndex(0)

            # Áp dụng style để loại bỏ border-image
            msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                        border: none;
                        border-image: none;
                    }
                """)
            msg_box.exec()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối: {str(e)}")

#Cửa sổ login
class Login_success_w(QMainWindow):
    def __init__(self):
        super(Login_success_w,self).__init__()
        uic.loadUi('login_success.ui',self)
        import Anhloginsuccess_rc

#Xử lý
app=QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet("""
    QMessageBox {
        background-color: white;
        border: none;
        border-image: none;
    }
""")
widget=QtWidgets.QStackedWidget()
Login_f=Login_w()
Reg_f=Reg_w()
Login_success_f=Login_success_w()
widget.addWidget(Login_f)
widget.addWidget(Reg_f)
widget.addWidget(Login_success_f)
widget.setCurrentIndex(0)
widget.setFixedSize(464, 716)
widget.show()
app.exec()