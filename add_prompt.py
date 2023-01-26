def add_prompt(ctx, msg):
    """Adds the message content and user to the .csv file.
    Uses the SUBMISSIONS filepath set in .env 
    Input: 2 arg: context and the message from discord API.
    Output: True upon completion."""
    
    import pandas as pd
    import os
    
    filepath = os.getenv("SUBMISSIONS") 

    user = ctx.author
    text = msg.content
    df = pd.read_csv(filepath, delimiter = ';')
    add_this = pd.DataFrame([[user, text]], columns=('user','text'))
    new_df = pd.concat([df, add_this], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
    new_df.to_csv(path_or_buf=filepath, index=False, sep=';') # Overwrite existing file
    #print(new_df)
    
    return True