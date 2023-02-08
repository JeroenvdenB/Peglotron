import pandas as pd
import os

def add_prompt(user: str, prompt: str, bucket: str):
    """
    Adds the user and the submitted prompt to a .csv file for a specific bucket, such as 'SFW' or 'Weekly'. 
    Raises a TypeError in case of invalid bucket notation.

    Parameters
    ----------
    name: :class:`str`
        The user id that should be logged in prompt systems.
    prompt: :class:`str`
        The content of the prompt. The Modal that creates this will accept up to 4000 characters.
    bucket: :class:`str`
        A denotion for which bucket the prompt goes in. This can be SFW, NSFW or Weekly. It is always put in the 'open' bucket, awaiting admin approval.
    """

    # Check bucket type
    if bucket == 'SFW':
        filepath = os.getenv("OPEN_SFW_SUBMISSIONS")
    elif bucket == 'NSFW':
        filepath = os.getenv("OPEN_NSFW_SUBMISSIONS")
    elif bucket == 'W':
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

    import pandas as pd
    import os
    filepath = os.getenv(bucket)
    response_text = pd.read_csv(filepath, delimiter = ';').to_markdown()
    return response_text