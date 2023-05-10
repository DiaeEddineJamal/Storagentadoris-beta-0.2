from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy,QTextEdit,QFileDialog,QTableWidgetItem,QComboBox,QAction, QDialog, QTableView, QVBoxLayout,QMenu
)
import sqlite3
from PyQt5.QtGui import QIcon, QPixmap,QColor,QStandardItemModel,QStandardItem,QFont
from PyQt5.QtCore import Qt, pyqtSignal,QPropertyAnimation, QRect

import datetime


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the inventory table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER, price REAL, description TEXT, alert_threshold INTEGER, last_stock_in TEXT, last_stock_out TEXT, image_url TEXT)")


class LoginWindow(QWidget):
    login_signal = pyqtSignal(bool)
    

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Marhaba")
        self.setWindowIcon(QIcon("./media/icon.png"))
        self.setGeometry(800, 300, 600, 300)
        self.setFixedSize(700,400)
        self.setup_ui()

    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('./media/log1.jpg')
        background_label.setPixmap(background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        background_label.setAlignment(Qt.AlignCenter)
        username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)

        password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login", self)
        
        

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

      if user_data:
          self.login_signal.emit(True)
          print("login signal emitted")
          MainWindow.show()
          self.close()
          return True
      else:
          error = QMessageBox()
          error.setWindowTitle("Login Failed")
          error.setText("Invalid username or password.")
          error.setIcon(QMessageBox.Critical)
          error.exec_()
          return False

        
    def signup(self):
        self.signup_window = SignUpWindow()
        self.signup_window.show()


class SignUpWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(800, 300, 600, 300)
        self.setFixedSize(700,400)
        self.setup_ui()
    def setup_ui(self):
        # Set background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('./media/logimage.jpg')
        background_label.setPixmap(background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        background_label.setAlignment(Qt.AlignCenter)

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
        self.setWindowTitle("Add stuff to your inventory")
        self.setup_ui()
        self.setGeometry(800, 300, 600, 300)
        self.setWindowIcon(QIcon("./media/icon.png"))

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
        quantity = self.quantity_entry.text()
        price = self.price_entry.text()
        description = self.description_entry.toPlainText()
        alert_threshold = self.alert_entry.text()
        image_url = self.image_button.text()
        last_stock_in = self.last_stock_in_entry.text()
        last_stock_out = self.last_stock_out_entry.text()

     # Check if all required fields are entered
        if not name or not quantity or not price or not alert_threshold or not last_stock_in or not last_stock_out:
           QMessageBox.warning(self, "Empty Fields", "Please enter the fields")
           return

     # Convert the values to the correct data types
        quantity = int(quantity)
        price = float(price)
        alert_threshold = int(alert_threshold)

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
        self.setGeometry(800, 300, 600, 300)
        self.setWindowIcon(QIcon("./media/icon.png"))
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

    # Check if search term is empty
     if not search_term:
        QtWidgets.QMessageBox.warning(self, "Error", "Please enter a search term.")
        return

    # SQL queries
     if search_type == "Name":
        sql = "SELECT * FROM inventory WHERE name LIKE ?"
        val = ("%" + search_term + "%",)
     elif search_type == "Unit Price":
        try:
            float(search_term)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid search term. Please enter a valid number.")
            return
        sql = "SELECT * FROM inventory WHERE price = ?"
        val = (float(search_term),)
     elif search_type == "Quantity":
        try:
            int(search_term)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid search term. Please enter a valid integer.")
            return
        sql = "SELECT * FROM inventory WHERE quantity = ?"
        val = (int(search_term),)
     elif search_type == "Date of Last Stock In":
        # Check if date is valid
        try:
            datetime.strptime(search_term, '%Y-%m-%d')
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid search term. Please enter a date in the format YYYY-MM-DD.")
            return
        sql = "SELECT * FROM inventory WHERE last_stock_in = ?"
        val = (search_term,)
     else:
        self.result_table.setRowCount(0)
        QtWidgets.QMessageBox.warning(self, "Invalid search type", "Please select a valid search type.")
        return

     self.cursor.execute(sql, val)
     rows = self.cursor.fetchall()

    # Set up the table rows
     if not rows:
        self.result_table.setRowCount(0)
        QtWidgets.QMessageBox.information(self, "No results found", "Your search returned no results.")
        return
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




class deletestuff(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("delete inventory")
        self.setGeometry(400, 300, 500, 100)
        self.setGeometry(800, 300, 500, 120)
        
        self.setWindowIcon(QIcon("./media/icon.png"))

        # Define class attributes
        self.name_label = QLabel(self, text="Product Name:")
        self.name_entry = QLineEdit(self)
        self.submit_button = QPushButton(self, text="Delete from Inventory")

        # Set positions for class attributes
        self.name_label.move(10, 10)
        self.name_label.setMinimumHeight(30)
        font=self.name_label.font()
        font.setPointSize(14) 
        self.name_label.setFont(font)

        self.name_entry.move(160, 13)
        self.name_entry.setFixedWidth(200)
        self.name_entry.setMinimumHeight(30)
        
        self.submit_button.move(250, 60)

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
        self.setGeometry(800, 300, 600, 300)
        self.setWindowIcon(QIcon("./media/icon.png"))
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

        # If the result set is empty, display a message to the user
        if len(rows) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The storage is empty.")
            msg.setWindowTitle("Empty storage")
            msg.exec_()
        else:
            # Set the number of rows and columns in the table
            self.result_table.setRowCount(len(rows))
            self.result_table.setColumnCount(len(headers))

            # Loop through each row in the result set and add the data to the table
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(col))
                    header_item = self.result_table.horizontalHeaderItem(j)
                    if header_item and header_item.text() == 'Name':
                        item.setFont(QFont("Arial", 10, QFont.Bold))
                    self.result_table.setItem(i, j, item)

        # Close the database connection
        conn.close()


class Emptystorage(QWidget):
    def __init__(self, ui, parent=None):
        super().__init__(parent)

        self.ui = ui

        # Find the pushButton_8 in the Ui_MainWindow and connect it to the empty_storage function
        self.empty_storage_button = self.ui.pushButton_8
        self.empty_storage_button.clicked.connect(self.empty_storage)

    def empty_storage(self):
        # Create a message box to confirm if the user wants to empty the storage
        confirm_box = QMessageBox()
        confirm_box.setIcon(QMessageBox.Question)
        confirm_box.setText("Are you sure you want to empty the storage?")
        confirm_box.setWindowTitle("Confirmation")
        confirm_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_box.setDefaultButton(QMessageBox.No)

        # Show the confirmation message box and get the user's response
        confirm_response = confirm_box.exec_()

        # If the user clicked "Yes" in the confirmation message box, show another message box to confirm again
        if confirm_response == QMessageBox.Yes:
            confirm_box2 = QMessageBox()
            confirm_box2.setIcon(QMessageBox.Question)
            confirm_box2.setText("Are you really sure you want to empty the storage?")
            confirm_box2.setWindowTitle("Confirmation")
            confirm_box2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm_box2.setDefaultButton(QMessageBox.No)

            # Show the second confirmation message box and get the user's response
            confirm_response2 = confirm_box2.exec_()

            # If the user clicked "Yes" in the second confirmation message box, empty the storage
            if confirm_response2 == QMessageBox.Yes:
                # Connect to the SQLite database and execute the delete query
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()
                cursor.execute("DELETE FROM inventory")
                connection.commit()
                connection.close()

                # Show a success message box
                success_box = QMessageBox()
                success_box.setIcon(QMessageBox.Information)
                success_box.setText("The storage has been emptied successfully.")
                success_box.setWindowTitle("Success")
                success_box.exec_()


class DisplayImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create image label widget
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 450)
        
        # Create combobox widget
        self.combobox = QComboBox(self)
        self.combobox.addItems(['Name'])
        
        # Create search input widget
        self.search_input = QLineEdit(self)
        
        # Create "Display Image" button widget
        self.display_button = QPushButton('Display Image', self)
        self.display_button.clicked.connect(self.display_image_by_name)
        
        # Add widgets to horizontal layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.combobox)
        hbox.addWidget(self.search_input)
        hbox.addWidget(self.display_button)
        
        # Add horizontal layout to vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)

        
    def display_image_by_name(self):
        name = self.search_input.text()
        if name:
            image = get_image_by_name(name)
            pixmap = QPixmap(image).scaled(self.image_label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
        
def get_image_by_name(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT image_url FROM inventory WHERE name=?", (name,))
    image = cursor.fetchone()[0]
    conn.close()
    return image
    

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("Storigentadoris")
        MainWindow.setWindowIcon(QIcon("./media/icon.png"))
        
        MainWindow.setGeometry(500,200,1100,625)
        MainWindow.setFixedSize(1100,625)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
       

    
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage('Disconnected  (please log in to access the database)')
        self.statusbar.move(0, 0)
        MainWindow.setStatusBar(self.statusbar)

        # set the status bar height to 40 pixels
        self.statusbar.setFixedHeight(40)

        # load Minecraft font using QFont
        minecraft_font = QtGui.QFont("Minecraft", 10)

        # set Minecraft font for the status bar
        self.statusbar.setFont(minecraft_font)

        self.statusbar.setStyleSheet("background-color: darkred; color: gainsboro;")



        
        # Get the size of the central widget
        central_size = self.centralwidget.size()

        # Create a QLabel widget to show the GIF
        self.gifLabel = QtWidgets.QLabel(self.centralwidget)
        self.gifLabel.setGeometry(QtCore.QRect(0, 0, 1100, 625))
        self.gifLabel.setObjectName("gifLabel")

        # Set the alignment of the QLabel to center it in the MainWindow
        self.gifLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Load the GIF from a file
        movie = QtGui.QMovie("./media/gif for app.gif")
        self.gifLabel.setMovie(movie)

        # Start the animation
        movie.start()
        
        # Create a QMediaPlayer object to play the music
        self.musicPlayer = QtMultimedia.QMediaPlayer(MainWindow)
        self.musicPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile("./media/bg music.mp3")))

        # Set the volume of the music player
        self.musicPlayer.setVolume(100)

        # Start playing the music
        self.musicPlayer.play()
        
        # Create a QPushButton widget for mute/unmute
        self.muteButton = QtWidgets.QPushButton(self.centralwidget)
        self.muteButton.setGeometry(QtCore.QRect(10, 10, 10, 10))
        self.muteButton.setMinimumSize(QtCore.QSize(20, 20))
        self.muteButton.setObjectName("muteButton")
        self.muteButton.setText("Music🔕")
        
        # Set the size policy and minimum size for the muteButton
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.muteButton.setSizePolicy(sizePolicy)
        self.muteButton.setMinimumSize(QtCore.QSize(20, 20))
        
        # Connect the muteButton to the toggleMute method
        self.muteButton.clicked.connect(self.toggleMute)

       
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 70, 200, 80))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 250, 200, 120))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(280, 250, 200, 120))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 250, 200, 120))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setGeometry(QtCore.QRect(870,250,210,120))

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setGeometry(QtCore.QRect(434,450,263,80))

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setGeometry(QtCore.QRect(870,520,220,50))
        

        # create a new style sheet for disabled buttons
        disabled_style = "QPushButton:disabled { background-color: gray; }"

# set the style sheet for each disabled button
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setStyleSheet(disabled_style)

        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setStyleSheet(disabled_style)

        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setStyleSheet(disabled_style)

        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setStyleSheet(disabled_style)

        self.pushButton_7.setEnabled(False)
        self.pushButton_7.setStyleSheet(disabled_style)

        self.pushButton_8.setEnabled(False)
        self.pushButton_8.setStyleSheet(disabled_style)

        

        
        

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
        
        self.displayimage=DisplayImage()
        self.loginWidget =LoginWindow()
        self.loginWidget.setGeometry(QtCore.QRect(200, 100, 300, 150))
        self.loginWidget.hide()
        self.addstuff=InventoryWindow()
        self.search=SearchProducts()
        self.delete=deletestuff()
        self.display=displayproducts()
        self.emptystorage = Emptystorage(self)
        
         # Connect the button to open the login window
        self.pushButton.clicked.connect(self.open_login_window)
        self.pushButton_3.clicked.connect(self.onAddProductClicked)
        self.pushButton_4.clicked.connect(self.onSearchProductClicked)
        self.pushButton_5.clicked.connect(self.onDeleteProductClicked)
        self.pushButton_6.clicked.connect(self.onDisplayingProductClicked)
        self.pushButton_7.clicked.connect(self.onDisplayingImageClicked)
        
 
        
    def toggleMute(self):
        if self.musicPlayer.volume() == 0:
            # Unmute the music player and restore the original volume
            self.musicPlayer.setVolume(self.originalVolume)
        else:
            # Mute the music player and save the original volume
            self.originalVolume = self.musicPlayer.volume()
            self.musicPlayer.setVolume(0)  
    def open_login_window(self):
        # Create an instance of the LoginWindow class
        self.login_window = LoginWindow()

        # Connect the login_button's clicked signal to the on_login function
        self.login_window.login_button.clicked.connect(self.on_login)

        # Show the login window
        self.login_window.show()
    
    def on_login(self):
     if self.login_window.login():
         self.enable_buttons()
         self.loginWidget.hide()
         self.statusbar.setStyleSheet("background-color: green; color: gainsboro;")
         self.statusbar.showMessage('Connected')
     else:
        # show error message or handle unsuccessful login
         pass
     
     
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Storagentadoris"))
        self.pushButton.setText(_translate("MainWindow", "🗝️ Login || Sign up"))
        self.pushButton_3.setText(_translate("MainWindow", "➕ Add product"))
        self.pushButton_4.setText(_translate("MainWindow", "🔎 Search product"))
        self.pushButton_5.setText(_translate("MainWindow", "🗑️ Delete product"))
        self.pushButton_6.setText(_translate("MainWindow", "📦 Display products"))
        self.pushButton_7.setText(_translate("MainWindow", "🖼️ Display product images"))
        self.pushButton_8.setText(_translate("MainWindow", "Empty storage 🗑"))

    def enable_buttons(self):
        # Enable buttons based on user type
         self.pushButton_3.setEnabled(True)
         self.pushButton_4.setEnabled(True)
         self.pushButton_5.setEnabled(True)
         self.pushButton_6.setEnabled(True)
         self.pushButton_7.setEnabled(True)
         self.pushButton_8.setEnabled(True)

    

    def onLoginSignUpClicked(self):
        # handle login/signup button click
        
        animation = QtCore.QPropertyAnimation(self.resultLabel, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(self.resultLabel.geometry())
        animation.setEndValue(QtCore.QRect(200, 100, 400, 40))
        animation.start()
        self.loginWidget.show()

    
    def onDisplayingImageClicked(self):
        self.displayimage.show()

    def onAddProductClicked(self):
        # handle add product button click
        self.addstuff.show()

    def onSearchProductClicked(self):
        # handle search product button click
        self.search.show()

    def onDeleteProductClicked(self):
        # handle delete product button click
        self.delete.show()

    def onDisplayingProductClicked(self):
        #handle display product button click
        self.display.show()

    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())