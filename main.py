import discord
from discord import default_permissions
from discord.utils import get
from discord.ext import tasks, commands
import os
import configparser
import pandas as pd
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
from helper_functions import set_channel
from helper_functions import prompt_to_embed
from helper_functions import format_prompt
from views import SubmissionButtons
from views import ApprovePrompt
from helper_functions import CyclePrompt


# Make a .env locally that contains the token of the server that the bot should log into.
load_dotenv()
token = os.getenv("TOKEN")
bot = discord.Bot()


# Confirm connection in the terminal
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")


@bot.command(description = "Summon the submissions buttons.")
async def submitbutton(ctx):
  await ctx.respond("Choose which type of submission you'd like to do!", view = SubmissionButtons(timeout=180))


@bot.command(description = "Ping in output channel")
@default_permissions(administrator = True)
async def channelping (ctx):
  config = configparser.ConfigParser()
  config.read('peglotron.ini')
  channel_id = int(config['OutputChannels']['channelping'])
  await bot.get_channel(channel_id).send("Ping!")
  await ctx.respond("Pinging...")


@bot.command(description = "Set channelping output channel")
@default_permissions(administrator = True)
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
    #index = int(config['CurrentPrompts'][bucket_name])
    channelId = int(config['OutputChannels'][f'{bucket.lower()}prompt'])

    # Then retrieve the prompt information from the USED prompts list 
    filepath = os.getenv(f"USED_{bucket_name}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter = ';')
    # Hey, guess what?! df.iloc[-1]['prompt'] works too, because the final row is always the current prompt :)
    prompt = df.iloc[-1]['prompt']
    user = df.iloc[-1]['user']
    shown = int(df.iloc[-1]['shown'])
    
    promptEmbed = format_prompt(bucket_name, prompt, user, shown)

    await bot.get_channel(channelId).send(content=None, embed=promptEmbed)
    await ctx.respond("I've repeated the prompt :)")
  else:
    await ctx.respond("Something went wrong. Notify my overlord, please.")

@bot.command(description = "Force cycle to next prompt")
@default_permissions(administrator = True)
async def forceprompt(ctx, bucket: discord.Option(str)):
  valid_buckets = ['SFW', 'NSFW', 'WEEKLY']

  if bucket.upper() in valid_buckets:
    prompt = CyclePrompt(bucket.upper())
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    channelId = int(config['OutputChannels'][f'{bucket.lower()}prompt'])
    await bot.get_channel(channelId).send(content=None, embed=prompt)
    await ctx.respond("Prompt cycled succesfully!")
  else:
    await ctx.respond("That's not a valid bucket. Please enter SFW, NSFW or WEEKLY")


@tasks.loop(minutes = 60)
async def promptcycler():
  hour = datetime.now().strftime("%H") # Fetches system time, hour only, on a 24-hour scale
  await bot.wait_until_ready()
  if int(hour) == 12:
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    buckets = ["sfw", "nsfw"]

    for bucket in buckets:
      channelId = int(config['OutputChannels'][f'{bucket}prompt'])
      nextPromptEmbed = CyclePrompt(bucket.upper())
      await bot.get_channel(channelId).send(content=None, embed=nextPromptEmbed)

@tasks.loop(hours = 24)
async def weeklycycle():
  if date.today().weekday() == 0:
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    channelId = int(config['OutputChannels']['weeklyprompt'])
    nextPromptEmbed = CyclePrompt("WEEKLY")
    await bot.get_channel(channelId).send(content=None, embed=nextPromptEmbed)

promptcycler.start()
weeklycycle.start()
bot.run(token)

# No code is executed after the bot.run()
# Don't put anything here