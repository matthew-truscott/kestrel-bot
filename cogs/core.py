from discord.ext import commands
import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class CoreCog(object):
    def __init__(self, bot):
        self.bot = bot

        with open(os.path.join(DATA_DIR, 'userbase.json'), 'r+') as f:
            self.users = json.load(f)

    @commands.command(hidden=True, pass_context=True)
    async def quit(self, ctx):
        if (ctx.message.author.id in self.users and "dev" in self.users[ctx.message.author.id] and
                self.users[ctx.message.author.id]["dev"]):
            sys.exit()
        else:
            print(ctx.message.author.id, "executed command without permission")

def setup(bot):
    bot.add_cog(CoreCog(bot))
