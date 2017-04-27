from cogs.utils import m_brain as br
from discord.ext import commands
from cogs import nlp_definition as nd

class Comprehend(object):
    def __init__(self, bot):
        self.bot = bot

    def process(self, sarg):
        """
        first make sure kess understands everything, she doesn't understand the
        concept of a question either at t=0 so how does she ask what things
        mean? Just repeat words back.
        """
        slist = sarg.split(" ")
        for word in slist:
            if nd.search_dict(word)[0] == 0

    @commands.command(hidden=True)
    async def reply(self, sarg):
        await self.bot.say(self.process(sarg))

def setup(bot):
    bot.add_cog(MarkovNet(bot))

if __name__ == '__main__':
    comp = Comprehend(test)
