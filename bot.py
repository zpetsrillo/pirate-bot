import os
import discord
from discord.ext import commands
from discord.utils import get
import discord_logger
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
async def subscribe(ctx):
    print(f"Adding user {ctx.author} to Users...")
    movie_role = get(ctx.guild.roles, name="Movies")
    await ctx.author.add_roles(movie_role)
    db.addUser(ctx.author.name, ctx.author.discriminator)
    await ctx.send(f"{ctx.author} has been added to the movie watchers group!")
    print("Added successfully")


@bot.command()
async def all(ctx):
    print(f"{ctx.author} listing all")
    await ctx.send("")


@bot.command()
async def watched(ctx):
    print(f"{ctx.author} listing watched")
    await ctx.send("")


@bot.command()
async def queued(ctx):
    print(f"{ctx.author} listing queued")
    await ctx.send("")


@bot.command()
async def myWatched(ctx):
    print(f"{ctx.author} listing personal watched")
    await ctx.send("")


@bot.command()
async def mySuggested(ctx):
    print(f"{ctx.author} listing personal suggested")
    await ctx.send("")


@bot.command()
async def rate(ctx, arg: int):
    if 0 < arg < 10:
        print(f"{ctx.author} rating movie: {arg}")
        await ctx.send("")
    else:
        await ctx.send("Sorry, rating must be between 0 - 10. 😢")


@bot.command()
async def add(ctx, arg):
    print(f"{ctx.author} adding movie: {arg}")
    movie = omdb.getMovie(arg)
    movie_id = db.addMovie(movie)
    user_id = db.getUser(ctx.author.name, ctx.author.discriminator)
    db.voteMovie(movie_id, user_id)
    await ctx.send(f"Added movie {movie['Title']}")


@bot.command()
async def schedule(ctx, arg0, arg1):
    now = datetime.now()
    date = datetime.strptime(f"{now.year}-{arg0} {arg1}", "%Y-%m-%d %H:%M")
    if date.month < now.month:
        date = date + relativedelta(years=1)
    print(f"{ctx.author} scheduled event for {date}")
    await ctx.send("")


# Run bot
# bot.run(TOKEN)
db.addUser("Zachariah", "0001")
movie_id = db.addMovie(omdb.getMovie("hereditary"))
user_id = db.getUser("Zachariah", "0001")
db.voteMovie(1, user_id)
print(db.all_unwatched())