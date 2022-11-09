# Importing Modules.
from discord.ext import commands
import discord
from colorama import Fore
from keep_alive import keep_alive
from os import environ
import json

bot = commands.Bot("!", self_bot=True) # Defining bot.

@bot.event
async def on_ready():
    print("LOG: Tool Đã Đăng Nhập Vào Tài Khoản Của Bạn! " + Fore.YELLOW + f"{bot.user}.\n")
    with open("data.json", "r") as f:
        data = json.load(f)
    if data["guild"] == None or data["channel"] == None:
        pass
    else:
        try:
            voice_channel = discord.utils.get(bot.get_guild(int(data["guild"])).channels, id = int(data["channel"]))
            await voice_channel.connect()
            print(f"{Fore.GREEN}[-]{Fore.WHITE} Đã Kết Nối Tới {Fore.CYAN}{voice_channel} {Fore.WHITE}in {Fore.CYAN}{voice_channel.guild}{Fore.WHITE}.")
        except:
            print(f"{Fore.RED} [ - ] Lỗi. Vui Lòng Vào VC Bằng Lệnh !join + IDVC")

@bot.command() # Join command.
async def join(ctx, voice_channel : discord.VoiceChannel):
    await voice_channel.connect()
    data = {"guild":str(ctx.guild.id),"channel":str(voice_channel.id)}
    with open("data.json", "w") as f:
        json.dump(data, f)
    print(f"{Fore.GREEN}[-]{Fore.WHITE} Đã Kết Nối Tới {Fore.CYAN}{voice_channel} {Fore.WHITE}in {Fore.CYAN}{voice_channel.guild}{Fore.WHITE}.")
    await ctx.message.delete()

@bot.command() # Leave command.
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    with open("data.json", "w") as f:
        json.dump({"guild":None,"channel":None}, f)
    print(f"{Fore.RED}[-]{Fore.WHITE} Đã Ngắt Kết Nối {Fore.CYAN}{voice_client.channel}{Fore.WHITE} in {Fore.CYAN}{ctx.message.guild}{Fore.WHITE}.")
    await ctx.message.delete()

keep_alive()
bot.run(environ["TOKEN"], bot=False)