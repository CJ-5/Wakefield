# Import Failsafe
try:
    import time
    import os
    from colorama import *
    import configparser
    import lib
    import game_data
    import movement_engine
    import sys
    import timeit
    from threading import Thread
    import pynput
    from ctypes import windll
    import win32gui

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
        os.system("pip install pywin32")
        time.sleep(2)
        print("Please restart the program... Exiting...")
        time.sleep(2)
        exit(0)
    else:
        exit(0)

"""
num = 4
print("5")
print("4")  # Clears this line
print("3")
print("2")
print("1")

print(f'\x1b[{num}A TestOver              ')  # Works
print(f'\x1b[{num//2}B', end='')
"""

"""
\x1b[{n}A : Up
\x1b[{n}B : Down
\x1b[{n}C : Right
\x1b[{n}D : Left
"""

lib.gprint("Initializing...", 25)
time.sleep(0.5)

# Font / Console Size Initialization
lib.reset_sys_font()  # Set the font and font size
lib.maximize_console()  # Maximize the console window
lib.get_max()  # Initiate the max console size
lib.maximize_console()
init()  # initiate colorama

# Config Pull Script
movement_engine.Data = game_data.StaticData()   # Initialize static data
# config_obj = configparser.ConfigParser()  # Setup configparser object
# config_obj.read("C:/Users/carte/Documents/GitHub/Python_Adventure_Game/config.ini")  # Read config

# Initialize main map
game_data.MapData.current_map = game_data.MainMap()
movement_engine.init_coord()

os.system("cls")

# Basic Controls tutorial
# lib.print_logo()
# lib.gprint(lib.MQ([lib.ck("WARNING", "yellow"),
#                    lib.ck(": This program should only be ran in the python 3.9+ interpreter\n"
#                           "and keep in mind that ALL keyboard input is listened to (for game commands)\n")]), 0)
# lib.gprint(lib.MQ([lib.ck("WARNING", "yellow"),
#                    lib.ck(": KEEP THIS PROGRAM IN FULLSCREEN FOR THE ENTIRE PLAY THROUGH"
#                           "(otherwise things will break, and I will be sad)\n"
#                           "The script does everything for you, let it do it's thing\n")]), 0)
# time.sleep(3.5)
# lib.gprint(lib.MQ([lib.ck("Welcome to the game, I couldn't be bothered to name it so its called "),
#                    lib.ck("Adventure Game", "green"), lib.ck(".")]))
# time.sleep(1)
# lib.gprint("Here is some info to help you get started")
# time.sleep(1.5)
#
# lib.gprint(lib.MQ([
#     lib.ck("- At anytime during the game if you want to see a list of all available actions simply type"),
#     lib.ck(" help", "yellow"), lib.ck(" or "), lib.ck("?", "yellow")]))
#
# time.sleep(2)
#
# lib.gprint("Why don't you give that a try now?")
# game_data.MapData.valid_cmd.append("help")
# game_data.MapData.valid_cmd.append("?")
# movement_engine.demo_prompt()
# print()
#
# game_data.MapData.valid_cmd.clear()
# lib.gprint("\nAs you can see here this list displays the info of all commands ")
#
# time.sleep(5)
# lib.clear_line(6 + len(game_data.HelpPage().ind_def))
# lib.gprint(lib.MQ([lib.ck("Now try the "), lib.ck("inventory", "yellow"),
#                    lib.ck(" command to display your current items.")]))
# game_data.MapData.valid_cmd.append("inventory")
# movement_engine.demo_prompt()
# game_data.MapData.valid_cmd.clear()
#
# time.sleep(2)
# lib.clear_line(3 + game_data.PlayerData.cur_inv_display_size)
# lib.gprint("")
game_data.PlayerData.Inventory_Accessible = True
lib.add_item(0)
game_data.Demo.inventory_demo = False
game_data.MapData.valid_cmd.append("inventory")
movement_engine.kb_listener()

while True:  # Debug code to hold in place while testing
    continue

# To-Do:
# - Remove functions for attempting to print map and inventory together
# - Finish intro script / tutorial
# - Start / Finish map intro
# - Fix help command to get list of valid moves for the specific map
# - Dungeon Entrance / Exit proximity system
# - Death System
# - Battle System
# - Map transition System
# - Save File ?
# - Floor Progression
# - Enemy Movement System
# - Enemy Spawning / Death System
# - System Watchdogs
