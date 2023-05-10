import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Storijentadoris")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(1200, 400, 350, 170)
        self.setup_ui()

    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('bgpic.jpg')
        background_label.setPixmap(background_pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setScaledContents(True)
        background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)

        password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login)

        signup_button = QPushButton("Sign up", self)
        signup_button.clicked.connect(self.signup)

        layout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(username_label)
        hbox1.addWidget(self.username_input)
        layout.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(password_label)
        hbox2.addWidget(self.password_input)
        layout.addLayout(hbox2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(signup_button)
        layout.addLayout(button_layout)

        # Add background image to layout
        layout.addWidget(background_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()

        if user_data:
            self.close()
            self.windowxx.show()
            
            
            # Open new window here
        else:
            error = QMessageBox()
            error.setWindowTitle("Login Failed")
            error.setText("Invalid username or password.")
            error.setIcon(QMessageBox.Critical)
            error.exec_()

    def signup(self):
        self.signup_window = SignUpWindow()
        self.signup_window.show()


class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(1200, 500, 350, 170)
        self.setup_ui()
    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('bgpic.jpg')
        background_label.setPixmap(background_pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setScaledContents(True)
        background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)

        password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        email_label = QLabel("Email:", self)
        self.email_input = QLineEdit(self)

        signup_button = QPushButton("Sign up", self)
        signup_button.clicked.connect(self.signup)

        layout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(username_label)
        hbox1.addWidget(self.username_input)
        layout.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(password_label)
        hbox2.addWidget(self.password_input)
        layout.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(email_label)
        hbox3.addWidget(self.email_input)
        layout.addLayout(hbox3)

        layout.addWidget(signup_button)
        # Add background image to layout
        layout.addWidget(background_label)

        self.setLayout(layout)


    def signup(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

# create table for storing user information
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT UNIQUE NOT NULL, 
                   password TEXT NOT NULL, 
                   email TEXT UNIQUE NOT NULL)''')
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()

        if not (username and password and email):
            QMessageBox.warning(self, "Error", "Please enter all fields")
            return

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()

        if user_data:
            QMessageBox.warning(self, "Error", "Username already exists")
            return

        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        cursor.execute(query, (username, password, email))
        connection.commit()
        connection.close()

        QMessageBox.information(self, "Success", "Account created successfully")
        self.close()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

        
        
        