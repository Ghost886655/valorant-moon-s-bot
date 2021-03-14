import os
import discord
import random
from discord.ext import commands
import json
from discord.utils import get

client = commands.Bot(command_prefix='++', case_insensitive=True)


@client.event
async def on_ready():
    print(f"{client.user.name} is online.")
    await client.change_presence(activity=discord.Game(name="++help"))


client.remove_command("help")

queue = []
queue_teamsize = [5]


@client.command()
async def teamsize(ctx, size=""):
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


@client.command(aliases=['queue'])
async def q(ctx):
    if str(ctx.channel) == "pugs" or str(ctx.channel) == "fixing-bugs" or str(ctx.channel) == "bot-commands":
        if f"<@{ctx.author.id}>" in queue:
            return await ctx.send("אתה כבר בקיו!")
        channel = get(ctx.guild.voice_channels, name="🎮Custom")
        if ctx.author not in channel.members:
            return await ctx.send("אתה חייב להיות ב<#818145379467919380> בשביל להיות בקיו!")
        role = get(ctx.guild.roles, name="In Queue")
        await ctx.author.add_roles(role)
        try:
            size = queue_teamsize[1]
        except IndexError:
            size = queue_teamsize[0]
        if len(queue) == 0:
            queue.append(f"<@{ctx.author.id}>")
            new_queue = discord.Embed(title="קיו חדש התחיל!",
                                      description=f" {ctx.author.mention} התחיל קיו של {size}v{size}! כתבו q++ בשביל להצטרף.",
                                      color=discord.Color.red())
            new_queue.set_footer(text="בוט על ידי Quidy")
            player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                          description=f" הצטרף לקיו{ctx.author.mention} ",
                                          color=discord.Color.red())
            player_joined.set_footer(text="בוט על ידי Quidy")
            player_joined.add_field(name=f"**שחקנים שכבר בקיו: {len(queue)}/{size * 2}**", value=f"{', '.join(queue)}")
            await ctx.send(embed=new_queue)
            return await ctx.send(embed=player_joined)
        if len(queue) < size * 2 - 1:
            queue.append(f"<@{ctx.author.id}>")
            player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                          description=f" הצטרף לקיו{ctx.author.mention} ",
                                          color=discord.Color.red())
            player_joined.add_field(name=f"**שחקנים שכבר בקיו: {len(queue)}/{size * 2}**", value=f"{', '.join(queue)}")
            player_joined.set_footer(text="בוט על ידי Quidy")
            await ctx.send(embed=player_joined)
        else:
            queue.append(f"<@{ctx.author.id}>")
            player_joined = discord.Embed(title="שחקן חדש הצטרף לקיו",
                                          description=f" הצטרף לקיו{ctx.author.mention} ",
                                          color=discord.Color.red())
            player_joined.set_footer(text="בוט על ידי Quidy")
            player_joined.add_field(name=f"**שחקנים שכרגע בקיו: {len(queue)}/{size * 2}**", value=f"{', '.join(queue)}")
            await ctx.send(embed=player_joined)
            team_1 = random.sample(queue, size)
            for i in team_1:
                queue.remove(i)
            teams = discord.Embed(title="קבוצה A", description=', '.join(team_1), inline=False,
                                  color=discord.Color.red())
            teams.add_field(name="קבוצה B", value=', '.join(queue), inline=False)
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
            for x in team_1:
                team_1.remove(x)
                y = x.replace("<@", "")
                y = y.replace(">", "")
                team_1.insert(-1, y)
            for x in queue:
                queue.remove(x)
                y = x.replace("<@", "")
                y = y.replace(">", "")
                queue.insert(-1, y)
            for user in channel.members:
                if str(user.id) in queue:
                    await user.remove_roles(role)
                    channel = client.get_channel(818145411633905694)
                    await user.move_to(channel)
                    await user.remove_roles(role)
                if str(user.id) in team_1:
                    await user.remove_roles(role)
                    channel = client.get_channel(818145622112731146)
                    await user.move_to(channel)
                    await user.remove_roles(role)
            queue.clear()


@client.command(aliases=['l'])
async def leave(ctx):
    if str(ctx.channel) == "pugs" or str(ctx.channel) == "fixing-bugs" or str(ctx.channel) == "bot-commands":
        if f"<@{ctx.author.id}>" in queue:
            queue.remove(f"<@{ctx.author.id}>")
            role = get(ctx.guild.roles, name="In Queue")
            await ctx.author.remove_roles(role)
            player_left = discord.Embed(title="שחקן יצא מהקיו",
                                        description=f"{ctx.author.mention} יצא מהקיו ",
                                        color=discord.Color.red())
            if len(queue) != 0:
                player_left.add_field(name=f"שחקנים שכרגע בקיו: **{len(queue)}/10**",
                                      value=f"{', '.join(queue)}")
                await ctx.send(embed=player_left)
            else:
                player_left.add_field(name=f"שחקנים שכרגע בקיו: **0/10**",
                                      value="אף אחד")
                await ctx.send(embed=player_left)
            player_left.set_footer(text="בוט על ידי Quidy")
        else:
            return await ctx.send("אתה לא בקיו!")


@client.command()
async def help(ctx):
    embed = discord.Embed(title="פקודות:",
                          description="++q -  בשביל להצטרף לקיו\n++l - בשביל לצאת מהקיו\n++teamsize משנה את מספר השחקנים בטים - מספר")
    embed.set_footer(text="בוט על ידי Quidy")
    await ctx.send(embed=embed)


@client.command()
async def status(ctx):
    global size
    if str(ctx.channel) == "pugs":
        embed = discord.Embed(title=f"{len(queue)}/{len(size * 2)}מספר שחקנים בקיו: ")
        embed.set_footer(text="בוט על ידי Quidy")
        await ctx.send(embed=embed)


@client.event
async def on_message(message):
    if message.content.lower.find("discord.gg"):
        await message.delete()
    client.proccess_command(message)
client.run("ODE4MTUwNTkwMTMwODE1MDE2.YET4HQ.HqPQubp23r2dXVBE7G-jG1979AU")
