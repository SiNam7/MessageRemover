import asyncio
import os

import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ROLE = os.getenv('DISCORD_ROLE')


class Bot(commands.Bot):
    def __init__(self, command_prefix='!', **options):
        super().__init__(command_prefix, **options)
        self.isActivated = False
        self.deleteDelay = 30  # unit: sec


bot = Bot()


@bot.check
async def check_perm(ctx: discord.ext.commands.Context):
    isAdmin = ctx.channel.permissions_for(ctx.author) and 8 == 8  # check Administrator permission
    hasRole = ROLE in [role.name for role in ctx.author.roles]
    return isAdmin or hasRole


@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, )

    if isinstance(error, ignored):
        return

    if isinstance(error, CheckFailure):
        await ctx.send("You don't have required permissions!")
        return


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


@bot.command(name='purge')
async def purge(ctx, amount=50):
    await ctx.send(
        f'This operation will delete **{amount}** non-pinned message(s) above in this channel, **{ctx.channel.name}**.'
        f'\nTo continue this operation, type "confirm" in 30 seconds.'
    )
    try:
        msg = await bot.wait_for("message", timeout=30,
                                 check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)

        if msg.content == 'confirm':
            deleted = await ctx.channel.purge(limit=amount+3,  # amount + (command, info msg, 'confirm')
                                              check=lambda m: not m.pinned)
            await ctx.send(f'Deleted {max(0, len(deleted)-3)} non-pinned message(s).', delete_after=bot.deleteDelay)
        else:
            await ctx.send('Purge cancelled.')

    except asyncio.TimeoutError:
        await ctx.send("Purge operation timed out (30s).")


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


@bot.command(name='delay')
async def setDelay(ctx: discord.ext.commands.Context, time: int):
    bot.deleteDelay = time
    await ctx.send("Message remove delay has been set to: " + str(time) + " second(s)")


@bot.event
async def on_message(msg: discord.Message):
    await bot.process_commands(msg)
    if not bot.isActivated:
        return
    else:
        if msg.channel.name == 'music':
            await msg.delete(delay=bot.deleteDelay)
        else:
            return

bot.run(TOKEN)
