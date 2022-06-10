"""
Code for the floofy Helper Bot for > https://discord.gg/4beans
You can find me on github > https://github.com/DoshiDog
The Repositorie for this project > https://github.com/Acestriker/floofyHelperBot
the modules required for this project can be found in the requirements.txt file
                                                          ,,          ,,                                   
`7MMMMMYp,                `7MMMMMYb.                    `7MM          db  `7MMMMMYb.                       
  MM    Yb                  MM    `Yb.                    MM                MM    `Yb.                     
  MM    dP `7M'   `MF'      MM     `Mb  ,pW"Wq.  ,pP"Ybd  MMpMMMb.  `7MM    MM     `Mb  ,pW"Wq.   .P"Ybmmm 
  MMWWWbg.   VA   ,V        MM      MM 6W'   `Wb 8I   `"  MM    MM    MM    MM      MM 6W'   `Wb :MI  I8   
  MM    `Y    VA ,V         MM     ,MP 8M     M8 `YMMMa.  MM    MM    MM    MM     ,MP 8M     M8  WmmmP"   
  MM    ,9     VVV          MM    ,dP' YA.   ,A9 L.   I8  MM    MM    MM    MM    ,dP' YA.   ,A9 8M        
.JMMmmmd9      ,V         .JMMmmmdP'    `Ybmd9'  M9mmmP'.JMML  JMML..JMML..JMMmmmdP'    `Ybmd9'   YMMMMMb  
              ,V                                                                                 6'     dP 
           OOb"                                                                                  Ybmmmd'   
DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOUR DOING Doshi is a very cool person :>
"""


# Imports
import os
#os.system("pip install -U git+https://github.com/Rapptz/discord.py")
#os.system("pip install pillow")
#import cronitor
import discord
from discord.ext import commands,tasks
from discord import app_commands
from Config import *
from discord.ext.commands import CommandNotFound


# Monitor Connector
#cronitor.api_key = CONTAINERAPIKEY
#monitor = cronitor.Monitor(MONITORTOKEN)

# Main Bot Class
class Mybot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=PREFIX,intents=discord.Intents.all(),help_command=None,application_id=APPID,case_insensitive=True)
		self.initial_extensions = STARTUP

	async def on_ready(self):
		#self.Ping.start()
		await self.load_extension("cogs.onStart")
		for ext in self.initial_extensions:
			await self.load_extension(ext)
			if ext == "cogs.Events":
				from cogs.Events import MyView
				import json
				with open("Data.json","r") as f:
					Data = json.load(f)
				guild = bot.get_guild(943404593105231882)
				msg= Data["LastEvent"]
				for channel in guild.text_channels:
					try:
						msg = await channel.fetch_message(msg)
					except:
						pass
					else:
						print("fixed last Event message")
						view = MyView(bot)
						await msg.edit(view=view)
						break
			if ext == "cogs.AI":
				from cogs.AI import ChatButtons
				guild = bot.get_guild(943404593105231882)
				channel = guild.get_channel(968225581462335488)
				msg = await channel.fetch_message(969271592133754890)
				view = ChatButtons(bot)
				await msg.edit(view=view)
				print("fixed Chat bot message")
		await bot.tree.sync(guild=discord.Object(id=943404593105231882))
		print(f'{self.user} has connected to Discord!')

	# Monitor ping routine
	@tasks.loop(seconds=30)
	async def Ping(self):    
	    monitor.ping(message="Alive!")

# Main RunTime
bot = Mybot()
bot.run(TOKEN)
