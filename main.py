from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
import sys
from PyQt6.QtGui import QAction
import sqlite3


class MainWindow(QMainWindow):
    def __int__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student = QAction("Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu_item.addAction(add_student)

        about = QAction("About", self)
        help_menu_item.addAction(about)
        about.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

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


app = QApplication(sys.argv)
main_app = MainWindow()
main_app.show()
main_app.load_data()
sys.exit(app.exec())
