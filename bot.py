import os
import discord
from discord.ext import commands
from discord.utils import get
import discord_logger
from bot_logger import BotLogger
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import io
import aiohttp
from OMDB import OMDB
from MovieDB import MovieDB
from Scheduler import Scheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Create bot
bot = commands.Bot(command_prefix="movie/")

# Create OMDB API object
omdb = OMDB()

# Private logging functions
botLogger = BotLogger(discord_logger.logger)

# Create MovieDB object
db = MovieDB(logger=botLogger)

# Create Scheduler object
scheduler = Scheduler()
scheduler.start()


@bot.command()
async def options(ctx):
    botLogger.log(f"{ctx.author} asked for help")
    await ctx.send(
        f"""
```
subscribe                   - join the Movies group
add [movie]                 - add movie to queue (movie title or IMDB Id)
all                         - list all unwatched movies
top [number]                - list top unwatched movies of requested number
myAll                       - list all movies you have added
vote [movie]                - vote to watch movie
watched [movie]             - mark movie as having been watched
schedule [mm-dd] [movie]    - schedule movie event
```
    """
    )


@bot.command()
async def subscribe(ctx):
    botLogger.log(f"Adding user {ctx.author} to Movies...")
    movie_role = get(ctx.guild.roles, name="Movies")
    await ctx.author.add_roles(movie_role)
    try:
        db.getUser(ctx.author.name, ctx.author.discriminator)
        await ctx.send(f"{ctx.author.display_name}, you are already subscribed.")
    except:
        try:
            db.addUser(
                ctx.author.name, ctx.author.discriminator,
            )
            await ctx.send(
                f"{ctx.author.display_name} has been added to the movie watchers group!"
            )
            botLogger.log("Added successfully")
        except Exception as e:
            botLogger.warn(repr(e))


@bot.command()
async def all(ctx):
    botLogger.log(f"{ctx.author} listing all")
    movies = db.all_unwatched()
    table = tabulate(movies, headers=["Id", "Title", "Votes"])
    if len(table) >= 2000:
        with open("all_movies.txt", "w") as f:
            f.write(table)
        await ctx.send(file=discord.File(r"./all_movies.txt"))
    else:
        await ctx.send(f"""```{table}```""")


@bot.command()
async def top(ctx, arg: int = 5):
    botLogger.log(f"{ctx.author} listing all")
    movies = db.all_unwatched()
    arg = min(len(movies), arg)
    movies = movies[:arg]
    table = tabulate(movies, headers=["Id", "Title", "Votes"])
    await ctx.send(f"""```{table}```""")


@bot.command()
async def watched(ctx, *args):
    user_id = await _getUser(ctx)
    if len(args) == 0:
        watched_movies = db.all_watched()
        table = tabulate(watched_movies, headers=["Id", "Title", "Date"])
        await ctx.send(f"""```{table}```""")
    elif user_id is not None:
        arg = " ".join(args)
        movie_id, movie_title = await _getMovie(ctx, arg)
        db.watchedMovie(movie_id, user_id)
        await ctx.send(f"{movie_title} marked as watched.")


@bot.command()
async def myAll(ctx):
    botLogger.log(f"{ctx.author} listing personal all")
    user_id = await _getUser(ctx)
    if user_id is not None:
        movies = db.user_unwatched(user_id)
        table = tabulate(movies, headers=["Id", "Title"])
        await ctx.send(f"""```{table}```""")


@bot.command()
async def add(ctx, *, arg):
    user_id = await _getUser(ctx)
    if user_id is not None:
        botLogger.log(f"{ctx.author} adding movie: {arg}")
        movie = omdb.getMovie(arg)
        try:
            movie_id = db.addMovie(movie)
            db.voteMovie(movie_id, user_id)
            await ctx.send(
                f"Added movie {movie['Title']}, released: {movie['Year']} (id: {movie_id})"
            )
        except Exception as e:
            botLogger.warn(repr(e))


@bot.command()
async def vote(ctx, *, arg):
    user_id = await _getUser(ctx)
    if user_id is not None:
        botLogger.log(f"{ctx.author} voting movie: {arg}")
        movie_id, movie_title = await _getMovie(ctx, arg)
        db.voteMovie(movie_id, user_id)
        await ctx.send(f"{ctx.author.display_name} voted for {movie_title}.")


@bot.command()
async def schedule(ctx, *args):
    user_id = await _getUser(ctx)
    if len(args) == 0:
        scheduled_movies = db.getScheduled()
        table = tabulate(scheduled_movies, headers=["Id", "Title", "Date"])
        await ctx.send(f"""```{table}```""")
    elif len(args) < 3:
        await ctx.send(f"Missing arguments. Try Again.")
    else:
        if user_id is not None:
            now = datetime.now()
            date = datetime.strptime(
                f"{now.year}-{args[0]} {args[1]}", "%Y-%m-%d %H:%M"
            )
            if date.month < now.month:
                date = date + relativedelta(years=1)
            if date <= datetime.now():
                await ctx.send(f"Please schedule event in the future.")
            else:
                announe_date = date + relativedelta(days=-1)
                movie_id, title = await _getMovie(ctx, " ".join(args[2:]))
                if announe_date <= datetime.now():
                    await _announce(ctx.channel.id, movie_id, date)
                else:
                    scheduler.add_job(
                        _announce, announe_date, ctx.channel.id, movie_id, date
                    )
                    await ctx.send(
                        f"{ctx.author.display_name} scheduled {title} for {date}."
                    )
                db.addSchedule(movie_id, date)
                scheduler.add_job(_watchedMovie, date, movie_id, user_id)
                botLogger.log(
                    f"{ctx.author} scheduled MOVIE_ID:{movie_id} as event for {date}"
                )


async def _announce(channel_id, movie_id, date):
    ctx = bot.get_channel(channel_id)

    botLogger.log(f"announcing movie: {movie_id}")
    movie_role = get(ctx.guild.roles, name="Movies")

    announcement = movie_announcement(movie_id, date)

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


def _watchedMovie(movie_id, user_id):
    db.watchedMovie(movie_id, user_id)


def movie_announcement(movie_id, date):
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

    e.set_author(name=f"📽🍿🎬 Movie Night 🎬🍿📽")
    e.set_image(url=poster)
    e.add_field(name="Genre", value=genre)
    e.add_field(name="Date", value=date.strftime("%A %b, %d"), inline=True)
    e.add_field(name="Time", value=f"{date.strftime('%I:%M %p')} CST", inline=True)
    e.set_footer(text=f"{plot}")

    return e


# Run bot
try:
    bot.run(TOKEN)
except Exception as e:
    botLogger.error(repr(e))
    bot.close()
    scheduler.shutdown()
