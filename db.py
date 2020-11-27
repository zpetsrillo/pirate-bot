from MovieDB import MovieDB


m = MovieDB()
# m.exec("""INSERT INTO discord_movies VALUES (1, 'Avatar', 2)""")
# m.c.execute("""delete from discord_movies""")
m.create_db()
m.insert(3, "Moon", 1)
print('id, name, votes, seen')
print(m.fetchall("discord_movies"))
m.close()
