import discord
from modals import PromptModal

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
    await interaction.response.send_modal(PromptModal(title = "Weekly prompt submission", custom_id = "W"))
  
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
  @discord.ui.button(label="OK", style = discord.ButtonStyle.success)
  async def ok_button_callback(self, button, interaction):
    await interaction.response.send_message("You pressed the A-OK button!")
  
  @discord.ui.button(label="X", style=discord.ButtonStyle.danger)
  async def x_button_callback(self, button, interaction):
    await interaction.response.send_message("You rejected this prompt. Or would have if the button worked.")

  @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary)
  async def edit_button_callback(self, button, interaction):
    await interaction.response.send_message("This feature is not available yet.")
  
  @discord.ui.button(label="Stop", style=discord.ButtonStyle.primary)
  async def stop_button_callback(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await self.message.edit(content = " ", view = self)
    await interaction.response.send_message("Thank you, I disabled the menu.")

