import os
import sys
from pathlib import Path
from src import KeyboardManager, SystemTrayManager, QtManager, ConfigurationManager
from PyQt6.QtWidgets import QApplication

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    # Set the working directory to the project root
    os.chdir(project_root)
    app = QApplication(sys.argv)
    config = ConfigurationManager()
    kb_handler = KeyboardManager()

    qt_handler = QtManager(kb_handler)
    SystemTrayManager(qt_handler, kb_handler)

    qt_handler.show_window()

    # Start the event loop and prevent the application from closing when the main window is closed
    # app.setQuitOnLastWindowClosed(False)
    app.exec()
