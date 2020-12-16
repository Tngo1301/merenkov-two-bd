# Работа со второй базой данных
import sqlite3
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()
cursor.execute("SELECT Hint from demo where Name = 'string_first'")
link = "".join(str(cursor.fetchall()).split('\'')[1:-1])
conn.close()
print(link)
