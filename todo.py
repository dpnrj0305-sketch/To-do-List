import sqlite3
import argparse
from datetime import datetime
import os

# --- Configuration ---
DB_FILE = 'todo.db'

def init_db():
    """Initializes the SQLite database and creates the tasks table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TEXT
            )
        ''')
        conn.commit()

def add_task(task_text):
    """Adds a new task to the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO tasks (task, created_at) VALUES (?, ?)", (task_text, now))
        conn.commit()
        print(f"✅ Added task: '{task_text}'")

def view_tasks():
    """Retrieves and displays all tasks."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, status, created_at FROM tasks")
        tasks = cursor.fetchall()
        
        if not tasks:
            print("📭 Your to-do list is empty! Use --add to create a task.")
            return

        print(f"\n{'ID':<5} | {'Status':<10} | {'Created At':<16} | {'Task'}")
        print("-" * 65)
        for task in tasks:
            t_id, t_text, t_status, t_date = task
            status_icon = "✅" if t_status == 'Done' else "⏳"
            print(f"{t_id:<5} | {status_icon} {t_status:<7} | {t_date:<16} | {t_text}")
        print("\n")

def complete_task(task_id):
    """Marks a specific task as 'Done'."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print(f"⚠️ No task found with ID {task_id}")
        else:
            conn.commit()
            print(f"🎉 Task {task_id} marked as complete!")

def delete_task(task_id):
    """Permanently removes a task from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            print(f"⚠️ No task found with ID {task_id}")
        else:
            conn.commit()
            print(f"🗑️ Task {task_id} deleted successfully.")

def main():
    # Ensure the database exists before doing anything
    init_db()
    
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="A lightweight CLI To-Do List powered by SQLite.")
    parser.add_argument("-a", "--add", type=str, help="Add a new task (wrap text in quotes)")
    parser.add_argument("-v", "--view", action="store_true", help="View all tasks")
    parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by providing its ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by providing its ID")
    
    args = parser.parse_args()

    # Route the user's command to the correct function
    if args.add:
        add_task(args.add)
    elif args.view:
        view_tasks()
    elif args.complete is not None:
        complete_task(args.complete)
    elif args.delete is not None:
        delete_task(args.delete)
    else:
        # If no arguments are passed, show the help menu
        parser.print_help()

if __name__ == "__main__":
    main()