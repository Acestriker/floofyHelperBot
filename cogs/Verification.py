import os
import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands,tasks
import json
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
import textwrap

class ModButtons(View):
    def __init__(self,bot,user):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.guild = 943404593105231882
        self.welocme = 943891195128578069
        self.general = 943404593105231885

    @discord.ui.button(label = "Accept",style=3)
    async def Submit_callback(self,interaction,button):
        guild =self.bot.get_guild(self.guild)
        member = guild.get_member(self.user.id)
        if member is not None:
            role = discord.utils.get(guild.roles, id=944776799974461511)
            await member.remove_roles(role)
            role = discord.utils.get(guild.roles, id=943895260612919317)
            await member.add_roles(role)

            embed=discord.Embed(title=f"Application Approved! <a:eeveeDance:945327984196337714>", description=f"Thank you for your responses. Here's a few things to enjoy in our server!\n> <:FD_orangeDash:976202267441119252> Head to <#943891320802529330> to get your roles sorted\n> <:FD_yellowDash:976202267298512898> Any announcements will be posted in <#943887232304037948>\n> <:FD_greenDash:976202267290140713> We have occasional giveaways and events in <#943888861069709383>\n> <:FD_blueDash:976202267235581992> There is a starboard here - <#943983948449583104>, If you like someone's post, react with a ⭐ to their post, if three people react to the post, it's placed in the starboard!", color=0x00ff00)
            embed.set_author(name="Approved!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
            await interaction.response.send_message("User Approved!",ephemeral=True)
            await self.user.send(embed=embed)

            embeds = interaction.message.embeds
            for embed in embeds:
                embed.to_dict()
            embed.color = 0x00ff00
            embed.title = f"{embed.title} (Approved)"
            embed.add_field(name="Accepted by: ", value=f"{interaction.user.mention}", inline=False)
            view = View()
            await interaction.message.edit(content=f"{self.user.mention}",view=view,embed=embed)

            channel = guild.get_channel(self.welocme)
            img = Image.open("./Assets/Banner.png")
            img = img.convert("RGBA")
            font =ImageFont.truetype("./Assets/whitneybold.otf",70) 
            Asset = self.user.avatar
            Avatar = BytesIO(await Asset.read())
            pfp = Image.open(Avatar)
            pfp = pfp.resize((427,427))
            mask = Image.open('./Assets/Mask.png').convert('L')
            pfpBack = Image.open("./Assets/BG.png")
            pfpBack= pfpBack.convert("RGBA")
            pfp = pfp.convert("RGBA")
            pfp = Image.composite(pfp,pfpBack, mask)
            img.paste(pfp, (117,90), pfp)
            draw = ImageDraw.Draw(img)
            W = 1350
            txt = f"Welcome {self.user.name}#{self.user.discriminator} to {member.guild.name}!"
            txt = textwrap.wrap(txt, width=40)
            txt.append(f"This server now has {len(guild.members)} members.")
            current_h, pad=300, 80
            LineNo = round(len(txt)/2)
            for i in range(0,LineNo):
                current_h -=pad
            for line in txt:
                w, h = draw.textsize(line, font=font)
                draw.text((((W - w) / 2)+600, current_h), line, font=font)
                current_h += pad
            img.save("./Assets/Welcome.png")
            await channel.send(file=discord.File("./Assets/Welcome.png"))
            channel = guild.get_channel(self.general)
            await channel.send(f"Everyone, welcome {self.user.mention} to the server! We hope you enjoy your stay!")
            with open("Users.json","r") as f:
                    Data = json.load(f)
            print(Data[f"{self.user.id}"]["age"])
            del Data[f"{self.user.id}"]
            with open("Users.json","w") as f:
                json.dump(Data,f)
        else:
            embeds = interaction.message.embeds
            for embed in embeds:
                embed.to_dict()
            embed.color = 0x000000
            embed.title = f"{embed.title} (User Left)"
            embed.add_field(name="Attempted approval by:", value=f"{interaction.user.mention}", inline=False)
            view = View()
            await interaction.message.edit(content="",view=view,embed=embed)

    @discord.ui.button(label = "Deny",style=4)
    async def Button_callback(self,interaction,button):
        guild =self.bot.get_guild(self.guild)
        member = guild.get_member(self.user.id)
        if member is not None:
            def check(m):
                return m.author == interaction.user
            await interaction.response.send_message("Send a message to add a reason",ephemeral=True)
            msg = await self.bot.wait_for('message', check=check)
            embed=discord.Embed(title=f"Application Rejected", description=f"Your application was rejected for the following reason:\n\n> {msg.content}\n\nTo re-apply, click the button below.", color=0xff0000)
            embed.set_author(name="Rejected", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
            view = VerifecationStart(interaction)
            await self.user.send(embed=embed,view=view)
            await msg.delete(delay=1)
            embeds = interaction.message.embeds
            for embed in embeds:
                embed.to_dict()
            embed.color = 0xff0000
            embed.title = f"{embed.title} (Rejected)"
            embed.add_field(name="Rejected by: ", value=f"{interaction.user.mention}", inline=False)
            embed.add_field(name="Rejected reason: ", value=msg.content, inline=False)
            view = View()
            await interaction.message.edit(content=f"{self.user.mention}",view=view,embed=embed)
        else:
            embeds = interaction.message.embeds
            for embed in embeds:
                embed.to_dict()
            embed.color = 0x000000
            embed.title = f"{embed.title} (User Left)"
            view = View()
            embed.add_field(name="Attempted denial by:", value=f"{interaction.user.mention}", inline=False)
            await interaction.message.edit(content="",view=view,embed=embed)
    

    @discord.ui.button(label = "Kick",style=4)
    async def kick_callback(self,interaction,button):
        def check(m):
            return m.author == interaction.user
        await interaction.response.send_message("Send a message to add a reason",ephemeral=True)
        msg = await self.bot.wait_for('message', check=check)
        embeds = interaction.message.embeds
        guild =self.bot.get_guild(self.guild)
        embed=discord.Embed(title=f"Your application was rejected and you were kicked", description=f"You were kicked for the following reason:\n\n> {msg.content}", color=0xff0000)
        embed.set_author(name="Kicked", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")         
        await self.user.send(embed=embed)
        await guild.kick(self.user,reason = msg.content)
        for embed in embeds:
            embed.to_dict()
        embed.color = 0xff0000
        embed.title = f"{embed.title} (Banned)"
        embed.add_field(name="Rejected by: ", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="Kick reason: ", value=msg.content, inline=False)
        view = View()
        await interaction.message.edit(content=f"{self.user.mention}",view=view,embed=embed)
        await msg.delete(delay=1)

    @discord.ui.button(label = "Ban",style=4)
    async def ban_callback(self,interaction,button):
        def check(m):
            return m.author == interaction.user
        await interaction.response.send_message("Send a message to add a reason",ephemeral=True)
        msg = await self.bot.wait_for('message', check=check)
        embeds = interaction.message.embeds
        guild =self.bot.get_guild(self.guild)
        embed=discord.Embed(title=f"Your application was rejected and you were banned", description=f"You were banned for the following reason:\n\n> {msg.content}\n\nTo appeal the ban, go to [**our ban appeal form**](https://dyno.gg/form/8d90fc8).", color=0xff0000)
        embed.set_author(name="Banned", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")         
        await self.user.send(embed=embed)
        await guild.ban(self.user,reason = msg.content)
        for embed in embeds:
            embed.to_dict()
        embed.color = 0xff0000
        embed.title = f"{embed.title} (Banned)"
        embed.add_field(name="Rejected by: ", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="Ban reason: ", value=msg.content, inline=False)
        view = View()
        await interaction.message.edit(content=f"{self.user.mention}",view=view,embed=embed)
        await msg.delete(delay=1)
		
    @discord.ui.button(label = "User ID",style=2)
    async def id_callback(self,interaction,button):
        await interaction.response.send_message(f"{self.user.id}",ephemeral=True)
        
    async def on_error(self,error,item,interaction):
        raise error

class VerifecationFinish(View):
    def __init__(self,bot,guild,Client):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild = guild
        self.Client =Client
    @discord.ui.button(label = "Submit",style=3,emoji="<:FD_greenDash:976202267290140713>")
    async def Submit_callback(self,interaction,button):
        embed=discord.Embed(title=f"Your verification has been submitted!", description="Once a staff member has approved your verification, you'll be given access to the server!\n This might take some time though so don't panic if you don't get accepted immediately.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        Submit = Button(label = "Submit",style=3,emoji="<:FD_greenDash:976202267290140713>",disabled=True)
        Restart = Button(label = "Restart",style=1,emoji="<:FD_blueDash:976202267235581992>",disabled=True)
        view = View()
        view.add_item(Submit)
        view.add_item(Restart)
        await interaction.response.edit_message(view=view)
        await interaction.channel.send(embed=embed)
        guild = self.guild
        channel = guild.get_channel(966440032325996635)
        embed=discord.Embed(title="Verification Application", color=0xffa200)
        with open("Users.json","r") as f:
                Data = json.load(f)
        embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", icon_url=f"{interaction.user.avatar}")
        embed.set_thumbnail(url=f"{interaction.user.avatar}")
        import time
        embed.add_field(name="Account created", value=f"<t:{round(time.mktime(interaction.user.created_at.timetuple()))}:R>", inline=False)
        embed.add_field(name="Age", value=f"{Data[f'{interaction.user.id}']['age']}", inline=False)
        embed.add_field(name="Why they joined", value=f"{Data[f'{interaction.user.id}']['whyJoin']}", inline=True)
        embed.add_field(name="Tell us about yourself", value=f"{Data[f'{interaction.user.id}']['TellusAboutYou']}", inline=True)
        embed.set_footer(text=f"{interaction.user.id}")
        import datetime
        embed.timestamp = datetime.datetime.utcnow()
        User = interaction.user
        await channel.send("<@&965729386915573791>",embed=embed,view=ModButtons(self.Client,User))
        
    @discord.ui.button(label = "Restart",style=1,emoji="<:FD_blueDash:976202267235581992>")
    async def Button_callback(self,interaction,button):
        with open("Users.json","r") as f:
          Data = json.load(f)
        Data[f"{interaction.user.id}"] = {
            "age":None,
            "whyJoin":None,
            "TellusAboutYou":None
        }
        with open("Users.json","w") as f:
            json.dump(Data,f)
        Submit = Button(label = "Submit",style=3,emoji="<:FD_greenDash:976202267290140713>",disabled=True)
        Restart = Button(label = "Restart",style=1,emoji="<:FD_blueDash:976202267235581992>",disabled=True)
        view = View()
        view.add_item(Submit)
        view.add_item(Restart)
        await interaction.response.edit_message(view=view)
        embed=discord.Embed(title=f"How old are you? {interaction.user.name}", description="Click one of the buttons below to select your age range.\n**Lying about your age will result in a ban.**", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        view = VerifecationAge(interaction)
        await interaction.channel.send(embed=embed,view=view)
    async def on_error(self,error,item,interaction):
        raise error

class VerifecationAgeDisabled(View):
    def __init__(self,bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label = "Under 13",style=2,custom_id="13",disabled=True)
    async def Under13_callback(self,interaction,button):
        pass
    @discord.ui.button(label = "13-15",style=1,custom_id="13+",disabled=True)
    async def Over13_callback(self,interaction,button):
        pass
    @discord.ui.button(label = "16-17",style=3,custom_id="16+",disabled=True)
    async def Over16_callback(self,interaction,button):
        pass
    @discord.ui.button(label = "18+",style=4,custom_id="18+",disabled=True)
    async def Over18_callback(self,interaction,button):
        pass
    async def on_error(self,error,item,interaction):
        raise error

class VerifecationAge(View):
    def __init__(self,bot):
        super().__init__(timeout=None)
        self.bot = bot
  #---------------------------------------------------------------------------------------------------------------------------
    @discord.ui.button(label = "Under 13",style=2,custom_id="13")
    async def Under13_callback(self,interaction,button):
        with open("Users.json","r") as f:
            Data = json.load(f)
        Data[f"{interaction.user.id}"]["age"] = "13"
        await interaction.response.edit_message(view=VerifecationAgeDisabled(interaction))
        guild =self.bot.get_guild(943404593105231882)
        channel = guild.get_channel(966440032325996635)
        embed=discord.Embed(title="Verification Application (Rejected)", color=0xff0000)
        embed.add_field(name="Rejected reason:", value=f"[Automod] User is under 13", inline=False)
        embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", icon_url=f"{interaction.user.avatar}")
        embed.set_thumbnail(url=f"{interaction.user.avatar}")
        embed.set_footer(text=f"{interaction.user.id}")
        import datetime
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        embed=discord.Embed(title=f"Sorry but you have to be 13+ to join", description="As per Discord's ToS you have to be 13+ to use this app, you are welcome to join the server once your are over 13.", color=0x000000)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        await interaction.channel.send(embed=embed)
        await guild.kick(interaction.user)

        
    @discord.ui.button(label = "13-15",style=1,custom_id="13+")
    async def Over13_callback(self,interaction,button):
        with open("Users.json","r") as f:
            Data = json.load(f)
        Data[f"{interaction.user.id}"]["age"] = "13-15"
        Data[f"{interaction.user.id}"]["stage"] = 1
        with open("Users.json","w") as f:
            json.dump(Data,f)
        await interaction.response.edit_message(view=VerifecationAgeDisabled(interaction))
        embed=discord.Embed(title=f"Why did you join this server?", description="**Tell us how you found us**\n If a friend invited you, tell us who!\n Next message will be submitted as a reponse to this question.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        await interaction.channel.send(embed=embed)
    @discord.ui.button(label = "16-17",style=3,custom_id="16+")
    async def Over16_callback(self,interaction,button):
        with open("Users.json","r") as f:
            Data = json.load(f)
        Data[f"{interaction.user.id}"]["age"] = "16-17"
        Data[f"{interaction.user.id}"]["stage"] = 1
        with open("Users.json","w") as f:
            json.dump(Data,f)
        await interaction.response.edit_message(view=VerifecationAgeDisabled(interaction))
        embed=discord.Embed(title=f"Why did you join this server?", description="**Tell us how you found us**\n If a friend invited you, tell us who!\nYour next message will be submitted as a reponse to this question.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        await interaction.channel.send(embed=embed)
    @discord.ui.button(label = "18+",style=4,custom_id="18+")
    async def Over18_callback(self,interaction,button):
        with open("Users.json","r") as f:
            Data = json.load(f)
        Data[f"{interaction.user.id}"]["age"] = "18+"
        Data[f"{interaction.user.id}"]["stage"] = 1
        with open("Users.json","w") as f:
            json.dump(Data,f)
        await interaction.response.edit_message(view=VerifecationAgeDisabled(interaction))
        embed=discord.Embed(title=f"Why did you join this server?", description="**Tell us how you found us**\n If a friend invited you, tell us who!\nYour next message will be submitted as a reponse to this question.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        await interaction.channel.send(embed=embed)
    async def on_error(self,error,item,interaction):
        raise error

class VerifecationStart(View):
  def __init__(self,bot):
    super().__init__(timeout=None)
    self.bot = bot
  #---------------------------------------------------------------------------------------------------------------------------#
  @discord.ui.button(label = "Start Verification",style=3,custom_id="StartVerify",emoji="<:FD_greenDash:976202267290140713>")
  async def Button_callback(self,interaction,button):
        with open("Users.json","r") as f:
            Data = json.load(f)
        print(interaction.user.id)
        Data[f"{interaction.user.id}"] = {
            "age":None,
            "whyJoin":None,
            "TellusAboutYou":None,
            "stage":0
        }
        with open("Users.json","w") as f:
            json.dump(Data,f)
        button.disabled = True
        await interaction.response.edit_message(view=self)
        embed=discord.Embed(title=f"How old are you, {interaction.user.name}?", description="Click one of the buttons below to select your age range.\n**Lying about your age will result in a ban.**", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        view = VerifecationAge(self.bot)
        await interaction.channel.send(embed=embed,view=view)

  async def on_error(self,error,item,interaction):
    raise error

class Verification(commands.GroupCog, name="verification"):
    def __init__(self,bot):
        self.bot = bot
        self.me =943873910699618364

    @commands.Cog.listener()
    async def on_member_join(self,member):
        with open("Users.json","r") as f:
            Data = json.load(f)
        Data["wait"].append(member.id) 
        with open("Users.json","w") as f:
            json.dump(Data,f)
        role = discord.utils.get(member.guild.roles, id=944776799974461511)
        await member.add_roles(role)
        embed=discord.Embed(title=f"Welcome {member.name} to {member.guild.name}! ", description="To gain access to the server, make sure to read over the <#943890671339733012> and **complete our verification.** \n You can get started by clicking the button below.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        view = VerifecationStart(self.bot)
        await member.send(embed=embed,view=view)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.id == 954988892556242965 and message.author != self.bot.user:
            with open("Users.json","r") as f:
                Data = json.load(f)
            if message.author.id in Data["wait"]:
                embed=discord.Embed(title=f"Hi {message.author.name}, don't forget to verify!", description="If you're having trouble verifying or didn't receive a DM from <@953794936736727110> (make sure your DMs are open), open a ticket in <#955991656568614972>." , color=0xadf3fd)
                await message.reply(embed=embed)
                Data["wait"].remove(message.author.id)
                with open("Users.json","w") as f:
                    json.dump(Data,f)
            
        if message.channel.type is discord.ChannelType.private and message.author != self.bot.user:
            with open("Users.json","r") as f:
                Data = json.load(f)
            if Data[f"{message.author.id}"]["stage"] == 1:
                Data[f"{message.author.id}"]["whyJoin"] = message.content
                Data[f"{message.author.id}"]["stage"] = 2
                embed=discord.Embed(title=f"Tell us a little about yourself!", description="Do you have any hobbies or interest? Have a fursona? Tell us about it!\n Your next message will be submitted as a reponse to this question.", color=0xadf3fd)
                embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
                await message.channel.send(embed=embed)
            elif Data[f"{message.author.id}"]["stage"] == 2:
                Data[f"{message.author.id}"]["TellusAboutYou"] = message.content
                Data[f"{message.author.id}"]["stage"] = 0
                embed=discord.Embed(title=f"**Thank you for completing our verifcation**", description=f"**Here is what you submitted:**\n>>> **Age:** {Data[f'{message.author.id}']['age']}\n\n **Why you joined:** {Data[f'{message.author.id}']['whyJoin']}\n\n **What you said about yourself:** {Data[f'{message.author.id}']['TellusAboutYou']}", color=0xadf3fd)
                embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
                embed.add_field(name="What now?", value="Once you click the submit button your verification will be sent to our staff team. A staff member may ask you to resubmit your verification if they feel like you haven't given enough detail. If you want to start over click the restart button.", inline=False)
                guild =self.bot.get_guild(943404593105231882)
                await message.channel.send(embed=embed,view=VerifecationFinish(message,guild,self.bot))

            with open("Users.json","w") as f:
                json.dump(Data,f)
    @app_commands.command(name="send",description="sends verification message to a user")
    async def message(self,interaction,member:discord.Member):
        embed=discord.Embed(title=f"Welcome {member.name} to {member.guild.name}!", description="To gain access to the server, make sure to read over the <#943890671339733012> and **complete our verification.** \n You can get started by clicking the button below.", color=0xadf3fd)
        embed.set_author(name="Welcome!", icon_url="https://cdn.discordapp.com/icons/943404593105231882/a_cb2346deeb9e18939507e33c8ae8e83f.png?width=180&height=180")
        view = VerifecationStart(self.bot)
        try:
            await member.send(embed=embed,view=view)
        except:
            embed=discord.Embed(title=f"Sent verification to user", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title=f"Sent verification to user", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot):
  await bot.add_cog(Verification(bot),guilds=[discord.Object(id=943404593105231882)]) 