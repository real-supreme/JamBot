from discord import Cog, commands
from discord import Option
from logger import log

class Moderation(Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_banned_words")
    async def add_banned_words(self, ctx):
        # expensive
        # out
        try:
            ctx.respond("Hello!")
        except:
            ctx.reply("Hello!")
            
    @commands.command(name="remove_banned_words")
    async def remove_banned_words(self, ctx):
        # remove banned words from db
        try:
            ctx.respond("Hello!")
        except:
            ctx.reply("Hello!")
        
    @commands.command(name="banned_words")
    async def banned_words(self, ctx):
        # view banned words
        try:
            ctx.respond("Hello!")
        except:
            ctx.reply("Hello!")
        
    @commands.command(name="fancy_profile")
    async def fancy_profile(self, ctx):
        # do something fancy with the pfp
        try:
            ctx.respond("Hello!")
        except:
            ctx.reply("Hello!")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
    log.debug("Moderation Cog Loaded")
    return Moderation(bot)