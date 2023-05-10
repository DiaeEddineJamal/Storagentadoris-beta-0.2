from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy,QTextEdit,QFileDialog,QTableWidgetItem
)
import sqlite3
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class LoginWindow(QWidget):
    login_signal = pyqtSignal(bool)

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Storijentadoris")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(630,430, 650, 350)
        self.setFixedSize(700,400)
        self.setup_ui()


        self.login_button.clicked.connect(self.login)
    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('ddd.jpg')
        background_label.setPixmap(background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        background_label.setAlignment(Qt.AlignCenter)
        username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)

        password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        

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
        button_layout.addWidget(self.login_button)
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

        if username == 'papoudo' and password == 'cojones':

            self.login_signal.emit(True)
            print("admin signal received")

            
            MainWindow.show()
            self.close()

        elif user_data:
            self.login_signal.emit(False)
            print("login signal emitted")
            MainWindow.show()
            self.close()
            # Open new window here
            
        else:
            error = QMessageBox()
            error.setWindowTitle("Login Failed")
            error.setText("Invalid username or password.")
            error.setIcon(QMessageBox.Critical)
            error.exec_()
            self.close()
        
    def signup(self):
        self.signup_window = SignUpWindow()
        self.signup_window.show()


class SignUpWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(600, 400, 600, 300)
        self.setFixedSize(700,400)
        self.setup_ui()
    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('bgpic.jpg')
        background_label.setPixmap(background_pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setFixedSize(700,400)

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
        
class InventoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de stock")
        self.setup_ui()

    def setup_ui(self):
        # Create the input fields

        layout = QVBoxLayout()
        name_label = QLabel("Product Name:")
        layout.addWidget(name_label)
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_entry)

        quantity_label = QLabel("Quantity:")
        layout.addWidget(quantity_label)
        self.quantity_entry = QLineEdit()
        layout.addWidget(self.quantity_entry)

        price_label = QLabel("Price:")
        layout.addWidget(price_label)
        self.price_entry = QLineEdit()
        layout.addWidget(self.price_entry)

        description_label = QLabel("Description:")
        layout.addWidget(description_label)
        self.description_entry = QTextEdit()
        layout.addWidget(self.description_entry)

        alert_label = QLabel("Alert Threshold:")
        layout.addWidget(alert_label)
        self.alert_entry = QLineEdit()
        layout.addWidget(self.alert_entry)
        
        #image stuff
        image_layout= QHBoxLayout()
        self.image_button = QPushButton("Select Image")
        self.image_button.clicked.connect(self.select_image)
        image_layout.addWidget( self.image_button)

        #•add layout to main layout
        
        layout.addLayout(image_layout)


        last_stock_in_label = QLabel("Last Stock In (YYYY-MM-DD HH:MM:SS):")
        layout.addWidget(last_stock_in_label)
        self.last_stock_in_entry = QLineEdit()
        layout.addWidget(self.last_stock_in_entry)

        last_stock_out_label = QLabel("Last Stock Out (YYYY-MM-DD HH:MM:SS):")
        layout.addWidget(last_stock_out_label)
        self.last_stock_out_entry = QLineEdit()
        layout.addWidget(self.last_stock_out_entry)

        # Create the submit button
        submit_button = QPushButton("Add Inventory")
        submit_button.clicked.connect(self.add_inventory)
        layout.addWidget(submit_button)

        # Set the layout for the window
        self.setLayout(layout)
        submit_button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: #2196F3;
            min-width: 10em;
            padding: 6px;
        """)
    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg)")
        file_dialog.selectNameFilter("Image files (*.png *.jpg)")
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.image_button.setText(file_path)
    def add_inventory(self):
        # Connect to the SQLite3 database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Prompt the user to enter inventory data
        name = self.name_entry.text()
        quantity = int(self.quantity_entry.text())
        price = float(self.price_entry.text())
        description = self.description_entry.toPlainText()
        alert_threshold = int(self.alert_entry.text())
        image_url = self.image_button.text()
        last_stock_in = self.last_stock_in_entry.text()
        last_stock_out = self.last_stock_out_entry.text()

        # Insert the inventory data into the database
        sql = "INSERT INTO inventory (name, quantity, price, description, alert_threshold, last_stock_in, last_stock_out, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        val = (name, quantity, price, description, alert_threshold, last_stock_in, last_stock_out, image_url)
        cursor.execute(sql, val)

        # Commit the changes to the database
        conn.commit()

        # Show a message box to indicate that the data was inserted successfully
        QMessageBox.information(self, "Success", f"{cursor.rowcount} record(s) inserted.")

        # Close the connection to the database
        conn.close()

class SearchProducts(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(900,300,950,300)
        # Connect to the SQLite3 database
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Set up the GUI widgets
        self.search_type_label = QtWidgets.QLabel("Search Type:")
        self.search_type_combobox = QtWidgets.QComboBox()
        self.search_type_combobox.addItem("Name")
        self.search_type_combobox.addItem("Unit Price")
        self.search_type_combobox.addItem("Quantity")
        self.search_type_combobox.addItem("Date of Last Stock In")
        self.search_term_label = QtWidgets.QLabel("Search Term:")
        self.search_term_entry = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("Search")
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(["Name", "Description", "Unit Price", "Quantity in Stock", "Stock Alert Threshold", "Date Last Stock In", "Date Last Stock Out", "Image"])

        # Set up the GUI layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.search_type_label, 0, 0)
        layout.addWidget(self.search_type_combobox, 0, 1)
        layout.addWidget(self.search_term_label, 1, 0)
        layout.addWidget(self.search_term_entry, 1, 1)
        layout.addWidget(self.search_button, 2, 0, 1, 2)
        layout.addWidget(self.result_table, 3, 0, 1, 2)
        self.setLayout(layout)

        # Connect the search button to the search_products method
        self.search_button.clicked.connect(self.search_products)

    def search_products(self):
        # Get the search type and search term from the GUI widgets
        search_type = self.search_type_combobox.currentText()
        search_term = self.search_term_entry.text()

        # SQL queries
        if search_type == "Name":
            sql = "SELECT * FROM inventory WHERE name LIKE ?"
            val = ("%" + search_term + "%",)
        elif search_type == "Unit Price":
            sql = "SELECT * FROM inventory WHERE unit_price = ?"
            val = (float(search_term),)
        elif search_type == "Quantity":
            sql = "SELECT * FROM inventory WHERE quantity_in_stock = ?"
            val = (int(search_term),)
        elif search_type == "Date of Last Stock In":
            sql = "SELECT * FROM inventory WHERE date_last_stock_in = ?"
            val = (search_term,)
        else:
            self.result_table.setRowCount(0)
            QtWidgets.QMessageBox.warning(self, "Invalid search type", "Please select a valid search type.")
            return

        self.cursor.execute(sql, val)
        rows = self.cursor.fetchall()

        # Check for empty search results
        if not rows:
            self.result_table.setRowCount(0)
            QtWidgets.QMessageBox.information(self, "No results found", "Your search returned no results.")
            return

        # Set up the table rows
        self.result_table.setRowCount(len(rows))
        self.result_table.setColumnCount(len(rows[0])) # set number of columns based on result set
        header_labels = [description[0] for description in self.cursor.description] # get header labels from cursor description
        self.result_table.setHorizontalHeaderLabels(header_labels) # set header labels
        for i, row in enumerate(rows):
         for j, val in enumerate(row):
            if j == 3: # format unit price as currency
              item = QtWidgets.QTableWidgetItem("${:,.2f}".format(val))
            else:
              item = QtWidgets.QTableWidgetItem(str(val))
            self.result_table.setItem(i, j, item)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the inventory table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER, price REAL, description TEXT, alert_threshold INTEGER, last_stock_in TEXT, last_stock_out TEXT, image_url TEXT)")

class deletestuff(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de stock")
        self.setGeometry(300, 200, 400, 100)
        

        # Define class attributes
        self.name_label = QLabel(self, text="Product Name:")
        self.name_entry = QLineEdit(self)
        self.submit_button = QPushButton(self, text="Delete Inventory")

        # Set positions for class attributes
        self.name_label.move(10, 10)
        self.name_entry.move(150, 10)
        self.submit_button.move(250, 40)

        # Create the submit button
        self.submit_button.clicked.connect(self.delete_inventory)

        

    def delete_inventory(self):
        # Prompt the user to enter the name of the product to be deleted
        name = self.name_entry.text()

        # Delete the inventory data from the database
        sql = "DELETE FROM inventory WHERE name = ?"
        val = (name,)
        cursor.execute(sql, val)

        # Commit the changes to the database
        conn.commit()

        # Show a message box to indicate that the data was deleted successfully
        QMessageBox.information(self, "Success", f"{cursor.rowcount} record(s) deleted.")

class displayproducts(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(900, 300, 950, 300)
        # Connect to the SQLite3 database
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Set up the GUI widgets
        self.search_button = QtWidgets.QPushButton("Display all products")
        self.result_table = QtWidgets.QTableWidget()

        # Set up the GUI layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.search_button, 2, 0, 1, 2)
        layout.addWidget(self.result_table, 3, 0, 1, 2)
        self.setLayout(layout)

        # Connect the search button to the search_products method
        self.search_button.clicked.connect(self.display_products)

    def display_products(self):
        # Set up the table headers
        headers = ['id','Name', 'Description', 'Unit Price', 'Quantity in Stock', 'Stock Alert Threshold', 'Date Last Stock In', 'Date Last Stock Out', 'Image']
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)

        # Connect to the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Execute a SELECT query to retrieve all products
        c.execute('SELECT * FROM inventory')
        rows = c.fetchall()

        # Set the number of rows and columns in the table
        self.result_table.setRowCount(len(rows))
        self.result_table.setColumnCount(len(headers))

        # Loop through each row in the result set and add the data to the table
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                header_item = self.result_table.horizontalHeaderItem(j)
                if header_item and header_item.text() == 'Name':
                    item.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                self.result_table.setItem(i, j, item)

        # Close the database connection
        conn.close()
 
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        MainWindow.setGeometry(500,400,1100,600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
       
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 220, 131, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330, 131, 28))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 450, 131, 28))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setGeometry(QtCore.QRect(20,560,131,28))
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 80, 121, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        
        
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(170, 0, 20, 571))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
        # add a label widget to display results
        self.resultLabel = QtWidgets.QLabel(self.centralwidget)
        self.resultLabel.setGeometry(QtCore.QRect(200, 50, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        with open("style for the main.css", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
        self.resultLabel.setFont(font)
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.resultLabel.setObjectName("resultLabel")
        # Create a QLabel widget to show the GIF
        self.gifLabel = QtWidgets.QLabel(self.centralwidget)
        self.gifLabel.setGeometry(QtCore.QRect(180, 0, 920, 600))
        self.gifLabel.setObjectName("gifLabel")

        # Load the GIF from a file
        movie = QtGui.QMovie("gif for app.gif")
        self.gifLabel.setMovie(movie)

        # Start the animation
        movie.start()
        
        self.loginWidget =LoginWindow()
        self.loginWidget.setGeometry(QtCore.QRect(200, 100, 300, 150))
        self.loginWidget.hide()
        self.addstuff=InventoryWindow()
        self.search=SearchProducts()
        self.delete=deletestuff()
        self.display=displayproducts()
         # connect button signals to slots
        self.pushButton.clicked.connect(self.on_login)
        self.pushButton_3.clicked.connect(self.onAddProductClicked)
        self.pushButton_4.clicked.connect(self.onSearchProductClicked)
        self.pushButton_5.clicked.connect(self.onDeleteProductClicked)
        self.pushButton_6.clicked.connect(self.onDisplayingProductClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Login || Sign up"))
        self.pushButton_3.setText(_translate("MainWindow", "Add product"))
        self.pushButton_4.setText(_translate("MainWindow", "Search product"))
        self.pushButton_5.setText(_translate("MainWindow", "Delete product"))
        self.pushButton_6.setText(_translate("MainWindow", "Display products"))
    def enable_buttons(self, is_admin):
        # Enable buttons based on user type
         self.pushButton_3.setEnabled(True)
         self.pushButton_4.setEnabled(True)
         self.pushButton_5.setEnabled(True)
         self.pushButton_6.setEnabled(True)
    def onLoginSignUpClicked(self):
        # handle login/signup button click
        
        animation = QtCore.QPropertyAnimation(self.resultLabel, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(self.resultLabel.geometry())
        animation.setEndValue(QtCore.QRect(200, 100, 400, 40))
        animation.start()
        self.loginWidget.show()
    def on_login(self, is_admin):
        self.enable_buttons(is_admin)
        self.loginWidget.show()
        

    def onAddProductClicked(self):
        # handle add product button click
        self.resultLabel.setText("Add product clicked")
        self.addstuff.show()

    def onSearchProductClicked(self):
        # handle search product button click
        self.resultLabel.setText("Search product clicked")
        self.search.show()

    def onDeleteProductClicked(self):
        # handle delete product button click
        self.resultLabel.setText("Delete product clicked")
        self.delete.show()

    def onDisplayingProductClicked(self):
        #handle display product button click
        self.resultLabel.setText("Display product clicked")
        self.display.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
