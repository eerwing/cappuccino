import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class Show_Coffee_Widget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Виды кофе')
        self.con = sqlite3.connect("coffee.db")
        info = list(map(list, self.con.cursor().execute("SELECT * FROM info").fetchall()))
        self.tableWidget.setRowCount(len(info))
        self.tableWidget.setColumnCount(len(info[0]))
        for i, row in enumerate(info):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'sort', 'roasting', 'ground/grain', 'taste', 'price', 'packaging volume'])
        self.tableWidget.resizeColumnsToContents()
        self.change_button.clicked.connect(self.open_change_coffee)
        self.add_button.clicked.connect(self.open_add_coffee)

    def update(self):
        info = list(map(list, self.con.cursor().execute("SELECT * FROM info").fetchall()))
        self.tableWidget.setRowCount(len(info))
        self.tableWidget.setColumnCount(len(info[0]))
        for i, row in enumerate(info):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'sort', 'roasting', 'ground/grain', 'taste', 'price', 'packaging volume'])
        self.tableWidget.resizeColumnsToContents()

    def open_change_coffee(self):
        if list(set([i.row() for i in self.tableWidget.selectedItems()])):
            self.to_change = list(set([i.row() for i in self.tableWidget.selectedItems()]))[0]
            self.window_show = Change_Coffee(self.to_change)
            self.window_show.show()
        else:
            self.not_aligned.setText('Выделите запись в таблице')

    def open_add_coffee(self):
        self.window_show = Add_Coffee()
        self.window_show.show()


class Change_Coffee(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Редактирование кофе')
        self.con = sqlite3.connect("coffee.db")
        self.sort.addItems(['Арабика', 'Робуста', 'Либерика', 'Эксцельза'])
        self.roasting.addItems(['светлая', 'средняя', 'темная'])
        self.type.addItems(['молотый', 'зерновой'])
        self.row = args[0]
        self.info = (self.con.cursor().execute("SELECT * FROM info").fetchall())[self.row]
        self.sort.setCurrentIndex(['Арабика', 'Робуста', 'Либерика', 'Эксцельза'].index(self.info[1]))
        self.roasting.setCurrentIndex(['светлая', 'средняя', 'темная'].index(self.info[2]))
        self.type.setCurrentIndex(['молотый', 'зерновой'].index(self.info[3]))
        self.taste.setText(str(self.info[4]))
        self.price.setText(str(self.info[5]))
        self.volume.setText(str(self.info[6]))
        self.button.setText("Отредактировать")
        self.button.clicked.connect(self.change)

    def change(self):
        if self.taste.text() != '' and self.price.text() != '' and self.volume.text() != '':
            self.con.cursor().execute(f"DELETE FROM info WHERE id = {self.row + 1}")
            self.con.commit()
            insert = [self.row + 1, self.sort.currentText(), self.roasting.currentText(), self.type.currentText(), self.taste.text(), self.price.text(), self.volume.text()]
            self.con.cursor().execute(f"INSERT INTO info(id, sort, roasting, ground_or_grain, taste, price, packaging_volume) VALUES (?, ?, ?, ?, ?, ?, ?)", insert)
            self.con.commit()
            form.update()
            self.close()
        else:
            self.error.setText('Неверно заполнена форма')


class Add_Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Добавить кофе')
        self.con = sqlite3.connect('coffee.db')
        self.sort.addItems(['Арабика', 'Робуста', 'Либерика', 'Эксцельза'])
        self.roasting.addItems(['светлая', 'средняя', 'темная'])
        self.type.addItems(['молотый', 'зерновой'])
        self.button.setText('Добавить')
        self.button.clicked.connect(self.add)

    def add(self):
        if self.taste.text() != '' and self.price.text() != '' and self.volume.text() != '':
            insert = [self.sort.currentText(), self.roasting.currentText(), self.type.currentText(), self.taste.text(), self.price.text(), self.volume.text()]
            self.con.cursor().execute(f"INSERT INTO info(sort, roasting, ground_or_grain, taste, price, packaging_volume) VALUES (?, ?, ?, ?, ?, ?)", insert)
            self.con.commit()
            form.update()
            self.close()
        else:
            self.error.setText('Неверно заполнена форма')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    form = Show_Coffee_Widget()
    form.show()
    sys.exit(app.exec())