import logging

logger = logging.getLogger('aiosqlite')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='db.log', encoding='utf-8', mode='w')
STD_LOG_FORMAT = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
handler.setFormatter(STD_LOG_FORMAT)
logger.addHandler(handler)
log = logger