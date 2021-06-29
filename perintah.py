import discord
import time
import os
import json
import random
import re
from discord.ext import commands
from dotenv import load_dotenv


class Perintah(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}. A DM has been sent to you, please check'.format(member))
            message = 'Mekanisme Pelatihan: https://komin.fo/mekanisme-pro-pyt2 \nDaftar Pembagian Kelas Peserta: https://komin.fo/ProA-PYT \nPatuhi peraturan di <#855769020070232104> \nLangkah pertama: pilih channel Kelas di <#856153338550550568>'
            await member.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        await channel.send('Dear {0.mention}. Sad to say goodbye'.format(member))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id != '854007172949868624':
            return
        if reaction.emoji == ':python:':
            role = discord.utils.get(user.server.roles, id='855828863861915649')
            await bot.add_roles(user, role)

    @commands.command(name='hello')
    async def hello_world(self, ctx: commands.Context):
        await ctx.send('Hello!!')

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send('Pinging...')
        end_time = time.time()
        await message.edit(
            content=f'Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms')

    @commands.command(name='setstatus')
    async def setstatus(self, ctx: commands.Context, *, text: str):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

    @commands.command(name='tebak')
    async def tebak(self, ctx: commands.Context, *, question):
        responses = ['Probably', 'I would not be so sure about that.',
                     'My answer is no.', 'Probably not', 'Of course!', 'Why not?',
                     'My answer is yes.', 'This is true, and it will stay like that.',
                     'Not even in a million years.', 'I mean, I do not see the point in saying no.',
                     'Why this question? The answer is a definitive no.',
                     'As my grandma used to say... no.',
                     'As my great great grandfather used to say... what even is this question?',
                     'I do not know.', 'Sources say no.']
        await ctx.send(f'Question: {question}\nAnswer:{random.choice(responses)}')

    @commands.command(name='tanya')
    async def tanya(self, ctx: commands.Context, *, text: str):
        await ctx.send('Checking answer please stand by.')
        if os.path.exists('Answer.txt'):
            with open('Answer.txt', 'r') as f:
                searching = re.compile(r'\b({0})\b'.format(text), flags=re.IGNORECASE).search
                line = True
                while line:
                    line = f.readline()
                    if not line:
                        break
                    if searching(line):
                        await ctx.send(line)
                        return
            await ctx.send('Sorry, we\'ll figure it out')

    @commands.command(name='clear')
    async def clear(ctx, amount=None):
        if amount is None:
            await ctx.channel.purge(limit=5)
        elif amount == "all":
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=int(amount))


def setup(bot: commands.Bot):
    bot.add_cog(Perintah(bot))
