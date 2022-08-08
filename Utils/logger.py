from config import STD_LOG_FORMAT
import logging

logger = logging.getLogger('images')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='image.log', encoding='utf-8', mode='w')
handler.setFormatter(STD_LOG_FORMAT)
logger.addHandler(handler)
log = logger