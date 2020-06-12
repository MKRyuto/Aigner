from discord.ext import commands
import discord
import platform
import os


class activeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cur_path = os.path.dirname(__file__)
    # Update Command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    # @commands.has_any_role('Admin')
    async def update(self, ctx, arg):
        server = os.path.relpath(f'Aigner/server/{ctx.guild.id}.txt', self.cur_path)
        if arg == 'on' or arg == 'ON':
            open(server, 'a').close()
            if f'{ctx.channel.id}' in open(server).read():
                return await ctx.send('Announcement Updates have been added on this Channel.')
            else:
                with open(server, 'a') as f:
                    f.write(f'{ctx.channel.id}' + '\n')
                return await ctx.send('Announcement Updates will be announced on this Channel.')
        elif arg == 'off' or arg == 'OFF':
            open(server, 'a').close()
            if f'{ctx.channel.id}' in open(server).read():
                with open(server) as f:
                    data = f.read()
                x = data.split()
                x.remove(f'{ctx.channel.id}')
                open(server, 'w').close()
                for delete in x:
                    with open(server, 'a') as f:
                        f.write(str(delete) + '\n')
                return await ctx.send('Update Announcement has been deleted on this Channel.')
            else:
                return await ctx.send('Announcement Updates have not been added on this Channel.')

        elif arg == 'list' or arg == 'LIST':
            open(server, 'a').close()
            with open(server) as f:
                data = f.read()
            x = data.split()
            embed = discord.Embed(
                title=f'{self.bot.get_emoji(670596720161456138)} **List Channel**',
                description='Channel that gets __updated__',
                colour=discord.Colour(16707843),
            )
            if x is not None:
                for data in x:
                    embed.add_field(
                        name=f'__**{self.bot.get_channel(int(data))}**__', value=f'ID : `{data}`', inline=False)
            if not x:
                embed.add_field(name='__**NONE**__',
                                value='Channel has not been added.', inline=False)
            embed.set_thumbnail(
                url=f'{self.bot.user.avatar_url}')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='__Active/Deactive__',
                colour=discord.Colour(16707843)
            )
            embed.set_author(name=f'{self.bot.user.name} help',
                             icon_url=f'{self.bot.user.avatar_url}')
            embed.add_field(name='Syntax:',
                            value='`sp!update on` : Enabling latest update on the current channel.\n`sp!update off` : Disabling latest update on the current channel.\n`sp!update list` : Get a list of active update on this server.', inline=False)
            embed.set_footer(
                text='AignerBot')
            await ctx.send(embed=embed)

    @update.error
    async def clear_update_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(
                title='__Active/Deactive__',
                colour=discord.Colour(16707843)
            )
            embed.set_author(name=f'{self.bot.user.name} help',
                             icon_url=f'{self.bot.user.avatar_url}')
            embed.add_field(name='Syntax:',
                            value='`sp!update on` : Enabling latest update on the current channel.\n`sp!update off` : Disabling latest update on the current channel.\n`sp!update list` : Get a list of active update on this server.', inline=False)
            embed.set_footer(
                text='AignerBot')
            await ctx.send(embed=embed)

    @update.error
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
    bot.add_cog(activeCommand(bot))
