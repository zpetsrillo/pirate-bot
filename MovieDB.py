import sqlite3

from TablesVocab import *


class MovieDB:
    conn = None
    c = None

    def __init__(self):
        self.conn, self.c = self.create_connection()
        self.create_all_db()

    def create_connection(self):
        conn, c = None, None
        try:
            conn = sqlite3.connect(MOVIES_DB)
            c = conn.cursor()
        except Exception as e:
            print(e)

        return conn, c

    def create_db(self, table_name, table_columns, table_types, table_extras=[]):
        info = list(zip(table_columns, table_types))
        info = [f"{x} {y}" for x, y in info]
        info += table_extras
        print(f"Creating table {table_name}")
        try:
            self.c.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(info)}
                )
                """
            )
        except Exception as e:
            print(e)

    def create_all_db(self):
        print("Creating all tables...")
        self.create_db(MOVIES_TABLE, MOVIES_COLUMNS, MOVIES_TYPES)
        self.create_db(USERS_TABLE, USERS_COLUMNS, USERS_TYPES)
        self.create_db(VOTES_TABLE, VOTES_COLUMNS, VOTES_TYPES, VOTES_EXTRAS)
        self.create_db(WATCHED_TABLE, WATCHED_COLUMNS, WATCHED_TYPES, WATCHED_EXTRAS)
        # self.create_db(RATINGS_TABLE, RATINGS_COLUMNS)
        # self.create_db(SCHEDULE_TABLE, SCHEDULE_COLUMNS)
        print("Tables finished building")

    def insert(self, table_name, table_columns, *args):
        values = tuple([x for x in args])
        self.c.execute(
            f"""INSERT INTO {table_name} ({', '.join(table_columns[1:])}) VALUES ({('?,'*len(values))[:-1]})""",
            values,
        )
        self.conn.commit()

    def fetchall(self, table_name):
        self.c.execute(f"""SELECT * FROM {table_name}""")
        return self.c.fetchall()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def addUser(self, name, discriminator):
        self.insert(USERS_TABLE, USERS_COLUMNS, name, discriminator)
        print(f"Added user {name}#{discriminator} to {USERS_TABLE}")
        return self.c.lastrowid

    def getUser(self, name, discriminator):
        self.c.execute(
            f"""
            SELECT {USERS_COLUMNS[0]}
            FROM {USERS_TABLE}
            WHERE
                {USERS_COLUMNS[1]} = '{name}'
                AND {USERS_COLUMNS[2]} = '{discriminator}'
            """
        )
        return self.c.fetchone()[0]

    def addMovie(self, movie):
        title = movie["Title"]
        year = int(movie["Year"])
        rated = movie["Rated"]
        released = movie["Released"]
        runtime = movie["Runtime"]
        genre = movie["Genre"]
        director = movie["Director"]
        plot = movie["Plot"]
        poster = movie["Poster"]
        imdbRating = int(float(movie["imdbRating"]) * 10)
        imdbId = movie["imdbID"]

        self.insert(
            MOVIES_TABLE,
            MOVIES_COLUMNS,
            title,
            year,
            rated,
            released,
            runtime,
            genre,
            director,
            plot,
            poster,
            imdbRating,
            imdbId,
        )
        print(f"Added {title} - {imdbId} to {MOVIES_TABLE}")
        return self.c.lastrowid

    def voteMovie(self, movie_id, user_id):
        self.insert(VOTES_TABLE, VOTES_COLUMNS, movie_id, user_id)
        print(f"USER_ID:{user_id} voted for MOVIE_ID:{movie_id}")

    def all_unwatched(self):
        self.c.execute(
            f"""
            SELECT
                M.movie_id,
                M.title,
                V.votes
            FROM
                {MOVIES_TABLE} AS M
                LEFT JOIN 
                (
                    SELECT
                        movie_id,
                        COUNT(user_id) as votes
                    FROM
                        {VOTES_TABLE}
                    GROUP BY
                        movie_id
                ) AS V ON M.movie_id = V.movie_id
                LEFT JOIN
                (
                    SELECT
                        movie_id,
                        count(user_id) as seen
                    FROM
                        {WATCHED_TABLE}
                    GROUP BY
                        movie_id
                ) AS W on M.movie_id = W.movie_id
            WHERE
                W.seen IS NULL
            ORDER BY
                votes DESC
            ;
            """
        )
        return self.c.fetchall()
