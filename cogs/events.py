from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("discord.gg") or message.content.lower().startswith("https://discord.gg"):
            if not message.author.bot:
                await message.delete()


def setup(bot):
    bot.add_cog(Events(bot))
