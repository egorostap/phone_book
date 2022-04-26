import sqlite3
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import ui_login
import ui_reg
import ui_interface

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT PRIMARY KEY,
    password TEXT,
    date DATE
)''')
# cursor.execute('INSERT INTO users (login, password) VALUES ("admin", "admin")')
# cursor.execute('DELETE FROM users')
cursor.execute('SELECT * FROM users')
db.commit()

for i in cursor.execute('SELECT * FROM users'):
    print(i)

'''registratoin'''
class Registration(ui_reg.QtWidgets.QWidget, ui_reg.Ui_Form):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('Регистрация')
        self.setWindowTitle('Регистрация')
        self.lineEdit_2.setPlaceholderText('Логин:')
        self.lineEdit_3.setPlaceholderText('Пароль:')
        self.lineEdit_4.setPlaceholderText('Повторите пароль:')
        # print('class registration')

        self.pushButton.pressed.connect(self.reg)
        self.pushButton_2.pressed.connect(self.cancel)
        # self.pushButton_2.pressed.connect(self.close)


    def cancel(self):
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.dateEdit.clear()


    def reg(self):
        user_login = self.lineEdit_2.text()
        user_password = self.lineEdit_3.text()
        user_password_check = self.lineEdit_4.text()
        date = self.dateEdit.text()

        # print(user_login, user_password)
        if len(user_login) == 0:
            return
        if len(user_password) == 0:
            return
        if user_password != user_password_check:
            self.label.setText('Пароли не совпадают!')
            return
        cursor.execute(f'''SELECT login FROM users WHERE login="{user_login}"''')
        if cursor.fetchone() is None:
            cursor.execute(f'''INSERT INTO users (login, password, date) VALUES ("{user_login}", "{user_password}", "{date}")''')
            self.label.setText('''Успешно зарегистрирован!''')
            db.commit()
        else:
            self.label.setText('Уже зарегистрирован!')

''' login'''
class Login(ui_login.QtWidgets.QWidget, ui_login.Ui_Form):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('Логин')
        self.setWindowTitle('Вход')
        self.lineEdit_2.setPlaceholderText('Логин:')
        self.lineEdit_3.setPlaceholderText('Пароль:')
        # print('class login')

        self.pushButton.pressed.connect(self.login)
        self.pushButton_3.pressed.connect(self.reg)
        self.pushButton_2.pressed.connect(self.cancel)
        # self.label_2.pressed.connect(self.cancel)

    def cancel(self):
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

    def reg(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    def interface(self):
        self.interface = Interface()
        self.interface.show()
        self.interface.create_db()
        self.hide()

    # выполняет вход
    def login(self):
        user_login = self.lineEdit_2.text()
        user_password = self.lineEdit_3.text()
        # print(user_login, user_password)
        if len(user_login) == 0:
            return
        if len(user_password) == 0:
            return
        # ищет пароль у пользователя с введенным логином
        cursor.execute(f'SELECT password FROM users WHERE login="{user_login}"')
        check_pass = cursor.fetchall()
        # print(check_pass)
        # ищет пользователя с введенным логином
        cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        check_login = cursor.fetchall()
        # print(check_login)
        # проверяет совпадает ли пароль
        if len(check_pass) != 0 and len(check_login) != 0 and check_pass[0][0] == user_password and check_login[0][0] == user_login:
            self.label.setText('Успешная авторизация!')
            self.interface()
        else:
            self.label.setText('Ошибка авторизации!')


class Interface(ui_interface.QtWidgets.QMainWindow, ui_interface.Ui_MainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Записная книжка')
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def create_db(self):
        with sqlite3.connect('database_phone.db') as connect:
            cursor = connect.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS phone_list(
                        name TEXT PRIMARY KEY,
                        phone TEXT,
                        date DATE
                    )''')
            # cursor.execute('INSERT INTO phone_list (name, phone, date) VALUES ("man", "123123123", "21.12.2112")')
            cursor.execute('SELECT * FROM phone_list')
            connect.commit()
            check = cursor.fetchall()
            print(check)
            if check:
                self.fill()

    def fill(self):
        self.table_widget.clear()
        print('фил работает')
        labels = ['Имя', 'Телефон', 'Дата рождения']

        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        with sqlite3.connect('database_phone.db') as connect:

            for name, phone, date in connect.execute("SELECT name, phone, date FROM phone_list"):
                row = self.table_widget.rowCount()
                self.table_widget.setRowCount(row + 1)

                self.table_widget.setItem(row, 0, QTableWidgetItem(str(name)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(phone))
                self.table_widget.setItem(row, 2, QTableWidgetItem(date))


App = ui_login.QtWidgets.QApplication([])
window = Login()
window.show()
App.exec()
