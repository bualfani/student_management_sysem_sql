from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar
import sys
from PyQt6.QtGui import QAction, QIcon
import sqlite3
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __int__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu(("&Edit"))

        add_student = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu_item.addAction(add_student)

        about = QAction("About", self)
        help_menu_item.addAction(about)
        about.setMenuRole(QAction.MenuRole.NoRole)

        search = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search)
        search.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Toolbar and add element
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student)
        toolbar.addAction(search)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        # reset the table
        self.table.setRowCount(0)

        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.table.setItem(row_num, column_num, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

class  InsertDialog(QDialog):
    def __int__(self):
        super().__int__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics", "Gym", "French", "Art", "English"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Phone Number widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Submit button
        button = QPushButton()
        button.clicked.connect(self.add_student)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO student (name, course, mobile) VALUE (?, ?, ?)",
                       (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        main_app.load_data()

class SearchDialog(QDialog):
    def __int__(self):
        super().__int__()
        # Window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(3000)
        self.setFixedHeight(300)

        # Layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Button
        button = QPushButton('Search')
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM student WHERE name = ?", (name, ))
        rows = list(result)
        items = main_app.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_app.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()



app = QApplication(sys.argv)
main_app = MainWindow()
main_app.show()
main_app.load_data()
sys.exit(app.exec())
