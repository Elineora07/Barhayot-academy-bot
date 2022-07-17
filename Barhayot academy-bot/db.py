import sqlite3

con = sqlite3.connect("data.db")

cur = con.cursor()


cur.execute('''CREATE TABLE user
            (user_id int,
            Full_name text,
            phone text
            )
''')


cur.execute('''CREATE TABlE admin
            (user_id int)
''')

cur.execute("INSERT INTO admin VALUES (701510985)")

con.commit()