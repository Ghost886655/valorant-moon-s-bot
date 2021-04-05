import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(title="פקודות:",
                              description="++j -  בשביל להצטרף לקיו\n++l - בשביל לצאת מהקיו\n++teamsize משנה את מספר השחקנים בטים - מספר\n++search שחקן")
        embed.set_footer(text="בוט על ידי ☿ 𝕲𝖍𝖔𝖘𝖙 ☿")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
