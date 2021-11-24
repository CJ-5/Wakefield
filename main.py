# Import Failsafe
try:
    import time
    import os
    from colorama import init
    from colorama import Fore, Back, Style
    import configparser
    import lib
    import game_data
    import movement_engine
    import sys
    import timeit

except ModuleNotFoundError:
    File_Set = dict()
    File_Set['lib'] = os.path.isfile("./lib.py")
    File_Set['movement_engine'] = os.path.isfile("./movement_engine.py")
    File_Set['game_data'] = os.path.isfile("./game_data.py")

    if list(File_Set.values()).__contains__(False):
        missing_files = str()
        for k in File_Set:
            if File_Set[k] is False:
                missing_files += f"{k}.py, "
        missing_files = missing_files[:-2]
        print(f"Looks like you missing the file(s) ({missing_files})")
        print(f"Please make sure that you have all of the required files in the SAME directory")

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


# Initialization Script
init()
movement_engine.Data = game_data.StaticData()
config_obj = configparser.ConfigParser()
config_obj.read("C:/Users/carte/Documents/GitHub/Python_Adventure_Game/config.ini")

# Initialize main map
game_data.MapData.current_map = game_data.MainMap()
movement_engine.init_coord()

# Basic Controls tutorial
# lib.print_logo()
# lib.gprint(lib.MQ([lib.ck("Welcome to the game, I couldn't be bothered to name it so its called "),
#                    lib.ck("'Adventure Game'", "green"), lib.ck(".")]))
# lib.gprint("Here is some info to help you get started")
#
# lib.gprint(lib.MQ([
#     lib.ck("- At anytime during the game if you want to see a list of all available actions simply type"),
#     lib.ck(" 'help'", "yellow"), lib.ck(" or "), lib.ck("?", "yellow")]))
#
# time.sleep(2)
#
# lib.gprint("Why don't you give that a try now?")
# Map Control Init Code
# game_data.MapData.current_map = game_data.MainMap()
# movement_engine.init_coord()
# movement_engine.kb_listener()


