from discord.ext import commands
import discord
import os
import sys
import cogs.background as cg

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class ReportCog(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    async def report(self, ctx, user: discord.Member, *, reason: str = None):
        message = ctx.message
        if message.server is None and not message.author == self.bot.user:
            pass

    @commands.command(hidden=True, pass_context=True)
    async def ping(self, ctx):
        message = ctx.message
        if message.server is None and not message.author == self.bot.user:
            try:
                self.bot.loop.create_task(cg.time(self.bot))
            except Exception as e:
                print(repr(e))

def setup(bot):
    bot.add_cog(ReportCog(bot))
