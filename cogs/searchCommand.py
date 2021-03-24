import time
import os
import discord
from discord.ext import commands
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-sh-usage')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
class searchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def search(self, ctx, *, player=""):
            if player == "" or "#" not in player:
                return await ctx.send("שימוש לא נכון בפקודה! שימוש נכון: שחקן search++")
            web = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options = chrome_options)
            web.get("https://tracker.gg/valorant")
            web.find_element_by_tag_name("input").send_keys(player)
            time.sleep(1)
            players = web.find_element_by_class_name("players")
            try:
                players.find_element_by_class_name("player-row").click()
            except NoSuchElementException:
                return await ctx.send("משתמש זה לא קיים או שלא מחובר לhttps://tracker.gg/valorant בדוק שנית אם כתבת ללא שגיאות.")
            name, discriminator = player.split("#")
            web.get(f"https://tracker.gg/valorant/profile/riot/{name}%23{discriminator}/overview?playlist=competitive")
            rank = web.find_element_by_class_name("valorant-highlighted-stat__value").text()
            name = web.find_element_by_class_name("trn-ign__username").text
            discriminator = web.find_element_by_class_name("trn-ign__discriminator").text
            KAD = web.find_elements_by_class_name("valorant-highlighted-stat__value")
            KAD = KAD[1].text
            stats = discord.Embed(title="שם:", description=name + discriminator,color=discord.Color.red())
            stats.add_field(name="ראנק:", value=rank)
            stats.add_field(name="KAD:", value=KAD)
            avatar = web.find_element_by_tag_name("image")
            avatar_url = avatar.get_attribute("href")
            stats.set_thumbnail(url=avatar_url)
            await ctx.send(embed=stats)
            web.close()

def setup(bot):
    bot.add_cog(searchCommand(bot))
