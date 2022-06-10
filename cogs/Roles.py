import discord
from discord import Embed, app_commands
from discord.app_commands import check
from discord.ext import commands

class Roles(commands.GroupCog,name="role"):
    def __init__(self,bot : commands.Bot) -> None:
        self.bot = bot
        self.guild = 943404593105231882
        super().__init__()

    @app_commands.command(name="over18",description="verifies a user as over 18")
    async def role_meture(self,interaction,member:discord.Member):
        guild =self.bot.get_guild(self.guild)
        role = discord.utils.get(guild.roles, id=966429116167487548)
        await member.add_roles(role)
        embed=discord.Embed(title=f'add {role.name} to {member.name}', color=0xadf3fd)
        await interaction.response.send_message(embed=embed,ephemeral=True)


    @app_commands.command(name="artist",description="verifies a user as an artist")
    async def role_meture(self,interaction,member:discord.Member):
        guild =self.bot.get_guild(self.guild)
        role = discord.utils.get(guild.roles, id=968587303599636501)
        await member.add_roles(role)
        try:
            role = discord.utils.get(guild.roles, id=945096251869896744)
            await member.remove_roles(role)
        except:
            pass
        embed=discord.Embed(title=f'add {role.name} to {member.name}', color=0xadf3fd)
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot),guilds=[discord.Object(id=943404593105231882)])