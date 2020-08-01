import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)"
cursor.execute(create_table)

user = (1, 'bob', 'abcd')

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'jose', 'abcd'),
    (3, 'ronald', 'abcd'),
    (4, 'alex', 'abcd'),
    (5, 'sam', 'abcd')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

#to save changes in database
connection.commit()
connection.close()
