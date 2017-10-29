from discord.ext import commands
import discord
import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class ModCog(object):
    def __init__(self, bot):
        self.bot = bot
        with open(os.path.join(DATA_DIR, 'userbase.json'), 'r') as f:
            self.userbase = json.load(f)

    @commands.command(pass_context=True)
    async def serverlist(self, ctx):
        chid = ctx.message.channel
        for server in self.bot.servers:
            await self.bot.send_message(chid, server.name)

    @commands.command(pass_context=True)
    async def memberlist(self, ctx):
        chid = ctx.message.channel
        desc = ""
        for member in self.bot.get_all_members():
            if ctx.message.server == member.server:
                desc += ("%s\n" % (member.name))
        em = discord.Embed(title='Member list',
                           description=desc,
                           colour=0xB15555)
        await self.bot.send_message(chid, embed=em)

    @commands.command(pass_context=True)
    async def update_members(self, ctx):
        for member in self.bot.get_all_members():
            if ctx.message.server == member.server:
                userExists = False
                for key, value in self.userbase.items():
                    if key == member.id:
                        self.userbase[member.id]["alive"] = True
                        userExists = True
                if not userExists:
                    # add user data
                    self.userbase[member.id] = {
                        "name": member.name,
                        "isbot": member.bot,
                        "avatar": member.avatar_url,
                        "created": member.created_at.strftime("%Y, %B %d"),
                        "display name": member.display_name,
                        "joined at": member.joined_at.strftime("%Y, %B %d"),
                        "alive": True
                    }
        # write
        with open(os.path.join(DATA_DIR, 'userbase.json'), 'w') as f:
            f.seek(0)
            json.dump(self.userbase, f, indent=4)
            f.truncate()


    @commands.command(pass_context=True)
    async def clean_members(self, ctx):
        for key, value in self.userbase.items():
            userExists = False
            for member in self.bot.get_all_members():
                if key == member.id:
                    userExists = True
            if not userExists:
                self.userbase[member.id]["alive"] = False
        # write
        with open(os.path.join(DATA_DIR, 'userbase.json'), 'w') as f:
            f.seek(0)
            json.dump(self.userbase, f, indent=4)
            f.truncate()



    @commands.command(pass_context=True)
    async def embedtest(self, ctx):
        chid = ctx.message.channel
        em = discord.Embed(type='rich',
                           title='My Embed Title',
                           description='reg *ita* **__emph__** [link](http://www.google.com)',
                           colour=0x660480)
        em.set_author(name='Someone', icon_url=self.bot.user.default_avatar_url)
        em.set_footer(text='messing with footers')
        await self.bot.send_message(chid, embed=em)


def setup(bot):
    bot.add_cog(ModCog(bot))
