import pandas as pd
import os
import configparser
import discord 
import random

def add_prompt(user: str, prompt: str, bucket: str, subbucket: str, shown = 0):
    """
    Adds the user and the submitted prompt to a .csv file for a specific bucket, such as 'SFW' or 'WEEKLY'. 
    Raises a TypeError in case of invalid bucket notation.

    Parameters
    ----------
    name: :class:`str`
        The user id that should be logged in prompt systems.
    prompt: :class:`str`
        The content of the prompt. The Modal that creates this will accept up to 4000 characters.
    bucket: :class:`str`
        A denotion for which bucket the prompt goes in. This can be SFW, NSFW or WEEKLY. It is always put in the 'open' bucket, awaiting admin approval.
    subbucket: :class:`str`
        Denotes the subbucket as open or ready
    """

    # Define valid buckets and subbuckets
    valid_buckets = ["SFW", "NSFW", "WEEKLY"]
    valid_subbuckets = ["OPEN", "READY", "USED"]

    # Check if subbucket is valid
    if subbucket.upper() not in valid_subbuckets:
        print("Invalid subbucket input - accepted are OPEN, READY and USED")
        raise TypeError
    
    # Check bucket type
    if bucket not in valid_buckets:
        print("Invalid bucket input. Valid buckets are SFW, NSFW and WEEKLY")
        raise TypeError
    
    # Create filepath
    filepath = os.getenv(f"{subbucket}_{bucket}_SUBMISSIONS")

    # Add input data to the file and resave
    df = pd.read_csv(filepath, delimiter = ';')

    if subbucket != "USED":
        add = pd.DataFrame([[user, prompt]], columns=('user','prompt'))
    else:
        add = pd.DataFrame([[user, prompt, shown]], columns=('user','prompt','shown'))
    
    new_df = pd.concat([df, add], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
    new_df.to_csv(path_or_buf=filepath, index=False, sep=';') # Overwrite existing file

    return True

def set_channel(command: str, channel_id: str):
    """
    Changes the ouput channel ID for a function that outputs into the server.
    Outputting functions need to be defined in the accompanying .ini file under ['OutputChannels'].
    Keys may be empty upon setup. 
    Raises KeyError when the given command does not correspond to a slash-command name listed under 'OutputChannels'.

    Parameters
    ----------
    command: :class:`str`
        The name of the command that has an output to a channel.
    channel_id: :class:`str`
        The channel ID that should be set in the .ini file. 
        It's initially accepted as discord.Option to a slash command, which always yields a string. Also too large a number as a standard integer. 
    """
    
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    valid_commands = []

    # Check if the command entered is a key in the ini file
    for key in config['OutputChannels']:
        valid_commands.append(key)
    print(valid_commands)

    if command in valid_commands:
        print("The command is valid")
    else:
        print("Invalid command type input")
        raise KeyError

    # Proceed to change the desired command
    config['OutputChannels'][command] = channel_id

    with open('peglotron.ini', 'w') as configfile:
        config.write(configfile)

def prompt_to_embed(bucket: str, index: int = 0):
# function works, just needs a description now.
# returns an embed object and the end boolean. If there are no prompts left to approve, end = True.
    # create embed with title
    embed = discord.Embed(title = f"Working on: {bucket}") # create embed object

    # Create end-reached flag
    end = False

    # Generate filepath based on bucket name and read file
    filepath = os.getenv(f"OPEN_{bucket}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter= ';')

    # Catch exception in case the index is out of bounds (skip was pressed too often)
    try:
        nextprompt = df['prompt'][index]
    except:
        # write error message
        embed.add_field(name = "Out of prompts!", value = "You're all caught up.")
        end = True
        return embed, end
    else:    
        embed.add_field(name = "Index", value= index)
        embed.add_field(name = "Prompt", value = nextprompt)
        embed.add_field(name = 'User', value = df['user'][index])
        return embed, end
    

def remove_prompt(index, bucket, subbucket):
    filepath = os.getenv(f"{subbucket}_{bucket}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter = ';')
    new_df = df.drop([index], axis='index')
    new_df.to_csv(path_or_buf=filepath, index = False, sep=';') # overwrite existing file
    
    # Overwriting the original file in a coroutine instead of using the drop command in the button code is better
    # This ensures the file is opened, altered, and saved/closed again.
    # This ensures that anything that tries to use this file, will use the most up-to-date version.

def format_prompt(bucket: str, prompt: str, user: str, shown: int):
    # Function should generate an embed for a prompt to show in the server.
    # It's called on by the /show command to show the current prompt.
    # It's called on by the task that creates new current prompts

    embed = discord.Embed(title = f':snowflake:  Daily {bucket} prompt  :dragon:')
    embed.add_field(name = " ", value = prompt)
    embed.set_footer(text = f'Suggested by {user}. This prompt was shown {shown} time(s) before')

    return embed

def CyclePrompt(bucket: str):
    #String for bucket, SFW, NSFW or WEEKLY
    #Current prompt number as int representing the line in the csv file

    # Selecting the next prompt text from READY, or if empty, from USED
    filepathREADY = os.getenv(f"READY_{bucket}_SUBMISSIONS")
    filepathUSED = os.getenv(f"USED_{bucket}_SUBMISSIONS")
    dfREADY = pd.read_csv(filepathREADY, delimiter= ';')
    dfUSED = pd.read_csv(filepathUSED, delimiter= ';')

    if dfREADY.size == 0: #Switch to recycling prompts instead
        index = random.randrange(0, dfUSED.size/3)
        nextPrompt = dfUSED['prompt'][index]
        user = dfUSED['user'][index]
        shown = dfUSED['shown'][index] + 1

        # Update the shown prompt - shown is increased by one
        # Updating = add new line, remove original
        add_prompt(user, nextPrompt, bucket, "USED", shown)
        remove_prompt(index, bucket, "USED")
    else:
        shown = 0
        nextPrompt = dfREADY['prompt'][0]
        user = dfREADY['user'][0]
        add_prompt(user, nextPrompt, bucket, "USED", shown + 1)
        remove_prompt(0, bucket, "READY")


    # Set current prompt index in config file
    # Later realized that the index of the current prompt is ALWAYS the last one of the USED file 
    index = dfUSED.size//3 - 1
    config = configparser.ConfigParser()
    config.read('peglotron.ini')
    config['CurrentPrompts'][bucket] = str(index)
    with open('peglotron.ini', 'w') as configfile:
        config.write(configfile)
    
    embed = format_prompt(bucket, nextPrompt, user, shown)
    
    return embed
