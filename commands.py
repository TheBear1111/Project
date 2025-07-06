import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import random
from lists import quotes, cheese_images  # Assuming you defined these

# === Keep-alive web server ===
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

# === Discord Bot Setup ===
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('❌ TOKEN NOT FOUND')
    exit(1)
else:
    print('✅ TOKEN LOADED')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='bear ', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return
    await before.channel.send(
        f'{before.author} edited a message.\nBefore: {before.content}\nAfter: {after.content}'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if str(message.channel) == 'images' and message.content != '':
        await message.channel.purge(limit=1)
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != 1100978913406091356:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if not member:
        print("❗ Member not found. Make sure you enabled 'Server Members Intent' in the dev portal.")
        return

    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, name='Verified')
        if role:
            await member.add_roles(role)
            channel = bot.get_channel(971605704421036065)
            if channel:
                await channel.send(f"<@{member.id}> has fallen into this eternal void...")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != 1100978913406091356:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if not member:
        return

    if payload.emoji.name == '👍':
        role = discord.utils.get(guild.roles, name='Verified')
        if role:
            await member.remove_roles(role)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Bear Commands',
        description="These are my powers!\nI'm so POWERFUL!",
        color=discord.Colour.dark_red()
    )
    bear_image = 'https://cdn.discordapp.com/attachments/1101663143727464468/1101950291903004835/Bear_image.jpg'
    embed.set_thumbnail(url=bear_image)
    embed.add_field(name='bear help', value='Lists my commands, and portrays my utter strength!', inline=False)
    embed.add_field(name='bear info', value="This isn't self-explanatory.", inline=False)
    embed.add_field(name='bear quote', value="Ya know, I can give some pretty good advice...", inline=False)
    embed.add_field(name='bear cheese', value="I will show you my collection of cheeses.", inline=False)
    embed.add_field(name='bear purge', value="I will rampage the channel, but only for those whom are worthy.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)

@bot.command()
async def quote(ctx, arg1=1):
    try:
        runs = int(arg1)
    except ValueError:
        await ctx.send("Please enter a number.")
        return

    for i in range(runs):
        Quote = random.choice(quotes)
        await ctx.send(f"{i + 1}. {Quote}")

@bot.command()
async def cheese(ctx):
    cheese_image = random.choice(cheese_images)
    await ctx.send(cheese_image)

@bot.command()
async def purge(ctx, amount=1):
    if ctx.author.id == senorratboi:  # Replace with your actual Discord user ID
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("You are not worthy. >_>")

bot.run(TOKEN)
