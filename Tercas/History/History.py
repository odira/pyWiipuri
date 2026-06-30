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
    QWidget
)


class TableView(QTableView):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel(self)
        self.model.setTable("history.vw_history")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnRowChange)
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "User ID")
        self.model.select()

        self.setModel(self.model)
        self.resizeColumnsToContents()
        self.setColumnWidth(3, 1000)
        #self.setSelectionBehavior(QSqlTableModel.selectRow())


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
    window.show()

    sys.exit(app.exec())