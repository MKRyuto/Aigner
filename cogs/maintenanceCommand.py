from discord.ext import commands
import discord
import platform
import os


class maintenanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cur_path = os.path.dirname(__file__)

    async def on(self, ctx):
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
                        title=f'{self.bot.get_emoji(670596720161456138)} **INFORMATION MAINTENANCE**',
                        description='The bot will perform maintenance so that the bot will be shut down during maintenance. Sorry for the intrusion and thank you.',
                        colour=discord.Colour(16707843),
                    )
                    embed.set_thumbnail(
                        url=f'{self.bot.user.avatar_url}')
                    await self.bot.get_guild(int(data[:-4])).get_channel(int(channel)).send(embed=embed)

    async def off(self, ctx):
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
                        title=f'{self.bot.get_emoji(670596720161456138)} **INFORMATION MAINTENANCE**',
                        description='Thank you for your patience. The maintanance has finished, the bot can be used normally again.',
                        colour=discord.Colour(16707843),
                    )
                    embed.set_thumbnail(
                        url=f'{self.bot.user.avatar_url}')
                    await self.bot.get_guild(int(data[:-4])).get_channel(int(channel)).send(embed=embed)

    # Maintenance Command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    # @commands.has_any_role('Admin')
    async def maintenance(self, ctx, arg):
        if arg == 'on' or arg == 'ON':
            await self.on(ctx)
        elif arg == 'off' or arg == 'OFF':
            await self.off(ctx)
        else:
            return await ctx.send('Command invalid.')

    @maintenance.error
    async def clear_maintenance_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send('Command invalid.')

    @maintenance.error
    async def clear_missing_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(
                colour=discord.Colour(16707843)
            )
            embed.set_author(name=f'{self.bot.user.name} help',
                             icon_url=f'{self.bot.user.avatar_url}')
            embed.add_field(name='Information:',
                            value='Only Role with Manager Message can use this command.', inline=False)
            embed.set_footer(
                text='AignerBot')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(maintenanceCommand(bot))
