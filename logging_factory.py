#!/usr/bin/python3

import logging

logger = logging.getLogger('root')

def init_config():
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="app.log", format=FORMAT, level=logging.INFO)

init_config()
