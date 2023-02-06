import discord
import pandas as pd
import os
from helper_functions import add_prompt

# A test modal
class TestModal(discord.ui.Modal):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self.add_item(discord.ui.InputText(label="Enter your prompt here and click submit.", style = discord.InputTextStyle.long))
  
  async def callback(self, interaction: discord.Interaction): # DO NOT alter the callback name
    embed = discord.Embed(title="Modal Results", color=5763719)
    embed.add_field(name="Suggested prompt:", value = self.children[0].value)
    print(interaction.user, " has filled in a Modal.") # Don't be a dum-dum and access the variable, not the Class. Thx, me.
    embed.set_author(name = interaction.user)
    await interaction.response.send_message(embeds=[embed])

    """ By callin on the interaction variable, several things
    like content, date, time, user, id, etc. can be accessed.
    Ideal for passing on important data.
    
    Address the fillable fields as children."""


# Modal to submit a prompt into any bucket.
class PromptModal(discord.ui.Modal):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self.val = None
    self.add_item(discord.ui.InputText(label = "Enter your prompt here and click submit.", style = discord.InputTextStyle.long))
  
  async def callback(self, interaction: discord.Interaction):
    embed = discord.Embed(title = "Prompt submitted for approval :)", color = 5763719)
    embed.add_field(name = " ", value = self.children[0].value)
    embed.set_author(name = interaction.user)
    # Dev lines printing in terminal - remove when done.
    print(interaction.user, " has submitted a prompt:")
    print("   ", self.children[0].value)
    print(self.custom_id)

    await interaction.response.send_message(embeds = [embed])

    user = interaction.user
    prompt = self.children[0].value
    bucket = self.custom_id
    add_prompt(user, prompt, bucket)

