import discord
from discord.ui import Button, View
from discord.ext import commands,tasks
import json

class MyView(View):
  def __init__(self,bot):
    super().__init__(timeout=None)
    self.bot = bot
    self.EventRole=952907898206441532 # < < < change to Your Wanted Role 
  
  @discord.ui.button(label = "Apply",style=1,custom_id="Apply",emoji="🎉")
  async def Button_callback(self, button, interaction):
    with open("Data.json","r") as f:
      Data = json.load(f)
    if interaction.user.id in Data["EventIDs"]:
      await interaction.response.send_message(f"You are already registered",ephemeral=True)
    else:
      Data["EventUsers"][interaction.user.name] = interaction.user.id
      await interaction.response.send_message(f"You have been registered, you can now join <#952674696497860668>! Check dms for invite code",ephemeral=True)
      role = discord.utils.get(interaction.user.guild.roles, id=self.EventRole)
      print(role)
      await interaction.user.add_roles(role)
      Data["EventIDs"].append(interaction.user.id)
    if Data["vrclink"] != None:
      try:
        embed=discord.Embed(title="Join us In VR!",description=f"**Join us here >>>** {Data['vrclink']}",color=0x00ffee)
        embed.set_thumbnail(url="https://assets.vrchat.com/www/brand/vrchat-logo-white-transparent-crop-background.png")
        embed.set_image(url="https://media.discordapp.net/attachments/943888861069709383/952670455217659924/VRChat_1920x1080_2022-03-13_20-41-09.979.png?width=960&height=540")
        await interaction.user.send(embed=embed)
      except:
         interaction.response.follow_up(f"You cant receive an invte link if your dms are closed",ephemeral=True)
    with open("Data.json","w") as f:
      json.dump(Data,f,indent=4)
  
  async def on_error(self,error,item,interaction):
    await interaction.response.follow_up("🔥Oh God Somthings gone wrong <@269759748302176256><@632029144196186122>🔥",ephemeral=False)
    raise error
    
class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        #self.guild = self.bot.get_guild(943404593105231882) # < < < change to Your Server ID
        self.me = 953641286232047627 # < < < change to Your Bots ID
        self.EventChannel = 952674696497860668 # < < < change to Your Wanted Role
        self.EventAttendeeRole = 952668569068511323 # < < < change to Your Wanted Role
        self.EventRole=952907898206441532

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
      if not before.channel and after.channel:
        print(f'{member} has joined {after.channel}')
      elif not after.channel and before.channel:
        print(f"{member} has left {before.channel}")
      elif before.channel.id != after.channel.id:
        print(f"{member} has switched from {before.channel} to {after.channel}")

      if after.channel and after.channel.id == self.EventChannel:
        import time
        now = int(time.time())
        with open("Data.json","r") as f:
          Data = json.load(f)
        Data["timeCodes"][member.name]=now
        with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      
      if not after.channel and before.channel.id == self.EventChannel:
        import time
        now = int(time.time())
        with open("Data.json","r") as f:
          Data = json.load(f)
        Then=Data["timeCodes"][member.name]
        del Data["timeCodes"][member.name]
        role = discord.utils.get(member.guild.roles, id=self.EventAttendeeRole)
        if (now-Then)>= 0 and role not in member.roles:
          await member.add_roles(role)
          Data["TempRoles"].append([member.id,now])
        with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)


    @commands.command()
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Event(self,ctx,unix:int,Link,*,args):
      if Link == "None" or Link == "none":
        with open("Data.json","r") as f:
          Data = json.load(f)
        Data["vrclink"]=None
        with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      else:
        with open("Data.json","r") as f:
          Data = json.load(f)
        Data["vrclink"]=Link
        with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      
      embed=discord.Embed(title="Event", description=args, color=0x00ffee)
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/944096582851231804/954016555765760020/C9851FF7-B5B1-42F2-A307-2D8E119B35A8-300x176.jpg")
      embed.add_field(name="Click The Button", value="Bellow To Apply", inline=False)
      embed.add_field(name="Event Starting in:",value=f"<t:{unix}:R>",inline=False)
      view = MyView(ctx)
      await ctx.send(view=view,embed=embed)
      await ctx.message.delete()

    @tasks.loop(seconds=30)
    async def TempRoles(self):
      import time
      guild = self.bot.get_guild(943404593105231882)
      now = int(time.time())
      with open("Data.json","r") as f:
        Data = json.load(f)
      i = 0
      for item in Data["TempRoles"]:
        if now -item[1]>20:
          del Data["TempRoles"][i]
          user = guild.get_member(item[0])
          role = discord.utils.get(guild.roles, id=self.EventAttendeeRole)
          await user.remove_roles(role)
        i =+1
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)

    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    @commands.command()
    async def TempClearON(self,ctx):
      self.TempRoles.start()
      await ctx.message.delete() 
      message = await ctx.send("Started removing temp roles")
      await message.delete(delay=5)
    
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    @commands.command()
    async def TempClearOFF(self,ctx):
      self.TempRoles.stop()
      await ctx.message.delete() 
      message = await ctx.send("Stopped removing temp roles")
      await message.delete(delay=5)
    @commands.command()
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def ClearEvents(self,ctx,msg:int=None):
        await ctx.message.delete()
        if msg != None:
          try:
            msg = await ctx.fetch_message(msg)
          except:
            await ctx.send("Invalid Message ID")
          else:
            embeds = msg.embeds
            for embed in embeds:
              embed.to_dict
            embed.title = f"{embed.title} (Event Over)"
            await msg.edit(embed=embed)
        with open("Data.json","r") as f:
            Data = json.load(f)
        Data["EventIDs"] = []
        print(Data["EventIDs"])
        for i in range(len(Data["TempRoles"])):
            del Data["TempRoles"][i]
        with open("Data.json","w") as f:
            json.dump(Data,f,indent=4)
        guild = self.bot.get_guild(943404593105231882)
        role = discord.utils.get(guild.roles, id=self.EventAttendeeRole)
        if role is None:
            await ctx.send("Role not found on this server!")
            return
        empty = True
        for member in guild.members:
            if role in member.roles:
                await ctx.send(f"Removed {role.mention} from {member.name}")
                await member.remove_roles(role)
                empty = False
        if empty:
            await ctx.send(f"Nobody has the role {role.mention}")
        role = discord.utils.get(guild.roles, id=self.EventRole)
        if role is None:
            await ctx.send("Role not found on this server!")
            return
        empty = True
        for member in guild.members:
            if role in member.roles:
                await ctx.send(f"Removed {role.mention} from {member.name}")
                await member.remove_roles(role)
                empty = False
        if empty:
            await ctx.send(f"Nobody has the role {role.mention}")
        await ctx.send("All temp roles removed")
def setup(bot):
  bot.add_cog(Events(bot))