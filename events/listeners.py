import discord
from discord import cog, commands


class Listeners(cog.Cog, name='Listeners'):
    """Listeners cog"""

    def __init__(self, client):
        self.client = client
        self.current_XP = 0 #TODO remove (temporary while waiting for DB)
        self.current_LVL = 1  #TODO remove


    # ---------------------------------------Events ----------------------------------------------------

    @cog.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Contains XP logic for levelling system"""
        """2 base XP per message, +1 XP per 20 char"""
        """Level up at every 100 XP"""
        if message.channel.type != discord.ChannelType.private and not message.author.bot:

            XP_gained = 2 + (len(message.content) // 20)
            #print(f'{message.author.name} gained {XP_gained} XP!')

            #TODO : add to current XP in DB
            self.current_XP = self.current_XP + XP_gained

            #TODO : get current XP from DB
            #TODO : get current LVL from DB

            # Level attained
            if self.current_XP >= (self.current_LVL * 100 + 100):


                print(f'{str(message.author)} wrote to the bot (Message: {message.content}')

                embed = discord.Embed(title=f'{message.author.name} leveled up! :star: {self.current_LVL}',
                                      description='Congratulations, you leveled up!')
                embed.set_thumbnail(url=f'{message.author.display_avatar}')
                #channel = await self.client.fetch_channel(channels["bot_logs_channelID"]) #TODO: fetch log channel
                await message.channel.send(embed=embed) #TODO: set to log channel



def setup(client):
    client.add_cog(Listeners(client))
