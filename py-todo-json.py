# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

import os
import json
from pathlib import Path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QListWidget
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QTextEdit, QHBoxLayout
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

#import ctypes
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('icon.png')

TASKS_FILE = 'tasks.json'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List")
#        self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.addTaskButton = QPushButton("Add Task")
        self.addTaskButton.setCheckable(True)
        self.addTaskButton.clicked.connect(self.add_task)

        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText('Enter a new task...')
        self.taskInput.returnPressed.connect(self.add_task)

        self.infoInput = QTextEdit()
        self.infoInput.setPlaceholderText('Enter additional information...')

        self.taskList = QListWidget()
        self.taskList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.taskList.installEventFilter(self)
        self.taskList.itemSelectionChanged.connect(self.display_task_info)

        self.saveChangesButton = QPushButton('Save Changes')
        self.saveChangesButton.clicked.connect(self.save_changes)

        self.delete_button = QPushButton('Delete Selected Task')
        self.delete_button.clicked.connect(self.delete_task)

        self.load_tasks()

        main_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.taskList)
        h_layout.addWidget(self.infoInput)

        main_layout.addWidget(self.taskInput)
        main_layout.addWidget(self.addTaskButton)
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.saveChangesButton)
        main_layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def load_tasks(self):
        try:
            with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
                for task in tasks:
                    if isinstance(task, dict) and 'title' in task and 'info' in task:
                        self.taskList.addItem(f"{task['title']} - {task['info']}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("Error loading tasks:", e)

    def save_tasks(self):
        tasks = []
        for index in range(self.taskList.count()):
            item = self.taskList.item(index)
            task_text = item.text()
            if " - " in task_text:
                title, info = task_text.split(" - ", 1)
            else:
                title, info = task_text, ""
            task = {
                'title': title,
                'info': info
            }
            tasks.append(task)

        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks,file,indent=2)

    def add_task(self):
        task_title = self.taskInput.text().strip()
        task_info = self.infoInput.toPlainText().strip()

        if task_title:
            task = {
                'title': task_title,
                'info': task_info
            }
            self.taskList.addItem(f"{task['title']} - {task['info']}")
            self.taskInput.clear()
            self.infoInput.clear()
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

    def display_task_info(self):
        selected_items = self.taskList.selectedItems()
        if selected_items:
            task_text = selected_items[0].text()
            if " - " in task_text:
                title, info = task_text.split(" - ", 1)
                self.selected_task = selected_items[0]
                self.infoInput.setText(info)

    def save_changes(self):
        if self.selected_task is None:
            return

        updated_info = self.infoInput.toPlainText().strip()
        task_text = self.selected_task.text()

        if " - " in task_text:
            title, _ = task_text.split(" - ", 1)
            updated_task_text = f"{title} - {updated_info}"

            row = self.taskList.row(self.selected_task)
            self.taskList.item(row).setText(updated_task_text)
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
#    window.setWindowIcon(QtGui.QIcon("icon.png"))

    app.exec()
