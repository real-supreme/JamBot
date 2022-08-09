import discord
import config
from discord.ext import tasks
import os, traceback, random
from logger import log
 
CONNECT = False
        
class JamDotBot(discord.bot.Bot):
    def __init__(self, *args, **options):
        super().__init__(description=config.bot_description,*args, **options)
        for folder in ["events", "commands"]:
            for ext in os.listdir(folder):
                if ext.endswith(".py"):
                    print(f"Loading {ext}")
                    try:
                        print(self.load_extension(f"{folder}.{ext[:-3]}"))
                    except Exception:
                        print(f"Failed to load {ext}\n",traceback.extract_tb())
                        log.error(f"Failed to load extension {ext}.\n")
                        traceback.print_exc()
        
    def run(self, *args, **kwargs):
        try:
            ex = super().run(*args, **kwargs)
        except:
            if len(args)>0 and args[0] is not None:
                args[0]=args[0][::-1]
            else:
                args=(os.getenv('BOT_TOKEN'),)
            ex = super().run(*args, **kwargs)
        return ex
    
    async def on_connect(self):
        if not CONNECT:
            log.info("Connected to Discord.")
        
    async def on_ready(self):
        global CONNECT
        CONNECT = True
        activity = discord.Game(name="with your Time", type=3)
        await self.change_presence(activity=activity)
        print(f"Bot is logged in as {self.user} [ID: {self.user.id}]")
        try:
            guilds = [g for g in self.guilds]
            print(f"Bot is in {len(guilds)} guilds:")
            for g in guilds:
                print(f"\t{g}")
        except discord.errors:
            pass
        except Exception as e:
            log.exception("Failed to get guilds info on_ready:: {}".format(e))
        self.update_status.start()
        # Uncomment to make prefixed commands
        if (pending_commands:=self.pending_application_commands):
            log.debug(f"Unsynced Commands: {pending_commands}")
            try:
                await self.sync_commands(method='bulk', commands=pending_commands)
            except:
                log.exception("Failed to sync command {}".format(pending_commands))
                traceback.print_exc()
                                  
        
    @tasks.loop(minutes=25)
    async def update_status(self):
        c = random.choice(list(config.bot_activity.keys()))
        def type_activity(acti, vity):
            try:
                return discord.Activity(
                    name=random.choice(vity),
                    type=eval("discord.ActivityType.{}".format(acti)),
                    url="https://twitch.tv/meme",
                )
            except AttributeError: # if the activity type is streaming
                return discord.Activity(
                    name=random.choice(vity),
                    type=discord.ActivityType.streaming,
                    url="https://twitch.tv/meme",
                )

        await self.change_presence(activity=type_activity(c, config.bot_activity[c]))

    @update_status.before_loop
    async def wait_for_status(self):
        print("[STATUS UPDATE]: Waiting for ready...")
        await self.wait_until_ready()
        print("[STATUS UPDATE]: Ready!... awaiting cooldown")
        
if __name__=='__main__':
    print("Running Bot")
    intents = discord.Intents.all()
    bot = JamDotBot(intents=intents)
    try:
        log.info("Starting bot...")
        bot.run(config.get_token())
    except:
        traceback.print_exc()
        log.critical("Failed to run bot.")