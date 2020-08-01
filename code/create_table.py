import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)"
cursor.execute(query)

query = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(query)

connection.close()
