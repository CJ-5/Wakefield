# Base file, contains the actual output of the game
from colorama import init
from colorama import Fore, Back, Style
import configparser
import time
import lib
import movement_engine
import sys
import game_data


init()

config_obj = configparser.ConfigParser()
config_obj.read("C:/Users/carte/Documents/GitHub/Python_Adventure_Game/config.ini")

lib.print_logo()
lib.gprint("Welcome to the game, I couldn't be bothered to name it so its called 'Adventure Game'!")
lib.gprint("Here is some info to help you get started")

lib.gprint(lib.MQ([lib.ck("- At anytime during the game if you want to see a list of all available actions simply use"),
                   ]))
