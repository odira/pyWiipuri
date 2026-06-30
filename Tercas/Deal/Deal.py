from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QTableView, QStyledItemDelegate, QLCDNumber, QHBoxLayout
from PySide6.QtCore import QCoreApplication, Qt, QAbstractTableModel, QModelIndex
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QMessageBox
from decimal import Decimal
import sys


class PriceDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(2, 2, 2, 2)

        self.lcd = QLCDNumber(editor)
        self.lcd.setDigitCount = 17
        layout.addWidget(self.lcd)

        editor.setFocusProxy(self.lcd)
        
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        lcd = editor.findChild(QLCDNumber)
        if lcd:
            lcd.display("123.45")
    
    def setModelData(self, editor, model, index):
        return super().setModelData(editor, model, index)
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class SqlTableModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        value = super().data(index, role)

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 6 and value is not None:
                try:
                    price = Decimal(value)
                    return f"{price:,.2f}"
                except ValueError:
                    return value
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 6:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        return value
            
            
def init_database():
    db = QSqlDatabase.addDatabase("QPSQL")

    db.setHostName("217.107.219.91")
    db.setDatabaseName("tercas")
    db.setUserName("postgres")
    db.setPassword("monrepo")

    if not db.open():
        print("Database Error: ", db.lastError().text())
        QMessageBox.critical(
            None,
            "App History - Error!",
            "Database Error: %s" % db.lastError().databaseText(),
        )
        sys.exit(-1)
    else:
        print("Connected to the database successfully!")

    return True


def create_model():
    model = SqlTableModel()
    model.setTable("deal.vw_deal")
    model.select()

    return model


if __name__ == '__main__':
    app = QApplication(sys.argv)

    init_database()

    model = create_model()

    view = QTableView()

    priceDelegate = PriceDelegate(view)
    view.setItemDelegateForColumn(6, priceDelegate)

    view.setModel(model)

    layout = QVBoxLayout()
    layout.addWidget(view)

    window = QMainWindow()
    window.setCentralWidget(view)
    window.setWindowTitle("Договоры")
    window.resize(2000, 1000)
    window.show()

    sys.exit(app.exec())


main()
