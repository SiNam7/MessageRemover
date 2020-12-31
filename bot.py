import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class Bot(commands.Bot):
    def __init__(self, command_prefix='!', **options):
        super().__init__(command_prefix, **options)
        self.isActivated = False


bot = Bot()


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to the server {guild.name}(id: {guild.id})')
    bot.isActivated = False
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='Chilling')
    )


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong!')


@bot.command(name='active')
async def activate(ctx):
    if not bot.isActivated:
        bot.isActivated = True
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name='Watching messages')
        )
        await ctx.send("Activated!")
    else:
        await ctx.send("Already activated!")


@bot.command(name='inactive')
async def inactivate(ctx):
    if bot.isActivated:
        bot.isActivated = False
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name='Chilling')
        )
        await ctx.send("Inactivated!")
    else:
        await ctx.send("Already inactivated!")

@bot.event
async def on_message(msg):
    if not bot.isActivated:
        return
    else:
        if msg.Guild.get_channel() ==

bot.run(TOKEN)
