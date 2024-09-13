import sqlite3


connection = sqlite3.connect("log.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE movie(title, year, score)")

result = cursor.execute("SELECT name FROM sqlite_master")
print(result.fetchone())

cursor.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")

connection.commit()

new_result = cursor.execute("SELECT score FROM movie")
print(new_result.fetchall())
