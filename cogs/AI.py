# Import
import os
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ui import Button, View
from discord.ext import commands,tasks
from dotenv import load_dotenv
from Config import OPENAIKEY,PREFIX
import openai
import asyncio
import json
import random

# AI Connection and Black List
load_dotenv()
openai.api_key = OPENAIKEY
completion = openai.Completion()

# View Classes 
class ChatButtons(View):
    def __init__(self,bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label = "Start a Chat",style=3)
    async def Submit_callback(self,button,interaction):
        with open("AI.json","r") as f:
            Data = json.load(f)
        import time
        now = int(time.time())
        try:
            then = Data[f"{interaction.user.id}"]["then"]
        except:
            then = 0
        if interaction.user.name not in Data["Users"] or (now - then) > 1800:
            channel=self.bot.get_channel(968225581462335488)
            msg = await channel.create_thread(name=f"🤖・chat-{interaction.user.name}")
            print("Thread Made")
            await msg.add_user(interaction.user)
            await msg.send("test")
            Data[f"{msg.id}"] = None
            Data["Threads"].append(msg.id)
            Data["Users"].append(interaction.user.name)
            Data[f"{interaction.user.id}"] = {"then":now,"tts":False}
            await interaction.response.send_message("chat Thread Created",ephemeral=True)
        else:
            await interaction.response.send_message("you already have an open Chat if you want to close your chat do ~ai close in the chat thread",ephemeral=True)
        with open("AI.json","w") as f:
            json.dump(Data,f,indent=3)
    #@discord.ui.button(label = "Deny",style=4)
    #async def Button_callback(self,button,interaction):
  
    async def on_error(self,error,item,interaction):
        raise error

# Main Cog
class AI(commands.Cog,app_commands.Group, name="ai"):
    def __init__(self,bot):
        super().__init__()
        self.bot = bot
        self.start_chat_log = '''User: Hello, who are you?
FloofyHelper: my name is Floofy Helper. we are currently in Ace's Abode, my friends are Ace, Doshi and Cidel who is a furry
'''
        super().__init__()

    def ask(self,question, chat_log=None):
        if chat_log is None:
            chat_log = self.start_chat_log
        prompt = f'{chat_log}User: {question}\nFloofyHelper:'
        response = completion.create(
            prompt=prompt, engine="davinci", stop=['\nUser'], temperature=0.9,
            top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
            max_tokens=150)
        answer = response.choices[0].text.strip()
        return answer
    def append_interaction_to_chat_log(self,question, answer, chat_log=None):
        if chat_log is None:
            chat_log = self.start_chat_log
        return f'{chat_log}User: {question}\nFloofyHelper: {answer}\n'

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(PREFIX):
            return
        if message.content.startswith('`'):
            return
        with open("AI.json","r") as f:
                Data = json.load(f)
        if message.channel.id in Data["Threads"]:
            try:
                tts = Data[f"{message.author.id}"]["tts"]
            except:
                tts = False
                import time
                now = int(time.time())
                Data[f"{message.author.id}"] = {"then":now,"tts":False}
            chat_log = Data[f"{message.channel.id}"]
            if chat_log != None and len(chat_log) > 5000:
               chat_log = chat_log[2000:]
               chat_log = chat_log[chat_log.find('User: '):]
               print("chat_log maxed out")
            question = message.content
            ans =self.ask(question,chat_log)
            ans =ans.replace("FloofyHelper: ", "")
            ans = ans.replace("\n", ".")
            ans = ans.strip("~@")
            print(ans)
            if any(x in ans.lower() for x in Data["BLACKLIST"]) or any(x in message.content.lower() for x in Data["BLACKLIST"]):
                await message.reply("Blacklisted word detected in response A.I context will be reset.")
                Data[f"{message.channel.id}"] = None
            else:
                chat_log = self.append_interaction_to_chat_log(question,ans,chat_log)   
                Data[f"{message.channel.id}"] = chat_log
                async with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.reply(ans,tts=tts)
        with open("AI.json","w") as f:
            json.dump(Data,f,indent=3)

    
    @app_commands.command(name="reset",description="reset A.I. context")
    async def reset(self,interaction):
        with open("AI.json","r") as f:
            Data = json.load(f)
        if interaction.channel.type == discord.ChannelType.private_thread and interaction.channel.id in Data["Threads"] and interaction.channel.parent_id == 968225581462335488:
            Data[f"{interaction.channel.id}"] = None
            with open("AI.json","w") as f:
                json.dump(Data,f,indent=3)
            
            embed=discord.Embed(title="A.I. context Reset", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title="this command can only be in an A.I. chat thread", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(name="close",description="close current A.I. chat")
    async def close(self,interaction):
        with open("AI.json","r") as f:
            Data = json.load(f)
        if interaction.channel.type == discord.ChannelType.private_thread and interaction.channel.id in Data["Threads"] and interaction.channel.parent_id == 968225581462335488:
            await interaction.channel.delete()
            del Data[f"{interaction.channel.id}"]
            Data["Threads"].remove(interaction.channel.id)
            Data["Users"].remove(interaction.user.name)
            del Data[f"{interaction.user.id}"]
        else:
            embed=discord.Embed(title="this command can only be in an A.I. chat thread", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        with open("AI.json","w") as f:
            json.dump(Data,f,indent=3)
    @app_commands.command(name="tts",description="toggle text to speech")
    @app_commands.choices(toggle=[
        Choice(name="on",value=1),
        Choice(name="off",value=0)
    ])
    async def ttstoggle(self,interaction,toggle : int):
        with open("AI.json","r") as f:
            Data = json.load(f)
        if interaction.channel.type == discord.ChannelType.private_thread and interaction.channel.id in Data["Threads"] and interaction.channel.parent_id == 968225581462335488:
            if toggle == 1:
                toggle = True
            elif toggle == 0:
                toggle = False
            try:    
                Data[f"{interaction.user.id}"]["tts"] = toggle
            except:
                import time
                now = int(time.time())
                Data[f"{interaction.user.id}"] = {"then":now,"tts":toggle}
            embed=discord.Embed(title="text to speace enabled", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed=discord.Embed(title="this command can only be in an A.I. chat thread", color=0xadf3fd)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        with open("AI.json","w") as f:
            json.dump(Data,f,indent=3)
    @app_commands.command(name="start",description="reset A.I. context")
    async def Start(self,interaction):
        embed=discord.Embed(title="Welcome to the Floofy Helper A.I.",description="Click the button below to start a chat with <@!953794936736727110>", color=0xadf3fd)
        embed.add_field(name="<a:zz_alert:958106160882409542> Disclaimer",value="The FloofyHelper A.I. can get out of hand sometimes as it essentially has a mind of its own. Do `/ai reset` to reset your conversation.")
        embed.set_author(name="FLoofyHelper A.I.", icon_url="https://media.discordapp.net/attachments/944096582851231804/954796896084439040/drctfvygbhbgvftcdrxctfvg.png?width=180&height=180")
        embed.set_thumbnail(url="https://openai.com/content/images/2021/08/openai-avatar.png")
        embed.set_footer(text="This A.I. was made using the openAI, find out more at https://openai.com/")
        view = ChatButtons(self.bot)
        await interaction.channel.send(embed=embed,view=view)
        #await ctx.send(embed=embed,view=view)

    
async def setup(bot):
  await bot.add_cog(AI(bot),guilds=[discord.Object(id=943404593105231882)])