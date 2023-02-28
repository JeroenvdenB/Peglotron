import pandas as pd
import os
import configparser
import discord 

def add_prompt(user: str, prompt: str, bucket: str):
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
    """

    # Check bucket type
    if bucket == 'SFW':
        filepath = os.getenv("OPEN_SFW_SUBMISSIONS")
    elif bucket == 'NSFW':
        filepath = os.getenv("OPEN_NSFW_SUBMISSIONS")
    elif bucket == 'WEEKLY':
        filepath = os.getenv("OPEN_WEEKLY_SUBMISSIONS")
    else:
        print("Invalid bucket input - accepted are SFW, NSFW and W.")
        raise TypeError

    df = pd.read_csv(filepath, delimiter = ';')
    add = pd.DataFrame([[user, prompt]], columns=('user','prompt'))
    new_df = pd.concat([df, add], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
    new_df.to_csv(path_or_buf=filepath, index=False, sep=';') # Overwrite existing file

    return True

def df_to_text(bucket: str):
    """
    Accepts a file bucket name and converts it to a string,
    suitable for printing in a discord message.
    It's formatted in markdown to show OK on discord too.
    
    Parameters
    ----------
    bucket: :class:`str`
        Input a filepath name from .env. That's different from the prompt storage system, which only uses SFW, NSFW and W for bucket denotion!
        Since this function can show any .csv content (open, ready and used prompt buckets), you need to be more specific.    
    """

    filepath = os.getenv(bucket)
    response_text = pd.read_csv(filepath, delimiter = ';').to_markdown()
    return response_text

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

    # Generate filepath based on bucket name and read file
    filepath = os.getenv(f"OPEN_{bucket}_SUBMISSIONS")
    df = pd.read_csv(filepath, delimiter= ';')

    # Catch exception in case the index is out of bounds
    try:
        nextprompt = df['prompt'][index]
    except:
        print("Requested prompt index is probably out of bounds")     
    else:    
        embed = discord.Embed(title = f"Next {bucket} prompt: ") # create embed object
        embed.add_field(name = " ", value= nextprompt)
        return embed