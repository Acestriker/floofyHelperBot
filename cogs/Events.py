from tokenize import Floatnumber
import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands,tasks
import json

from numpy import double
class LateEvent(View):
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
      embed=discord.Embed(title="Join us In VR!",description=f"**Join us here >>>** {Data['vrclink']}",color=0x00ffee)
      embed.set_thumbnail(url="https://assets.vrchat.com/www/brand/vrchat-logo-white-transparent-crop-background.png")
      embed.set_image(url="https://media.discordapp.net/attachments/943888861069709383/952670455217659924/VRChat_1920x1080_2022-03-13_20-41-09.979.png?width=960&height=540")
      try:
        await interaction.user.send(embed=embed)
      except:
        pass
    with open("Data.json","w") as f:
      json.dump(Data,f,indent=4)
  
  async def on_error(self,error,item,interaction):
    guild = self.bot.get_guild(943404593105231882)
    channel = self.bot.get_channel(933389497599688704)
    await guild.channel.send("🔥Oh no the interaction! its Broken D: <@269759748302176256><@632029144196186122>🔥",ephemeral=False)
    raise error


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
    #guild = self.bot.get_guild(943404593105231882)
    #channel = guild.get_channel(933389497599688704)
    #await channel.send("🔥Oh no the interaction! its Broken D: <@269759748302176256><@632029144196186122>🔥")
    raise error

#---------------------------------------------------------------------------------------------------------------------------#
class Events(commands.Cog,app_commands.Group, name="event"):
    def __init__(self,bot):
        self.bot = bot
        self.guild = 943404593105231882 # < < < change to Your Server ID
        self.me = 953641286232047627 # < < < change to Your Bots ID
        self.EventChannel = 952674696497860668 # < < < change to Your Wanted Role
        self.EventAttendeeRole = 952668569068511323 # < < < change to Your Wanted Role
        self.EventRole=952907898206441532
        super().__init__()
    def has_any_role(interaction):
      for id in [953518880100352081,943881682275160124,953523758373679136,949433575525191700]:
        role = discord.utils.get(interaction.guild.roles, id=id)
        if role in interaction.user.roles:
          return True
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
      with open("messages.json","r") as f:
        Data = json.load(f)
      if user.id != self.me:
        try:
          Polls =Data["Polls"][f"{reaction.message.id}"]
        except:
          pass
        else:
          if reaction.emoji in ["🔴","🟠","🟡","🟢","🔵","🟣"]:
            try:
              lastReactions=Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"]
            except:
              if reaction.emoji == "🔴":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 1
              elif reaction.emoji == "🟠":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 2
              elif reaction.emoji == "🟡":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 3
              elif reaction.emoji == "🟢":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 4
              elif reaction.emoji == "🔵":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 5
              elif reaction.emoji == "🟣":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 6
              with open("messages.json","w") as f:
                json.dump(Data,f,indent=4)
            else:
              if lastReactions == 1:
                lastReactions ="🔴"
              elif lastReactions == 2:
                lastReactions ="🟠"
              elif lastReactions == 3:
                lastReactions ="🟡"
              elif lastReactions == 4:
                lastReactions ="🟢"
              elif lastReactions == 5:
                lastReactions ="🔵"
              elif lastReactions == 6:
                lastReactions ="🟣"
              await reaction.message.remove_reaction(lastReactions, user)
              if reaction.emoji == "🔴":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 1
              elif reaction.emoji == "🟠":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 2
              elif reaction.emoji == "🟡":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 3
              elif reaction.emoji == "🟢":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 4
              elif reaction.emoji == "🔵":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 5
              elif reaction.emoji == "🟣":
                Data["Polls"][f"{reaction.message.id}"]["Reactions"][f"{user.id}"] = 6
              with open("messages.json","w") as f:
                json.dump(Data,f,indent=4)

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
      elif after.channel and before.channel and before.channel.id == self.EventChannel:
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

    @app_commands.command(name="end",description="ends Event")
    @app_commands.check(has_any_role)
    async def end(self,interaction):
      with open("Data.json","r") as f:
          Data = json.load(f)
      found = False
      embed=discord.Embed(title="<a:loading:717856603340013669> Searching for message", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemeral=True)
      for channel in interaction.guild.text_channels:
        try:
          msg = await channel.fetch_message(Data["LastEvent"])
        except:
          found = False
        else:
            embed=discord.Embed(title=f"Message was found and disabled",description=f"Found in <#{channel.id}>.", color=0xadf3fd)
            await interaction.edit_original_message(embed=embed)
            button = Button(label="Event Over",style=discord.ButtonStyle.red,emoji="☹",disabled=True)
            view = View()
            view.add_item(button)
            await msg.edit(view=view)
            found = True
            break
      if found == False:
        embed=discord.Embed(title=f"Message could not be found in any channel :/", color=0xadf3fd)
        await interaction.edit_original_message(embed=embed,ephemeral=True)

      embed=discord.Embed(title="<a:loading:717856603340013669> Removing Roles", color=0xadf3fd)
      await interaction.edit_original_message(embed=embed)
      for i in range(len(Data["TempRoles"])):
          del Data["TempRoles"][i]
      Data["EventIDs"] = []
      guild = self.bot.get_guild(self.guild)
      role = discord.utils.get(guild.roles, id=self.EventRole)
      if role is None:
          embed=discord.Embed(title=f"Role not found on this server!", color=0xadf3fd)
          await interaction.edit_original_message(embed=embed)
          return
      empty = True
      has = len(role.members)
      removed = 0
      for member in guild.members:
          if role in member.roles:
              removed += 1
              await member.remove_roles(role)
              empty = False
      users = f"Removed {role.mention} from {removed}/{has} users."
      if empty:
          embed=discord.Embed(title=f"Nobody has the role",description=f"{role.mention}.", color=0xadf3fd)
          await interaction.edit_original_message(embed=embed)
      else:
        embed=discord.Embed(title=f"Role removal",description=users, color=0xadf3fd)
        await interaction.edit_original_message(embed=embed)
      with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)

    @app_commands.command(name="repair",description="Lets you repair the button attached to an event embed")
    @app_commands.check(has_any_role)
    async def Fix(self,interaction,msg:str):
      found = False
      embed=discord.Embed(title="<a:loading:717856603340013669> Searching for message", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemeral=True)
      for channel in interaction.guild.text_channels:
        try:
          msg = await channel.fetch_message(msg)
        except:
          found = False
        else:
          view = MyView(self.bot)
          await msg.edit(view=view)
          embed=discord.Embed(title=f"message was fixed",description=f"Found in <#{channel.id}>.", color=0xadf3fd)
          await interaction.edit_original_message(embed=embed)
          found = True
          break
      if found == False:
        embed=discord.Embed(title="message could not be Found In any Channel :/", color=0xadf3fd)
        await interaction.edit_original_message(embed=embed)

    @app_commands.command(name="create",description="let you create an event message")
    @app_commands.check(has_any_role)
    async def event(self,interaction,unix:int,msg:str,link:str=None):
      if unix == 0:
        import time
        unix = int(time.time())
      with open("Data.json","r") as f:
          Data = json.load(f)
      Data["vrclink"]=link
      Data["EventUnix"] = unix 
      embed=discord.Embed(title="Event", description=msg, color=0x00ffee)
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/944096582851231804/954098014937575484/sfegrge.png?width=351&height=203")
      embed.add_field(name="Click The Button", value="Bellow To Apply", inline=False)
      embed.add_field(name="Event Start Time:",value=f"<t:{unix}:R>",inline=False)
      view = MyView(self.bot)
      message = await interaction.channel.send(view=view,embed=embed)
      Data["LastEvent"] = message.id
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)
      embed=discord.Embed(title="message sent", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemeral=True)



    @app_commands.command(name="endperks",description="Running this command will remove the event atendee role from Everyone on the server")
    @app_commands.check(has_any_role)
    async def EndPerks(self,interaction):
      embed=discord.Embed(title="<a:loading:717856603340013669> Removing Roles", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemral=True)
      with open("Data.json","r") as f:
          Data = json.load(f)
      Data["EventIDs"] = []
      with open("Data.json","w") as f:
          json.dump(Data,f,indent=4)
      guild = self.bot.get_guild(self.guild)
      role = discord.utils.get(guild.roles, id=self.EventAttendeeRole)
      if role is None:
          embed=discord.Embed(title="Role not found on this server!", color=0xadf3fd)
          await interaction.response.edit_original_message(embed=embed,ephemeral=True)
          return
      has = len(role.members)
      removed = 0
      for member in guild.members:
          if role in member.roles:
              await member.remove_roles(role)
              removed += 1
      users = f"Removed {role.mention} from {removed}/{has} users."
      embed=discord.Embed(title=f"Role removal",description=users, color=0xadf3fd)
      await interaction.edit_original_message(embed=embed)


    @app_commands.command(name="poll",description="lets you make a quick and easy poll")
    @app_commands.check(has_any_role)
    async def Poll(self,interaction,title:str,item1:str,item2:str,item3:str=None,item4:str=None,item5:str=None,item6:str=None):
      embed=discord.Embed(title=f"<a:loading:717856603340013669> Creating Poll", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemeral=True)
      message = f"🔴 {item1} \n🟠 {item2} \n"
      emojis =["🔴","🟠"]
      if item3 != None:
        message = message +f"🟡 {item3} \n"
        emojis.append("🟡")
      if item4 != None:
        message = message +f"🟢 {item4} \n"
        emojis.append("🟢")
      if item5 != None:
        message = message +f"🔵 {item5} \n"
        emojis.append("🔵")
      if item6 != None:
        message = message +f"🟣 {item6} \n"
        emojis.append("🟣")

      embed=discord.Embed(title=title, description=message, color=0x000000)
      embed.set_author(name="POLL TIME!")

      message = await interaction.channel.send(embed=embed)
      for emoji in emojis:
        await message.add_reaction(emoji)
      with open("messages.json","r") as f:
        Data = json.load(f)
      Data["Polls"][f"{message.id}"]={"Reactions":{}}
      with open("messages.json","w") as f:
        json.dump(Data,f,indent=4)

    @app_commands.command(name="start",description="starts the event")
    @app_commands.check(has_any_role)
    async def StartEvent(self,interaction,link:str=None):
      embed=discord.Embed(title=f"<a:loading:717856603340013669> Starting Event", color=0xadf3fd)
      await interaction.response.send_message(embed=embed,ephemeral=True)
      with open("Data.json","r") as f:
        Data = json.load(f)
      guild = self.bot.get_guild(self.guild)
      role = discord.utils.get(guild.roles, id=self.EventRole)
      if link!=None:
        Data['vrclink'] = link
      if role is None:
          embed=discord.Embed(title=f"Role not found on this server!", color=0xadf3fd)
          await interaction.followup.send(embed=embed,ephemeral=True)
          return
      empty = True
      count = 0
      sent = 0
      for member in guild.members:
          if role in member.roles:
              count += 1 
              embed=discord.Embed(title="Join us In VR!",description=f"**Join us here >>>** {Data['vrclink']}",color=0x00ffee)
              embed.set_thumbnail(url="https://assets.vrchat.com/www/brand/vrchat-logo-white-transparent-crop-background.png")
              embed.set_image(url="https://media.discordapp.net/attachments/943888861069709383/952670455217659924/VRChat_1920x1080_2022-03-13_20-41-09.979.png?width=960&height=540")
              try:
                await member.send(embed=embed)
              except:
                await interaction.followup.send(f"{member.mention} dose not have their dms open and will not receive this an invite")
              else:
                sent += 1
              empty = False
    
      users = f"sent a dm to {count}/{sent} users."
      embed=discord.Embed(title=f"Event DM",description=users, color=0xadf3fd)
      await interaction.edit_original_message(embed=embed)
      with open("Data.json","w") as f:
        json.dump(Data,f,indent=4)

      found = False
      for channel in interaction.guild.text_channels:
        try:
          msg = await channel.fetch_message(Data['LastEvent'])
        except:
          found = False
        else:
            view = LateEvent(self.bot)
            await msg.edit(view=view)
            await interaction.followup.send(f"message was found and Changed in <#{channel.id}>",ephemeral=True)
            found = True
            break
      if found == False:
        await interaction.followup.send("message could not be Found In any Channel :/",ephemeral=True)

async def setup(bot):
  await bot.add_cog(Events(bot),guilds=[discord.Object(id=943404593105231882)])