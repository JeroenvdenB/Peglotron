# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
import os
from dotenv import load_dotenv
from helper_functions import add_prompt
from helper_functions import df_to_text
import pandas as pd
from views import SubmissionButtons

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
  await ctx.author.send("Hi there! I'll log your messages. Type \"stop\" to stop this interaction.") # DM user that invoked the command
  await ctx.respond(f"I sent you a DM.") # send in channel the command was issued
  listen = True # To keep the bot listening for the next reply.

  while listen:
    msg = await bot.wait_for("message") # await response in DM. Allows for only 1 respons sent. He stops listening after 1 response.
    
    if msg.content.lower() == "stop":
      listen = False
      await ctx.author.send("Okay! Thanks for talking to me. I'll stop listening now.")
      break
    else:
      pass
  
    user = ctx.author
    bucket = 'SFW' # Default open_SFW bucket for now
    added = add_prompt(user,msg,bucket) # Add the prompt given to a csv file - uses add_prompt function
    if added:
      await ctx.author.send("I saved your message. Thanks!")
    else:
      await ctx.author.send("A problem occurred when processing your prompt.")


# A command to make the bot show what's in a specific csv file
# Example: show the submissions.csv
# Used a helper function because this behavior will return for all seperate buckets.
@bot.command(description = "Show saved submissions.")
async def show(ctx):
  bucket = "OPEN_SFW_SUBMISSIONS"
  response_text = f'```' + df_to_text(bucket) + f'```' #formatting with ``` triggers a markdown window.
  await ctx.respond(response_text)


# BUTTONS
# All views are in views.py
@bot.command(description = "Summon the submissions buttons.")
async def submitbutton(ctx):
  await ctx.respond("Choose which type of submission you'd like to do!", view = SubmissionButtons(timeout=180))

@bot.command(description = "Ping in output channel")
async def channelping (ctx):
  channel_id = int(os.getenv("PINGSET")) # .env yields strings. Convert to int for channel id
  channel = bot.get_channel(channel_id)
  await channel.send("Ping!")
  await ctx.respond("Pinging...")

@bot.command(description = "Set channelping output channel")
async def pingset(ctx, channel_id: discord.Option(str)):
  os.environ["PINGSET"] = channel_id
  print(os.environ["PINGSET"])
  print(os.getenv("PINGSET"))
  await ctx.respond(f'You entered the id: {channel_id}') # I'd like to get the id as int but the number is too big.


bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here