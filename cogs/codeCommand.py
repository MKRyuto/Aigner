import discord
from discord.ext import commands, tasks
import bs4 as bs
import urllib.request
import filecmp
import os
import re
import datetime
import asyncio
import mechanicalsoup


class code(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.change_codePromotion.start()
        self.change_codeNews.start()
        self.change_codeEvent.start()

    cur_path = os.path.dirname(__file__)

    # Embed for Code Promotion
    async def do_change_codePromotion(self):
        await self.bot.wait_until_ready()
        # GET WEB
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/11-promotions.xml/').read()
        url_codePromotion = bs.BeautifulSoup(url, 'xml')
        url = urllib.request.urlopen(
            f'{url_codePromotion.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET TITLE
        title_codePromotion = url.find("meta",  property="og:title")
        # GET URL PAGE
        url_codePromotion = url.find("meta",  property="og:url")
        # GET BANNER
        banner_codePromotion = url.find('div', class_='ipsColumn')
        banner_codePromotion = banner_codePromotion.find('img')
        # GET PROFIL IMAGE and NAME
        profile_codePromotion = url.find('a', class_='ipsUserPhoto_small')
        profile_codePromotion = profile_codePromotion.find('img')
        # GET DESCRIPTION
        description_codePromotion = url.find(
            "meta",  property="og:description")
        # GET DATE
        date_codePromotion = url.find("meta",  property="og:updated_time")
        date_codePromotion = datetime.datetime.strptime(
            date_codePromotion['content'], '%Y-%m-%dT%H:%M:%SZ')

        # Embed
        server = []
        entries = os.listdir('server/')
        for entry in entries:
            server.append(entry)
        for data in server:
            with open(f'server/{data}') as f:
                y = f.read()
            x = y.split()
            id_guild = []
            for guild in self.bot.guilds:
                id_guild.append(str(guild.id))
            if any(f"{int(data[:-4])}" in s for s in id_guild):
                for channel in x:
                    embed = discord.Embed(
                        title=title_codePromotion["content"],
                        description=description_codePromotion["content"],
                        colour=discord.Colour(16707843),
                        url=url_codePromotion["content"]
                    )
                    embed.set_footer(
                        text=date_codePromotion.strftime('%d %B, %Y'))
                    embed.set_thumbnail(url=banner_codePromotion.get('src'))
                    embed.set_author(
                        name=profile_codePromotion.get("alt"), icon_url=profile_codePromotion.get("src"))
                    await self.bot.get_guild(int(data[:-4])).get_channel(int(channel)).send(embed=embed)
            else:
                os.remove(f'server/{data}')

    # Embed for Code News
    async def do_change_codeNews(self):
        await self.bot.wait_until_ready()
        # GET WEB SCRAPING
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/4-journals-broadcasts.xml/').read()
        url_updateCode = bs.BeautifulSoup(url, 'xml')

        url = urllib.request.urlopen(
            f'{url_updateCode.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET TITLE
        title_updateCode = url.find("meta",  property="og:title")
        # GET URL PAGE
        url_updateCode = url.find("meta",  property="og:url")
        # GET BANNER
        try:
            banner_updateCode = url.find('div', class_='ipsColumn')
            banner_updateCode = banner_updateCode.find_all('img')

            for i in range(len(banner_updateCode)):
                if banner_updateCode[i].get('src')[-3:] == "png" or banner_updateCode[i].get('src')[-3:] == "jpg" or banner_updateCode[i].get('src')[-4:] == "jpeg":
                    banner_updateCode = banner_updateCode[i].get('src')
                    break
        except AttributeError:
            banner_updateCode = None
        # GET PROFIL IMAGE AND NAME
        profile_updateCode = url.find('a', class_='ipsUserPhoto_small')
        profile_updateCode = profile_updateCode.find('img')
        # GET DESCRIPTION
        description_updateCode = url.find("meta",  property="og:description")
        # GET DATE
        date_updateCode = url.find("meta",  property="og:updated_time")
        date_updateCode = datetime.datetime.strptime(
            date_updateCode['content'], '%Y-%m-%dT%H:%M:%SZ')
        server = []
        entries = os.listdir('server/')
        for entry in entries:
            server.append(entry)
        for data in server:
            with open(f'server/{data}') as f:
                y = f.read()
            x = y.split()
            id_guild = []
            for guild in self.bot.guilds:
                id_guild.append(str(guild.id))
            if any(f"{int(data[:-4])}" in s for s in id_guild):
                for channel in x:
                    embed = discord.Embed(
                        title=title_updateCode["content"],
                        description=description_updateCode["content"],
                        colour=discord.Colour(16707843),
                        url=url_updateCode["content"]
                    )
                    embed.set_footer(
                        text=date_updateCode.strftime('%d %B, %Y'))
                    if banner_updateCode:
                        embed.set_thumbnail(url=banner_updateCode)
                    embed.set_author(
                        name=profile_updateCode.get("alt"), icon_url=profile_updateCode.get("src"))
                    await self.bot.get_guild(int(data[:-4])).get_channel(int(channel)).send(embed=embed)
            else:
                os.remove(f'server/{data}')

    # Embed for Code Event
    async def do_change_codeEvent(self):
        await self.bot.wait_until_ready()
        # GET LOGIN SESSIONS
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://codeclosers.to/forums/index.php?/login/")
        browser.select_form(
            'form[action="https://codeclosers.to/forums/index.php?/login/"]')
        browser["auth"] = "randiprawira23@gmail.com"
        browser["password"] = "sampit230599"
        browser.submit_selected()

        # GET URL EVENT LOG LATEST
        browser.open(
            "https://codeclosers.to/forums/index.php?/forum/47-event-log/")
        page = browser.get_current_page()
        data = page.find_all(class_="ipsDataItem_main")
        url = []
        time = []
        for d in data:
            d1 = d.find('a', href=True)
            url.append(d1['href'])
            d2 = d.find('time')
            time.append(d2['datetime'])
        time, url = zip(*sorted(zip(time, url), reverse=True))
        browser.open(f"{url[0]}")

        # Get Page Event Log Latest
        page = browser.get_current_page()

        # Get Title
        title = page.find("meta",  property="og:title")

        # Get URL
        url = page.find("meta",  property="og:url")

        # Get Banner
        try:
            banner = page.find('div', class_='ipsColumn')
            banner = banner.find_all('img')

            for i in range(len(banner)):
                if banner[i].get('src')[-3:] == "png" or banner[i].get('src')[-3:] == "jpg" or banner[i].get('src')[-4:] == "jpeg":
                    banner = banner[i].get('src')
                    break
        except AttributeError:
            banner = None

        # Get Profile Name and Image
        profile = page.find('a', class_='ipsUserPhoto_small')
        profile = profile.find('img')
        # Get Description
        description = page.find("meta",  property="og:description")
        # Get Datetime
        date = page.find("meta",  property="og:updated_time")
        date = datetime.datetime.strptime(
            date['content'], '%Y-%m-%dT%H:%M:%SZ')
        server = []
        entries = os.listdir('server/')
        for entry in entries:
            server.append(entry)
        for data in server:
            with open(f'server/{data}') as f:
                y = f.read()
            x = y.split()
            id_guild = []
            for guild in self.bot.guilds:
                id_guild.append(str(guild.id))
            if any(f"{int(data[:-4])}" in s for s in id_guild):
                for channel in x:
                    embed = discord.Embed(
                        title=title["content"],
                        description=description['content'],
                        colour=discord.Colour(16707843),
                        url=url["content"]
                    )
                    embed.set_footer(
                        text=date.strftime('%d %B, %Y'))
                    if banner:
                        embed.set_thumbnail(url=banner)
                    embed.set_author(
                        name=profile['alt'], icon_url=profile['src'])
                    await self.bot.get_guild(int(data[:-4])).get_channel(int(channel)).send(embed=embed)
            else:
                os.remove(f'server/{data}')

    # Latest Embed Promotion
    async def latest_codePromotion(self, ctx):
        # GET WEB SCRAPING
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/11-promotions.xml/').read()
        url_codePromotion = bs.BeautifulSoup(url, 'xml')

        url = urllib.request.urlopen(
            f'{url_codePromotion.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET TITLE
        title_codePromotion = url.find("meta",  property="og:title")
        # GET URL PAGE
        url_codePromotion = url.find("meta",  property="og:url")
        # GET BANNER
        banner_codePromotion = url.find('div', class_='ipsColumn')
        banner_codePromotion = banner_codePromotion.find('img')
        # GET PROFIL IMAGE and NAME
        profile_codePromotion = url.find('a', class_='ipsUserPhoto_small')
        profile_codePromotion = profile_codePromotion.find('img')
        # GET DESCRIPTION
        description_codePromotion = url.find(
            "meta",  property="og:description")
        # GET DATE
        date_codePromotion = url.find("meta",  property="og:updated_time")
        date_codePromotion = datetime.datetime.strptime(
            date_codePromotion['content'], '%Y-%m-%dT%H:%M:%SZ')
        embed = discord.Embed(
            title=title_codePromotion["content"],
            description=description_codePromotion["content"],
            colour=discord.Colour(16707843),
            url=url_codePromotion["content"]
        )
        embed.set_footer(
            text=date_codePromotion.strftime('%d %B, %Y'))
        embed.set_thumbnail(url=banner_codePromotion.get('src'))
        embed.set_author(
            name=profile_codePromotion.get("alt"), icon_url=profile_codePromotion.get("src"))
        await ctx.send(embed=embed)

    # Latest Embed News
    async def latest_codeNews(self, ctx):
        # GET WEB SCRAPING
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/4-journals-broadcasts.xml/').read()
        url_updateCode = bs.BeautifulSoup(url, 'xml')
        url = urllib.request.urlopen(
            f'{url_updateCode.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET TITLE
        title_updateCode = url.find("meta",  property="og:title")
        # GET URL PAGE
        url_updateCode = url.find("meta",  property="og:url")
        # GET BANNER
        try:
            banner_updateCode = url.find('div', class_='ipsColumn')
            banner_updateCode = banner_updateCode.find_all('img')

            for i in range(len(banner_updateCode)):
                if banner_updateCode[i].get('src')[-3:] == "png" or banner_updateCode[1].get('src')[-3:] == "jpg" or banner_updateCode[1].get('src')[-4:] == "jpeg":
                    banner_updateCode = banner_updateCode[i].get('src')
                    break
        except AttributeError:
            banner_updateCode = None
        # GET PROFIL IMAGE AND NAME
        profile_updateCode = url.find('a', class_='ipsUserPhoto_small')
        profile_updateCode = profile_updateCode.find('img')
        # GET DESCRIPTION
        description_updateCode = url.find("meta",  property="og:description")
        # GET DATE
        date_updateCode = url.find("meta",  property="og:updated_time")
        date_updateCode = datetime.datetime.strptime(
            date_updateCode['content'], '%Y-%m-%dT%H:%M:%SZ')
        embed = discord.Embed(
            title=title_updateCode["content"],
            description=description_updateCode["content"],
            colour=discord.Colour(16707843),
            url=url_updateCode["content"]
        )
        embed.set_footer(text=date_updateCode.strftime('%d %B, %Y'))
        if banner_updateCode:
            embed.set_thumbnail(url=banner_updateCode)
        embed.set_author(
            name=profile_updateCode.get("alt"), icon_url=profile_updateCode.get("src"))
        await ctx.send(embed=embed)

    # Latest Embed Event
    async def latest_codeEvent(self, ctx):
        # GET LOGIN SESSIONS
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://codeclosers.to/forums/index.php?/login/")
        browser.select_form(
            'form[action="https://codeclosers.to/forums/index.php?/login/"]')
        browser["auth"] = "randiprawira23@gmail.com"
        browser["password"] = "sampit230599"
        browser.submit_selected()

        # GET URL EVENT LOG LATEST
        browser.open(
            "https://codeclosers.to/forums/index.php?/forum/47-event-log/")
        page = browser.get_current_page()
        data = page.find_all(class_="ipsDataItem_main")
        url = []
        time = []
        for d in data:
            d1 = d.find('a', href=True)
            url.append(d1['href'])
            d2 = d.find('time')
            time.append(d2['datetime'])
        time, url = zip(*sorted(zip(time, url), reverse=True))
        browser.open(f"{url[0]}")

        # Get Page Event Log Latest
        page = browser.get_current_page()

        # Get Title
        title = page.find("meta",  property="og:title")

        # Get URL
        url = page.find("meta",  property="og:url")

        # Get Banner
        try:
            banner = page.find('div', class_='ipsColumn')
            banner = banner.find_all('img')

            for i in range(len(banner)):
                if banner[i].get('src')[-3:] == "png" or banner[i].get('src')[-3:] == "jpg" or banner[i].get('src')[-4:] == "jpeg":
                    banner = banner[i].get('src')
                    break
        except AttributeError:
            banner = None

        # Get Profile Name and Image
        profile = page.find('a', class_='ipsUserPhoto_small')
        profile = profile.find('img')
        # Get Description
        description = page.find("meta",  property="og:description")
        # Get Datetime
        date = page.find("meta",  property="og:updated_time")
        date = datetime.datetime.strptime(
            date['content'], '%Y-%m-%dT%H:%M:%SZ')
        embed = discord.Embed(
            title=title["content"],
            description=description["content"],
            colour=discord.Colour(16707843),
            url=url["content"]
        )
        embed.set_footer(text=date.strftime('%d %B, %Y'))
        if banner:
            embed.set_thumbnail(url=banner)
        embed.set_author(
            name=profile.get("alt"), icon_url=profile.get("src"))
        await ctx.send(embed=embed)

    async def promotionlog(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Promotion Log link you can click the button below. [```Click Here...```](https://codeclosers.to/forums/index.php?/forum/11-promotions/)")

        embed.set_thumbnail(
            url="https://codeclosers.to/forums/uploads/monthly_2017_01/logo.png.809598e84f548a4ce23f05fa333c3705.png")
        embed.set_author(
            name="Promotion Log", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    async def eventlog(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Event Log link you can click the button below. [```Click Here...```](https://codeclosers.to/forums/index.php?/forum/47-event-log/)")

        embed.set_thumbnail(
            url="https://codeclosers.to/forums/uploads/monthly_2017_01/logo.png.809598e84f548a4ce23f05fa333c3705.png")
        embed.set_author(
            name="Event Log", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    async def link(self, ctx):
        embed = discord.Embed(
            title='__Link__',
            description='Get a list of CODE:Closers related link.',
            colour=discord.Colour(16707843)
        )
        embed.set_author(name=f'{self.bot.user.name} Link',
                         icon_url=f'{self.bot.user.avatar_url}')
        embed.add_field(name='Syntax:', value='`sp!code game` : Get the official game link.\n`sp!code forum` : Get the game forum link.\n`sp!code discord` : Get the official discord link.', inline=False)
        embed.set_thumbnail(
            url=f'{self.bot.user.avatar_url}')
        embed.set_footer(text='AignerBot')
        await ctx.send(embed=embed)

    async def game(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Official Game link you can click the button below. [```Click Here...```](https://codeclosers.to/)")

        embed.set_thumbnail(
            url="https://codeclosers.to/forums/uploads/monthly_2017_01/logo.png.809598e84f548a4ce23f05fa333c3705.png")
        embed.set_author(
            name="Official Game Link", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    async def forum(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Official Forum link you can click the button below. [```Click Here...```](https://codeclosers.to/forums/)")

        embed.set_thumbnail(
            url="https://codeclosers.to/forums/uploads/monthly_2017_01/logo.png.809598e84f548a4ce23f05fa333c3705.png")
        embed.set_author(
            name="Official Forum Link", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    async def discord(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Official Discord link you can click the button below. [```Click Here...```](https://discord.gg/RBNypcK)")

        embed.set_thumbnail(
            url="https://codeclosers.to/forums/uploads/monthly_2017_01/logo.png.809598e84f548a4ce23f05fa333c3705.png")
        embed.set_author(
            name="Official Discord Link", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    async def inviteslur(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour(16707843),
            description="To get the Invite Bot link you can click the button below. [```Click Here...```](https://discordapp.com/api/oauth2/authorize?client_id=668091535836839957&permissions=388160&scope=bot)")

        embed.set_thumbnail(
            url=f"{self.bot.user.avatar_url}")
        embed.set_author(
            name="Invite Bot Link", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_footer(text="AignerBot")
        await ctx.send(embed=embed)

    # Looping the Code Promotion
    @tasks.loop(seconds=600)
    async def change_codePromotion(self):
        await self.bot.wait_until_ready()
        # GET WEB SCRAPING
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/11-promotions.xml/').read()
        url_codePromotion = bs.BeautifulSoup(url, 'xml')
        url = urllib.request.urlopen(
            f'{url_codePromotion.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET URL PAGE
        url_codePromotion = url.find("meta",  property="og:url")
        codePromotion_update = os.path.relpath(f'Aigner/url/codeClosers/promotion/update.txt', self.cur_path)
        codePromotion_updateLatest = os.path.relpath(f'Aigner/url/codeClosers/promotion/updateLatest.txt', self.cur_path)
        with open(codePromotion_update, "w") as file:
            file.write(url_codePromotion['content'])
        if filecmp.cmp(codePromotion_update, codePromotion_updateLatest) == False:
            with open(codePromotion_updateLatest, "w") as file:
                file.write(url_codePromotion['content'])
            try:
                await self.do_change_codePromotion()
            except Exception as error:
                print(error)

    # Looping the Code News
    @tasks.loop(seconds=540)
    async def change_codeNews(self):
        await self.bot.wait_until_ready()
        # GET WEB SCRAPING
        url = urllib.request.urlopen(
            'https://codeclosers.to/forums/index.php?/forum/4-journals-broadcasts.xml/').read()
        url_updateCode = bs.BeautifulSoup(url, 'xml')
        url = urllib.request.urlopen(
            f'{url_updateCode.item.link.text}').read()
        url = bs.BeautifulSoup(url, 'lxml')
        # GET URL PAGE
        url_updateCode = url.find("meta",  property="og:url")
        codeNews_update = os.path.relpath(f'Aigner/url/codeClosers/news/update.txt', self.cur_path)
        codeNews_updateLatest = os.path.relpath(f'Aigner/url/codeClosers/news/updateLatest.txt', self.cur_path)
        with open(codeNews_update, "w") as file:
            file.write(url_updateCode['content'])
        if filecmp.cmp(codeNews_update, codeNews_updateLatest) == False:
            with open(codeNews_updateLatest, "w") as file:
                file.write(url_updateCode['content'])
            try:
                await self.do_change_codeNews()
            except Exception as error:
                print(error)

    # Looping the Code News
    @tasks.loop(seconds=480)
    async def change_codeEvent(self):
        await self.bot.wait_until_ready()
        # GET LOGIN SESSIONS
        browser = mechanicalsoup.StatefulBrowser()
        browser.open("https://codeclosers.to/forums/index.php?/login/")
        browser.select_form(
            'form[action="https://codeclosers.to/forums/index.php?/login/"]')
        browser["auth"] = "randiprawira23@gmail.com"
        browser["password"] = "sampit230599"
        browser.submit_selected()

        # GET URL EVENT LOG LATEST
        browser.open(
            "https://codeclosers.to/forums/index.php?/forum/47-event-log/")
        page = browser.get_current_page()
        data = page.find_all(class_="ipsDataItem_main")
        url = []
        time = []
        for d in data:
            d1 = d.find('a', href=True)
            url.append(d1['href'])
            d2 = d.find('time')
            time.append(d2['datetime'])
        time, url = zip(*sorted(zip(time, url), reverse=True))
        codeEvent_update = os.path.relpath(f'Aigner/url/codeClosers/event/update.txt', self.cur_path)
        codeEvent_updateLatest = os.path.relpath(f'Aigner/url/codeClosers/event/updateLatest.txt', self.cur_path)
        with open(codeEvent_update, "w") as file:
            file.write(url[0])
        if filecmp.cmp(codeEvent_update, codeEvent_updateLatest) == False:
            with open(codeEvent_updateLatest, "w") as file:
                file.write(url[0])
            try:
                await self.do_change_codeEvent()
            except Exception as error:
                print(error)

    # Commends for Code Update
    @commands.command()
    async def code(self, ctx, arg):
        if arg == 'promotion' or arg == 'PROMOTION':
            await self.latest_codePromotion(ctx)
        elif arg == 'news' or arg == 'NEWS':
            await self.latest_codeNews(ctx)
        elif arg == 'event' or arg == 'EVENT':
            await self.latest_codeEvent(ctx)
        elif arg == 'promotionlog' or arg == 'PROMOTIONLOG':
            await self.promotionlog(ctx)
        elif arg == 'eventlog' or arg == 'EVENTLOG':
            await self.eventlog(ctx)
        elif arg == 'link' or arg == 'LINK':
            await self.link(ctx)
        elif arg == 'game' or arg == 'GAME':
            await self.game(ctx)
        elif arg == 'forum' or arg == 'FORUM':
            await self.forum(ctx)
        elif arg == 'discord' or arg == 'DISCORD':
            await self.discord(ctx)
        elif arg == 'inviteslur':
            await self.inviteslur(ctx)
        else:
            await ctx.send('Command invalid.')

    # Error Information
    @code.error
    async def clear_code_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send('Command invalid.')


def setup(bot):
    bot.add_cog(code(bot))
