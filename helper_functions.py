import pandas as pd
import os

def add_prompt(user, prompt, bucket):
    """Adds the user and the submitted prompt to a .csv file
    for a specific bucket, such as 'SFW' or 'Weekly'. 
    Input: 3 arg: user id (str), prompt content (str), and bucket (str).
    Output: True upon completion.
    Raises a type error if the bucket name is invalid."""

    # Check bucket type
    if bucket == 'SFW':
        filepath = os.getenv("OPEN_SFW_SUBMISSIONS")
    elif bucket == 'NSFW':
        filepath = os.getenv("OPEN_NSFW_SUBMISSIONS")
    elif bucket == 'W':
        filepath = os.getenv("OPEN_WEEKLY_SUBMISSIONS")
    else:
        print("Invalid bucket input - known are SFW, NSFW and W.")
        raise TypeError

    df = pd.read_csv(filepath, delimiter = ';')
    add = pd.DataFrame([[user, prompt]], columns=('user','prompt'))
    new_df = pd.concat([df, add], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
    new_df.to_csv(path_or_buf=filepath, index=False, sep=';') # Overwrite existing file

    return True

def df_to_text(bucket):
    """Accepts a file bucket name and converts it to a string,
    suitable for printing in a discord message."""

    import pandas as pd
    import os
    filepath = os.getenv(bucket)
    response_text = pd.read_csv(filepath, delimiter = ';').to_markdown()
    return response_text