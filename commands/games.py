import asyncio
from Utils.Games import Games as Game
from discord import cog, commands, Embed
from discord.ext.commands import Cooldown,BucketType, CooldownMapping
from discord import Option
from logger import log
from Utils.metautils import send
import random

cooldown_ = CooldownMapping(Cooldown(1,5),BucketType.channel)
_cooldown = CooldownMapping(Cooldown(1,12),BucketType.user)

class Games(cog.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gamesAPI = Game()
        
    @commands.slash_command(name="Truth_or_Dare".lower(),cooldown=cooldown_)
    async def tord(self, ctx, choice: Option(str, "Truth or Dare?",choices=['truth','dare'])):
        if choice == 'truth':
            q = await self.gamesAPI.get_truth()
        else:
            q = await self.gamesAPI.get_dare()
        em = Embed(title=choice.capitalize(), description="Q: "+q, color=0x00ff00)
        await send(ctx,embed=em)
    
    @commands.slash_command(name="Would_you_rather".lower(),cooldown=cooldown_)
    async def wyr(self, ctx):
        q = await self.gamesAPI.get_wyr()
        em = Embed(title="Would you rather", description="Q: "+q, color=0x00ff00)
        await send(ctx,embed=em)
        
    @commands.slash_command(name="Never_have_I_ever".lower(),cooldown=cooldown_)
    async def nhie(self, ctx):
        q = await self.gamesAPI.get_nhie()
        em = Embed(title="Never have I ever", description="Q: "+q, color=0x00ff00)
        await send(ctx,embed=em)
        
    @commands.slash_command(name="Paranoia".lower(),cooldown=cooldown_)
    async def paranoia(self, ctx):
        q = await self.gamesAPI.get_paranoia()
        em = Embed(title="Paranoia", description="Q: "+q, color=0x00ff00)
        await send(ctx,embed=em)
    
    @commands.slash_command(name='trivia',cooldown=_cooldown)
    async def trivia(self, ctx):
        qjs = await self.gamesAPI.get_trivia()
        q = qjs['question']
        em = Embed(title="Trivia", description=f"`Q: ` **{q}**", color=0x00ff00)
        em.set_author(name=f"{qjs['category']} | {qjs['difficulty'].capitalize()}")
        if qjs['type'] == 'multiple':
            ca = qjs['correct_answer']
            ops = qjs['incorrect_answers']+[ca]
            random.shuffle(ops)
            em.add_field(name="Choices", value=">>> "+"\n".join(ops), inline=False)
        else:
            em.add_footer(text="True or False?")
        m = await send(ctx,embed=em)
        
        def check(m):
            return m.content==ca and m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=12.0)
        except asyncio.TimeoutError:
            em.clear_fields()
        else:
            if msg.content == ca:
                await msg.add_reaction('✅')
        finally:
            em.set_footer(text='Correct Answer: '+ca)
            await send(ctx,embed=em)
        
    
def setup(bot):
    bot.add_cog(Games(bot))
    log.debug("Games Cog Loaded")
    print("Games Cog Loaded")
    return Games(bot)