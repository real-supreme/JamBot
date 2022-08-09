import asyncio
import random
from Utils.Games import Games as Game
from discord import cog, commands, Embed, File
from discord.ext.commands import Cooldown,BucketType, CooldownMapping
from discord import Option
from logger import log
from Utils.metautils import send
import requests
from PIL import Image

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
        
    @commands.slash_command(name="Horoscope".lower(),cooldown=cooldown_)
    async def horoscope(self, ctx, zodiac: Option(str, "Select the zodiac you'd like a horoscope for.",choices=['aries','taurus','gemini','cancer','leo','virgo','libra','scoprio','sagittarius','capricorn','aquarius','pisces'])):
        params = (
                ('sign', zodiac),
                ('day','today'),
            )
        response = requests.post('https://aztro.sameerkumar.website/', params=params)
        em = Embed(title="**Daily Horoscope** - " + str(response.json()['current_date']), description="**Compatibility**: "+response.json()['compatibility']+"\n**Lucky Time**: "+response.json()['lucky_time']+"\n**Lucky Number**: "+response.json()['lucky_number']+"\n**Color**: "+response.json()['color']+"\n**Mood**: "+response.json()['mood']+"\n\n*"+response.json()['description']+"*", color=0x00ff00)
        await send(ctx,embed=em)
        
    @commands.slash_command(name="Tarot".lower(),cooldown=cooldown_)
    async def tarot(self, ctx):
        cards = ["Fool", "Magician", "High Priestess","Empress","Emperor","Hierophant","Lovers","Chariot","Strength","Hermit","Wheel of Fortune","Justice","Hanged Man","Death", "Temperance","Devil","Tower","The Star","The Moon","The Sun","Judgement","World",
            "Ace of Cups","Two of Cups","Three of Cups","Four of Cups","Five of Cups","Six of Cups","Seven of Cups","Eight of Cups","Nine of Cups","Ten of Cups","Page of Cups","Knight of Cups","Queen of Cups","King of Cups",
            "Ace of Swords","Two of Swords","Three of Swords","Four of Swords","Five of Swords","Six of Swords","Seven of Swords","Eight of Swords","Nine of Swords","Ten of Swords","Page of Swords","Knight of Swords","Queen of Swords","King of Swords",
            "Ace of Pentacles","Two of Pentacles","Three of Pentacles","Four of Pentacles","Five of Pentacles","Six of Pentacles","Seven of Pentacles","Eight of Pentacles","Nine of Pentacles","Ten of Pentacles","Page of Pentacles","Knight of Pentacles","Queen of Pentacles","King of Pentacles",
            "Ace of Wands","Two of Wands","Three of Wands","Four of Wands","Five of Wands","Six of Wands","Seven of Wands","Eight of Wands","Nine of Wands","Ten of Wands","Page of Wands","Knight of Wands","Queen of Wands","King of Wands",
            ]
        upright = ["Innocence, new beginnings, free spirit", "Willpower, desire, creation, manifestation","Intuitive, unconscious, inner voice","Motherhood, fertility, nature","Authority, structure, control, fatherhood","Tradition, conformity, morality, ethics","Partnerships, duality, union","Direction, control, willpower","Inner strength, bravery, compassion, focus","Contemplation, search for truth, inner guidance","Change, cycles, inevitable fate","Cause and effect, clarity, truth","Sacrifice, release, martyrdom","End of cycle, beginnings, change, metamorphosis","Middle path, patience, finding meaning","Addiction, materialism, playfulness","Sudden upheaval, broken pride, disaster","Hope, faith, rejuvenation","Unconscious, illusions, intuition","Joy, success, celebration, positivity","Reflection, reckoning, awakening","Fulfillment, harmony, completion",
            "New feelings, spirituality, intuition","Unity, partnership, connection","Friendship, community, happiness","Apathy, contemplation, disconnectedness","Loss, grief, self-pity","Familiarity, happy memories, healing","Searching for purpose, choices, daydreaming","Walking away, disillusionment, leaving behind","Satisfaction, emotional stability, luxury","Inner happiness, fulfillment, dreams coming true","Charity, generosity, sharing","Following the heart, idealist, romantic","Compassion, calm, comfort","Compassion, control, balance",
            "Breakthrough, clarity, sharp mind","Difficult choices, indecision, stalemate","Heartbreak, suffering, grief","Rest, restoration, contemplation","Unbridled ambition, win at all costs, sneakiness","Transition, leaving behind, moving on","Deception trickery, tactics and strategy","Imprisonment, entrapment, self-victimization","Anxiety, hopelessness, trauma","Failure, collapse, defeat","Curiosity, restlessness, mental energy","Action, impulsiveness, defending beliefs","Complexity, perceptiveness, clear mindedness","Head over heart, discipline, truth",
            "Opportunity, prosperity, new venture","Balancing decisions, priorities, adapting to change","Teamwork, collaboration, building","Conservation, frugality, security","Need, poverty, insecurity","Charity, generosity, sharing","Hard work, perseverance, diligence","Apprenticeship, passion, high standards","Fruits of labor, rewards, luxury","Legacy, culmination, inheritance","Ambition, desire, diligence","Efficiency, hard work, responsibility",'Practicality, creature comforts, financial security',"Abundance, prosperity, security",
            "Creation, willpower, inspiration, desire","Planning, making decisions, leaving home","Looking ahead, expansion, rapid growth","Community, home, celebration","Competition, rivalry, conflict","Victory, success, public reward","Perseverance, defensive, maintaining control","Rapid action, movement, quick decisions","Resilience, grit, last stand","Accomplishment, responsibility, burden","Exploration, excitement, freedom","Action, adventure, fearlessness","Courage, determination, joy","Big picture, leader, overcoming challenges"]
        reversed = ["Recklessness, taken advantage of, inconsideration", "Trickery, illusions, out of touch","Lack of center, lost inner voice, repressed feelings","Dependence, smothering, emptiness, nosiness","Tyranny, rigidity, coldness","Rebellion, subversiveness, new approaches","Loss of balance, one-sidedness, disharmony","Lack of control, lack of direction, aggression","Self doubt, weakness, insecurity","Loneliness, isolation, lost your way","No control, clinging to control, bad luck","Dishonesty, unaccountability, unfairness","Stalling, needless sacrifice, fear of sacrifice","Fear of change, holding on, stagnation, decay","Extremes, excess, lack of balance","Freedom, release, restoring control","Disaster avoided, delayed disaster, fear of suffering","Faithlessness, discouragement, insecurity","Confusion, fear, misinterpretation","Negativity, depression, sadness","Lack of self awareness, doubt, self loathing","Incompletion, no closure",
            "Emotional loss, blocked creativity, emptiness","Imbalance, broken communication, tension","Overindulgence, gossip, isolation","Sudden awareness, choosing happiness, acceptance","Acceptance, moving on, finding peace","Moving forward, leaving home, independence","Lack of purpose, diversion, confusion","Avoidance, fear of change, fear of loss","Lack of inner joy, smugness, dissatisfaction","Shattered dreams, broken family, domestic disharmony","Strings attached, stinginess, power and domination","Moodiness, disappointment","Martyrdom, insecurity, dependence","Coldness, moodiness, bad advice",
            "Confusion, brutality, chaos","Lesser of two evils, no right choice, confusion","Recovery, forgiveness, moving on","Restlessness, burnout, stress","Lingering resentment, desire to reconcile","Emotional baggage, unresolved issues, resisting transition","Coming clean, rethinking approach","Self acceptance, new perspective, freedom","Hope, reaching out, despair","Can't get worse, only upwards, inevitable end","Deception, manipulation, all talk","No direction, disregard for consequences, unpredictability","Cold hearted, cruel, bitterness","Manipulative, cruel, weakness",
            "Lost opportunity, missed chance, bad investment","Loss of balance, disorganized, overwhelmed","Lack of teamwork, disorganized, group conflict","Greediness, stinginess, possessiveness","Recovery, charity, improvement","Strings attached, stinginess, power and domination","Work without results, distractions, lack of rewards","Lack of passion, uninspired, no motivation","Reckless spending, living beyond means, false success","Fleeting success, lack of stability, lack of resources","Lack of commitment, greediness, laziness","Laziness, obsessiveness, work without reward","Self-centeredness, jealousy, smothering","Greed, indulgence, sensuality",
            "Lack of energy, lack of passion, boredom","Fear of change, playing safe, bad planning","Obstacles, delays, frustration","Lack of support, transience, home conflicts","Avoiding conflict, respecting differences","Excess pride, lack of recognition, punishment","Give up, destroyed confidence, overwhelmed","Panic, waiting, slowdown","Exhaustion, fatigue, questioning motivations","Inability to delegate, overstressed, burnt out","Direction, procrastination, creating conflict","Anger, impulsiveness, recklessness","Selfishness, jealousy, insecurities","Impulsive, overbearing, unachievable expectations"]
        orientation = [0,1]
        card = random.choice(cards)
        cardindex = cards.index(card)
        if random.choice(orientation) == 0:
            # Return embed with the name of the card, reversed or upright, the description, and the image.
            em = Embed(title=card, description=upright[cardindex], color=0xD4A91E)
            image = card.replace(" ", "_").lower() + ".jpg"
            file = File("tarot/"+image, filename=image)
            em.set_image(url="attachment://" + image)
        else:
            em = Embed(title=card+" (R)", description=reversed[cardindex], color=0x9111CD)
            imgfilepath = "tarot/"+ card.replace(" ", "_").lower()+".jpg"
            flimgfilepath = "tarot/"+ card.replace(" ", "_").lower()+"_reversed.jpg"
            image = Image.open(imgfilepath)
            flimage = image.transpose(Image.FLIP_TOP_BOTTOM)
            flimage.save(flimgfilepath)
            image = card.replace(" ", "_").lower() + "_reversed.jpg"
            file = File("tarot/"+image, filename=image)
            em.set_image(url="attachment://" + image)
        await send(ctx,embed=em, file=file)
    
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