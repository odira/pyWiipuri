from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QStyledItemDelegate,
    QTextEdit
)

import sys


DB_HOST_NAME = "217.107.219.91"
DB_USER_NAME = "postgres"
DB_PASSWORD = "monrepo"
DB_DATABASE_NAME = "tercas"
DB_TABLE_NAME = "history.vw_history"

COLUMN_NAME_0 = "ID"
COLUMN_NAME_1 = "Event ID"


class TextEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Create a TextEdit when editing starts
        editor = QTextEdit(parent)
        editor.setStyleSheet(
        """
        QTextEdit {
            border: 2px solid #3498db;
            border-radius: 4px;
            background-color: #ffccaa;
        }
        """)
        return editor
    
    def setEditorData(self, editor, index):
        # Load the data from the model into the QTextEdit
        # value = index.model().data(index, Qt.DisplayRole)
        # editor.setPlainText(str(value))

        editor.setText(index.data())
    
    def setModelData(self, editor, model, index):
        # Save the edited text back to the model
        model.setData(index, editor.toPlainText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        # Keep the widget bounds identical to the item cell
        editor.setGeometry(option.rect)


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

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.resizeColumnsToContents()

        self.setColumnWidth(3, 300)
        self.setColumnWidth(4, 300)

        self.verticalHeader().setDefaultSectionSize(100)

        delegate = TextEditDelegate()
        self.setItemDelegateForColumn(3, delegate)



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