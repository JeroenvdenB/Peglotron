import discord
from modals import PromptModal
import pandas as pd
import os

class MyView(discord.ui.View): # Create a class called Myview that subclasses discord.ui.View
  @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary) # Create a blurple button with "click me" on it.
  async def first_button_callback(self, button, interaction): # Don't give callbacks the same name!
    await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked.

  # A second button that will disable all buttons
  @discord.ui.button(label="Disable", style = discord.ButtonStyle.danger)
  async def second_button_callback(self, button, interaction):
    for child in self.children: # Loop over the children of the view
      child.disabled = True # Set the button to disabled
    await interaction.response.edit_message(view=self) 

  # Add a time-out here
  pass

# SUBMISSION BUTTONS VIEW
class SubmissionButtons(discord.ui.View):
  @discord.ui.button(label="SFW", style = discord.ButtonStyle.primary)
  async def SFW_button_callback(self, button, interaction):
    await interaction.response.send_modal(PromptModal(title = "SFW Submission", custom_id = "SFW"))
    # Use the custom_id to send the bucket type into the modal


  @discord.ui.button(label="NSFW", style = discord.ButtonStyle.primary)
  async def NSFW_button_callback(self, button, interaction):
    await interaction.response.send_message("You cicked the NSFW button.")
  
  @discord.ui.button(label="Weekly", style = discord.ButtonStyle.primary)
  async def weekly_button_callback(self, button, interaction):
    await interaction.response.send_message("You clicked the weekly prompt button.")
  
  @discord.ui.button(label="Stop", style= discord.ButtonStyle.danger)
  async def promptStop_button_callback(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.response.edit_message(view= self)

  # Add a time-out here.
  pass

