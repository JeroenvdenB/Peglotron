def add_prompt(ctx, msg):
    """Adds the message content and user to the .csv file. Requires context and the message as input."""
    import pandas as pd

    user = ctx.author
    text = msg.content
    df = pd.read_csv('recieved_msg.csv', delimiter = ';')
    add_this = pd.DataFrame([[user, text]], columns=('user','text'))
    new_df = pd.concat([df, add_this], ignore_index=True) # Don't reference df = pd.concat[df... etc. Gives unbound variable error.
    new_df.to_csv('recieved_msg.csv', index=False, sep=';') # Overwrite existing file
    print(new_df)
    return True