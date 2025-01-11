from pathlib import Path
# import json
# import sqlite3

from ..data.database_manager import DatabaseManager
# from src.data.database import DatabaseManager


class ConfigurationManager:
    def __init__(self):
        self.check_configuration()

    def check_configuration(self) -> None:
        """Check if the current configuration is valid, if not then begin the configuration process -- likely only necessary for first-time users"""

        db_path: str = DatabaseManager.get_db_path()
        if not db_path.exists():
            ConfigurationManager.configure_database()
            return None
        return True

    @staticmethod
    def configure_database() -> None:
        """Configures the database for first-time users to ensure the tables are create and populated with default values"""

        with DatabaseManager() as db:
            db.create_table(
                "snippets",
                "id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, description TEXT NOT NULL, content TEXT NOT NULL",
            )
            db.create_table("hotkeys", "id INTEGER PRIMARY KEY, hotkey TEXT NOT NULL")
            db.create_table(
                "default_theme", "id INTEGER PRIMARY KEY, theme TEXT NOT NULL"
            )

            # Pass values as a tuple instead of a single string
            db.insert_data("default_theme", ["theme"], ("Acorn",))
            db.insert_data("hotkeys", ["hotkey"], ("<alt>+<shift>+p",))

    def __enter__(self):
        """Context manager for the ConfigurationManager class"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager for the ConfigurationManager class"""
        return None


# class ConfigManager:
#     def __init__(self):
#         self.main_config_path = Path.home() / ".acorn"
#         self.db_path = Path.cwd() / "src" / "db" / "acorn.db"
#         self.default_schema_path = self.main_config_path / "schema" / "schema.json"
#         self.db_config()
#         # self.load_config()

#     def db_config(self):
#         if not self.db_path.exists():
#             with DatabaseManager() as db:
#                 db.create_hotkey_table()
#                 db.create_snippet_table()
#                 db.insert_table_defaults()

#     def create_snippet_table(self):
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()

#         c.execute(
#             """
#             CREATE TABLE IF NOT EXISTS snippets (
#                 id INTEGER PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 type TEXT NOT NULL,
#                 description TEXT NOT NULL,
#                 content TEXT NOT NULL
#             )
#             """
#         )

#         conn.commit()
#         conn.close()

#     def create_hotkey_table(self):
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()

#         c.execute(
#             """
#             CREATE TABLE IF NOT EXISTS hotkeys (
#                 id INTEGER PRIMARY KEY,
#                 hotkey TEXT NOT NULL
#             )
#             """
#         )

#         conn.commit()
#         conn.close()

#     def insert_table_defaults(self):
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()

#         c.execute(
#             """
#             INSERT INTO hotkeys (hotkey)
#             VALUES (?)
#             """,
#             ("<alt>+<shift>+p",),
#         )

#         conn.commit()
#         conn.close()

#     def create_defaults(self):
#         defaults = {
#             "hotkey": "<alt>+<shift>+p",
#         }
#         return json.dumps(defaults, indent=4)

#     def load_config(self):
#         self.config_file = self.main_config_path / "config.json"

#         if not self.default_schema_path.exists():
#             (self.main_config_path / "schema").mkdir(parents=True, exist_ok=True)

#         if self.config_file.exists():
#             with open(self.config_file, "r") as file:
#                 return json.load(file)
#         else:
#             self.main_config_path.mkdir(parents=True, exist_ok=True)
#             with open(self.config_file, "w") as file:
#                 file.write(self.create_defaults())

#             return json.loads(self.create_defaults())

#     def get_hotkey_config(self):
#         return self.load_config().get("hotkey")


if __name__ == "__main__":
    is_configured = ConfigurationManager.check_configuration()
    print(is_configured)

    # with ConfigurationManager() as config:
    # print(config.get_db_path())
