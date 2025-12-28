import logging

def logging(file_name:str ,level, name, levelname, message):
    logging.basicConfig(filename='{file_name}')
    logger = logging.getLogger('{name}')
    logger.setLevel(logging.INFO)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)s-%(name)s-%({levelname})s:%({message})s', datefmt='%d/%M/%Y%I:%M:%S %P')
    consoleHandler.setFormatter(format)
    logger.addHandler(consoleHandler)
    return logger
