from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit,\
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction(
            QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
        search_action.triggered.connect(self.search_box)
        edit_menu_item.addAction(search_action)

        # main window
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # creates toolbar and adds elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create status bar and add status bar element
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # detect cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)

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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

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
        self.close()
        main_window.load_data()


class SearchBox(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Students')
        self.setFixedHeight = self.setFixedWidth = 300

        layout = QVBoxLayout()

        # defines name to be searched in DB
        self.search_argument = QLineEdit()
        self.search_argument.setPlaceholderText('Name')
        layout.addWidget(self.search_argument)

        button = QPushButton('Search')
        layout.addWidget(button)

        self.setLayout(layout)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # get student record from DB
        rowIndex = main_window.table.currentRow()

        # get student id

        self.student_id = main_window.table.item(rowIndex, 0).text()

        # get student name from record
        student_name = main_window.table.item(rowIndex, 1).text()

        # student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # course widget
        course_name = main_window.table.item(rowIndex, 2).text()
        self.course_name = QComboBox()
        courses = ['Biology', 'Astronomy', 'Physics', 'Dishwasher Repair']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # mobile widget
        mobile_number = main_window.table.item(rowIndex, 3).text()
        self.mobile_number = QLineEdit(mobile_number)
        self.mobile_number.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile_number)

        # submit button
        button = QPushButton('Update')
        layout.addWidget(button)
        button.clicked.connect(self.update_student)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?', (
                self.student_name.text(),
                self.course_name.itemText(self.course_name.currentIndex()),
                self.mobile_number.text(),
                self.student_id
            )
        )
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student Data')

        layout = QGridLayout()

        confirmation = QLabel('Are you sure?')
        positive_confirmation = QPushButton('Yes')
        negative_confirmation = QPushButton('No')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(positive_confirmation, 1, 0)
        layout.addWidget(negative_confirmation, 1, 1)
        self.setLayout(layout)

        positive_confirmation.clicked.connect(self.delete_student)

    def delete_student(self):
        # get student record from DB
        rowIndex = main_window.table.currentRow()

        # get student id
        student_id = main_window.table.item(rowIndex, 0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id = ?', (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle('Success')
        confirmation_widget.setText('Deletion was successful')
        confirmation_widget.exec()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
