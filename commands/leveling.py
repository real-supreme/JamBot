import discord
from discord import cog, commands
from operator import itemgetter


class Leveling(cog.Cog, name='Leveling'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, member: discord.Member):
        """Get the user's rank"""
        embed = discord.Embed(title=f':trophy: {member.name}\'s rank')
        embed.set_thumbnail(url=f'{member.display_avatar}')
        embed.add_field(name="XP", value='XX', inline=True) #TODO: get current_XP from DB
        embed.add_field(name="Level", value='XX', inline=True)  # TODO: get current_LVL from DB
        embed.add_field(name="XP to next level", value='XX', inline=True) # TODO: value= (current_LVL * 100 + 100) - current_XP
        await ctx.respond(embed=embed)


    @commands.command()
    async def leaderboard(self, ctx):
        """See the current leaderboard"""
        #TODO: iterate over BD, order according to current_XP
        #example
        users = [{"name": 'Lia', "current_xp": 125},
                  {"name": 'Supy', "current_xp": 412},
                  {"name": 'Tri', "current_xp": 322}]
        users_sorted = sorted(users, key=itemgetter('current_xp'), reverse=True)

        desc = ''
        position = 1
        for user in users_sorted:
            desc += f'{position} :star: {user["name"]} - {user["current_xp"]} XP\n'
            position += 1

        embed = discord.Embed(title=f'Leaderboard for {ctx.guild.name}', description=desc)
        embed.set_thumbnail(url=f'{ctx.guild.icon.url if ctx.guild.icon else "https://logos-world.net/discord-logo/"}')
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Leveling(bot))
    print("Leveling Cog Loaded")
    return Leveling(bot)