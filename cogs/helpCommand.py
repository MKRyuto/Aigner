from discord.ext import commands
import discord


class helpCommmand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Help Commands
    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title='	__Command starts with [sp!]__',
            description='I am specialized at finding UNION\'s intel. Please use these commands for me to assist you.\n\nUse `sp!help <command>` for some help about a specific command.',
            colour=discord.Colour(16770416)
        )
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.set_author(name='Help Page',
                         icon_url=f'{self.bot.user.avatar_url}')
        embed.add_field(name=f'{self.bot.get_emoji(669228689455841280)} __Code:Closers__',
                        value='`sp!code news` : Get latest news information.\n`sp!code promotion` : Get latest gacha preview information.\n`sp!code event` : Get latest staff event information.\n`sp!code promotionlog` : Get link to the gacha preview log.\n`sp!code eventlog` : Get link to the event log.\n`sp!code link` : Get a list of CODE:Closers related link.', inline=False)
        embed.add_field(name=f'{self.bot.get_emoji(670338765675298818)} __Active/Deactive__',
                        value='`sp!update on` : Enabling latest update on the current channel.\n`sp!update off` : Disabling latest update on the current channel.\n`sp!update list` : Get a list of active update on this server.', inline=False)
        embed.add_field(name=f'{self.bot.get_emoji(670596720161456138)} __About__',
                        value='`sp!about` : Sends general informations about me!', inline=False)
        embed.set_footer(text='AignerBot')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(helpCommmand(bot))
