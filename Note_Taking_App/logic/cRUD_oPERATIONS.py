from typing import Dict, List, Tuple
import mysql.connector
from mysql.connector import Error
from db_config import db_config, os


def insert_note(db_config: Dict[str, str], title: str, content: str) -> bool:
    """Insert a new note into the database."""
    try:
        with mysql.connector.connect(**db_config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "INSERT INTO notes (title, content) VALUES (%s, %s)"
                    cursor.execute(sql, (title, content))
                    connection.commit()
                    print(f"✅ Note '{title}' inserted successfully.")
                    return True
    except Error as e:
        print(f"Error inserting note: {e}")
        return False


def get_notes(db_config: Dict[str, str]) -> List[Tuple[int, str, str]]:
    """Retrieve all notes from the database."""
    try:
        with mysql.connector.connect(**db_config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, title, content FROM notes")
                    return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving notes: {e}")
        return []


def update_note(db_config: Dict[str, str], note_id: int, new_title: str, new_content: str) -> bool:
    """Update a note by ID."""
    try:
        with mysql.connector.connect(**db_config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "UPDATE notes SET title=%s, content=%s WHERE id=%s"
                    cursor.execute(sql, (new_title, new_content, note_id))
                    connection.commit()
                    print(f"🔄 Note {note_id} updated successfully.")
                    return True
    except Error as e:
        print(f"Error updating note: {e}")
        return False


def delete_note(db_config: Dict[str, str], note_id: int) -> bool:
    """Delete a note by ID."""
    try:
        with mysql.connector.connect(**db_config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    sql = "DELETE FROM notes WHERE id=%s"
                    cursor.execute(sql, (note_id,))
                    connection.commit()
                    print(f"🗑️ Note {note_id} deleted successfully.")
                    return True
    except Error as e:
        print(f"Error deleting note: {e}")
        return False


def menu(db_config: Dict[str, str]) -> None:
    """Command-line menu for managing notes."""
    while True:
        print("\n--- Notes App ---")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Update Note")
        print("4. Delete Note")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Enter note title: ").strip()
            content = input("Enter note content: ").strip()
            insert_note(db_config, title, content)

        elif choice == "2":
            notes = get_notes(db_config)
            for note_id, title, content in notes:
                print(f"ID: {note_id} | Title: {title} | Content: {content}")

        elif choice == "3":
            note_id = int(input("Enter note ID to update: "))
            new_title = input("Enter new title: ").strip()
            new_content = input("Enter new content: ").strip()
            update_note(db_config, note_id, new_title, new_content)

        elif choice == "4":
            note_id = int(input("Enter note ID to delete: "))
            delete_note(db_config, note_id)

        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, try again.")


if __name__ == "__main__":
    menu(db_config)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")  # default if not set
DEBUG = os.getenv("DEBUG", "False").lower() == "true"