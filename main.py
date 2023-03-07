# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
import os
import configparser
import pandas as pd
from dotenv import load_dotenv
from helper_functions import add_prompt
from helper_functions import df_to_text
from helper_functions import set_channel
from helper_functions import prompt_to_embed
from views import SubmissionButtons
from views import ApprovePrompt


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


# SETTING OUTPUTS
@bot.command(description = "Ping in output channel")
async def channelping (ctx):
  config = configparser.ConfigParser()
  config.read('peglotron.ini')
  channel_id = int(config['OutputChannels']['channelping'])
  await bot.get_channel(channel_id).send("Ping!")
  await ctx.respond("Pinging...")

@bot.command(description = "Set channelping output channel")
async def pingset(ctx, channel_id: discord.Option(str)):
  set_channel('channelping', channel_id)
  await ctx.respond(f'The output channel for `\\channelping` was set to: {channel_id}')


# APPROVE PROMPTS WITH BUTTONS
@bot.command(description = "Approve or reject prompts")
async def approveprompt(ctx, bucket: discord.Option(str)):
  valid_buckets = ['SFW', 'NSFW', 'WEEKLY']
  bucket_name = bucket.upper()
  embed = discord.Embed(title = f"Next {bucket_name} prompt: ")

  if bucket_name in valid_buckets: # Check if bucket type is valid
    [embed, end] = prompt_to_embed(bucket_name, 0) # create embed to show the initial prompt before the first viewing of ApprovePrompt()
    if end: # end = True if there are no prompts to approve, as handled by prompt_to_embed
      await ctx.respond(content = None, embeds = [embed]) # This does not summon buttons, since there are no prompts to approve
    else:
      await ctx.respond(content = None, view = ApprovePrompt(), embeds = [embed])
  else:
    print("Invalid bucket input")
    await ctx.respond(f"Invalid bucket name. Valid buckets are (not case sensitive): `{valid_buckets}`")   

bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here