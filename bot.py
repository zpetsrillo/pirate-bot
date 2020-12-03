import os
import discord
from discord.ext import commands
from discord.utils import get
import discord_logger
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import io
import aiohttp
from OMDB import OMDB
from MovieDB import MovieDB

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Create bot
bot = commands.Bot(command_prefix="movie/")

# Create OMDB API object
omdb = OMDB()

# Create MovieDB object
db = MovieDB()


@bot.command()
async def options(ctx):
    print(f"{ctx.author} asked for help")
    await ctx.send(
        f"""
```
subscribe       - join the Movies role on the server to be mentioned in announcements
add [movie]     - add movie to queue in order to be voted on and announced (movie title or IMDB Id)
all             - list all unwatched movies
top [number]    - list top unwatched movies of requested number
myAdded         - list all movies you have added
myWatched       - list all movies you have watched
vote [movie]    - vote to watch movie
watched [movie] - mark movie as having been watched
announce [movie]- announce movie to be watched that night
```
    """
    )


@bot.command()
async def subscribe(ctx):
    print(f"Adding user {ctx.author} to Movies...")
    movie_role = get(ctx.guild.roles, name="Movies")
    await ctx.author.add_roles(movie_role)
    try:
        db.getUser(ctx.author.name, ctx.author.discriminator)
        await ctx.send(f"{ctx.author.display_name}, you are already subscribed.")
    except:
        try:
            db.addUser(
                ctx.author.name,
                ctx.author.discriminator,
            )
            await ctx.send(
                f"{ctx.author.display_name} has been added to the movie watchers group!"
            )
            print("Added successfully")
        except Exception as e:
            print(e)


@bot.command()
async def all(ctx):
    print(f"{ctx.author} listing all")
    movies = db.all_unwatched()
    table = tabulate(movies, headers=["Id", "Title", "Votes"])
    await ctx.send(f"""```{table}```""")


@bot.command()
async def top(ctx, arg: int = 5):
    print(f"{ctx.author} listing all")
    movies = db.all_unwatched()
    arg = min(len(movies), arg)
    movies = movies[:arg]
    table = tabulate(movies, headers=["Id", "Title", "Votes"])
    await ctx.send(f"""```{table}```""")


@bot.command()
async def watched(ctx, *, arg):
    user_id = await _getUser(ctx)
    movie_id, movie_title = await _getMovie(ctx, arg)
    db.watchedMovie(movie_id, user_id)
    await ctx.send(f"{ctx.author.display_name} watched {movie_title}.")


@bot.command()
async def myWatched(ctx):
    print(f"{ctx.author} listing personal watched")
    user_id = await _getUser(ctx)
    movies = db.user_watched(user_id)
    table = tabulate(movies, headers=["Id", "Title", "Watch Date"])
    await ctx.send(f"""```{table}```""")


@bot.command()
async def myAdded(ctx):
    print(f"{ctx.author} listing personal added")
    user_id = await _getUser(ctx)
    movies = db.user_unwatched(user_id)
    table = tabulate(movies, headers=["Id", "Title", "Add Date"])
    await ctx.send(f"""```{table}```""")


# @bot.command()
# async def rate(ctx, arg: int):
#     if 0 < arg < 10:
#         print(f"{ctx.author} rating movie: {arg}")
#         await ctx.send("")
#     else:
#         await ctx.send("Sorry, rating must be between 0 - 10. 😢")


@bot.command()
async def add(ctx, *, arg):
    user_id = await _getUser(ctx)
    print(f"{ctx.author} adding movie: {arg}")
    movie = omdb.getMovie(arg)
    try:
        movie_id = db.addMovie(movie)
        db.voteMovie(movie_id, user_id)
        await ctx.send(f"Added movie {movie['Title']}")
    except Exception as e:
        print(e)


@bot.command()
async def vote(ctx, *, arg):
    user_id = await _getUser(ctx)
    print(f"{ctx.author} voting movie: {arg}")
    movie_id, movie_title = await _getMovie(ctx, arg)
    db.voteMovie(movie_id, user_id)
    await ctx.send(f"{ctx.author.display_name} voted for {movie_title}.")


# @bot.command()
# async def schedule(ctx, arg0, arg1):
#     now = datetime.now()
#     date = datetime.strptime(f"{now.year}-{arg0} {arg1}", "%Y-%m-%d %H:%M")
#     if date.month < now.month:
#         date = date + relativedelta(years=1)
#     print(f"{ctx.author} scheduled event for {date}")
#     await ctx.send(f"{ctx.author.display_name} scheduled event for {date}.")


@bot.command()
async def announce(ctx, *, arg):
    movie_id, _ = await _getMovie(ctx, arg)
    print(f"{ctx.author} announcing movie: {movie_id}")
    movie_role = get(ctx.guild.roles, name="Movies")

    announcement = movie_announcement(movie_id)

    await ctx.send(movie_role.mention, embed=announcement)


async def _getMovie(ctx, movie):
    try:
        return db.getMovie(movie)
    except:
        await ctx.send(f"Couldn't find that movie 😢. Please try again.")


async def _getUser(ctx):
    try:
        return db.getUser(ctx.author.name, ctx.author.discriminator)
    except:
        await ctx.send(f"Sorry, you must be subscribed to use this command. 😿")


def movie_announcement(movie_id):
    movie = db.getMovieFull(movie_id)

    (
        movie_id,
        title,
        _,
        rated,
        released,
        runtime,
        genre,
        director,
        plot,
        poster,
        imdb_rating,
        _,
        _,
    ) = movie

    q, mod = divmod(imdb_rating, 10)

    e = discord.Embed(
        title=title,
        description=f"imdb _{q}.{mod}_, runtime _{runtime}_, rated _{rated}_, released _{released}_, director _{director}_",
        colour=discord.Colour.green(),
    )

    e.set_author(name=f"📽🍿🎬 Tonight We're Watching 🎬🍿📽")
    e.set_image(url=poster)
    e.add_field(name="Genre", value=genre)
    e.set_footer(text=f"{plot}")

    return e


# Run bot
try:
    bot.run(TOKEN)
except Exception as e:
    print(e)
    bot.close()