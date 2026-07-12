from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QVBoxLayout, QHBoxLayout,
    QWidget,
    QAbstractItemView,
    QStyledItemDelegate,
    QTextEdit,
    QLabel,
    QPushButton
)

import sys

from TableViewDelegates import (
    ButtonDelegate,
    TextEditDelegate
)


DB_HOST_NAME = "217.107.219.91"
DB_USER_NAME = "postgres"
DB_PASSWORD = "monrepo"
DB_DATABASE_NAME = "tercas"
DB_TABLE_NAME = "history.vw_history"

COLUMN_NAME_0 = "ID"
COLUMN_NAME_1 = "Event ID"


class SqlTableModel(QSqlTableModel):
    def __init__(self):
        super().__init__()

        self.setTable(DB_TABLE_NAME)
        
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnRowChange)

        # self.setHeaderData(0, Qt.Orientation.Horizontal, "User ID")
        # self.setHeaderData(3, Qt.Orientation.Horizontal, "User ID")
        # self.setHeaderData(4, Qt.Orientation.Horizontal, "User ID")

        self.select()

        
class TableView(QTableView):
    def __init__(self):
        super().__init__()

        self.model = SqlTableModel()
        self.setModel(self.model)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.resizeColumnsToContents()

        self.setColumnWidth(3, 300)
        self.setColumnWidth(4, 300)

        self.verticalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setStretchLastSection(True)

        self.textEditDelegate = TextEditDelegate()
        self.setItemDelegateForColumn(2, self.textEditDelegate)

        btn = QPushButton("Click Me")
        btn.clicked.connect(lambda: print("Button clicked!"))
        target_index = self.model.index(1, 1)
        self.setIndexWidget(target_index, btn)

        self.buttonDelegate = ButtonDelegate()
        self.setItemDelegateForColumn(6, self.buttonDelegate)

        for row in range(self.model.rowCount()):
            index = self.model.index(row, 6)
            self.openPersistentEditor(index)

        self.selectRow(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = TableView()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)


def createConnection():
    db = QSqlDatabase.addDatabase("QPSQL")

    db.setHostName(DB_HOST_NAME)
    db.setUserName(DB_USER_NAME)
    db.setPassword(DB_PASSWORD)
    db.setDatabaseName(DB_DATABASE_NAME)

    if not db.open():
        QMessageBox.critical(
            None,
            "Histories Example - Error!",
            "Database Error: %s" % db.lastError().databaseText()
        )
        return False
    return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not createConnection():
        sys.exit(1)

    window = MainWindow()
    window.resize(2000, 1200)
    window.show()

    sys.exit(app.exec())