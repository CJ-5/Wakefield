# Import Failsafe
try:
    import time
    import os
    import lib
    from colorama import init
    from colorama import Fore, Back, Style
    import configparser
    import movement_engine
    import sys
    import game_data
except ModuleNotFoundError:
    File_Set = set()
    File_Set.add(os.path.isfile("./lib.py"))
    File_Set.add(os.path.isfile("./movement_engine.py"))
    File_Set.add(os.path.isfile("./game_data.py"))
    if File_Set.__contains__(False):
        print("Error you are missing non-package dependencies..."
              "\nPlease make sure all files in the given program package are in the SAME directory")
        time.sleep(4)
        exit(0)
    print("Error: Some packages could not be imported...")
    print("Feel free to check to code if this code seems suspicious")
    ri = input("Would you like to install the required packages (yes / no): ")

    if ri.lower() == "yes":
        os.system("pip install colorama")
        os.system("pip install pynput")
        os.system("pip install dataclasses")
        time.sleep(2)
        print("Please restart the program... Exiting...")
        time.sleep(2)
        exit(0)
    else:
        exit(0)

init()

config_obj = configparser.ConfigParser()
config_obj.read("C:/Users/carte/Documents/GitHub/Python_Adventure_Game/config.ini")

lib.print_logo()
lib.gprint(lib.MQ([lib.ck("Welcome to the game, I couldn't be bothered to name it so its called '"),
                   lib.ck("'Adventure Game'", "green"), lib.ck(".")]))
lib.gprint("Here is some info to help you get started")

lib.gprint(lib.MQ([
    lib.ck("- At anytime during the game if you want to see a list of all available actions simply type"),
    lib.ck(" 'help'", "yellow"), lib.ck(" or "), lib.ck("?", "yellow")]))

# Map Control Init Code
# game_data.MapData.current_map = game_data.MainMap()
# movement_engine.init_coord()
# movement_engine.kb_listener()
