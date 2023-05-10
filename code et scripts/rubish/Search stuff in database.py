import sqlite3
from PyQt5 import  QtCore, QtGui
import PyQt5.QtWidgets as QtWidgets


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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = SearchProducts()
    window.show()
    app.exec_()
