import discord

# Make a simple button appear with a slash command
# First, we have to build the view that has the buttons, and what the buttons do.
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