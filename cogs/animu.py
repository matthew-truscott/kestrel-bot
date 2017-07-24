import discord
from discord.ext import commands
import os
import sys
import urllib.request
import random

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'cogs/images')
GLOMP_DIR = os.path.join(IMAGE_DIR, 'glomp')


class AnimuCog(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def glomp(self, ctx, person: str):
        chid = ctx.message.channel
        print(ctx.message.channel.id)
        imagesum = len([name for name in os.listdir('.') if os.path.isfile(name)])
        print(imagesum)
        imagenumber = random.randint(1, imagesum)
        imagepath = str(imagenumber) + '.gif'
        path = os.path.join(GLOMP_DIR, imagepath)
        print(path)
        message = ctx.message.author.name + ' glomps ' + person
        await self.bot.send_message(chid, message)
        with open(path, 'rb') as f:
            await self.bot.send_file(chid, f)


def setup(bot):
    bot.add_cog(AnimuCog(bot))


if __name__ == '__main__':
    imc = EditCog("rq")
    imc.hyperize("http://i.imgur.com/NYwSoYp.jpg")
