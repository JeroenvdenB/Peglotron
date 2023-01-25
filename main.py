# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
import os
from dotenv import load_dotenv
import pandas as pd

# Make a .env locally that contains the token of the server that the bot should log into.
load_dotenv()
token = os.getenv("TOKEN")

bot = discord.Bot()

# Load any required csv files
df = pd.read_csv('recieved_msg.csv', delimiter = ';')
print(f'file loaded. Printing...', df)

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
  print("recieved message: " + msg.content) # print to terminal to confirm received message

  # Add the prompt given to a csv file (loaded at start of the code)
  user = ctx.author
  text = msg.content
  add_this = pd.DataFrame([[user, text]], columns=('user','text'))
  new_df = pd.concat([df, add_this], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
  new_df.to_csv('recieved_msg.csv', index=False, sep=';') # Overwrite existing file
  print(new_df)
  # Move the writing to csv to a helper function to call on. Overwrites prompts file.
  # Every function that uses prompts must reload the file fresh and save changes!
  # Don't let it linger in memory!
  





bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here