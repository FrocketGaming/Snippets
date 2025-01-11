from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy,
    QStyle,
    QToolButton,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import (
    QPalette,
    QPixmap,
)


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.setObjectName("titleBarLayout")
        self.initial_pos = None

        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )

        icon_label = QLabel(self)
        icon_label.setObjectName("iconLabel")
        icon_label.setFixedSize(QSize(28, 28))
        icon_pixmap = QPixmap("./src/icon/acorn.png")  # Set path to your icon
        icon_label.setPixmap(
            icon_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
        )

        self.title = QLabel(f"{self.__class__.__name__}", self)

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)

        title_bar_layout.addWidget(icon_label)
        title_bar_layout.addWidget(self.title)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setObjectName("closeButton")
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button.setFixedSize(QSize(28, 28))
        title_bar_layout.addWidget(self.close_button)

    # def window_state_changed(self, state):
    #     if state == Qt.WindowState.WindowMaximized:
    #         self.normal_button.setVisible(True)
    #         self.max_button.setVisible(False)
    #     else:
    #         self.normal_button.setVisible(False)
    #         self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()
