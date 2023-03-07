import discord
from modals import PromptModal
from helper_functions import prompt_to_embed
from helper_functions import add_prompt
from helper_functions import remove_prompt
import pandas as pd

# SUBMISSION BUTTONS VIEW
# Use the custom_id to send the bucket type into the modal
class SubmissionButtons(discord.ui.View):
  @discord.ui.button(label="SFW", style = discord.ButtonStyle.primary)
  async def SFW_button_callback(self, button, interaction):
    await interaction.response.send_modal(PromptModal(title = "SFW prompt submission", custom_id = "SFW"))

  @discord.ui.button(label="NSFW", style = discord.ButtonStyle.primary)
  async def NSFW_button_callback(self, button, interaction):
    await interaction.response.send_modal(PromptModal(title = "NSFW prompt submission", custom_id = "NSFW"))
  
  @discord.ui.button(label="Weekly", style = discord.ButtonStyle.primary)
  async def weekly_button_callback(self, button, interaction):
    await interaction.response.send_modal(PromptModal(title = "Weekly prompt submission", custom_id = "WEEKLY"))
  
  @discord.ui.button(label="Stop", style= discord.ButtonStyle.danger)
  async def promptStop_button_callback(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.response.edit_message(view= self)

  # Timeout
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    await self.message.edit(content = "Thank you for submitting your prompts! Feel free to send more at any time through `/submit`", view= self)


# APPROVE PROMPT MENU
class ApprovePrompt(discord.ui.View):

  @discord.ui.button(label="Accept", style = discord.ButtonStyle.success, row=0)
  async def accept_button_callback(self, button, interaction):
    prompt = self.message.embeds[0].fields[1].value # grab the prompt text out of the embed that was previously sent
    user = self.message.embeds[0].fields[2].value # grab the username of the prompt out of the embed
    bucket = self.message.embeds[0].title.split(" ")[2] # grab the buckete name from the embed

    # Add prompt to ready-prompts file
    add_prompt(user, prompt, bucket, subbucket = "READY")

    # Remove prompt from open-prompts file
    index = int(self.message.embeds[0].fields[0].value) # grab the index of the prompt out of the embed
    remove_prompt(index, bucket)

    # Proceed to next prompt
    [embed, end] = prompt_to_embed(bucket, index) # prompt is made with the same index, because that's the next unchecked prompt in the OPEN prompts file. The approved prompt was removed and indeces reset.

    # Check if end has been reached. Disable buttons if there are no more prompts to prevent accidental invalid inputs.
    if end:
      for child in self.children:
        child.disabled = True
    await self.message.delete()
    await interaction.response.send_message(content = None, view = self, embeds = [embed])
  
  @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, row=0)
  async def reject_button_callback(self, button, interaction):
    await interaction.response.send_message("You rejected this prompt. Or would have if the button worked.")

  @discord.ui.button(label="Skip", style = discord.ButtonStyle.secondary, row=1)
  async def skip_button_callback(self, button, interaction):
    index = int(self.message.embeds[0].fields[0].value) # grab the index of the prompt out of the embed that was previously sent
    index += 1 # increase the index to move to the next prompt
    bucket = self.message.embeds[0].title.split(" ")[2] # grab the buckete name from the embed
    [embed, end] = prompt_to_embed(bucket, index)
    await self.message.delete() # remove original message to keep the channel clutter-free
    await interaction.response.send_message(content = None, view = self, embeds = [embed]) # don't edit, send a new message! Otherwise self.message does NOT update!

  @discord.ui.button(label="Edit", style=discord.ButtonStyle.secondary, row=1)
  async def edit_button_callback(self, button, interaction):
    await interaction.response.send_message("This feature is not available yet.")
  
  @discord.ui.button(label="Stop", style=discord.ButtonStyle.secondary, row=1)
  async def stop_button_callback(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await self.message.edit(content = " ", view = self)
    await interaction.response.send_message("Thank you, I disabled the menu.")

