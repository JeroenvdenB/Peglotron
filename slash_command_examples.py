# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
import os
from dotenv import load_dotenv

# Make a .env locally that contains the token of the server that the bot should log into.
load_dotenv()
token = os.getenv("TOKEN")

# Declare intents
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

# Confirm connection in terminal
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Create Slash commands group with the bot.create_group
greetings = bot.create_group("greetings","Greet people")

@greetings.command(description = "Say hello!")
async def hello(ctx):
    await ctx.respond(f"Hello, {ctx.author}!")

@greetings.command(description = "Say goodbye :(")
async def bye(ctx):
    await ctx.respond(f"Bye, {ctx.author}!")



# Create the ping-pong slas command
@bot.command(description = "Sends the bot's latency")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

# Testing some math thingy
@bot.command(description = "Add two integers")
async def add(ctx, first: discord.Option(int), second: discord.Option(int)): # pycord will figure out the types for you
  # you can use them as they were actual integers
  sum = first + second
  await ctx.respond(f"The sum of {first} and {second} is {sum}.")

@bot.command(description = "Add two strings") # this explicitly tells pycord what types the options are instead of it figuring it out by itself
async def join(
  ctx,
  first: discord.Option(discord.SlashCommandOptionType.string),
  second: discord.Option(discord.SlashCommandOptionType.string)
):
  joined = first + second
  await ctx.respond(f"When you join \"{first}\" and \"{second}\", you get: \"{joined}\".")



bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here