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
        # editor.setText(index.data())
        pass

    def setModelData(self, editor, model, index):
        pass

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


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