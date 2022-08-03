from discord import Cog, commands
from discord import Option
from logger import log

class Basic(Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hi")
    async def hey(self, ctx):
        # expensive
        # out
        try:
            ctx.respond("Hello!")
        except:
            ctx.reply("Hello!")
            
def setup(bot):
    bot.add_cog(Basic(bot))
    log.debug("Basic Cog Loaded")
    return Basic(bot)