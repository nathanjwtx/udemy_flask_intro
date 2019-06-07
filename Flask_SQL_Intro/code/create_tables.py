import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# must use integer for auto-increment number field instead of int
# create_table = ("create table if not exists users (id integer primary key," +
#                 "username text, password text)")
# cursor.execute(create_table)

create_table = ("create table if not exists items (id integer primary key," +
                "name text, price float)")
cursor.execute(create_table)

cursor.execute("insert into items values(null, 'Grill', 199.99)")

connection .commit()
connection.close()
