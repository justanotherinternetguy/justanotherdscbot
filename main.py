# NOTE TO SELF: DO NOT UPLOAD THE DISCORD BOT TOKEN
import random
import discord
import os
from dotenv import load_dotenv
import requests
import json
import asyncio
import time
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

description = "justanotherdscbot testing..."
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~', description=description, intents=intents)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@bot.event
async def on_ready():
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("_____________")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'welcome this kid --> {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_message_edit(before, after):
    await ctx.send('**{0.author}** got sniped:\n{0.content} -> {1.content}'.format(before, after))

@bot.event
async def on_message_delete(message):
    await message.channel.send('**{0.author}** has deleted: {0.content}'.format(message))


@bot.command()
async def ping(ctx):
    await ctx.send('Hello {}'.format(ctx.author.mention))

@bot.command()
async def HELP(ctx):
    await ctx.send("""
                justanotherdscbot help:
Prefix is ~
**COMMANDS**:
    `HELP`: show this message
    `howlarge`: how large is your mother?
    `guess`: guessing game
    `quote`: random quote

**PASSIVE**:
    bot will automatically display before/after on edited msgs
    bot will automatically display deleted msgs          
            """)

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('+'))
    except Exception:
        await ctx.send('{} - Format must be in `<# of dice>+<# of faces per die>`'.format(ctx.author.mention))
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def joininfo(ctx, member: discord.Member):
    await ctx.send('{0.name}, `{0.id}` joined in {0.joined_at}'.format(member))

@bot.command()
async def getquote(ctx):
    quote = get_quote()
    await ctx.reply(quote, mention_author=True)

@bot.command()
async def howlarge(ctx):
    size = random.randint(1000, 99999)
    await ctx.reply('your mom is {} pounds large'.format(size), mention_author=True)

bot.run(DISCORD_TOKEN)
