import sqlite3
from PyQt5 import QtWidgets
from ui import *

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    password TEXT
)''')

cursor.execute('SELECT * FROM users')
db.commit()

for i in cursor.execute('SELECT * FROM users'):
    print(i)

class Registration(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('Регистрация')

        self.pushButton.pressed.connect(self.reg)
        self.pushButton_3.pressed.connect(self.login)

    def login(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def reg(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        if len(user_login) == 0:
            return
        if len(user_password) == 0:
            return
        cursor.execute(f'''SELECT login FROM users WHERE login="{user_login}"''')
        if cursor.fetchone() is None:
            cursor.execute(f'''INSERT INTO users VALUES ("{user_login}", "{user_password}")''')
            self.label.setText(f'''Аккаунт {user_login} успешно зарегистрирован!''')
            db.commit()
        else:
            self.label.setText('Такая запись уже имеется!')

class Login(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('Логин')

        self.pushButton.pressed.connect(self.login)
        self.pushButton_3.pressed.connect(self.reg)


    def reg(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    # выполняет вход
    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        if len(user_login) == 0:
            return
        if len(user_password) == 0:
            return
        # ищет пароль у пользователя с введенным логином
        cursor.execute(f'SELECT password FROM users WHERE login="{user_login}"')
        check_pass = cursor.fetchall()
        # ищет пользователя с введенным логином
        cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        check_login = cursor.fetchall()
        # проверяет совпадает ли пароль
        if check_pass[0][0] == user_password and check_login[0][0] == user_login:
            self.label.setText('Успешная авторизация!')
        else:
            self.label.setText('Ошибка авторизации!')


App = QtWidgets.QApplication([])
window = Login()
# window = Registration()
window.show()
App.exec()
