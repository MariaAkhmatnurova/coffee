import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import sqlite3
from PyQt5.QtCore import QTimer


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.initUI()

    def initUI(self):
        QTimer.singleShot(0, self.showCoffeeData)
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
        VALUES ('Арабика', 'Средняя', 'В зернах', 'Нежный и фруктовый', 750, 250),
       ('Робуста', 'Темная', 'Молотый', 'Крепкая и смелая', 600, 500),
       ('Эфиопский Иргачиффе', 'Легкая', 'В зернах', 'Цитрусовый и цветочный', 900, 200);
        ;""")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    sys.exit(app.exec_())