import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QListWidgetItem, QLabel,
                             QInputDialog, QMessageBox, QTextEdit)
import os


class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Note App')
        self.setFixedSize(700, 500)

        self.layout = QHBoxLayout()

        self.button_layout = QVBoxLayout()
        self.note_layout = QVBoxLayout()
        self.description_layout = QVBoxLayout()

        self.new_note_button = QPushButton('New Note')
        self.new_note_button.clicked.connect(self.add_new_note)
        self.button_layout.addWidget(self.new_note_button)

        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_note)
        self.button_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton('Edit')
        self.edit_button.clicked.connect(self.edit_note)
        self.button_layout.addWidget(self.edit_button)

        self.done_button = QPushButton('Done')
        self.done_button.clicked.connect(self.mark_done)
        self.button_layout.addWidget(self.done_button)

        self.load_done_button = QPushButton('Load Done')
        self.load_done_button.clicked.connect(self.load_done)
        self.button_layout.addWidget(self.load_done_button)

        self.load_due_button = QPushButton('Load Due')
        self.load_due_button.clicked.connect(self.load_due)
        self.button_layout.addWidget(self.load_due_button)

        self.note_list = QListWidget()
        self.note_list.itemDoubleClicked.connect(self.show_details_double_click)
        self.note_layout.addWidget(self.note_list)

        self.description_text = QTextEdit()
        # self.description_list.itemDoubleClicked.connect(self.show_details_double_click)
        self.description_layout.addWidget(self.description_text)

        self.save_button = QPushButton('save')
        self.save_button.clicked.connect(self.save_description)
        self.description_layout.addWidget(self.save_button)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.note_layout)
        self.layout.addLayout(self.description_layout)
        self.setLayout(self.layout)

        # Create the "notes" folder if it doesn't exist
        if not os.path.exists("notes"):
            os.mkdir("notes")

        self.load_notes("notes")

    def load_notes(self, folder):
        # Remove all notes from the note list
        self.note_list.clear()
        # Read the list of files in the "notes" folder and add them to the note list
        for file_name in os.listdir(folder):
            if file_name.endswith(".txt"):
                note_name = os.path.splitext(file_name)[0]
                with open(os.path.join(folder, file_name), "r") as f:
                    note_description = f.read()
                note_item = QListWidgetItem(note_name)
                note_item.description = note_description
                self.note_list.addItem(note_item)

    def add_new_note(self):
        note_name, ok = QInputDialog.getText(self, 'New Note', 'Enter note name:')
        if ok and note_name:
            note_item = QListWidgetItem(note_name)
            note_item.description = "No description"
            self.note_list.addItem(note_item)

            # Create a new file with the note name and description
            file_path = os.path.join("notes", note_name + ".txt")
            with open(file_path, "w") as f:
                f.write(note_item.description)

    def delete_note(self):
        current_item = self.note_list.currentItem()
        if current_item:
            # Delete the file associated with the note
            file_path = os.path.join("notes", current_item.text() + ".txt")
            os.remove(file_path)

            self.note_list.takeItem(self.note_list.row(current_item))

    def edit_note(self):
        current_item = self.note_list.currentItem()
        if current_item:
            old_file_path = os.path.join("notes", current_item.text() + ".txt")
            new_name, ok = QInputDialog.getText(self, 'Edit Note', 'Enter new note name:', text=current_item.text())
            if ok and new_name:
                new_file_path = os.path.join("notes", new_name + ".txt")

                # Rename the file associated with the note
                os.rename(old_file_path, new_file_path)

                current_item.setText(new_name)

    def mark_done(self):
        current_item = self.note_list.currentItem()
        if current_item:
            # Transfer the note file to another folder
            file_path = os.path.join("notes", current_item.text() + ".txt")
            new_folder = "done_notes"
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
            new_file_path = os.path.join(new_folder, current_item.text() + ".txt")
            os.rename(file_path, new_file_path)

            self.note_list.takeItem(self.note_list.row(current_item))

    def load_done(self):
        self.load_notes("done_notes")

    def load_due(self):
        self.load_notes("notes")

    def save_description(self):
        current_item = self.note_list.currentItem()
        description = self.description_text.toPlainText()
        current_item.description = description

        new_file_path = os.path.join("notes", current_item.text() + ".txt")
        # Update the file with the new description
        with open(new_file_path, "w") as f:
            f.write(description)

    def show_details(self):
        current_item = self.note_list.currentItem()
        if current_item:
            self.description_text.setText(current_item.description)

    def show_details_double_click(self, item):
        self.show_details()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    note_app = NoteApp()
    note_app.show()
    sys.exit(app.exec_())
