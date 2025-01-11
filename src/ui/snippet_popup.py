from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QLineEdit,
)
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import (
    QIcon,
)

from src.ui.ui_factory import UIFactory
from src.ui.title_bar import CustomTitleBar


class SnippetPopupManager(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None, snippet=None):
        super().__init__(parent)
        self.parent = parent
        self.existing_snippet = snippet
        self.setWindowTitle("Acorn Vault")
        self.setWindowIcon(QIcon("./src/icon/acorn.png"))
        self.setFixedSize(QSize(700, 400))  # Set a fixed size
        self.setWindowFlag(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        )  # Ensure it's a top-level window
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Add Offset to the window
        self.move(parent.x() + 50, parent.y() + 50)

        layout = QVBoxLayout()
        self.title_bar = CustomTitleBar(self)
        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        title_bar_layout.addWidget(self.title_bar)
        title_bar_layout.addLayout(layout)

        self.setLayout(title_bar_layout)

        # Snippet Name Input
        snippet_name_layout = QHBoxLayout()
        self.snippet_name_label = QLabel("Snippet Name:")
        self.snippet_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        snippet_name_layout.addWidget(self.snippet_name_label)

        self.snippet_name_input = QLineEdit()
        self.snippet_name_input.setFixedWidth(580)

        if snippet:
            self.snippet_name_input.setText(snippet["name"])
        snippet_name_layout.addWidget(self.snippet_name_input)

        layout.addLayout(snippet_name_layout)

        # Type Input
        type_layout = QHBoxLayout()
        self.type_label = QLabel("Snippet Type:")
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_layout.addWidget(self.type_label)

        self.type_input = QLineEdit()
        self.type_input.setFixedWidth(580)

        if snippet:
            self.type_input.setText(snippet["type"])
        type_layout.addWidget(self.type_input)

        layout.addLayout(type_layout)

        # Description Input
        description_layout = QHBoxLayout()
        self.description_label = QLabel("Description:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_layout.addWidget(self.description_label)

        self.description_input = QLineEdit()
        self.description_input.setFixedWidth(580)

        if snippet:
            self.description_input.setText(snippet["description"])
        description_layout.addWidget(self.description_input)

        layout.addLayout(description_layout)

        # Snippet Text Area
        self.snippet_text_area = QTextEdit()
        self.snippet_text_area.setObjectName("snippetTextArea")
        self.snippet_text_area.setPlaceholderText("Type your snippet here...")

        # Set the content preserving the original formatting
        if snippet:
            self.snippet_text_area.setPlainText(snippet["content"])
        layout.addWidget(self.snippet_text_area)

        # Save and Close Buttons, Maybe Delete
        button_layout = QHBoxLayout()
        self.save_button = UIFactory.create_QPushButton(
            "Save", self.save_snippet, "saveButton", shadow=True
        )
        button_layout.addWidget(self.save_button)

        self.close_button = UIFactory.create_QPushButton(
            "Close", self.close_popup, "closePopupButton", shadow=True
        )
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        self.closed_emitted = False

    def close_popup(self):
        if not self.closed_emitted:
            self.closed.emit()  # Emit closed signal
            self.closed_emitted = True  # Set flag to prevent further emissions
        self.close()

    def delete_snippet(self):
        print(f"Deleting snippet: {self.existing_snippet}")
        self.parent.snippet_manager.delete_snippet(self.existing_snippet)
        self.snippet_changed.emit()
        self.close()

    def save_snippet(self):
        # Retrieve input values
        snippet_name = self.snippet_name_input.text()
        snippet_type = self.type_input.text()
        description = self.description_input.text()
        snippet_content = self.snippet_text_area.toPlainText()

        # Create the new snippet entry
        new_snippet = {
            "Name": f"""{snippet_name}""",
            "Type": f"""{snippet_type}""",
            "Description": f"""{description}""",
            "Content": f"""{snippet_content}""",
        }

        if self.existing_snippet is None:
            self.parent.snippet_manager.save_snippet(new_snippet)
        else:
            self.parent.snippet_manager.update_existing_snippet(
                new_snippet, self.existing_snippet
            )
        self.parent.re_focus_selection()
        self.close()

    def closeEvent(self, event):
        if not self.closed_emitted:
            self.closed.emit()
            self.closed_emitted = True
        event.accept()
