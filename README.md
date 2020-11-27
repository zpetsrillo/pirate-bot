# Pirate Bot

## Movies

Keep track of movies to be watched on the server. Bot will record all movies suggestions and then document wether they have been watched and assign a rating from the average of user feedback. Movie selection will be based on how many times a movie has been suggested with tie breakers decided by random. Alerts will be sent out to all users with movie watcher role at time of movie screening.

### commands
 - subscribe: join the movie role in server
 - all: list all movies
 - watched: list all watched movies
 - queued: list of queued movies
 - rate X: rate current movie
 - suggest X: suggest movie
 - schedule mm-dd-yyyy hh:mm : schedule next viewing
 - my watched: list of all movies you have watched
 - my suggested: list of all movies you have suggested


#### Movie

| movie_id | movie_name       | watched | schedule_id |
| -------- | ---------------- | ------- | ----------- |
| 420      | Fateful Findings | 1       | 78          |

#### User

| user_id | user_name |
| ------- | --------- |
| 69      | qwak      |

#### Votes

| vote_id | movie_id | user_id |
| ------- | -------- | ------- |
| 10      | 420      | 69      |

#### Watched

| watch_id | movie_id | user_id |
| -------- | -------- | ------- |
| 27       | 420      | 69      |

#### Ratings

| rating_id | movie_id | user_id | rating |
| --------- | -------- | ------- | ------ |
| 213       | 420      | 69      | 5      |

#### Schedule
| schedule_id | watch_date       | movie_id |
| ----------- | ---------------- | -------- |
| 78          | 11-20-2020 10:30 | 420      |
