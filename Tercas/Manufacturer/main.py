import sys
from PySide6 import QtGui
from PySide6.QtCore import (
    QAbstractTableModel
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView
)
from PySide6.QtCore import Qt


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



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()