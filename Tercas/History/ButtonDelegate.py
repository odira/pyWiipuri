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


class ButtonDelegate(QStyledItemDelegate):
    button_clicked = Signal(QSqlTableModel)

    def createEditor(self, parent, option, index):
        # Create a container widget and a QPushButton
        self.editor = QWidget(parent)
        self.layout = QHBoxLayout(self.editor) 
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton("Click me", self.editor)
        self.button.clicked.connect(lambda: self.button_clicked.emit(index))

        self.layout.addWidget(self.button)
        self.editor.setLayout(self.layout)

        return self.editor

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)