import psycopg2
import time

class TaskManager:
    def __init__(self, dbname, password, user, host, port):
        self.conn = psycopg2.connect(dbname=dbname, password=password, user=user, host=host, port=port)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.drop_table()
        self.create_table()

    def drop_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS todo')

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id SERIAL PRIMARY KEY,
                task_name VARCHAR(255) NOT NULL
            )
        ''')
        self.conn.commit()

    def add_task(self, task):
        if not task:
            print("Task name cannot be empty.")
            return
        self.cursor.execute('INSERT INTO todo (task_name) VALUES (%s) RETURNING id', (task,))
        task_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return task_id

    def remove_task(self, task_id):
        self.cursor.execute('DELETE FROM todo WHERE id = %s', (task_id,))
        if self.cursor.rowcount == 0:
            print(f"No task found with ID {task_id}.")
        else:
            self.conn.commit()
            print(f"Task with ID {task_id} has been removed successfully.")

    def update_task(self, task_id, new_task_name):
        if not new_task_name:
            print("Please enter a valid task name.")
            return
        self.cursor.execute('UPDATE todo SET task_name = %s WHERE id = %s', (new_task_name, task_id))
        if self.cursor.rowcount == 0:
            print(f"No task found with ID {task_id}.")
        else:
            self.conn.commit()
            print(f"Task with ID {task_id} has been updated successfully.")

    def view_tasks(self):
        self.cursor.execute('SELECT * FROM todo')
        tasks = self.cursor.fetchall()
        if not tasks:
            print('No tasks found.')
        else:
            for task in tasks:
                print(f"ID: {task[0]}, Task: {task[1]}")

    def close(self):
        self.cursor.close()
        self.conn.close()

def main():
    task_manager = TaskManager(dbname='todolist', password='123', user='postgres', host='localhost', port=5432)
    while True:
        user_choice = input("1) Add task, 2) Remove task, 3) Update task, 4) View tasks, 5) Exit: ")
        if user_choice == '1':
            task_name = input("Enter task name: ")
            task_manager.add_task(task_name)
        elif user_choice == '2':
            try:
                task_id = int(input("Enter Task ID to remove: "))
                task_manager.remove_task(task_id)
            except ValueError:
                print("Please enter a valid integer for Task ID.")
        elif user_choice == '3':
            try:
                task_id = int(input("Enter Task ID to update: "))
                new_task_name = input("Enter new task name: ")
                task_manager.update_task(task_id, new_task_name)
            except ValueError:
                print("Please enter a valid integer for Task ID.")
        elif user_choice == '4':
            task_manager.view_tasks()
        elif user_choice == '5':
            task_manager.close()
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == "__main__":
    main()