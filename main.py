from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit,\
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        edit_action = QAction('Search', self)
        edit_action.triggered.connect(self.search_box)
        edit_menu_item.addAction(edit_action)

        # main window
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_box(self):
        dialog = SearchBox()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedHeight = self.setFixedWidth = 300

        layout = QVBoxLayout()

        # student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # add course widget
        self.course_name = QComboBox()
        courses = ['Biology', 'Astronomy', 'Physics', 'Dishwasher Repair']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile)

        # add submit button
        button = QPushButton('Register')
        layout.addWidget(button)
        button.clicked.connect(self.add_student)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        studentManager.load_data()


class SearchBox(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedHeight = self.setFixedWidth = 300

        layout = QVBoxLayout()

        # defines name to be searched in DB
        self.search_argument = QLineEdit()
        self.search_argument.setPlaceholderText('Name')
        layout.addWidget(self.search_argument)

        button = QPushButton('Search')
        layout.addWidget(button)

        self.setLayout(layout)


app = QApplication(sys.argv)
studentManager = MainWindow()
studentManager.show()
studentManager.load_data()
sys.exit(app.exec())
