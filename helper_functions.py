import pandas as pd
import os
import configparser
import discord 

def add_prompt(user: str, prompt: str, bucket: str, subbucket: str):
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
    valid_subbuckets = ["OPEN", "READY"]

    # Check if subbucket is valid
    if subbucket.upper() not in valid_subbuckets:
        print("Invalid subbucket input - accepted are OPEN and READY")
        raise TypeError
    
    # Check bucket type
    if bucket not in valid_buckets:
        print("Invalid bucket input. Valid buckets are SFW, NSFW and WEEKLY")
        raise TypeError
    
    # Create filepath
    filepath = os.getenv(f"{subbucket}_{bucket}_SUBMISSIONS")

    # Add input data to the file and resave
    df = pd.read_csv(filepath, delimiter = ';')
    add = pd.DataFrame([[user, prompt]], columns=('user','prompt'))
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
    
def errorlog(date, error):
# This function was never tested. Dunno if I need it after all.
    # Open the filein append and read mode (a+)
    with open ("Errorlog.txt", 'a+') as file_object:
        # Move the read cursor to the start of the file.
        file_object.seek(0)
        # If file is not empty append '\n' for new line
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of the file
        file_object.write(date, " ; ", error)
    
    file_object.close()

def remove_prompt(index, bucket, subbucket):
    filepath = os.getenv(f"{subbucket}_{bucket}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter = ';')
    new_df = df.drop([index], axis='index')
    new_df.to_csv(path_or_buf=filepath, index = False, sep=';') # overwrite existing file
    
    # Overwriting the original file in a coroutine instead of using the drop command in the button code is better
    # This ensures the file is opened, altered, and saved/closed again.
    # This ensures that anything that tries to use this file, will use the most up-to-date version.

def format_prompt(prompt: str, user: str, shown: int):
    # Function should generate an embed for a prompt to show in the server.
    # It's called on by the /show command to show the current prompt.
    # It's called on by the task that creates new current prompts and moves
    # the used prompts between files.

    pass