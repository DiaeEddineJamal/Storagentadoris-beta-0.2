import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QSizePolicy,QTextEdit,QFileDialog,
)
import sqlite3
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
class display(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()
        self.setGeometry(900,300,950,300)
        # Connect to the SQLite3 database
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Set up the GUI widgets
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(["Name", "Description", "Unit Price", "Quantity in Stock", "Stock Alert Threshold", "Date Last Stock In", "Date Last Stock Out", "Image"])

        
        



    def display(self):
        # Get the search type and search term from the GUI widgets
        

        # SQL queries
        
        sql = "SELECT * FROM inventory WHERE name LIKE ?"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
           
        
            

         

        # Check for empty search results
        if not rows:
            self.result_table.setRowCount(0)
            QtWidgets.QMessageBox.information(self, "No results found")
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = display()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
