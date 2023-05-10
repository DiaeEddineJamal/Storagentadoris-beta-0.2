import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox

app = QApplication(sys.argv)

# create a main window instance
window = QMainWindow()

# Connect to the SQLite3 database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the inventory table if it does not exist
cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER, price REAL, description TEXT, alert_threshold INTEGER, last_stock_in TEXT, last_stock_out TEXT, image_url TEXT)")

# Create the PyQt window
class MainWindow(QMainWindow):
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

        # Show the window
        self.show()

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

window = MainWindow()
sys.exit(app.exec_())
