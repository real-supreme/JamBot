import traceback
from Database.interactions import DB
from discord import Cog, commands, Option
from logger import log
from Utils.metautils import *

class Moderation(Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_banned_words")
    async def add_banned_words(self, ctx, *, words: Option(str, "Enter a list of words separated by spaces"), punishment: Option(str, "Enter a punishment for the set of words entered (ex: Mute, Kick, Ban)")):
        guild_id = ctx.guild.id
        words = words.lower().split(" ")
        try:
            # connect to db
            conn = DB()
            await conn.add_banned_word(guild_id, words, punishment)
            await conn.close()
            await send(ctx, f"Added banned words: {words}")
        except Exception:
            try:
                with open("data.txt", "a") as f:
                    f.write("\n" + str(guild_id) + "," + " ".join(words) + "," + punishment)
                await send(ctx, f"Added banned words: {words}")
            except Exception as e:
                traceback.print_exc()
                await send(ctx, "Error adding banned words")
        
            
    @commands.command(name="remove_banned_words")
    async def remove_banned_words(self, ctx, *, word):
        guild_id = ctx.guild.id
        word = word.lower()
        try:
            # connect to db
            conn = DB()
            await conn.remove_banned_word(guild_id, word)
            await conn.close()
            await send(ctx, f"Removed banned words: {word}")
        except Exception:
            try:
                lst = []
                with open("data.txt", "r") as f:
                    # go over all the lines in the file and remove the word from the line if the guildid matches
                    for line in f:
                        if line != "" and guild_id not in line:
                            lst.append(line)
                        elif guild_id in line:
                            for w in word:
                                if word in line:
                                    line = line.replace(word, "")
                            lst.append(line)
                with open("data.txt", "w") as f:
                    for line in lst:
                        f.write(line)      
                await send(ctx, f"Removed banned words: {word}")
            except Exception as e:
                traceback.print_exc()
                await send(ctx, "Error removing banned words")
        
    @commands.command(name="banned_words")
    async def banned_words(self, ctx):
        guild_id = ctx.guild.id
        try:
            conn = DB()
            words = await conn.get_all_banned_words(guild_id)
            await conn.close()
            await send(ctx, f"Banned words: {words}")
        except Exception:
            try:
                lst = []
                with open("data.txt", "r") as f:
                    # if the guildid is in the line, add the line to the list
                    for line in f:
                        if str(guild_id) in line:
                            # ignore the first word in the line (the guildid)
                            lst.append(line.split(",")[1:])
                await send(ctx, f"Banned words and their punishments: {lst}")
            except Exception as e:
                traceback.print_exc()
                await send(ctx, "Error getting banned words")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
    log.debug("Moderation Cog Loaded")
    return Moderation(bot)
