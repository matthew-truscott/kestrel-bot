from discord.ext import commands
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')


class ChatCog(object):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(CoreCog(bot))
