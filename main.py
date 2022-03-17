#Version 1.0 | By DoshiDog | https://github.com/DoshiDog
#DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOUR DOING
#you also might need this if you dont have python 2.0 installed 
import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ui import Button, View
from Config import *
from keep_alive import keep_alive



def isDoshi(ctx):
	return ctx.author.id ==269759748302176256
def isAce(ctx):
	return ctx.author.id==632029144196186122

intents = discord.Intents().all()
bot = commands.Bot(command_prefix =PREFIX,intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="~help | Ace's Abode"))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		await ctx.message.delete()
		embed=discord.Embed(title="Command Error ☹", color=0xff4d00)
		embed.add_field(name="Unknown Command", value="Invalid Command Entered for a list of commands do .help", inline=False)
		message = await ctx.send(embed=embed)
		await message.delete(delay=10)
		return
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.delete()
		embed=discord.Embed(title="Command Error ☹", color=0xff4d00)
		embed.add_field(name="Missing Arguments", value="make sure you using the command correctly", inline=False)
		message = await ctx.send(embed=embed)
		await message.delete(delay=10)
		return
	raise error

@bot.command()
@commands.check_any(commands.check(isDoshi),commands.check(isAce))
async def load(ctx,extension):
		await ctx.message.delete()
		try:
			bot.load_extension(f"cogs.{extension}")	
		except:
			message = await ctx.send(f"Faild to load {extension}")
			await message.delete(delay=5)
		else:
			message = await ctx.send(f"loaded {extension}")		
			await message.delete(delay=5)

@bot.command()
@commands.check_any(commands.check(isDoshi),commands.check(isAce))
async def unload(ctx,extension):
		await ctx.message.delete()
		try:
			bot.unload_extension(f"cogs.{extension}")
		except:
			message = await ctx.send(f"Faild to unload {extension}")
			await message.delete(delay=5)
		else:
			message = await ctx.send(f"unloaded {extension}")
			await message.delete(delay=5)

@bot.command()
@commands.check_any(commands.check(isDoshi),commands.check(isAce))
async def reload(ctx,extension):
		await ctx.message.delete()
		try:
			bot.unload_extension(f"cogs.{extension}")
			bot.load_extension(f"cogs.{extension}")
		except:
			message = await ctx.send(f"faild to reload {extension}")
			await message.delete(delay=5)
		else:
			message = await ctx.send(f"reloaded {extension}")
			await message.delete(delay=5)
@bot.command()
@commands.check_any(commands.check(isDoshi),commands.check(isAce))
async def ListAll(ctx):
	extentions = []
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			extentions.append(filename)
	await ctx.send(extentions)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f"cogs.{filename[:-3]}")\
		
keep_alive()
bot.run(os.environ.get("TOKEN"))