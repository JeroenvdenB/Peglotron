# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
import os
from dotenv import load_dotenv
from helper_functions import add_prompt
from helper_functions import df_to_text
import pandas as pd

# Make a .env locally that contains the token of the server that the bot should log into.
load_dotenv()
token = os.getenv("TOKEN")
bot = discord.Bot()


# Confirm connection in the terminal
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")

# Create Slash commands group with the bot.create_group
# Keep until release as test-commands
greetings = bot.create_group("greetings","Greet people")

@greetings.command(description = "Say hello!")
async def hello(ctx):
  await ctx.respond(f"Hello, {ctx.author}!")

@greetings.command(description = "Say goodbye :(")
async def bye(ctx):
  await ctx.respond(f"Bye, {ctx.author}!")


# Command 'DM me' to make the bot send whoever invokes the command a DM.
@bot.command(description = "The bot DM's you")
async def dm(ctx):
  await ctx.author.send("Hi there!") # DM user that invoked the command
  await ctx.respond(f"Message sent.") # send in channel the command was issued
  msg = await bot.wait_for("message") # await response in DM. Allows for only 1 respons sent. He stops listening after 1 response.
  
  # Add the prompt given to a csv file - uses add_prompt function
  added = add_prompt(ctx,msg) # Function returns True when completed.
  if added:
    await ctx.author.send("I saved your message. Thanks!")
  else:
    await ctx.author.send("A problem occurred when processing your prompt.")

# A command to make the bot show what's in a specific csv file
# Example: show the submissions.csv
# Used a helper function because this behavior will return for all seperate buckets.
@bot.command(decription = "Show submissions.")
async def show(ctx):
  bucket = "SUBMISSIONS"
  response_text = f'```' + df_to_text(bucket) + f'```' #formatting with ``` triggers a markdown window.
  await ctx.respond(response_text)

bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here