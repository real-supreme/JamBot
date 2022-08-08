import sqlite3

class DB_Backup:
    def __init__(self, db_path="Database/backup.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        
    @property
    def db(self):
        return self.conn