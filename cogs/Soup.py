import os
import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands,tasks
import requests
import json
class Soup(commands.Cog,description=":bowl_with_spoon: Soup Module"):
    def __init__(self,bot):
        self.bot = bot
        self.me =943873910699618364
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        with open("messages.json","r") as f:
            Data = json.load(f)
        Soups = Data["soup"]
        if reaction.message.id in Soups and user != self.bot.user:
            if reaction.emoji == "🎲":
                x = requests.get('https://meme-api.herokuapp.com/gimme/soup')
                Post = json.loads(x.text)
                embed=discord.Embed(title=Post["title"], url=Post["postLink"], description=f"by {Post['author']}", color=0xfa7000)
                embed.set_image(url=Post["url"])
                await reaction.message.remove_reaction("🎲", user)
                await reaction.message.edit(embed=embed)

    @app_commands.command(name="soup",description="Run it and find out :|")
    async def soup(self,interaction :discord.Integration)->None:
        x = requests.get('https://meme-api.herokuapp.com/gimme/soup')
        Post = json.loads(x.text)
        embed=discord.Embed(title=Post["title"], url=Post["postLink"], description=f"by {Post['author']}", color=0xfa7000)
        embed.set_image(url=Post["url"])
        message = await interaction.channel.send(embed=embed)
        await interaction.response.send_message("SOUP!",ephemeral=True)
        await message.add_reaction("🎲")
        with open("messages.json","r") as f:
            Data = json.load(f)
        Data["soup"].append(message.id)
        with open("messages.json","w") as f:
            json.dump(Data,f)

async def setup(bot):
  await bot.add_cog(Soup(bot),guilds=[discord.Object(id=943404593105231882)])