from discord.ext import commands
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

class ModCog(object):
    def __init__(self, bot):
        self.bot = bot

    @commands

def setup(bot):
    bot.add_cog(ModCog(bot))
