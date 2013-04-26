# encoding=utf8
'''
Created on 2013-4-24
@author: corleone
'''
from bot.configutil import ConfigFile
import os

def read_config():
    cfg_path = os.sep.join([os.getcwd(), 'validproxy.cfg'])
    configdata = ConfigFile.readconfig(cfg_path).data
    return configdata 

configdata = read_config()
