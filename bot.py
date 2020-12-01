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
async def watched(ctx, arg):
    user_id = _getUser(ctx)
    movie_id, movie_title = await _getMovie(ctx, arg)
    db.watchedMovie(movie_id, user_id)
    await ctx.send(f"{ctx.author.display_name} watched {movie_title}.")


# @bot.command()
# async def myWatched(ctx):
#     print(f"{ctx.author} listing personal watched")
#     await ctx.send("")


# @bot.command()
# async def mySuggested(ctx):
#     print(f"{ctx.author} listing personal suggested")
#     await ctx.send("")


# @bot.command()
# async def rate(ctx, arg: int):
#     if 0 < arg < 10:
#         print(f"{ctx.author} rating movie: {arg}")
#         await ctx.send("")
#     else:
#         await ctx.send("Sorry, rating must be between 0 - 10. 😢")


@bot.command()
async def add(ctx, arg):
    user_id = _getUser(ctx)
    print(f"{ctx.author} adding movie: {arg}")
    movie = omdb.getMovie(arg)
    try:
        movie_id = db.addMovie(movie)
        db.voteMovie(movie_id, user_id)
        await ctx.send(f"Added movie {movie['Title']}")
    except Exception as e:
        print(e)


@bot.command()
async def vote(ctx, arg):
    user_id = _getUser(ctx)
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
async def announce(ctx, arg):
    movie_id, _ = await _getMovie(ctx, arg)
    print(f"{ctx.author} announcing movie: {movie_id}")
    movie_role = get(ctx.guild.roles, name="Movies")

    announcement, poster_url = movie_announcement(movie_id, movie_role.mention)

    async with aiohttp.ClientSession() as session:
        async with session.get(poster_url) as resp:
            if resp.status != 200:
                return await ctx.send(announcement)
            data = io.BytesIO(await resp.read())
            await ctx.send(announcement, file=discord.File(data, "movie_poster.png"))


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


def movie_announcement(movie_id, role):
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

    announcement = f"""
{role}
Tonight we will be watching

**{title}**

runtime _{runtime}_, rated _{rated}_, released _{released}_, director _{director}_

**{genre}**

IMDB Rating: **{q}.{mod}**

Plot (click to show)
||{plot}||

    """

    return announcement, poster


# Run bot
try:
    bot.run(TOKEN)
except Exception as e:
    print(e)
    bot.close()