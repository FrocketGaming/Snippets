from typing import List


class QueryManager:
    @staticmethod
    def create_table(table_name, table_columns) -> str:
        """Generic method to create a table in the database"""

        return f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_columns}
        )
        """

    @staticmethod
    def update_query(table_name, columns, conditions=None) -> str:
        """Query to update data in the database"""

        if isinstance(columns, str):
            set_clause = f"{columns} = ?"
        else:
            set_clause = ", ".join([f"{col} = ?" for col in columns])

        query = f"UPDATE {table_name} SET {set_clause}"

        if conditions:
            query += f" WHERE {conditions}"
        return query

    @staticmethod
    def insert_query(table_name: str, columns: List[str]) -> str:
        """Query to insert data into the database"""

        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))

        return f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})"""

    @staticmethod
    def create_query(columns, table_name, conditions=None) -> str:
        """Query to read all data from the database"""
        if conditions:
            return f"SELECT {columns} FROM {table_name} WHERE {conditions}"

        return f"SELECT {columns} FROM {table_name}"

    @staticmethod
    def snippet_table_query() -> str:
        """Query to create the snippets table in the database"""

        return QueryManager.create_table(
            "snippets",
            """
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            content TEXT NOT NULL
            """,
        )

    @staticmethod
    def hotkey_table_query() -> str:
        """Query to create the hotkeys table in the database"""

        return QueryManager.create_table(
            "hotkeys",
            """
            id INTEGER PRIMARY KEY,
            hotkey TEXT NOT NULL
            """,
        )
