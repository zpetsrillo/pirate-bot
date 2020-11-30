# Pirate Bot

## Movies

Keep track of movies to be watched on the server. Bot will record all movies suggestions and then document wether they have been watched and assign a rating from the average of user feedback. Movie selection will be based on how many times a movie has been suggested with tie breakers decided by random. Alerts will be sent out to all users with movie watcher role at time of movie screening.

### commands
 - subscribe: join the movie role in server
 - all: list all queued movies
 - watched: list all watched movies
 - complete: list all movies
 - rate X: rate current movie
 - add X: add movie
 - vote X: vote to watch movie
 - schedule mm-dd hh:mm : schedule next viewing
 - my watched: list of all movies you have watched
 - my suggested: list of all movies you have suggested


#### Movie

| movie_id | title      | year | rated | released    | runtime | genre                           | director  | plot                                                               | poster                                                                                                                             | imdb_rating | imdb_id   |
| -------- | ---------- | ---- | ----- | ----------- | ------- | ------------------------------- | --------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------- |
| 1        | Hereditary | 2018 | R     | 08 Jun 2018 | 127 min | Drama, Horro, Mystery, Thriller | Ari Aster | A grieving family is haunted by tragic and disturbing occurrences. | https://m.media-amazon.com/images/M/MV5BOTU5MDg3OGItZWQ1Ny00ZGVmLTg2YTUtMzBkYzQ1YWIwZjlhXkEyXkFqcGdeQXVyNTAzMTY4MDA@._V1_SX300.jpg | 73          | tt7784604 |

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

#### Ratings

| rating_id | movie_id | user_id | rating |
| --------- | -------- | ------- | ------ |
| 213       | 1        | 7       | 5      |

#### Schedule
| schedule_id | watch_date       | movie_id |
| ----------- | ---------------- | -------- |
| 78          | 11-20-2020 10:30 | 1        |
