# Module and Library
import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
from webserver import keep_alive
import os

# Prefix
client = commands.Bot(command_prefix='sp!',
                      case_insensitive=True, help_command=None)

# Status Playing in Discord
status = ['Seha', 'Seulbi', 'Yuri', 'J', 'Misteltein', 'Nata', 'Levia', 'Harpy',
          'Tina', 'Violet', 'Wolfgang', 'Luna', 'Soma', 'Bai', 'Seth', 'Mirae', 'Kim']
status = status[:]
random.shuffle(status)
status = cycle(status)

# Notifikasi Bot Online
@client.event
async def on_ready():
    change_status.start()
    print('Aigner is Online.')

# Looping Status
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status) + ' | sp!help'))

# Load Extensions
extensions = ['cogs.helpCommand', 'cogs.aboutCommand',
              'cogs.activeCommand', 'cogs.maintenanceCommand','cogs.codeCommand']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

# Invalid Command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return await ctx.send('Command invalid.')
    raise error

# Token Bot
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)