from tkinter.tix import Tree
from .db_logger import log
from .base import BaseDB, DB_Error
from config import db_path
from .startup import StartupDB
from functools import lru_cache

class DB(BaseDB):
    def __init__(self, db_name=db_path):
        if db_name!=db_path:
            StartupDB(db_name).run()
        super().__init__(db_name)
    
    async def add_banned_word(self, guild_id:int, word:list, punish:str):
        try:
            words = list(await self.get_all_banned_words(guild_id))
            word = " ".join(set(words+word))
            await self.execute("INSERT INTO BanWords(guild_id, words, punish) VALUES(?, ?, ?)", guild_id, words, punish)
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    async def remove_banned_word(self, guild_id:int, word:list):
        try:
            bannedwords = list(await self.get_all_banned_words(guild_id))
            if str(bannedwords) not in word:
                return True
            roles.remove(str(role_id))
            if word:
                words = " ".join(word)
                await self.execute("INSERT INTO Whilelist(guild_id, roleid) VALUES(?, ?)", guild_id, word)
            else:
                await self.execute("DELETE FROM BanWords WHERE guild_id=?", guild_id)
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)

    @lru_cache(maxsize=20) 
    async def get_all_banned_words(self, guild_id):
        try:
            await self.execute("SELECT words FROM BanWords WHERE guild_id=?", guild_id)
            words = await self.fetchone()[0]
            words = words.split(" ")
            return words
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    @lru_cache(maxsize=20)
    async def get_banwords_punishment(self, guild_id, word):
        try:
            await self.execute("SELECT punish FROM BanWords WHERE guild_id=? AND word=?", guild_id, word)
            return await self.fetchone()[0]
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    @lru_cache(maxsize=20)
    async def check_banned_word(self, guild_id, word):
        try:
            await self.execute("SELECT word FROM BanWords WHERE guild_id=? AND word=?", guild_id, word)
            return True
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    @lru_cache(maxsize=20)
    async def get_whitelist_roles(self, guild_id):
        try:
            self.execute("SELECT roleid FROM Whilelist WHERE guild_id=?", guild_id)
            return await self.fetchall()[0].split(" ")
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    async def add_whitelist_role(self, guild_id:int, role_id:int):
        try:
            roles = list(await self.get_whitelist_roles(guild_id))
            if str(role_id) in roles:
                return True
            roles.append(str(role_id))
            roles = " ".join(roles)
            await self.execute("INSERT INTO Whilelist(guild_id, roleid) VALUES(?, ?)", guild_id, role_id)
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)
        
    async def remove_whitelist_role(self, guild_id:int, role_id:int):
        try:
            roles = list(await self.get_whitelist_roles(guild_id))
            if str(role_id) not in roles:
                return True
            roles.remove(str(role_id))
            if roles:
                roles = " ".join(roles)
                await self.execute("INSERT INTO Whilelist(guild_id, roleid) VALUES(?, ?)", guild_id, role_id)
            else:
                await self.execute("DELETE FROM Whilelist WHERE guild_id=?", guild_id)
        except Exception as e:
            log.exception(e)
            raise DB_Error(args=e)