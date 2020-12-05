import sqlite3
from datetime import datetime
import discord_logger

from TablesVocab import *


class MovieDB:
    conn = None
    c = None

    def __init__(self, logger):
        self.logger = logger
        self.conn, self.c = self.create_connection()
        self.create_all_db()

    def create_connection(self):
        conn, c = None, None
        try:
            conn = sqlite3.connect(MOVIES_DB, check_same_thread=False)
            c = conn.cursor()
        except Exception as e:
            self.logger.log(e)

        return conn, c

    def create_db(self, table_name, table_columns, table_types, table_extras=[]):
        info = list(zip(table_columns, table_types))
        info = [f"{x} {y}" for x, y in info]
        info += table_extras
        self.logger.log(f"Creating table {table_name}")
        try:
            self.c.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(info)}
                )
                """
            )
        except Exception as e:
            self.logger.log(e)

    def create_all_db(self):
        self.logger.log("Creating all tables...")
        self.create_db(MOVIES_TABLE, MOVIES_COLUMNS, MOVIES_TYPES)
        self.create_db(USERS_TABLE, USERS_COLUMNS, USERS_TYPES, USERS_EXTRAS)
        self.create_db(VOTES_TABLE, VOTES_COLUMNS, VOTES_TYPES, VOTES_EXTRAS)
        self.create_db(WATCHED_TABLE, WATCHED_COLUMNS, WATCHED_TYPES, WATCHED_EXTRAS)
        # self.create_db(RATINGS_TABLE, RATINGS_COLUMNS)
        self.logger.log("Tables finished building")

    def insert(self, table_name, table_columns, *args):
        values = tuple([x for x in args])
        self.c.execute(
            f"""INSERT OR IGNORE INTO {table_name} ({', '.join(table_columns[1:])}) VALUES ({('?,'*len(values))[:-1]}, '{datetime.now()}')""",
            values,
        )
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def addUser(self, name, discriminator):
        self.insert(USERS_TABLE, USERS_COLUMNS, name, discriminator)
        self.logger.log(f"Added user {name}#{discriminator} to {USERS_TABLE}")
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
        self.logger.log(f"Added {title} - {imdbId} to {MOVIES_TABLE}")
        return self.c.lastrowid

    def getMovie(self, movie_id):
        try:
            int(movie_id)
            return self._getMovieById(movie_id)
        except:
            if movie_id[:2] == "tt":
                return self._getMovieByIMDB(movie_id)
            else:
                return self._getMovieByTitle(movie_id)

    def _getMovieById(self, movie_id):
        self.c.execute(
            f"""
            SELECT {", ".join(MOVIES_COLUMNS[:2])}
            FROM {MOVIES_TABLE}
            WHERE movie_id = '{movie_id}'
            """
        )
        return self.c.fetchone()

    def _getMovieByTitle(self, title):
        self.c.execute(
            f"""
            SELECT {", ".join(MOVIES_COLUMNS[:2])}
            FROM {MOVIES_TABLE}
            WHERE title LIKE '%{title}%'
            """
        )
        return self.c.fetchone()

    def _getMovieByIMDB(self, imdb_id):
        self.c.execute(
            f"""
            SELECT {", ".join(MOVIES_COLUMNS[:2])}
            FROM {MOVIES_TABLE}
            WHERE imdb_id = '{imdb_id}'
            """
        )
        return self.c.fetchone()

    def getMovieFull(self, movie_id):
        self.c.execute(
            f"""
            SELECT *
            FROM {MOVIES_TABLE}
            WHERE movie_id = '{movie_id}'
            """
        )
        return self.c.fetchone()

    def voteMovie(self, movie_id, user_id):
        self.insert(VOTES_TABLE, VOTES_COLUMNS, movie_id, user_id)
        self.logger.log(f"USER_ID:{user_id} voted for MOVIE_ID:{movie_id}")

    def watchedMovie(self, movie_id, user_id):
        self.insert(WATCHED_TABLE, WATCHED_COLUMNS, movie_id, user_id)
        self.logger.log(f"USER_ID:{user_id} watched MOVIE_ID:{movie_id}")

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

    def user_unwatched(self, user_id):
        self.c.execute(
            f"""
            SELECT
                M.movie_id,
                M.title
            FROM
                {MOVIES_TABLE} AS M
                LEFT JOIN 
                (
                    SELECT
                        movie_id,
                        user_id
                    FROM
                        {VOTES_TABLE}
                    WHERE
                        user_id = '{user_id}'
                ) AS V ON M.movie_id = V.movie_id
            WHERE
                V.user_id = '{user_id}'
            ORDER BY
                M.timestamp DESC
            ;
            """
        )
        return self.c.fetchall()
