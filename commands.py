
from discord.ext import commands
from lists import *
import discord
import random
from dotenv import load_dotenv as dot
import os

dot()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_message_id = 1100978913406091356


    async def on_ready(self):
        print('Online')


    async def on_raw_reaction_add(self, payload):
        """
        Give a role based on a reaction emoji
        """

        if payload.message_id != self.target_message_id:
            return
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)


        if payload.emoji.name == '👍':
            role = discord.utils.get(guild.roles, name='Verified')
            await payload.member.add_roles(role)
            channel = MyClient.get_channel(self, 971605704421036065)
            await channel.send(f"<@{member.id}> has fallen into this eternal void...")


    async def on_raw_reaction_remove(self, payload):
        """
        remove a role based on a reaction emoji
        """

        if payload.message_id != self.target_message_id:
            return
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print(member)

        if payload.emoji.name == '👍':
            role = discord.utils.get(guild.roles, name='Verified')
            await member.remove_roles(role)


bot = commands.Bot(command_prefix='bear ', intents=intents)
bot.remove_command('help')
client = MyClient(intents=intents)

@bot.event
async def on_ready():
    print('Bot is online')


@bot.event
async def on_message_edit(before, after):
    await before.channel.send(
        f'{before.author} edited a message. \n'
        f'Before: {before.content} \n'
        f'After: {after.content} >_>')


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Bear Commands',
        description="These are my powers!\nI'm so POWERFUL!",
        color=discord.Colour.dark_red()
    )
    bear_image = 'https://cdn.discordapp.com/attachments/1101663143727464468/1101950291903004835/Bear_image.jpg'
    embed.set_thumbnail(url=bear_image)
    embed.add_field(
        name='bear help',
        value='Lists my commands, and portrays my utter strength!',
        inline=False
    )
    embed.add_field(
        name='bear info',
        value="This isn't self-explanatory.",
        inline=False
    )
    embed.add_field(
        name='bear quote',
        value="Ya know, I can give some pretty good advice... ",
        inline=False
    )
    embed.add_field(
        name='bear cheese',
        value="I will show you my collection of cheeses.",
        inline=False
    )
    embed.add_field(
        name='bear purge',
        value="I will rampage the channel, but only for those whom are worthy.",
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):

    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)


@bot.command()
async def quote(ctx, arg1=1):
    print('quote')
    runs = int(arg1)
    for i in range(runs):
        Quote = random.choice(quotes)
        await ctx.send(f"{i + 1}.{Quote}")

@bot.command()
async def cheese(ctx):
    cheese_image = random.choice(cheese_images)
    await ctx.send(cheese_image)


@bot.command()
async def purge(ctx, amount=1):
    if str(ctx.author) == 'Señor Rat Boi#5481':
        await ctx.channel.purge(limit=amount)
    else:
        await  ctx.channel.send('You are not worthy.>_>')


@bot.event
async def on_ready():
    print('Bot is online')


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return
    else:
        await before.channel.send(
            f'{before.author} edited a message. \n'
            f'Before: {before.content} \n'
            f'After: {after.content} >_>'
        )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if str(message.channel) == 'images' and message.content != '':
        await message.channel.purge(limit=1)



bot.run(TOKEN)

client.run(TOKEN)
