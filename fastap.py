from fastapi import FastAPI
import uuid
import sqlite3

conn = sqlite3.connect('mydatabase.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        task_id TEXT,
        result TEXT,
        status TEXT,
    )
''')

app = FastAPI()

my_dict = {}
results = {}


@app.get("/function1")
async def function1(x: int, y: int, operator: str):
    try:
        if operator == "*":
            task_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO users (task_id, result, status) VALUES (?, ?, ?)",
                           (task_id, x * y, 'Ready'))
            return task_id
        elif operator == "+":
            task_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO users (task_id, result, status) VALUES (?, ?, ?)",
                           (task_id, x + y, 'Ready'))
            return task_id
        elif operator == "-":
            task_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO users (task_id, result, status) VALUES (?, ?, ?)",
                           (task_id, x - y, 'Ready'))
            return task_id
        elif operator == "/":
            task_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO users (task_id, result, status) VALUES (?, ?, ?)",
                           (task_id, x / y, 'Ready'))
            return task_id
        else:
            raise ValueError("Некорректный оператор")
    except ZeroDivisionError:
        raise ZeroDivisionError("На ноль делить нельзя!")
    except TypeError:
        raise TypeError("x и y должны быть целыми числами")


@app.get("/function2")
async def function2(task_id: str):
    cursor.execute("SELECT result FROM items WHERE task_id = ?", (task_id,))
    result = cursor.fetchone()
    return result[0]


@app.get("/function3")
async def function3():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for i in users:
        print(f'Task ID: {i[1]}, Result: {i[2]}, Status: {i[3]}')
    conn.close()
