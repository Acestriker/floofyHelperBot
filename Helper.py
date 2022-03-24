from distutils.log import error
import os
from pydoc import describe
from turtle import delay
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from Config import *

#---------------------------------------------------------------------#
class Helper(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.Owner = "`Doshi#4882` and `Acestriker#0001`"
    async def send_bot_help(self, mapping,):
        await self.context.message.delete(delay=1)
        emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{PREFIX}help <module>` to gain more information about that module '
                                            f':smiley:\n')
        emb.set_author(name="⚒ Help Menu", icon_url="https://media.discordapp.net/attachments/944096582851231804/954796896084439040/drctfvygbhbgvftcdrxctfvg.png?width=180&height=180")
        cogs_desc = ''
        for cog in mapping:
            if cog != None and cog.qualified_name not in HIDDENCOGS:
                Desc = ""
                if cog.description != None:
                    Desc = f"{cog.description}" 
                    Commands = [command.brief for command in cog.get_commands()]
                cogs_desc += f'{Desc} -**`{cog.qualified_name}`**\n'

            # adding 'list' of cogs to embed
        emb.add_field(name='Modules', value=cogs_desc, inline=False)
        #emb.add_field(name='Modules', value=cogs_desc, inline=False)
        emb.add_field(name="About", value=f"The Bots is developed by {self.Owner}, based on discord.py 2.0\n feel free to put any ideas you have in <#945107606249299979>\n message me if you find any bugs or notice the bot is offline!")
        emb.set_footer(text=f"Bot is running {VERSION}")
        await self.get_destination().send(embed=emb)

    async def send_cog_help(self, cog):
        emb = discord.Embed(title=f'{cog.qualified_name} - Commands', color=discord.Color.green(),
                                description=f'Use `{PREFIX}help <Command>` to gain more information about that Command '
                                            f':smiley:\n')
        emb.set_author(name="⚒ Help Menu", icon_url="https://media.discordapp.net/attachments/944096582851231804/954796896084439040/drctfvygbhbgvftcdrxctfvg.png?width=180&height=180")
        Command_desc=""
        for command in cog.get_commands():
            if command != None:
                breif = ""
                help = ""
                if command.help != None:
                    help = f" {command.help}"
                if cog.description != None:
                    breif = f"{command.brief}" 
                Command_desc += f'**`{PREFIX}{command.name}{help}`** {breif}\n'
        emb.add_field(name='Modules', value=Command_desc, inline=False)
        emb.set_footer(text=f"Bot is running {VERSION}")
        await self.get_destination().send(embed=emb)
    
    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        help = ""
        description = ""
        if command.help != None:
            help = f" {command.help}"
        if command.description != None:
            description = f" {command.description}"
        
        emb = discord.Embed(title=f'{command.name} - Command', color=discord.Color.blurple(),
                                description=f'`{PREFIX}{command.name}{help}` {description}')
        await self.get_destination().send(embed=emb)