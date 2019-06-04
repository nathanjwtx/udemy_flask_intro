import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# must use integer for auto-increment number field instead of int
create_table = ("create table if not exists users (id integer primary key," +
                "username text, password text)")
cursor.execute(create_table)

connection .commit()
connection.close()
