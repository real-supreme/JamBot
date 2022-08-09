from discord import cog, commands
from discord import Option
from logger import log
from Utils.metautils import send

class Basic(cog.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hi")
    async def hey(self, ctx):
        # expensive
        # out
        print("hi")
        await send(ctx, "Hello!")
            
def setup(bot):
    bot.add_cog(Basic(bot))
    log.debug("Basic Cog Loaded")
    print("Basic Cog Loaded")
    return Basic(bot)