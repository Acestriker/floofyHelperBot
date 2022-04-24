import os
import time
import discord
import asyncio
from discord.ui import Button, View
from discord.ext import commands
import json
import random
class Interactions(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.me =943873910699618364
    @commands.Cog.listener()
    async def on_message(self,message):
        with open("messages.json","r") as f:
            Data = json.load(f)
        now = int(time.time())
        if message.type == discord.MessageType.premium_guild_subscription:
            print(str(message.author))
            embed=discord.Embed(title="THANK YOU!", description="Thanks for Boosting our Server, \nwe really appreciate it! \n you should now have access to some Cool Booster only features!", color=0xf47fff)
            embed.set_author(name="Floofy Messenger", icon_url="https://media.discordapp.net/attachments/944096582851231804/954796896084439040/drctfvygbhbgvftcdrxctfvg.png?width=180&height=180")
            embed.add_field(name="Colored Roles!",value="You can now select a coloured role in <#944280501605261362>",inline=False)
            embed.add_field(name="Media Perms!",value="embed + media perms in <#943404593105231885>",inline=False)
            embed.add_field(name="Emoji Requests", value="access to <#944280717255381013> to suggest emojis to add to the server!",inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/944096582851231804/956574419793362984/IMG_1458.png")
            await message.author.send(embed=embed)
        if "gm" in message.content.lower() and now - Data["Last"]>1800 and message.author.id != 953794936736727110 and message.reference == None:
            async with message.channel.typing():
               await asyncio.sleep(1)
               await message.channel.send(random.choice(Data["GmRespones"]))
            Data["Last"] = now
        with open("messages.json","w") as f:
            json.dump(Data,f)
    @commands.command()
    async def manual(self,ctx,Channel:int,*,args):
        await ctx.message.delete(delay=1)
        channel = self.bot.get_channel(Channel)
        await channel.send(args)


async def setup(bot):
  await bot.add_cog(Interactions(bot))