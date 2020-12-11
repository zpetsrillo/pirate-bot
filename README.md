# Pirate Bot

## Movies

Keep track of movies to be watched on the server. Bot will record all movies suggestions and then document wether they have been watched and assign a rating from the average of user feedback. Movie selection will be based on how many times a movie has been suggested with tie breakers decided by random. Alerts will be sent out to all users with movie watcher role at time of movie screening.

### commands
 - options                     - list available commands with explanation
 - subscribe                   - join the Movies group
 - add [movie]                 - add movie to queue (movie title  - or IMDB Id)
 - all                         - list all unwatched movies
 - top [number]                - list top unwatched movies of  - requested number
 - myAll                       - list all movies you have added
 - vote [movie]                - vote to watch movie
 - watched [movie]             - mark movie as having been watched
 - schedule [mm-dd] [movie]    - schedule movie event

### Setup

Create .env file with the following in same folder as project (you need to complete all the files with your own API keys and file locations)
```
DISCORD_TOKEN=
OMDB_KEY=
MOVIE_DB=
LOG_FILE_DISCORD=
```
Install all required packages
```
pip install -r requirements.txt
```
To run bot, execute bot python file
```
python bot.py
```

### Tables

Not that all tables include a timestamp column as their last column (not displayed here)

#### Movie

| movie_id | title      | year | rated | released    | runtime | genre                            | director  | plot                                                               | poster                                                                                                                             | imdb_rating | imdb_id   |
| -------- | ---------- | ---- | ----- | ----------- | ------- | -------------------------------- | --------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------- |
| 1        | Hereditary | 2018 | R     | 08 Jun 2018 | 127 min | Drama, Horror, Mystery, Thriller | Ari Aster | A grieving family is haunted by tragic and disturbing occurrences. | https://m.media-amazon.com/images/M/MV5BOTU5MDg3OGItZWQ1Ny00ZGVmLTg2YTUtMzBkYzQ1YWIwZjlhXkEyXkFqcGdeQXVyNTAzMTY4MDA@._V1_SX300.jpg | 73          | tt7784604 |

#### User

| user_id | user_name | discriminator |
| ------- | --------- | ------------- |
| 7       | qwak      | 6969          |

#### Votes

| vote_id | movie_id | user_id |
| ------- | -------- | ------- |
| 10      | 1        | 7       |

#### Watched

| watch_id | movie_id | user_id |
| -------- | -------- | ------- |
| 27       | 1        | 7       |
