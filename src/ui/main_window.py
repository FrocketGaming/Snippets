from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QApplication,
    QScrollArea,
    QToolTip,
    QLabel,
    QLineEdit,
    QComboBox,
    QSizePolicy,
    QScrollArea,
    QStyle,
    QToolButton,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import (
    QTextCursor,
    QIcon,
    QColor,
    QBrush,
    QFont,
    QTextCharFormat,
)

from src.ui.themes.themes_manager import ThemeManager
from src.ui.title_bar import CustomTitleBar
from src.ui.snippet_popup import SnippetPopupManager
from src.ui.ui_factory import UIFactory
from src.data.snippet_manager import SnippetManager
from src.utils.utils import UtilityManager
from functools import partial


class UIConstants:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_base_window()

    def _setup_base_window(self):
        """Setup basic window properties common to all windows"""
        self.setWindowTitle("Acorn")
        self.setWindowIcon(QIcon(UtilityManager.get_resource_path("icon/acorn.png")))
        self.setFixedSize(QSize(UIConstants.WINDOW_WIDTH, UIConstants.WINDOW_HEIGHT))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def create_main_widget(self) -> QWidget:
        """Create and return the main widget with basic setup"""
        main_widget = QWidget()
        main_widget.setFont(QFont("Helvetica", 10))
        main_widget.setObjectName("Container")
        return main_widget

    def create_base_layout(self) -> tuple[QVBoxLayout, QVBoxLayout]:
        """Create and return the basic layouts for the window"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)

        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return main_layout, title_bar_layout

    def show_window(self):
        """Show and activate the window"""
        self.show()
        self.raise_()
        self.activateWindow()


class QtManager(BaseWindow):
    def __init__(self, kb_handler):
        super().__init__()
        self._initalize_managers(kb_handler)
        # self.popup = None
        # self.search_results = []
        self.ui = UIComponents(self)
        self.ui._setup_main_ui()
        self.keyboard_manager.show_hide_window.connect(self.show_hide_window)
        self.keyboard_manager.enter_key_pressed.connect(
            self.search_manager.perform_search
        )
        self.default_view = False
        self.selected_snippet_type = None

    def _initalize_managers(self, kb_handler):
        self.keyboard_manager = kb_handler
        self.snippet_manager = SnippetManager()
        self.theme_manager = ThemeManager()
        self.content_manager = ContentManager(
            self,
            self.snippet_manager,
            self.theme_manager,
        )
        self.search_manager = SearchManager(
            self, self.snippet_manager, self.content_manager
        )

    def show_hide_window(self):
        """Show or hide the main application window based on its current state."""

        if self.isVisible():
            self.search_bar.clearFocus()
            self.hide()

        else:
            self.show()
            self.showNormal()
            self.raise_()
            self.activateWindow()

    def missing_schema_default_layout(self, parent_layout):
        label = QLabel("No snippets found, please create your first snippet")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px")
        parent_layout.addWidget(label)

    # def close_popup(self):
    #     self.popup = None
    #     print("closed")
    #     self.re_focus_selection()

    def re_focus_selection(self):
        """Re-focus the selected snippet type button after a snippet is created or edited."""
        self.ui._setup_main_ui()
        if (
            self.selected_snippet_type is not None
            and self.selected_snippet_type in self.snippet_manager.get_snippet_types()
        ):
            button = self.ui.active_buttons[self.selected_snippet_type]
            self.content_manager.display_snippets(self.selected_snippet_type)
            button.setFocus()
            button.click()

    # TODO: Move to ClipboardManager
    def copy_to_clipboard(self, text):
        """Copy the snippet content to the clipboard and show a tooltip."""

        QApplication.clipboard().setText(text)
        tooltip_pos = QPoint(600, 120)
        QToolTip.showText(self.mapToGlobal(tooltip_pos), "Copied!", self)
        QTimer.singleShot(1500, QToolTip.hideText)


class ContentManager:
    def __init__(self, parent, snippet_manager, theme_manager):
        self.parent = parent
        self.popup = None
        self.snippet_manager = snippet_manager
        self.theme_manager = theme_manager
        self.search_results = []

    def clear_content(self):
        """Clear the search bar and search results, and remove all snippets from the content area."""

        self.clear_layout(self.parent.ui.content_layout)

        self.search_results = []
        self.parent.ui.search_bar.clear()

    def clear_layout(self, layout):
        """Clear the layout of all widgets."""

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def create_and_edit_snippet_popup(self, snippet=None):
        if not hasattr(self, "popup") or self.popup is None:
            self.popup = SnippetPopupManager(self.parent, snippet)
            self.popup.closed.connect(self.on_popup_closed)
            self.popup.show()

    def on_popup_closed(self):
        if self.popup:
            self.popup = None
            self.display_snippets(self.parent.selected_snippet_type)

    def display_snippets(self, snippet_type=None):
        """Display snippets based on the snippet_type selected or search results."""

        self.parent.selected_snippet_type = snippet_type
        self.clear_content()

        if snippet_type and self.search_results:
            self.search_results = []

        filtered_content = (
            self.search_results
            or self.parent.snippet_manager.get_snippets(snippet_type)
        )

        for item in filtered_content:
            row_layout = QHBoxLayout()

            text_area = UIFactory.create_QTextarea(
                text="",
                tooltip=item["content"],
                object_name="SnippetTextArea",
                read_only=True,
            )
            cursor = text_area.textCursor()

            # Set name to bold and larger font
            name_format = QTextCharFormat()
            name_format.setForeground(
                QBrush(self.parent.theme_manager.get_theme_color("Highlight"))
            )
            name_format.setFontWeight(QFont.Weight.Bold)
            name_format.setFontPointSize(14)
            cursor.insertText(item["name"], name_format)

            # Insert separator and description in a smaller font
            desc_format = QTextCharFormat()
            desc_format.setFontPointSize(10)

            cursor.insertText(": " + item["description"], desc_format)

            text_area.setTextCursor(cursor)  # Apply the styled text

            copy_button = UIFactory.create_QPushButton(
                "",
                partial(self.parent.copy_to_clipboard, item["content"]),
                "copyButton",
                shadow=True,
            )
            copy_button.setIcon(
                QIcon(UtilityManager.get_resource_path("icon/copy-solid.svg"))
            )
            copy_button.setToolTip("Copy Snippet")

            edit_button = UIFactory.create_QPushButton(
                "",
                partial(
                    self.parent.content_manager.create_and_edit_snippet_popup,
                    snippet=item,
                ),
                "editButton",
                width=10,
                shadow=True,
            )
            edit_button.setIcon(
                QIcon(UtilityManager.get_resource_path("icon/edit.png"))
            )
            edit_button.setToolTip("Edit Snippet")

            delete_button = UIFactory.create_QPushButton(
                "X",
                partial(self.delete_snippet, item),
                "deleteButton",
                shadow=True,
            )
            delete_button.setToolTip("Delete Snippet")

            row_layout.addWidget(delete_button)
            row_layout.addWidget(text_area)
            row_layout.addWidget(copy_button)
            row_layout.addWidget(edit_button)

            self.parent.ui.content_layout.addLayout(row_layout)
            self.parent.ui.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def delete_snippet(self, snippet):
        self.snippet_manager.delete_snippet(snippet["id"])
        self.parent.re_focus_selection()


class SearchManager:
    def __init__(self, parent, snippet_manager, content_manager):
        self.parent = parent
        self.snippet_manager = snippet_manager
        self.content_manager = content_manager

    def perform_search(self):
        """Search for snippets based on the query in the search bar."""

        if self.parent.isActiveWindow() and self.parent.isVisible():
            if self.parent.default_view is False:
                query = self.parent.ui.search_bar.text()
                self.search_results = self.snippet_manager.perform_search(query)
                if self.search_results:
                    self.content_manager.display_snippets()


class UIComponents:
    """Handles UI component creation and layout"""

    def __init__(self, parent):
        self.parent = parent

    def _setup_main_ui(self):
        """Setup the main UI structure"""
        main_widget = self._create_main_widget()
        main_layout, title_bar_layout = self._create_base_layout()

        self.parent.title_bar = CustomTitleBar(self.parent)
        title_bar_layout.addWidget(self.parent.title_bar)
        title_bar_layout.addLayout(main_layout)

        self._setup_ui_elements(main_layout)

        main_widget.setLayout(title_bar_layout)
        self.parent.setCentralWidget(main_widget)

    def _create_main_widget(self):
        """Create the main widget with basic setup"""
        main_widget = QWidget()
        main_widget.setFont(QFont("Helvetica", 10))
        main_widget.setObjectName("Container")
        return main_widget

    def _create_base_layout(self):
        """Create the base layouts"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)

        title_bar_layout = QVBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return main_layout, title_bar_layout

    def _setup_ui_elements(self, main_layout):
        """Setup all UI elements"""
        main_elements = [
            self.add_theme_picker,
            self.add_search_bar,
            self.add_type_buttons,
            self.add_content_area,
            self.create_snippets_button,
        ]

        if self.parent.snippet_manager.load_snippets() is False:
            self.parent.default_view = True
            self.parent.missing_schema_default_layout(main_layout)
            self.create_snippets_button(main_layout)
        else:
            for element in main_elements:
                element(main_layout)

    def add_theme_picker(self, parent_layout):
        """Add a combo box to select the theme to the main layout."""

        layout = QHBoxLayout()
        layout.addStretch()
        self.theme_picker_combo = QComboBox()
        self.theme_picker_combo.addItems(self.parent.theme_manager.get_theme_names())
        self.theme_picker_combo.setFixedWidth(90)
        self.theme_picker_combo.setObjectName("themePicker")
        self.theme_picker_combo.currentTextChanged.connect(
            self.parent.theme_manager.apply_theme
        )

        self.theme_picker_combo.setCurrentText(
            self.parent.theme_manager.current_theme.name
        )
        layout.addWidget(self.theme_picker_combo)
        parent_layout.addLayout(layout)

    def add_content_area(self, parent_layout):
        """Add a scrollable area to display the snippets, but remove it if no snippets are found."""

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("contentScrollArea")

        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setObjectName("contentLayout")

        scroll_area.setWidget(self.content_widget)
        parent_layout.addWidget(scroll_area)

    def add_search_bar(self, parent_layout):
        """Add a search bar to the main layout to filter snippets."""

        layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search snippets...")
        self.search_bar.setFixedHeight(35)
        self.search_bar.setObjectName("searchBar")

        search_btn = UIFactory.create_QPushButton(
            "Search",
            self.parent.search_manager.perform_search,
            "searchButton",
            shadow=True,
        )
        clear_btn = UIFactory.create_QPushButton(
            "Clear",
            self.parent.content_manager.clear_content,
            "clearButton",
            shadow=True,
        )

        layout.addWidget(self.search_bar)
        layout.addWidget(search_btn)
        layout.addWidget(clear_btn)
        parent_layout.addLayout(layout)

    def create_text_area(self, text):
        """Create the text area to display snippet information."""

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setPlainText(str(text))
        text_area.setFixedHeight(35)
        text_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor = text_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        text_area.setTextCursor(cursor)
        text_area.ensureCursorVisible()
        return text_area

    def create_snippets_button(self, parent_layout):
        """Add buttons to create and edit snippets to the main layout."""

        layout = QHBoxLayout()
        create_button = UIFactory.create_QPushButton(
            "Create Snippet",
            partial(
                self.parent.content_manager.create_and_edit_snippet_popup, snippet=None
            ),
            "createButton",
            shadow=True,
        )
        layout.addWidget(create_button)
        parent_layout.addLayout(layout)

    def add_type_buttons(self, parent_layout):
        """Add buttons to filter snippets by snippet_type to the main layout. Remove them if no snippets are found."""
        self.active_buttons = {}

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(55)
        scroll_area.setObjectName("typeScrollArea")

        button_widget = QWidget()
        button_widget.setObjectName("typeWidget")

        button_layout = QHBoxLayout(button_widget)

        for snippet_type in self.parent.snippet_manager.get_snippet_types():
            button = UIFactory.create_QPushButton(
                snippet_type,
                lambda checked,
                t=snippet_type: self.parent.content_manager.display_snippets(t),
                "typeButton",
                shadow=True,
            )

            self.active_buttons[snippet_type] = button

            button_layout.addWidget(button)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            button_layout.setContentsMargins(10, 10, 10, 0)

        scroll_area.setWidget(button_widget)

        # Make the scroll bar appear only horizontally
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        parent_layout.addWidget(scroll_area)
