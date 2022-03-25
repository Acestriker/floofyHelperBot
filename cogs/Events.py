import discord
from discord.ui import Button, View
from discord.ext import commands,tasks
import json

class MyView(View):
  def __init__(self,bot):
    super().__init__(timeout=None)
    self.bot = bot
    self.EventRole=952907898206441532 # < < < change to Your Wanted Role 
  
  #---------------------------------------------------------------------------------------------------------------------------#
  @discord.ui.button(label = "Apply",style=1,custom_id="Apply",emoji="🎉")
  async def Button_callback(self, button, interaction):
    with open("Data.json","r") as f:
      Data = json.load(f)
    if interaction.user.id in Data["EventIDs"]:
      await interaction.response.send_message(f"You are already registered",ephemeral=True)
    else:
      Data["EventUsers"][interaction.user.name] = interaction.user.id
      Data["EventIDs"].append(interaction.user.id)
      role = discord.utils.get(interaction.user.guild.roles, id=self.EventRole)
      await interaction.user.add_roles(role)
      await interaction.response.send_message(f"You have been registered, you can now join <#952674696497860668>! Check dms for invite code",ephemeral=True)
    with open("Data.json","w") as f:
      json.dump(Data,f,indent=4)
  
  async def on_error(self,error,item,interaction):
    await interaction.interaction.channel.send("🔥Oh no the interaction! its Broken D: <@269759748302176256><@632029144196186122>🔥",ephemeral=False)
    raise error

#---------------------------------------------------------------------------------------------------------------------------#
class Events(commands.Cog,description=":tada: Event Hosting Module"):
    def __init__(self,bot):
        self.bot = bot
        self.guild = 943404593105231882 # < < < change to Your Server ID
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
        if (now-Then)>= 600 and role not in member.roles:
          await member.add_roles(role)
        with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)

#---------------------------------------------------------------------------------------------------------------------------#

    @commands.command(brief="Disables The Button on Event Post",help="<Message ID>",description="lets you disable the button attached to an Event Embed")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Disable(self,ctx,msg:int):
      found = False
      for channel in ctx.guild.text_channels:
        try:
          msg = await channel.fetch_message(msg)
        except:
          found = False
        else:
            await ctx.message.delete(delay=1)
            button = Button(label="Event Over",style=discord.ButtonStyle.red,emoji="☹")
            async def button_callback(interaction):
                await interaction.response.send_message("Looks like you missed the event ☹, if you dont want to miss another get the <@&943946711208980602> Role in <#943891320802529330>",ephemeral=True)
            button.callback = button_callback
            view = View()
            view.add_item(button)
            await msg.edit(view=view)
            await ctx.send(f"message was found and Disabled in <#{channel.id}>")
            found = True
            break
      if found == False:
        await ctx.send("message could not be Found In any Channel :/")

    @commands.command(brief="Repair The Button on Event Post",help="<Message ID>",description="lets you Repair the button attached to an Event Embed")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Fix(self,ctx,msg:int):
      found = False
      for channel in ctx.guild.text_channels:
        try:
          msg = await channel.fetch_message(msg)
        except:
          found = False
        else:
          await ctx.message.delete(delay=1)
          view = MyView(ctx)
          await msg.edit(view=view)
          await ctx.send(f"message was found and Fixed in <#{channel.id}>")
          found = True
          break
      if found == False:
        await ctx.send("message could not be Found In any Channel :/")

    @commands.command(brief="Create Event Embed With Button",help="<unix Time Stamp> <link / 'None'> <Event Description>",description="let you create an event message with an interaction button that will send a link to anyone pressing the button and give them an event role")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Event(self,ctx,unix:int,Link,*,args):
      if unix == 0:
        import time
        unix = int(time.time())
      with open("Data.json","r") as f:
          Data = json.load(f)
      if Link == "None" or Link == "none":
        Data["vrclink"]=None
      else:
        Data["vrclink"]=Link
      Data["EventUnix"] = unix  
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)
      embed=discord.Embed(title="Event", description=args, color=0x00ffee)
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/944096582851231804/954098014937575484/sfegrge.png?width=351&height=203")
      embed.add_field(name="Click The Button", value="Bellow To Apply", inline=False)
      embed.add_field(name="Event Start Time:",value=f"<t:{unix}:R>",inline=False)
      view = MyView(ctx)
      await ctx.send(view=view,embed=embed)
      await ctx.message.delete(delay=1)

    @commands.command(brief="Removes the <@&952668569068511323> Role from Everyone",help="",description="Running this command will remove the <@&952668569068511323> role from **Everyone** on the server")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def EndPerks(self,ctx):
      await ctx.message.delete(delay=1)
      with open("Data.json","r") as f:
          Data = json.load(f)
      Data["EventIDs"] = []
      with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      guild = self.bot.get_guild(self.guild)
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
        

    @commands.command(brief="Removes the <@&952907898206441532> Role from Everyone",help="",description="Running this command will remove the <@&952907898206441532> role from **Everyone** on the server")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def EndEvent(self,ctx):
      await ctx.message.delete(delay=1)
      with open("Data.json","r") as f:
          Data = json.load(f)
      for i in range(len(Data["TempRoles"])):
          del Data["TempRoles"][i]
      with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      guild = self.bot.get_guild(self.guild)
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
    
    @commands.command(brief="let you make a quick and easy poll!",help="<Poll Name>,<Option1>,<Option2>,<Option3>....",description="lets you make a quick and easy poll, note that the ',' is very importent its how the bot distinguishes between options you may also only have up too 6 options")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def Poll(self,ctx,*,args):
      poll = args.split(",")
      message = f"🔴 {poll[1]} \n🟠 {poll[2]} \n"
      emojis =["🔴","🟠"]
      if len(poll) >= 4:
        message = message +f"🟡 {poll[3]} \n"
        emojis.append("🟡")
      if len(poll) >= 5:
        message = message +f"🟢 {poll[4]} \n"
        emojis.append("🟢")
      if len(poll) >= 6:
        message = message +f"🔵 {poll[5]} \n"
        emojis.append("🔵")
      if len(poll) >= 7:
        message = message +f"🟣 {poll[6]} \n"
        emojis.append("🟣")

      embed=discord.Embed(title=poll[0], description=message, color=0x000000)
      embed.set_author(name="POLL TIME!")
      message = await ctx.send(embed=embed)
      for emoji in emojis:
        await message.add_reaction(emoji)
    @commands.command(brief="DMs everyone with the <@&952907898206441532> Role",help="",description="Running this command will message **Everyone** with the <@&952907898206441532>")
    @commands.has_any_role(953518880100352081,943881682275160124,953523758373679136,949433575525191700)
    async def StartEvent(self,ctx):
      with open("Data.json","r") as f:
        Data = json.load(f)
      guild = self.bot.get_guild(self.guild)
      role = discord.utils.get(guild.roles, id=self.EventRole)
      if role is None:
          await ctx.send("Role not found on this server!")
          return
      empty = True
      for member in guild.members:
          if role in member.roles:
              await ctx.send(f"Removed {role.mention} from {member.name}")
              embed=discord.Embed(title="Join us In VR!",description=f"**Join us here >>>** {Data['vrclink']}",color=0x00ffee)
              embed.set_thumbnail(url="https://assets.vrchat.com/www/brand/vrchat-logo-white-transparent-crop-background.png")
              embed.set_image(url="https://media.discordapp.net/attachments/943888861069709383/952670455217659924/VRChat_1920x1080_2022-03-13_20-41-09.979.png?width=960&height=540")
              try:
                await member.send(embed=embed)
              except:
                ctx.send(f"{member.mention} dose not have their dms open and will not receive this an invite")
              empty = False
      if empty:
          await ctx.send(f"Nobody has the role {role.mention}")
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)
async def setup(bot):
  await bot.add_cog(Events(bot))