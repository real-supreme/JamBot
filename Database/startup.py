from .base import BaseDB, DB_Error
from .db_logger import log
from config import db_path

class StartupDB(BaseDB):
    def __init__(self, db_name=db_path):
        super().__init__(db_name)
        
    async def run(self):
        try:
            await self.execute("CREATE TABLE IF NOT EXISTS BanWords(guild_id BIGINT PRIMARY KEY, words TEXT, punish TEXT)".lower())
            await self.execute("CREATE TABLE IF NOT EXISTS Whilelist(guild_id BIGINT PRIMARY KEY, roleid TEXT)".lower())
        except Exception as e:
            raise DB_Error(args=e)