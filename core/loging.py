import logging
import sys
from logging.handlers import RotatingFileHandler
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s:%(message)s', datefmt='%d/%M/%Y%I:%M:%S %P')
