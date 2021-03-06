import os
from dotenv import load_dotenv

load_dotenv()
MOVIE_DB = os.getenv("MOVIE_DB")

# Database
MOVIES_DB = MOVIE_DB

# Movies table
MOVIES_TABLE = "movies"
MOVIES_COLUMNS = [
    "movie_id",
    "title",
    "year",
    "rated",
    "released",
    "runtime",
    "genre",
    "director",
    "plot",
    "poster",
    "imdb_rating",
    "imdb_id",
    "timestamp",
]
MOVIES_TYPES = [
    "INTEGER PRIMARY KEY",
    "TEXT NOT NULL",
    "INTEGER",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "TEXT",
    "INTEGER",
    "TEXT NOT NULL UNIQUE",
    "TEXT NOT NULL",
]

# Users table
USERS_TABLE = "users"
USERS_COLUMNS = ["user_id", "name", "discriminator", "timestamp"]
USERS_TYPES = [
    "INTEGER PRIMARY KEY",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
]
USERS_EXTRAS = [f"UNIQUE(name, discriminator)"]

# Votes table
VOTES_TABLE = "votes"
VOTES_COLUMNS = ["vote_id", "movie_id", "user_id", "timestamp"]
VOTES_TYPES = [
    "INTEGER PRIMARY KEY",
    "INTEGER NOT NULL",
    "INTEGER NOT NULL",
    "TEXT NOT NULL",
]
VOTES_EXTRAS = [
    f"FOREIGN KEY (movie_id) REFERENCES {MOVIES_TABLE} (movie_id)",
    f"FOREIGN KEY (user_id) REFERENCES {USERS_TABLE} (user_id)",
    f"UNIQUE(movie_id, user_id)",
]

# Watched table
WATCHED_TABLE = "watched"
WATCHED_COLUMNS = ["watch_id", "movie_id", "user_id", "timestamp"]
WATCHED_TYPES = [
    "INTEGER PRIMARY KEY",
    "INTEGER NOT NULL UNIQUE",
    "INTEGER NOT NULL",
    "TEXT NOT NULL",
]
WATCHED_EXTRAS = [
    f"FOREIGN KEY (movie_id) REFERENCES {MOVIES_TABLE} (movie_id)",
    f"FOREIGN KEY (user_id) REFERENCES {USERS_TABLE} (user_id)",
]

SCHEDULE_TABLE = "schedule"
SCHEDULE_COLUMNS = ["schedule_id", "movie_id", "date", "timestamp"]
SCHEDULE_TYPES = [
    "INTEGER PRIMARY KEY",
    "INTEGER NOT NULL",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
]
SCHEDULE_EXTRAS = [
    f"FOREIGN KEY (movie_id) REFERENCES {MOVIES_TABLE} (movie_id)",
    f"UNIQUE(movie_id, date)",
]