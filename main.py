import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog, QLabel, QLineEdit, QTextEdit
from PyQt5.uic import loadUi
import sqlite3
from PyQt5.QtCore import QTimer


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id
        self.initUI()

    def initUI(self):
        if self.coffee_id is not None:
            self.setWindowTitle("Редактирование записи о кофе")
            self.load_coffee_data()
            self.saveButton.clicked.connect(self.edit_coffee)
        else:
            self.setWindowTitle("Добавление записи о кофе")
            self.saveButton.clicked.connect(self.add_coffee)

        self.show()

    def load_coffee_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM coffee WHERE id={self.coffee_id}")
        coffee_data = cursor.fetchone()
        connection.close()

        if coffee_data:
            self.nameEdit.setText(coffee_data[1])
            self.roastEdit.setText(coffee_data[2])
            self.groundOrWholeEdit.setText(coffee_data[3])
            self.flavorDescriptionEdit.setText(coffee_data[4])
            self.priceEdit.setText(str(coffee_data[5]))
            self.packagingVolumeEdit.setText(str(coffee_data[6]))

    def add_coffee(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        ground_or_whole = self.groundOrWholeEdit.text()
        flavor_description = self.flavorDescriptionEdit.text()
        price = float(self.priceEdit.text())
        packaging_volume = int(self.packagingVolumeEdit.text())

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, packaging_volume) "
                       "VALUES (?, ?, ?, ?, ?, ?)", (name, roast, ground_or_whole, flavor_description, price, packaging_volume))
        connection.commit()
        connection.close()

        self.accept()

    def edit_coffee(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        ground_or_whole = self.groundOrWholeEdit.text()
        flavor_description = self.flavorDescriptionEdit.text()
        price = float(self.priceEdit.text())
        packaging_volume = int(self.packagingVolumeEdit.text())

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("UPDATE coffee SET name=?, roast_degree=?, ground_or_whole=?, flavor_description=?, price=?, packaging_volume=? "
                       "WHERE id=?", (name, roast, ground_or_whole, flavor_description, price, packaging_volume, self.coffee_id))
        connection.commit()
        connection.close()

        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.initUI()

    def initUI(self):
        QTimer.singleShot(0, self.showCoffeeData)
        self.edit_button.clicked.connect(self.open_add_edit_form)
        self.show()

    def showCoffeeData(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS coffee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roast_degree TEXT NOT NULL,
        ground_or_whole TEXT NOT NULL,
        flavor_description TEXT NOT NULL,
        price REAL NOT NULL,
        packaging_volume INTEGER NOT NULL
        );''')
        cursor.execute("""INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, packaging_volume)
            VALUES ('Arabica', 'Medium', 'Whole', 'Delicate and fruity', 15.99, 250);""")

        cursor.execute("""INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, packaging_volume)
            VALUES ('Robusta', 'Dark', 'Ground', 'Strong and bold', 12.99, 500);""")

        cursor.execute("""INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, packaging_volume)
            VALUES ('Ethiopian Yirgacheffe', 'Light', 'Whole', 'Citrusy and floral', 18.99, 200);""")
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()
        connection.close()

        for row in coffee_data:
            self.textBrowser.append(f"ID: {row[0]}\n"
                                    f"Название: {row[1]}\n"
                                    f"Степень обжарки: {row[2]}\n"
                                    f"Молотый/в зернах: {row[3]}\n"
                                    f"Описание вкуса: {row[4]}\n"
                                    f"Цена: {row[5]}\n"
                                    f"Объем упаковки: {row[6]}\n"
                                    "-------------------------")

    def open_add_edit_form(self, coffee_id=None):
        form = AddEditCoffeeForm(self, coffee_id)
        if form.exec_() == QDialog.Accepted:
            self.showCoffeeData()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    sys.exit(app.exec_())