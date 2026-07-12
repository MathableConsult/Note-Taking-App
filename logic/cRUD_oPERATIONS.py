# Logic for Mysql Version of the app
# In case of persistent storage

# from typing import Dict, List, Tuple
# import mysql.connector
# from mysql.connector import Error
# from .db_config import db_config
# import os

# # Comment your functions to specify their purpose, parameters, 
# # and return values. This will help others (and your future self) 
# # understand the code better.

# # Functions for CRUD operations on notes
# # It returns a boolean value indicating success or failure
# def insert_note(db_config: Dict[str, str], title: str, content: str) -> bool:
#     """Insert a new note into the database."""
#     try:
#         with mysql.connector.connect(**db_config) as connection:
#             if connection.is_connected():
#                 with connection.cursor() as cursor:
#                     # this query uses parameterized queries to handle sql injection.
#                     query = "INSERT INTO notes (title, content) VALUES (%s, %s)"
#                     cursor.execute(query, (title, content))
#                     # Commit query to database to save changes. This is important for data integrity.
#                     connection.commit()
#                     # Notification of successful insert operation
#                     print(f"✅ Note '{title}' inserted successfully.")
#                     return True
#     except Error as e:
#         print(f"Error inserting note: {e}")
#         return False


# # Function to retreive all notes from the database. 
# # It returns a list of tuples,
# # where each tuple contains the id, title, and content of a note.
# def get_notes(db_config: Dict[str, str]) -> List[Tuple[int, str, str]]:
#     """Retrieve all notes from the database."""
#     try:
#         with mysql.connector.connect(**db_config) as connection:
#             if connection.is_connected():
#                 with connection.cursor() as cursor:
#                     cursor.execute("SELECT id, title, content FROM notes")
#                     return cursor.fetchall()
#     except Error as e:
#         print(f"Error retrieving notes: {e}")
#         return []


# # Function to update a note by its ID.
# # It returns a boolean value indicating success or failure.
# def update_note(db_config: Dict[str, str], note_id: int, new_title: str, new_content: str) -> bool:
#     """Update a note by ID."""
#     try:
#         with mysql.connector.connect(**db_config) as connection:
#             if connection.is_connected():
#                 with connection.cursor() as cursor:
#                     sql = "UPDATE notes SET title=%s, content=%s WHERE id=%s"
#                     cursor.execute(sql, (new_title, new_content, note_id))
#                     connection.commit()
#                     print(f"🔄 Note {note_id} updated successfully.")
#                     return True
#     except Error as e:
#         print(f"Error updating note: {e}")
#         return False

# # Function to delete a note by its ID.
# # It returns a boolean value indicating success or failure.
# def delete_note(db_config: Dict[str, str], note_id: int) -> bool:
#     """Delete a note by ID."""
#     try:
#         with mysql.connector.connect(**db_config) as connection:
#             if connection.is_connected():
#                 with connection.cursor() as cursor:
#                     sql = "DELETE FROM notes WHERE id=%s"
#                     cursor.execute(sql, (note_id,))
#                     connection.commit()
#                     print(f"🗑️ Note {note_id} deleted successfully.")
#                     return True
#     except Error as e:
#         print(f"Error deleting note: {e}")
#         return False

# # Function to display a command-line menu for managing notes.
# # If user chooses to perform a command-line operation, 
# # it will call the appropriate function.
# def menu(db_config: Dict[str, str]) -> None:
#     """Command-line menu for managing notes."""
#     while True:
#         print("\n--- Notes App ---")
#         print("1. Add Note")
#         print("2. View Notes")
#         print("3. Update Note")
#         print("4. Delete Note")
#         print("5. Exit")

#         choice = input("Choose an option: ").strip()

#         if choice == "1":
#             title = input("Enter note title: ").strip()
#             content = input("Enter note content: ").strip()
#             insert_note(db_config, title, content)

#         elif choice == "2":
#             notes = get_notes(db_config)
#             for note_id, title, content in notes:
#                 print(f"ID: {note_id} | Title: {title} | Content: {content}")

#         elif choice == "3":
#             note_id = int(input("Enter note ID to update: "))
#             new_title = input("Enter new title: ").strip()
#             new_content = input("Enter new content: ").strip()
#             update_note(db_config, note_id, new_title, new_content)

#         elif choice == "4":
#             note_id = int(input("Enter note ID to delete: "))
#             delete_note(db_config, note_id)

#         elif choice == "5":
#             print("👋 Goodbye!")
#             break
#         else:
#             print("⚠️ Invalid choice, try again.")


# # If this script is run directly, 
# # it will launch the command-line menu for managing notes.
# if __name__ == "__main__":
#     menu(db_config)

# UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")  # default if not set
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Logic for SQLite Version of the app
# For quick demo and test

from typing import Dict, List, Tuple
import sqlite3
from sqlite3 import Error
from .db_config import db_config

# Functions for CRUD operations on notes
# DDL - Operation
def init_db(config: Dict[str, str]) -> None:
    """Creates schema with file_path column. Upgrades older schemas automatically."""
    try:
        with sqlite3.connect(config["database"]) as connection:
            cursor = connection.cursor()
            # 1. Base table setup
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    file_path TEXT
                )
            """)
            connection.commit()
            
            # 2. Upgrade system for existing databases missing the column
            cursor.execute("PRAGMA table_info(notes)")
            columns = [col[1] for col in cursor.fetchall()]
            if "file_path" not in columns:
                cursor.execute("ALTER TABLE notes ADD COLUMN file_path TEXT")
                connection.commit()
                print("🔄 Migrated database schema to support file uploads.")
    except Error as e:
        print(f"Error initializing schema: {e}")

# Initialize schema instantly on loading module
init_db(db_config)


# Function to insert a note into the SQLite database, 
# optionally with a file attachment path.
def insert_note(config: Dict[str, str], title: str, content: str, file_path: str = None) -> bool:
    """Insert a note containing an optional file attachment reference path."""
    try:
        with sqlite3.connect(config["database"]) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO notes (title, content, file_path) VALUES (?, ?, ?)"
            cursor.execute(query, (title, content, file_path))
            connection.commit()
            return True
    except Error as e:
        print(f"Database insertion error: {e}")
        return False

# Function to retrieve all notes from the SQLite database,
# including their file attachment paths if present.
def get_notes(config: Dict[str, str]) -> List[Tuple[int, str, str, str]]:
    """Retrieve all columns including files from the SQLite storage layer."""
    try:
        with sqlite3.connect(config["database"]) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, title, content, file_path FROM notes")
            return cursor.fetchall()
    except Error as e:
        print(f"Database retrieval error: {e}")
        return []


# Function to update a note in the SQLite database,
# using its ID and new title/content values.
def update_note(config: Dict[str, str], note_id: int, new_title: str, new_content: str) -> bool:
    """Update a note using universal SQL parameters."""
    try:
        with sqlite3.connect(config["database"]) as connection:
            cursor = connection.cursor()
            sql = "UPDATE notes SET title=?, content=? WHERE id=?"
            cursor.execute(sql, (new_title, new_content, note_id))
            connection.commit()
            return True
    except Error as e:
        print(f"Database update error: {e}")
        return False


# Function to Delete a note in the SQLite database,
# using its ID and new title/content values.
def delete_note(config: Dict[str, str], note_id: int) -> bool:
    """Delete a note using universal SQL parameters."""
    try:
        with sqlite3.connect(config["database"]) as connection:
            cursor = connection.cursor()
            sql = "DELETE FROM notes WHERE id=?"
            cursor.execute(sql, (note_id,))
            connection.commit()
            return True
    except Error as e:
        print(f"Database deletion error: {e}")
        return False


# Function to display a command-line menu for managing notes.
# If user chooses to perform a command-line operation
def menu(config: Dict[str, str]) -> None:
    """Local terminal interface menu."""
    while True:
        print("\n--- Notes App (Universal SQLite) ---")
        print("1. Add Note | 2. View Notes | 3. Update Note | 4. Delete Note | 5. Exit")
        choice = input("Option: ").strip()

        if choice == "1":
            t = input("Title: ").strip()
            c = input("Content: ").strip()
            insert_note(config, t, c)
        elif choice == "2":
            for nid, t, c in get_notes(config):
                print(f"[{nid}] {t}: {c}")
        elif choice == "3":
            nid = int(input("Note ID: "))
            t = input("New Title: ").strip()
            c = input("New Content: ").strip()
            update_note(config, nid, t, c)
        elif choice == "4":
            nid = int(input("Note ID to delete: "))
            delete_note(config, nid)
        elif choice == "5":
            break

# Main execution block
if __name__ == "__main__":
    menu(db_config)
