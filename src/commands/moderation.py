from Database.interactions import DB
from discord import Cog, commands
from logger import log
from Utils.metautils import *

class Moderation(Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_banned_words")
    async def add_banned_words(self, ctx, *, words: list):
        guild_id = ctx.guild.id
        for word in words:
            word = word.lower()
        try:
            DB.add_banned_words(guild_id, words)
            await send(ctx, f"Added banned words: {words}")
        except Exception:
            await send(ctx, "Error adding banned words")
        
            
    @commands.command(name="remove_banned_words")
    async def remove_banned_words(self, ctx, *, word):
        guild_id = ctx.guild.id
        word = word.lower()
        if DB.check_banned_words(guild_id, word):
            try:
                DB.remove_banned_words(guild_id, word)
                await send(ctx, f"Removed banned words: {word}")
            except Exception:
                await send(ctx, "Error removing banned words")
        else:
            await send(ctx, "Word not found")
        
    @commands.command(name="banned_words")
    async def banned_words(self, ctx):
        # view banned words
        guild_id = ctx.guild.id
        try:
            DB.get_all_banned_words(guild_id)
            await send(ctx, f"Banned words: {DB.get_all_banned_words(guild_id)}")
        except Exception:
            await send(ctx, "Error getting banned words")
        
    #@commands.command(name="fancy_profile")
    #async def fancy_profile(self, ctx):
    #    # do something fancy with the pfp
    #    try:
    #        ctx.respond("Hello!")
    #    except:
    #        ctx.reply("Hello!")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
    log.debug("Moderation Cog Loaded")
    return Moderation(bot)
