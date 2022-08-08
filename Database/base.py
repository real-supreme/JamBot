import aiosqlite
from .db_logger import log

class BaseDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.cursor = None

    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
        if exc_type:
            log.exception(exc_type, exc_value, traceback)
        return True

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_name)
        self.cursor = await self.db.cursor()

    async def close(self):
        await self.cursor.close()
        await self.db.close()

    async def execute(self, *query, Multiple=False, data=None):
        """
        Execute a query on the database.

        Send Queries as positional arguments.
        Send Multiple as keyword argument.
        Send data as keyword argument.

        Args:
            Multiple (bool, optional): Check if multiple datas are expected as output (more than 1 row of data). Defaults to False.
            data ([type], optional): Send an Iterable of data to enter into the database. Defaults to None.

        Returns:
            None: Error (Will be logged)
            True: successful (Not for SELECT queries)
            Data: Data (for SELECT queries)
        """
        try:
            for q in query:
                q.lower()
                if q.startswith("insert") and data is not None:
                    return await self.excall(q, data)
                if q.startswith("select"):
                    return await self.exec_select(q, Multiple)
                else:
                    try:
                        await self.cursor.execute(q)
                        await self.commit()
                    except Exception as e:
                        log.exception(e)
                        return None
                    return True
        except Exception as e:
            log.exception(e)
            return None
        
    async def excall(self, query, data):
        try:
            await self.cur.executemany(query, data)
            await self.commit()
            return True
        except aiosqlite.Error as e:
            log.exception(e)
            return None
        
    async def exec_select(self, query, many):
        try:
            await self.cur.execute(query)
            if many:
                return await self.cur.fetchall()
            return await self.cur.fetchone()
        except aiosqlite.Error as e:
            log.exception(e)
            return None
        
    async def fetchall(self):
        return await self.cursor.fetchall()

    async def fetchone(self):
        return await self.cursor.fetchone()

    async def fetchmany(self):
        return await self.cursor.fetchmany()
    
class DB_Error(Exception):
    def __init__(self, message="An error occured in the Database.", *args):
        if args:
            self.message = message + "\n" + str(args.join("\n"))
        else:
            self.message = message