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


class MyMenu(discord.ui.View):
  @discord.ui.select( # the decorator that lets you specify the properties of the select menu
    placeholder = "Check to approve prompts.", # the placeholder text that's displayed if nothing is selected
    min_values = 1, # the minimum number of values that have to be selected by the user
    max_values = 2, # the maximum number of values that can be selected by the user
    options = [ # the list of options from which the users can choose, a required field
      discord.SelectOption(
        label = 'Option 1',
        description= "Pick the first option."
      ),
      discord.SelectOption(
        label = 'Option 2',
        description= "Second options goes here."
      ),
      discord.SelectOption(
        label = 'option 3',
        description= 'And the last one is number 3.'
      )
    ]
  )
  async def select_callback(self, select, interaction): #the fucntion called when the user is done selecting
    # give chosen elements back as an embed
    # how many elements will the embed have? One for each approved prompt.
    n = len(select.values)
    embed = discord.Embed(title = "Approved prompts", color = 5763719)
    embed.add_field(name = "Approved!", value = "The following prompts were sent to the bucket: \n")
    for i in range(n):
      embed.add_field(name = " ", value = f'{select.values[i]} \n')
    # Problem: embed elements are added side by side instead of vertically
    await interaction.response.send_message(embeds = [embed])