import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QVBoxLayout


class InventoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de stock")
        self.setStyleSheet("""
            * {
                font-family: Arial;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QPushButton {
                background-color: #005fec;
                border: none;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #003c9b;
            }
        """)
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

        image_label = QLabel("Image URL:")
        layout.addWidget(image_label)
        self.image_entry = QLineEdit()
        layout.addWidget(self.image_entry)

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
        image_url = self.image_entry.text()
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


if __name__ == '__main__':
    # Create the PyQt5 application
    app = QApplication([])
    inventory_window = InventoryWindow()
    inventory_window.show()

    # Run the PyQt5 event loop
    app.exec_()
