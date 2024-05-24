# The TaskManager class in Python manages a todo list stored in a PostgreSQL database, allowing users
# to add, remove, update, and view tasks.
import psycopg2
import time

class TaskManager:
    def __init__(self, dbname, password, user, host, port):
        self.conn = psycopg2.connect(dbname=dbname, password=password, user=user, host=host, port=port)
        self.cursor = self.conn.cursor()
        self.rename_table()
        self.drop_table()
        self.create_table()

    def rename_table(self):
        try:
            table_choice = input('1) to create a new todo list , 2) to work with the default new todo list: ')
            if table_choice == '1':
                new_table_name = input('Enter the new table name: ')
                self.cursor.execute(f'''ALTER TABLE todo RENAME TO {new_table_name}''')
            else:
                self.cursor.execute('ALTER TABLE todo RENAME TO todo')
            self.commit()
        except Exception as error:
            print(f'Error while renaming the table, {str(error)}')
            self.conn.rollback()
    def drop_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS todo''')

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS todo (
                            id SERIAL PRIMARY KEY,
                            task_name CHAR(255)
        )''')
    
    def add_task(self, task): 
        self.cursor.execute('''INSERT INTO todo (task_name) VALUES (%s) RETURNING id''', (task,))
        task_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return task_id
    def remove_task(self, id):
        task_list = self.cursor.fetchall()
        if not task_list:
            print('the list is empty')
        else:
            self.cursor.execute('''DELETE FROM todo WHERE id = %s''', (id,))
            self.conn.commit()
    def update_task(self, taskID, newTaskName):
        try:
            if newTaskName != '':
                self.cursor.execute('''UPDATE todo SET task_name = %s WHERE id = %s''', (newTaskName, taskID))
                self.conn.commit()
            else:
                print("Please enter a task name.")
                print('Task updated successfully')
        except Exception as error:
            print(f'Error while updating the task,{str(error)}')
    def view_tasks(self):
        self.cursor.execute('SELECT * FROM todo')
        tasks_seen = self.cursor.fetchall()
        if not tasks_seen:
            print('No tasks found')
        else:
            for task in tasks_seen:
                print(f"The ID: {task[0]}, The task name: {task[1]}")
            self.conn.commit()
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()

task_manager = TaskManager(dbname='todolist', password='123', user='postgres', host='localhost', port=8080)
while True:
    user_choice = input("1) to add task , 2) to remove task , 3) to update task , 4) to view task , 5) to exit the program: \n")
    if user_choice == '1':
        try:
            addTask = str(input("Add task: "))
            task_manager.add_task(addTask)
            print(f"The '{addTask}' Task has been added successfully")
        except Exception as error:
            print(f"Error while adding the task,{str(error)}")
    elif user_choice == '2':
        try:
            remove_task = input("Remove Task ID: ")
            task_manager.remove_task(remove_task)
            print(f"The '{remove_task}' task has been removed successfully")
        except Exception as error:
            print(f"Error while removing the task,{str(error)}")
    elif user_choice == '3':
        updateTaskById = int(input('Enter the ID of the task you want to update: '))
        newTaskName = input('Enter the new task name: ')
        task_manager.update_task(updateTaskById, newTaskName)
    elif user_choice == '4':
        try:
            print('View tasks: ')
            task_manager.view_tasks()
            task_manager.commit()
        except Exception as error:
            print(f"Error while viewing the task,{str(error)}")
    elif user_choice == '5':
        task_manager.close()
        print('Goodbye!')
        time.sleep(0.5)
        exit()
    else:
        print('please enter a valid choice.')

