from discord.ext import commands
import discord
import platform


class aboutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # About Command
    @commands.command(pass_context=True)
    async def about(self, ctx):
        embed = discord.Embed(
            title=f'About {self.bot.user.name} {self.bot.get_emoji(664014152913780736)}',
            description='Bot Discord for Game __Code:Closers__ using Discord.py',
            colour=discord.Colour(16707843)
        )
        embed.set_thumbnail(
            url=f'{self.bot.user.avatar_url}')
        embed.set_author(name='About Page',
                         icon_url=f'{self.bot.user.avatar_url}')
        embed.add_field(name=f'{self.bot.get_emoji(670332871617019912)} GitHub:',
                        value='[MKRyuto](https://github.com/MKRyuto/)')
        embed.add_field(name=f'{self.bot.get_emoji(664017956128292865)} Python:',
                        value=f'{platform.python_version()}')
        embed.add_field(name=f'{self.bot.get_emoji(664017888193019914)} discord.py:',
                        value=f'{discord.__version__}')

        embed.add_field(name=f'{self.bot.get_emoji(670332871512162305)} Created by',
                        value='MKRyuto#5445')
        embed.add_field(name=f'{self.bot.get_emoji(670332871633797160)} Server count:',
                        value=f'{str(len(self.bot.guilds))}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(aboutCommand(bot))
