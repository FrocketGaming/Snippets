# from src.git import GitHubManager
from typing import List
from .database_manager import DatabaseManager
from pathlib import Path
import json


class SnippetManager:
    def load_snippets(self):
        data_check = DatabaseManager().read_database("snippets", "*")
        if len(data_check) > 0:
            return True
        return False

    def perform_search(self, query: str) -> List:
        """Filter snippets based on query"""
        if not query:
            return None

        results = [
            snippet
            for snippet in self.get_snippets()
            if query.lower() in snippet["description"].lower()
        ]
        return results

    def get_snippet_types(self) -> List:
        """Get all snippet types"""
        snippet_types = DatabaseManager().read_database("snippets", "type")
        return sorted(set(snippet_types["type"]))

    def get_snippets(self, snippet_type=None) -> List:
        """Get all snippets"""

        if snippet_type:
            return (
                DatabaseManager()
                .read_database("snippets", "*", f"type = '{snippet_type}'")
                .to_dicts()
            )

        return DatabaseManager().read_database("snippets", "*").to_dicts()

    def save_snippet(self, new_snippet: dict) -> None:
        """Save a new snippet to the database"""

        columns = list(new_snippet.keys())
        data = tuple(new_snippet.values())
        DatabaseManager().insert_data("snippets", columns, data)

    def update_existing_snippet(
        self, new_snippet: dict, existing_snippet: dict
    ) -> None:
        """Update an existing snippet in the database

        Args:
            existing_snippet: dict - the snippet to update
        """

        columns = [key for key in new_snippet.keys() if key != "id"]
        values = tuple(new_snippet[key] for key in columns)

        condition = f"id = {existing_snippet['id']}"

        DatabaseManager().update_database("snippets", columns, values, condition)

    def delete_snippet(self, snippet_id: int) -> None:
        """Delete a snippet from the database"""
        DatabaseManager().delete_data("snippets", f"id = {snippet_id}")


if __name__ == "__main__":
    pass
