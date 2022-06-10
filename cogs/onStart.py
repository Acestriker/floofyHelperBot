import discord
from discord import Embed, app_commands
from discord.app_commands import check
from discord.ext import commands

class onStart(commands.GroupCog,name="core"):
    def __init__(self,bot : commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    def isDev(interaction):
        return interaction.user.id ==269759748302176256 or interaction.user.id==632029144196186122

    
    @app_commands.command(name="load",description="load a module of the bot")
    @app_commands.check(isDev)
    async def load(self,interaction,extension:str):
        try:
            await self.bot.load_extension(f"cogs.{extension}")	
        except:
            embed=discord.Embed(title=f"Failed to load {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title=f"loaded {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        await self.bot.tree.sync(guild=discord.Object(id=943404593105231882))

    @app_commands.command(name="unload",description="unload a module of the bot")
    @app_commands.check(isDev)
    async def unload(self,interaction,extension:str):
        try:
            await self.bot.unload_extension(f"cogs.{extension}")
        except:
            embed=discord.Embed(title=f"Failed to unload {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title=f"unloaded {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        await self.bot.tree.sync(guild=discord.Object(id=943404593105231882))

    @app_commands.command(name="reload",description="reload a module of the bot")
    @app_commands.check(isDev)
    async def reload(self,interaction,extension:str):
        try:
            await self.bot.unload_extension(f"cogs.{extension}")
            await self.bot.load_extension(f"cogs.{extension}")
        except:
            embed=discord.Embed(title=f"Failed to reload {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title=f"reloaded {extension}", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        await self.bot.tree.sync(guild=discord.Object(id=943404593105231882))
        

    @app_commands.command(name="ping",description="Sends the ping of the bot")
    async def ping(self,interaction):
        import time
        embed=discord.Embed(title=f'Ping is: {round(self.bot.latency*1000)}ms', color=0xadf3fd)
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(onStart(bot),guilds=[discord.Object(id=943404593105231882)])