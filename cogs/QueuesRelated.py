import random

import discord
from discord.ext import commands
from discord.utils import get

queue = []
queue_teamsize = [5]

bot = commands.Bot(command_prefix="++", case_insensitive=True)


class QueuesRelated(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix='++')

    @commands.command(aliases=['ts'])
    async def teamsize(self, ctx, size=""):
        try:
            teamsize = queue_teamsize[1]
        except Exception:
            teamsize = queue_teamsize[0]
        if size == "":
            return await ctx.send(f"מספר השחקנים בקבוצה כרגע הוא {teamsize}")
        try:
            size = int(size)
        except Exception or int(size) > 5 or int(size) < 1:
            return await ctx.send("מספר השחקנים בקבוצה חייב להיות מספר וקטן מ6!")
        queue_teamsize.insert(1, size)
        await ctx.send(f" מספר השחקנים בטים השתנה ל{size} ")

    @commands.command(aliases=['j', 'q'])
    async def join(self, ctx):
        if str(ctx.channel) == "pugs" or str(ctx.channel) == "fixing-bugs" or str(ctx.channel) == "bot-commands":
            if str(ctx.author.id) in queue:
                return await ctx.send("אתה כבר בקיו!")
            try:
                size = queue_teamsize[1]
            except IndexError:
                size = queue_teamsize[0]
            if len(queue) == 0:
                queue.append(str(ctx.author.id))
                new_queue = discord.Embed(title="קיו חדש התחיל!",
                                          description=f" {ctx.author.mention} התחיל קיו של {size}v{size}! כתבו q++ בשביל להצטרף.",
                                          color=discord.Color.red())
                new_queue.set_footer(text="בוט על ידי Quidy")
                player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                              description=f" הצטרף לקיו{ctx.author.mention} ",
                                              color=discord.Color.red())
                player_joined.set_footer(text="בוט על ידי Quidy")
                player_joined.add_field(name=f"**שחקנים שכבר בקיו: {len(queue)}/{size * 2}**",
                                        value=f"<@{'>, <@'.join(queue)}>")
                await ctx.send(embed=new_queue)
                print(queue)
                return await ctx.send(embed=player_joined)
            if len(queue) < size * 2 - 1:
                queue.append(str(ctx.author.id))
                player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                              description=f" הצטרף לקיו{ctx.author.mention} ",
                                              color=discord.Color.red())
                player_joined.add_field(name=f"**שחקנים שכבר בקיו: {len(queue)}/{size * 2}**",
                                        value=f"<@{'> , <@'.join(queue)}>")
                player_joined.set_footer(text="בוט על ידי Quidy")
                await ctx.send(embed=player_joined)
            else:
                queue.append(str(ctx.author.id))
                player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                              description=f" הצטרף לקיו{ctx.author.mention} ",
                                              color=discord.Color.red())
                player_joined.set_footer(text="בוט על ידי Quidy")
                player_joined.add_field(name=f"**שחקנים שכרגע בקיו: {len(queue)}/{size * 2}**",
                                        value=f"<@{'> , <@'.join(queue)}>")
                await ctx.send(embed=player_joined)
                team_1 = random.sample(queue, size)
                await ctx.send(f'<@{">, <@".join(queue)}')
                for i in team_1:
                    queue.remove(i)
                teams = discord.Embed(title="קבוצה A", description=f">@{'> , <@'.join(team_1)}>", inline=False,
                                      color=discord.Color.red())
                teams.add_field(name="קבוצה B", value=f"<@{'> , <@'.join(queue)}>", inline=False)
                defenders_or_attackers = random.randint(0, 1)
                if defenders_or_attackers == 0:
                    teams.add_field(name="קבוצה A:", value="מתחילים כAttackers", inline=False)
                    teams.add_field(name="קבוצה B:", value="מתחילים כDefenders", inline=False)
                if defenders_or_attackers == 1:
                    teams.add_field(name="קבוצה A:", value="מתחילים כDefenders", inline=False)
                    teams.add_field(name="קבוצה B:", value="מתחילים כAttackers", inline=False)
                map = random.randint(1, 5)
                if map == 1:
                    teams.add_field(name="מפה:", value="Bind")
                    teams.set_image(
                        url="https://cdn.discordapp.com/attachments/730106200053645334/819624847973154872/Z.png")
                if map == 2:
                    teams.add_field(name="מפה:", value="Icebox")
                    teams.set_image(
                        url="https://cdn.discordapp.com/attachments/730106200053645334/819626129618763886/9k.png")
                if map == 3:
                    teams.add_field(name="מפה:", value="Ascent")
                    teams.set_image(
                        url="https://cdn.discordapp.com/attachments/730106200053645334/819625519359459339/2Q.png")
                if map == 4:
                    teams.add_field(name="מפה:", value="Haven")
                    teams.set_image(
                        url="https://cdn.discordapp.com/attachments/730106200053645334/819625851481358346/2Q.png")
                if map == 5:
                    teams.add_field(name="מפה:", value="Split")
                    teams.set_image(
                        url="https://cdn.discordapp.com/attachments/730106200053645334/819626012178513950/9k.png")
                teams.set_footer(text="בוט על ידי Quidy")
                await ctx.send(embed=teams)
                queue.clear()

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        if str(ctx.channel) == "pugs" or str(ctx.channel) == "fixing-bugs" or str(ctx.channel) == "bot-commands":
            if str(ctx.author.id) in queue:
                queue.remove(str(ctx.author.id)
                player_left = discord.Embed(title="שחקן יצא מהקיו",
                                            description=f"{ctx.author.mention} יצא מהקיו ",
                                            color=discord.Color.red())
                if len(queue) != 0:
                    player_left.add_field(name=f"שחקנים שכרגע בקיו: **{len(queue)}/10**",
                                          value=f"<@{'> , <@'.join(queue)}>")
                    await ctx.send(embed=player_left)
                else:
                    player_left.add_field(name=f"שחקנים שכרגע בקיו: **0/10**",
                                          value="אף אחד")
                    await ctx.send(embed=player_left)
                player_left.set_footer(text="בוט על ידי Quidy")
            else:
                return await ctx.send("אתה לא בקיו!")

    @commands.command()
    async def status(self, ctx):
        try:
            size = queue_teamsize[1]
        except Exception:
            size = queue_teamsize[0]
        embed = discord.Embed(title=f"מספר שחקנים בקיו: {len(queue)}/{(size * 2)} ")
        embed.set_footer(text="בוט על ידי Quidy")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(QueuesRelated(bot))
