from ast import Delete
from pydoc import describe
import discord
from discord.ui import Button, View
from discord.ext import commands,tasks
import json

#---------------------------------------------------------------------------------------------------------------------------#
class Movies(commands.Cog,description=":film_frames: Movies Nights Module"):
    def __init__(self,bot):
        self.bot = bot
        self.me = 953641286232047627 
#---------------------------------------------------------------------------------------------------------------------------#
    @commands.command(brief="Auto Movie Poll Command",description="this Command let you automaticaly Create a movie Poll, it will pick 3 films form our server side list and Put them in a poll")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Movie(self,ctx):
      await ctx.message.delete()
      import random
      with open("Data.json","r") as f:
          Data = json.load(f)
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)
      Movies = []
      for i in range(0,3):
        Movie = random.choice(Data["Movies"])
        while Movie in Movies:
          Movie = random.choice(Data["Movies"])
        Movies.append(Movie)
      embed=discord.Embed(title="Time to Vote For what Film you want to watch!", description=f"🟢 {Movies[0]} \n 🟡 {Movies[1]} \n 🔴 {Movies[2]}", color=0x000000)
      embed.set_thumbnail(url="https://i0.wp.com/www.printmag.com/wp-content/uploads/2021/02/4cbe8d_f1ed2800a49649848102c68fc5a66e53mv2.gif?fit=476%2C280&ssl=1")
      embed.set_author(name="Movie Night!", icon_url="https://cdn0.iconfinder.com/data/icons/peppyicons-rounded/512/clapper-2-512.png")
      message = await ctx.send(embed=embed)
      await message.add_reaction("🟢")
      await message.add_reaction("🟡")
      await message.add_reaction("🔴")

    @commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
    @commands.command(brief="Add a Moive to Our Movie List!",help="<Movie Name>",description="Add a Moive to Our Movie List!")
    async def addMovie(self,ctx,*,args):
      with open("Data.json","r") as f:
          Data = json.load(f)
      if args.lower() not in Data["Movies"]:
        Data["Movies"].append(args.lower())
        message = await ctx.send(f"Thanks For the sugestion! {args} has been added to our movie Listings!")
      else:
        await ctx.message.delete()
        message = await ctx.send("movie has alread been suggested!")
        await message.delete(delay=10)
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)

    @addMovie.error
    async def on_command_error(self,ctx, error):
      if isinstance(error,commands.CommandOnCooldown):
        await ctx.message.delete(delay=10)
        embed=discord.Embed(title="Command Error ☹", color=0xff4d00)
        embed.add_field(name="Boi you movin Too Fast", value=f"This command is on cooldown try again in {error.retry_after:.2f} 😵", inline=False)
        message = await ctx.send(embed=embed)
        await message.delete(delay=10)
        
async def setup(bot):
  await bot.add_cog(Movies(bot))