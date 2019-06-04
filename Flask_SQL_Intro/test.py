import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# create_table = "create table users (id int, username text, password text)"
# cursor.execute(create_table)

user = (1, "nathan", "wibble")
insert_query = "insert into users values (?, ?, ?)"
# cursor.execute(insert_query, user)

users = [
    (2, "bob", "wobble"),
    (3, "fred", "wilma")
]

# cursor.executemany(insert_query, users)

select_query = "select * from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
