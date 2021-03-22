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
bot.load_extension('cogs.searchCommand')
bot.run(os.environ.get('TOKEN')
