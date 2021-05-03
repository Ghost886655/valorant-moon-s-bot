import discord
from discord.ext import commands
import os
bot = commands.Bot(command_prefix='++', case_insensitive=True)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")
    await bot.change_presence(activity=discord.Game(name="++help"))


bot.remove_command("help")
bot.load_extension('cogs.QueuesRelated')
bot.load_extension('cogs.help')
bot.load_extension('cogs.events')
bot.run("ODM4ODI5MzU1OTk5NDI4Njg5.YJAytw.hsS2HmN2Aiu5UnmZ5IKUmGUy7R4")
