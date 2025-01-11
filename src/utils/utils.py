from pathlib import Path
import sys


class UtilityManager:
    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """Get the absolute path to a resource, handling .exe and source environments."""
        if hasattr(sys, "_MEIPASS"):
            # PyInstaller's temporary directory
            base_path = Path(sys._MEIPASS)
        else:
            # Normal environment
            base_path = Path(__file__).resolve().parent.parent

        return str(base_path / relative_path)
