import sys
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QAbstractItemView
)


TABLE_NAME = "history.vw_history"


class SqlTableModel(QSqlTableModel):
    def __init__(self):
        super().__init__()

        self.setTable(TABLE_NAME)
        
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnRowChange)

        # self.setHeaderData(3, Qt.Orientation.Horizontal, "User ID")
        # self.setHeaderData(4, Qt.Orientation.Horizontal, "User ID")

        self.select()


class TableView(QTableView):
    def __init__(self):
        super().__init__()

        self.model = SqlTableModel()
        self.setModel(self.model)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.resizeColumnsToContents()

        self.setColumnWidth(3, 300)
        self.setColumnWidth(4, 300)



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

    db.setHostName("217.107.219.91")
    db.setPassword("monrepo")
    db.setUserName("postgres")
    db.setDatabaseName("tercas")

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