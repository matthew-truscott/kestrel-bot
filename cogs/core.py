from discord.ext import commands
import os
import sys
import json
import cogs.utils.sortinghat as ush

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class CoreCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.houselist = {
            1: 'House Elaassar',
            2: 'House Scriabin',
            3: 'House Kishimoto',
            4: 'House Lowry'
        }
        self.main_server = '374223751132479492'

        with open(os.path.join(DATA_DIR, 'userbase.json'), 'r+') as f:
            self.users = json.load(f)

    @commands.command(hidden=True, pass_context=True)
    async def quit(self, ctx):
        print("quit...")
        if (ctx.message.author.id in self.users and "dev" in self.users[ctx.message.author.id] and
                self.users[ctx.message.author.id]["dev"]):
            sys.exit()
        else:
            print(ctx.message.author.id, "executed command without permission")

    @commands.command(hidden=True, pass_context=True)
    async def hi(self, ctx):
        await self.bot.send_message(ctx.message.channel, 'hi')

    def get_member_from_user(self, user, server):
        return server.get_member(user.id)

    @commands.command(hidden=True, pass_context=True)
    async def sort(self, ctx):
        message = ctx.message
        if message.server is None and not message.author == self.bot.user:
            # read message
            print("sorting...")
            with open(os.path.join(DATA_DIR, 'userbase.json'), 'r+') as f:
                data = json.load(f)

                if message.author.id in data:
                    user = data[message.author.id]
                    if "house" in user and user["house"] is not None:
                        await self.bot.send_message(message.author, "It appears you have already been sorted. A role will be given according to system information.")
                        m = self.get_member_from_user(message.author, self.bot.get_server(self.main_server))
                        rolelist = self.bot.get_server(self.main_server).roles
                        for role in rolelist:
                            if role.name == user["house"]:
                                # assign
                                await self.bot.add_roles(m, role)
                            elif role.name in self.houselist.values():
                                # house already assigned, something is wrong, just remove house
                                await self.bot.remove_roles(m, role)
                    else:
                        fullname = message.author.name + "#" + str(message.author.discriminator)
                        house = ush.get_house(fullname)
                        strhouse = self.houselist[house]
                        print(fullname, 'sorted into', strhouse)
                        data[message.author.id]["house"] = strhouse
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                        # now actually allocate
                        await self.bot.send_message(message.author, "Congraulations! You have been sorted into %s." % (strhouse))
                        m = self.get_member_from_user(message.author, self.bot.get_server(self.main_server))
                        rolelist = self.bot.get_server(self.main_server).roles
                        for role in rolelist:
                            if role.name == strhouse:
                                # assign
                                await self.bot.add_roles(m, role)
                            elif role.name in self.houselist.values():
                                # house already assigned, something is wrong, just remove house
                                await self.bot.remove_roles(m, role)

                else:
                    await self.bot.send_message(message.author, "It seems like you are not in the system. Contact Akharis#1903"
                    "for help regarding this issue.")




def setup(bot):
    bot.add_cog(CoreCog(bot))
