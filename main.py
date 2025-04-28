# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QListWidget
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt

TASKS_FILE = 'tasks.txt'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List")

        self.addTaskButton = QPushButton("Add Task")
        self.addTaskButton.setCheckable(True)
        self.addTaskButton.clicked.connect(self.add_task)

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText('Enter a new task...')
        self.taskInput.returnPressed.connect(self.add_task)

        self.taskList = QListWidget()
        self.taskList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.taskList.installEventFilter(self)


        self.delete_button = QPushButton('Delete Selected Task')
        self.delete_button.clicked.connect(self.delete_task)

        self.load_tasks()

        layout = QVBoxLayout()
        layout.addWidget(self.taskInput)
        layout.addWidget(self.addTaskButton)
        layout.addWidget(self.taskList)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def load_tasks(self):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = file.readlines()
                for task in tasks:
                    task = task.strip()
                    if task:
                        self.taskList.addItem(task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            for index in range(self.taskList.count()):
                item = self.taskList.item(index)
                file.write(item.text() + '\n')

    def add_task(self):
        #Add in functionality to write to file
        task_text = self.taskInput.text().strip()
        if task_text:
            self.taskList.addItem(task_text)
            self.taskInput.clear()
            self.save_tasks()

    def delete_task(self):
        selected_items = self.taskList.selectedItems()
        if not selected_items:
            return

        if len(selected_items) > 1:
            reply = QMessageBox.question(
                self,
                'Confirm Delete',
                'Are you sure you want to delete the selected task(s)?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        for item in selected_items:
            self.taskList.takeItem(self.taskList.row(item))
        self.save_tasks()

    def eventFilter(self,source,event):
        if source == self.taskList and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.delete_task()
                return True
        return super().eventFilter(source,event)

    def closeEvent(self,event):
        self.save_tasks()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()

