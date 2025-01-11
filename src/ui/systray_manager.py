from PyQt6.QtWidgets import (
    QHBoxLayout,
    QCheckBox,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QPushButton,
    QDialog,
    QSystemTrayIcon,
    QMenu,
    QApplication,
)
from PyQt6.QtGui import QIcon, QAction
from src.ui.themes.themes_manager import all_themes, ThemeManager


class HotkeyConfigDialog(QDialog):
    def __init__(self, parent=None, current_hotkey=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Hotkey")
        # self.theme_manager = ThemeManager()
        self.current_hotkey = current_hotkey
        self.setup_ui()
        # self.theme_manager.apply_theme("Acorn")

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Modifier keys
        modifier_layout = QHBoxLayout()
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        modifier_layout.addWidget(self.ctrl_checkbox)
        modifier_layout.addWidget(self.alt_checkbox)
        modifier_layout.addWidget(self.shift_checkbox)
        layout.addLayout(modifier_layout)

        # Key selection
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("Key:"))
        self.key_combo = QComboBox()
        self.key_combo.addItems([chr(i) for i in range(65, 91)])  # A to Z
        key_layout.addWidget(self.key_combo)
        layout.addLayout(key_layout)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.parse_current_hotkey()

    def parse_current_hotkey(self):
        if self.current_hotkey:
            parts = self.current_hotkey.split("+")
            for part in parts:
                part = part.strip("<>")
                if part == "ctrl":
                    self.ctrl_checkbox.setChecked(True)
                elif part == "alt":
                    self.alt_checkbox.setChecked(True)
                elif part == "shift":
                    self.shift_checkbox.setChecked(True)
                elif len(part) == 1:
                    index = self.key_combo.findText(part.upper())
                    if index >= 0:
                        self.key_combo.setCurrentIndex(index)

    def get_hotkey(self):
        modifiers = []
        if self.ctrl_checkbox.isChecked():
            modifiers.append("<ctrl>")
        if self.alt_checkbox.isChecked():
            modifiers.append("<alt>")
        if self.shift_checkbox.isChecked():
            modifiers.append("<shift>")
        key = self.key_combo.currentText().lower()
        return "+".join(modifiers + [key])


class DefaultThemeDialog(QDialog):
    def __init__(self, parent=None, current_theme=None):
        super().__init__(parent)
        self.setWindowTitle("Default Theme")
        self.theme_manager = ThemeManager()
        self.current_theme = current_theme
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select a default theme:"))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_theme_names())
        layout.addWidget(self.theme_combo)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.parse_current_theme()

    def parse_current_theme(self):
        index = self.theme_combo.findText(self.current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)


class SystemTrayManager(QSystemTrayIcon):
    def __init__(self, parent=None, keyboard_manager=None):
        super().__init__(parent)
        self.keyboard_manager = keyboard_manager
        self.setIcon(QIcon("./src/icon/acorn.png"))
        self.setVisible(True)
        self.menu = QMenu(parent)
        self.create_menu()
        self.setContextMenu(self.menu)

    def create_menu(self):
        self.setToolTip("Acorn")

        default_theme = QAction("Default Theme", self.parent())
        default_theme.triggered.connect(self.default_theme)
        self.menu.addAction(default_theme)

        configure_hotkey = QAction("Configure Hotkey", self.parent())
        configure_hotkey.triggered.connect(self.configure_hotkey)
        self.menu.addAction(configure_hotkey)

        quit_action = QAction("Quit", self.parent())
        quit_action.triggered.connect(QApplication.quit)
        self.menu.addAction(quit_action)

    def add_action(self, name, callback):
        action = QAction(name, self.parent())
        action.triggered.connect(callback)
        self.menu.addAction(action)

    def configure_hotkey(self):
        dialog = HotkeyConfigDialog(self.parent(), self.keyboard_manager.hotkey_config)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_hotkey = dialog.get_hotkey()
            self.keyboard_manager.update_hotkey(new_hotkey)

    def default_theme(self):
        dialog = DefaultThemeDialog(self.parent(), None)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            theme_name = dialog.theme_combo.currentText()
            dialog.theme_manager.update_default_theme(theme_name)
