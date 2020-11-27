import sqlite3

from TablesVocab import MOVIES_DB, MOVIES_TABLE, MOVIES_COLUMNS


class MovieDB:
    def __init__(self):
        self.conn = sqlite3.connect(f"{MOVIES_DB}")
        self.c = self.conn.cursor()

    def create_db(self):
        self.c.execute(f"""CREATE TABLE {MOVIES_TABLE} ({', '.join(MOVIES_COLUMNS)})""")

    def insert(self, *args):
        values = tuple([x for x in args])
        self.c.execute(f"""INSERT INTO {MOVIES_TABLE} VALUES (?,?,?,0)""", values)
        self.conn.commit()

    def fetchall(self, table):
        self.c.execute(f"""SELECT * FROM {MOVIES_TABLE}""")
        return self.c.fetchall()

    def close(self):
        self.conn.commit()
        self.conn.close()

