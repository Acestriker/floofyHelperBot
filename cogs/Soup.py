import os
import discord
from discord.ui import Button, View
from discord.ext import commands
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
		if reaction.message.id in Soups and user.id != self.me:
			if reaction.emoji == "🎲":
				x = requests.get('https://meme-api.herokuapp.com/gimme/soup')
				Post = json.loads(x.text)
				embed=discord.Embed(title=Post["title"], url=Post["postLink"], description=f"by {Post['author']}", color=0xfa7000)
				embed.set_image(url=Post["url"])
				await reaction.message.remove_reaction("🎲", user)
				await reaction.message.edit(embed=embed)

	@commands.command(brief="Run it and find out <:death:946550673502273586>",description="Run it and find out <:death:946550673502273586>")
	async def soup(self,ctx):
		x = requests.get('https://meme-api.herokuapp.com/gimme/soup')
		Post = json.loads(x.text)
		embed=discord.Embed(title=Post["title"], url=Post["postLink"], description=f"by {Post['author']}", color=0xfa7000)
		embed.set_image(url=Post["url"])
		message = await ctx.send(embed=embed)
		await message.add_reaction("🎲")
		await ctx.message.delete()
		with open("messages.json","r") as f:
			Data = json.load(f)
		Data["soup"].append(message.id)
		with open("messages.json","w") as f:
			json.dump(Data,f)
	@commands.command(brief="Run it and find out <:death:946550673502273586>",description="Run it and find out <:death:946550673502273586>")
	async def nerd(self,ctx):
		x = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
		Post = json.loads(x.text)
		await ctx.send(f"{Post['joke']}")
		await ctx.message.delete()
async def setup(bot):
  await bot.add_cog(Soup(bot))