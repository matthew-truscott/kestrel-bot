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
        with open(os.path.join(DATA_DIR, 'perms_cache.json'), 'r') as f:
            perms_cache = json.load(f)
        self._perms_cache = defaultdict(dict, perms_cache)
        self.ban_message = 'ban'
        self.softban_message = 'softban'

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def serverlist(self, ctx):
        chid = ctx.message.channel
        for server in self.bot.servers:
            await self.bot.send_message(chid, server.name)

    @commands.command(pass_context=True)
    @commands.has_role(god)
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
    @commands.has_role(god)
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
    @commands.has_role(god)
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
    @commands.has_role(god)
    async def embedtest(self, ctx):
        chid = ctx.message.channel
        em = discord.Embed(type='rich',
                           title='My Embed Title',
                           description='reg *ita* **__emph__** [link](http://www.google.com)',
                           colour=0x660480)
        em.set_author(name='Someone', icon_url=self.bot.user.default_avatar_url)
        em.set_footer(text='messing with footers')
        await self.bot.send_message(chid, embed=em)

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def codetest(self, ctx):
        chid = ctx.message.channel
        cm = '```test```'
        await self.bot.send_message(chid, cm)

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def welcomemessage(self, ctx):
        chid = ctx.message.channel
        cm = '''
            ```Markdown
Welcome to The Foundry!

To get started, please begin the following sorting process,
[1] https://goo.gl/forms/JF35YL5wBGbRta912
[2] https://goo.gl/forms/k75LCpCs61mUyumx2

The possible houses are Elaassar, Lowry, Scriabin, and Kishimoto.

After you are sorted you may join clubs, roles, and projects.
            ```
             '''
        await self.bot.send_message(chid, cm)

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def welcomelink1(self, ctx):
        chid = ctx.message.channel
        await self.bot.send_message(chid, 'https://goo.gl/forms/JF35YL5wBGbRta912')

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def welcomelink2(self, ctx):
        chid = ctx.message.channel
        await self.bot.send_message(chid, 'https://goo.gl/forms/k75LCpCs61mUyumx2')

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def ban(self, ctx, user: discord.Member, days: str = None, *,
                  reason: str = None):
        author = ctx.message.author
        server = author.server
        if days:
            if days.isdigit():
                days = int(days)
            else:
                if reason:
                    reason = days + ' ' + reason
                else:
                    reason = days
                days = 0
        else:
            days = 0

        if days < 0:
            days = 0

        if days > 7:
            days = 7

        try:
            await self.bot.ban(user, days)
            await self.bot.say(self.ban_message)
        except discord.errors.Forbidden:
            await self.bot.say("I'm not allowed to do that.")
        except Exception as e:
            print(e)

    @commands.command(pass_context=True)
    @commands.has_role(god)
    async def softban(self, ctx, user: discord.Member, *, reason: str = None):
        server = ctx.message.server
        channel = ctx.message.channel
        can_ban = channel.permissions_for(server.me).ban_members

        try:
            invite = await self.bot.create_invite(server, max_age=3600*24)
            invite = "\nInvite: " + invite
        except:
            invite = ""

        if can_ban:
            try:
                try:
                    msg = await self.bot.send_message(user, """
                    You have been banned and then unbanned as a quick way to delete
                    your messages.\n You can now join the server again.{}""".format(invite))
                except:
                    pass
                await self.bot.ban(user, 1)
                await self.bot.unban(user)
                await self.bot.say(self.softban_message)
            except discord.errors.Forbidden:
                await self.bot.say("My role is not high enough to softban that user.")
                await self.bot.delete_message(msg)
            except Exception as e:
                print(e)
        else:
            await self.bot.say("I'm not allowed to do that.")

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    @commands.has_role(god)
    async def mute(self, ctx, user: discord.Member, * reason: str = None):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.channel_mute, user=user, reason=reason)

    @commands.has_role(god)
    @mute.command(name="channel", pass_context=True, no_pm=True)
    async def channel_mute(self, ctx, user: discord.Member, *, reason: str = None):
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server
        overwrites = channel.overwrites_for(user)

        if overwrites.send_messages is False:
            await self.bot.say("That user can't send messages in this channel.")
            return
        self._perms_cache[user.id][channel.id] = overwrites.send_messages
        overwrites.send_messages = False
        try:
            await self.bot.edit_channel_permissions(channel, user, overwrites)
        except discord.Forbidden:
            await self.bot.say("Failed to mute user.")
        else:
            with open(os.path.join(DATA_DIR, 'perms_cache.json'), 'w+') as f:
                json.dump(self._perms_cache, f)
            await self.bot.say("User has been muted in this channel.")

    @commands.has_role(god)
    @mute.command(name="server", pass_context=True, no_pm=True)
    async def server_mute(self, ctx, user: discord.Member, *, reason: str = None):
        author = ctx.message.author
        server = ctx.message.server
        register = {}

        for channel in server.channels:
            if not channel.type == discord.ChannelType.text:
                continue
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages is False:
                continue
            register[channel.id] = overwrites.send_messages
            overwrites.send_messages = False
            try:
                await self.bot.edit_channel_permissions(channel, user, overwrites)
            except discord.Forbidden:
                await self.bot.say("Failed to mute user.")
                return
            else:
                await asyncio.sleep(0.1)
        if not register:
            await self.bot.say("That user is already muted in all channels.")
            return
        self._perms_cache[user.id] = register
        with open(os.path.join(DATA_DIR, 'perms_cache.json'), 'w+') as f:
            json.dump(self._perms_cache, f)
        await self.bot.say("User has been muted in this server.")

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    @commands.has_role(god)
    async def unmute(self, ctx, user: discord.Member, * reason: str = None):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.channel_unmute, user=user)

    @commands.has_role(god)
    @mute.command(name="channel", pass_context=True, no_pm=True)
    async def channel_mute(self, ctx, user: discord.Member):
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server
        overwrites = channel.overwrites_for(user)

        if overwrites.send_messages:
            await self.bot.say("That user does not seem to be muted in this channel.")
            return
        if user.id in self._perms_cache:
            old_value = self._perms_cache[user.id].get(channel.id)
        else:
            old_value = None
        overwrites.send_messages = old_value
        is_empty = self.are_overwrites_empty(overwrites)
        try:
            if not is_empty:
                await self.bot.edit_channel_permissions(channel, user, overwrites)
            else:
                await self.bot.delete_channel_permissions(channel, user)
        except discord.Forbidden:
            await self.bot.say("Failed to unmute user.")
        else:
            try:
                del self._perms_cache[user.id][channel.id]
            except KeyError:
                pass
            if user.id in self._perms_cache and not self._perms_cache[user.id]:
                del self._perms_cache[user.id] # cleanup
            with open(os.path.join(DATA_DIR, 'perms_cache.json'), 'w+') as f:
                json.dump(self._perms_cache, f)
            await self.bot.say("User has been unmuted.")

    @commands.has_role(god)
    @mute.command(name="server", pass_context=True, no_pm=True)
    async def server_mute(self, ctx, user: discord.Member, *, reason: str = None):
        author = ctx.message.author
        server = ctx.message.server

        if user.id not in self._perms_cache:
            await self.bot.say("That user doesn't seem to have been muted.")
        for channel in server.channels:
            if not channel.type == discord.ChannelType.text:
                continue
            if channel.id not in self._perms_cache[user.id].get(channel.id):
                continue
            value = self._perms_cache[user.id].get(channel.id)
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages = False:
                overwrites.send_messages = value
                is_empty = self.are_overwrites_empty(overwrites)
                try:
                    if not is_empty:
                        await self.bot.edit_channel_permissions(channel, user, overwrites)
                    else:
                        await self.bot.delete_channel_permissions(channel, user)
                except discord.Forbidden:
                    await self.bot.say("Failed to unmute user")
                    return
                else:
                    del self._perms_cache[user.id][channel.id]
                    await asyncio.sleep(0.1)
        if user.id in self._perms_cacheand not self._perms_cache[user.id]:
            del self._perms_cache[user.id] # cleanup
        with open(os.path.join(DATA_DIR, 'perms_cache.json'), 'w+') as f:
            json.dump(self._perms_cache, f)
        await self.bot.say("User has been unmuted in this server.")

def setup(bot):
    bot.add_cog(ModCog(bot))
