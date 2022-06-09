# NOTE TO SELF: DO NOT UPLOAD THE DISCORD BOT TOKEN

# TODO:
# Moderation (mute + kick + ban)
# Music bot
# Reaction roles?
# Air quality heh

import random
import discord
import os
import re
from dotenv import load_dotenv
import requests
import json
import asyncio
import time
from discord.ext import commands, tasks
import functools
import itertools
from discord.utils import get

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
description="justanotherdscbot: MADE BY justanotherinternetguy#6982"
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~', intents=intents)

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
    print(discord.__version__)
    print("_____________")

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'welcome this kid --> {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_message_edit(before, after):
    fmt = '**{0.author}** got sniped:\n{0.content} -> {1.content}'
    await before.channel.send(fmt.format(before, after))

@bot.event
async def on_message_delete(message):
    await message.channel.send('**{0.author}** has deleted: {0.content}'.format(message))


@bot.command()
async def ping(ctx):
    """Pong!"""
    await ctx.reply('Hello {}'.format(ctx.author.mention))

@bot.command()
async def roll(ctx, dice: str):
    """Roll NdN dice"""
    try:
        rolls, limit = map(int, dice.split('+'))
    except Exception:
        await ctx.reply('{} - Format must be in `<# of dice>+<# of faces per die>`'.format(ctx.author.mention))
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.reply(result)


@bot.command()
async def joininfo(ctx, member: discord.Member):
    """Get the join information of a user"""
    await ctx.send('{0.name}, `{0.id}` joined in {0.joined_at}'.format(member))

@bot.command()
async def inspire(ctx):
    """Get an inspirational quote"""
    quote = get_quote()
    await ctx.reply(quote, mention_author=True)

@bot.command()
async def howlarge(ctx):
    """how large is it?"""
    size = random.randint(1000, 99999)
    await ctx.reply('your mom is {} pounds large'.format(size), mention_author=True)


@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, reason=None):
    """Bans a user"""
    if member.id == ctx.author.id:
        await ctx.reply("You can't ban yourself!")
        return;
    if reason == None:
        await ctx.reply(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        messageok = f"You have been **banned** from {ctx.guild.name} for {reason}"
        to_send = '{0.mention}, {1} has been **banned**!'.format(member, member.id)
        await ctx.reply(to_send)
        await member.send(messageok)
        await member.ban(reason=reason)


@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    """Unbans a user"""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(f'Unbanned {user.mention}')


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, reason=None):
    """Kicks a user"""
    if member.id == ctx.author.id:
        await ctx.reply("You can't kick yourself!")
        return;
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        messageok = f"You have been **kicked** from {ctx.guild.name} for {reason}"
        to_send = '{0.mention} has been **kicked**!'.format(member)
        await ctx.reply(to_send)
        await member.send(messageok)
        await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(administrator=True)
async def create_role(ctx, name, r, g, b, permissions):
	"""Creates a custom role

	Creates a custom roles with RGB colors and custom permissions

	USE https://discordapi.com/permissions.html to calculate permission value

	"""
	guild = ctx.guild
	await guild.create_role(name=name, color=discord.Color.from_rgb(int(r), int(g), int(b)), permissions=discord.Permissions(permissions=int(permissions)))
	await ctx.reply("Role {} created!".format(name))


@bot.command()
@commands.has_permissions(administrator=True)
async def add_role(ctx, name, member : discord.Member):
	"""Assign a premade role to a user"""
	role = discord.utils.get(ctx.guild.roles, name=name)
	await member.add_roles(role)
	await ctx.reply("Role {} added to {}".format(name, member))


@bot.command()
@commands.has_permissions(administrator=True)
async def rm_role(ctx, name, member : discord.Member):
	"""Remove a role from a user"""
	role = discord.utils.get(ctx.guild.roles, name=name)
	await member.remove_roles(role)
	await ctx.reply("Role {} removed from {}".format(name, member))


@bot.command()
@commands.has_permissions(administrator=True)
async def delete_role(ctx, name):
	"""Delete a role from the server"""
	role = discord.utils.get(ctx.message.guild.roles, name=name)
	await role.delete()
	await ctx.reply ("Role {} deleted!".format(name))

# await ctx.channel.purge(limit = 1)
@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, count):
	"""Purge messages from chat"""
	await ctx.channel.purge(limit = int(count))


bot.run(DISCORD_TOKEN)
