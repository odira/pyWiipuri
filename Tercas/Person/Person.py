from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableView
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import QSqlDatabase, QSqlTableModel

import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QPSQL")

    db.setHostName("217.107.219.91")
    db.setDatabaseName("tercas")
    db.setUserName("postgres")
    db.setPassword("monrepo")

    if not db.open():
        print("Database Error: ", db.lastError().text())
        sys.exit(-1)
    else:
        print("Connected to the database successfully!")

    model = QSqlTableModel()
    model.setTable("person.person")
    model.select()

    view = QTableView()
    view.setModel(model)

    layout = QVBoxLayout()
    layout.addWidget(view)

    window = QMainWindow()
    window.setCentralWidget(view)
    window.setWindowTitle("Контакты")
    window.resize(2000, 1000)
    window.show()

    sys.exit(app.exec())


main()
