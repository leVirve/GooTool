import logging

from gootool.drive import *


logger = logging.getLogger('gootool')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('gootool.log', encoding='utf8')
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
simple_formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(simple_formatter)
logger.addHandler(fh)
logger.addHandler(ch)
