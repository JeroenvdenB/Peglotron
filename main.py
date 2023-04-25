# The main goal of this version is to get slash commands working
# and show a whole bunch of examples for future reference.

import discord
from discord import default_permissions
from discord.ext import tasks, commands
import os
import configparser
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from helper_functions import set_channel
from helper_functions import prompt_to_embed
from helper_functions import format_prompt
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
@default_permissions(administrator = True)
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

@bot.command(description = "Show the current prompt.")
async def show(ctx, bucket: discord.Option(str)):
  valid_buckets = ['SFW', 'NSFW', 'WEEKLY']
  bucket_name = bucket.upper()

  if bucket_name in valid_buckets:
    # The index number of the current prompt is stored in the ini file
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    index_str = config['CurrentPrompts'][bucket_name]
    index = int(index_str)
    # Then retrieve the prompt information from the USED prompts list 
    filepath = os.getenv(f"USED_{bucket_name}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter = ';')
    prompt = df['prompt'][index]
    user = df['user'][index]
    shown = int(df['shown'][index])
    
    embed = format_prompt(bucket_name, prompt, user, shown)
    await ctx.respond(embeds = [embed])
  else:
    await ctx.respond("Something went wrong. Notify my overlord, please.")
  

@tasks.loop(minutes = 60)
async def refresh_prompts():
  hour = datetime.now().strftime("%H") # Fetches system time, hour only on a 24-hour scale
  if hour == 12:
    print("The hour is 12 - time for a new prompt.")
    # Insert code to poop out prompt and refresh
  else:
    print("The hour is not 12.")

@tasks.loop(minutes = 1) # This works! Use this kind of code to send daily prompts after a new one is assigned.
async def send_server_message(): # use code from channelping command, because I know it works.
  config = configparser.ConfigParser()
  config.read('peglotron.ini')
  # channel_id = int(config['OutputChannels']['channelping'])
  await bot.wait_until_ready() # hold off on next task until the bot has connected, or it'll error out looking for a channel ID it can't find.
  await bot.get_channel(int("975425044190732328")).send("One minute has passed.")

send_server_message.start()
refresh_prompts.start()
bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here