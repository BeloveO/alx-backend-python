import sqlite3
from contextlib import contextmanager
import time
import functools


#### Reusable context manager that takes a query as input and executes it, managing both connection and the query execution

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params or ())
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print(f"Closed connection to {self.db_name}")

#### Example usage of the ExecuteQuery context manager
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as cursor:
    users = cursor.fetchall()
    print(users)
    cursor.close()
