import time
import os
import discord
from discord.ext import commands
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
web = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options = chrome_options)

class searchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def search(self, ctx, *, player=""):
        if player == "" or "#" not in player:
            return await ctx.send("שימוש לא נכון בפקודה! שימוש נכון: שחקן search++\nלדוגמא: search Q B O S T#GHOST++")
        await ctx.send("מחפש...")
        web.get("https://tracker.gg/valorant")
        web.find_element_by_tag_name("input").send_keys(player)
        time.sleep(1)
        try:
            name = web.find_element_by_class_name("trn-ign__username").text
            descriminator = web.find_element_by_class_name("trn-ign__discriminator").text
            web.get(
                f"https://tracker.gg/valorant/profile/riot/{name}%23{descriminator.replace('#', '')}/overview?playlist=competitive")
        except NoSuchElementException:
            return await ctx.send(
                "משתמש זה לא קיים או שלא מחובר לhttps://tracker.gg/valorant בדוק שנית אם כתבת ללא שגיאות.")
        stats_on_page = web.find_elements_by_class_name("valorant-highlighted-stat__value")
        try:
            rank = stats_on_page[0].text
            KAD = stats_on_page[1].text
        except IndexError:
            return await ctx.send(
                "משתמש זה לא קיים או שלא מחובר לhttps://tracker.gg/valorant בדוק שנית אם כתבת ללא שגיאות.")
        stats = discord.Embed(title="שם:", description=name + descriminator, color=discord.Color.red())
        main_char = web.find_element_by_class_name("agent__name").text
        stats.add_field(name="מיין:", value=main_char)
        stats.add_field(name="ראנק:", value=rank, inline=False)
        stats.add_field(name="KAD:", value=KAD, inline=False)
        main_gun = web.find_element_by_class_name("weapon__info")
        main_gun_image = main_gun.find_element_by_tag_name("img").get_attribute("src")
        main_gun_text = main_gun.find_element_by_class_name("weapon__name").text
        stats.add_field(name="נשק אהוב:", value=main_gun_text)
        avatar = web.find_element_by_tag_name("image")
        avatar_url = avatar.get_attribute("href")
        stats.set_thumbnail(url=avatar_url)
        stats.set_image(url=main_gun_image)
        await ctx.send(embed=stats) 
    @commands.command()
    async def spam(ctx, count: int, member:discord.Member, *, message: str):
        if ctx.author.id == 551107475798229010:
            for i in range(count):
                await member.send(message)
def setup(bot):
    bot.add_cog(searchCommand(bot))
