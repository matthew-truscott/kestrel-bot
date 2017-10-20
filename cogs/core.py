from discord.ext import commands
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class CoreCog(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def quit(self):
        bot.logout()

def setup(bot):
    bot.add_cog(CoreCog(bot))
