import logging

logger = logging.getLogger('commands')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='commands.log', encoding='utf-8', mode='w')
STD_LOG_FORMAT = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
handler.setFormatter(STD_LOG_FORMAT)
logger.addHandler(handler)
log = logger