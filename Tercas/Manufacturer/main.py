import sys
from PySide6 import QtGui
from PySide6.QtCore import (
    QAbstractTableModel
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtSql import (
    QSqlDatabase,
    QSqlTableModel,
    QSqlQuery
)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()

        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            print(self._data[index.row()][index.column()])
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manufacturers Database")
        self.resize(2000, 1000)

        if not self.create_connection():
            QMessageBox.critical(self, "Error", "Could not connected to database.")
            return 1

        self.table = QTableView()

        data = [
            [4, 6, 9],
            [5, 2, 1],
            [7, 8, 2],
            [2, 3, 5],
            [9, 8, 7]
        ]

        self.model = TableModel(data) 
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

    def create_connection(self):
        return True



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()