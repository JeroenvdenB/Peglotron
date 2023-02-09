import discord
from helper_functions import add_prompt

# Modal to submit a prompt into any bucket.
class PromptModal(discord.ui.Modal):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self.val = None
    self.add_item(discord.ui.InputText(label = "Enter your prompt here and click submit.", style = discord.InputTextStyle.long))
  
  async def callback(self, interaction: discord.Interaction):
    # Save the prompt to the correct .csv
    user = interaction.user
    prompt = self.children[0].value
    bucket = self.custom_id
    add_prompt(user, prompt, bucket)
    
    # Create an embed and respond
    embed = discord.Embed(title = "Prompt submitted for approval :)", color = 5763719) # Green embed
    if bucket == 'NSFW':
      embed.add_field(name = " ", value = f'[Redacted for NSFW]: || prompt ||') # Redact NSFW prompts with spoiler brackets.
    else:
      embed.add_field(name = " ", value = prompt)
    embed.set_author(name = user.display_name) # User is stored, but display_name is shown in response

    await interaction.response.send_message(embeds = [embed])
