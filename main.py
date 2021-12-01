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

# Initialization Script
init()  # initiate colorama
# user32 = windll.user32
# user32.SetProcessDPIAware()
# hwnd = user32.GetForegroundWindow()
movement_engine.Data = game_data.StaticData()
config_obj = configparser.ConfigParser()
config_obj.read("C:/Users/carte/Documents/GitHub/Python_Adventure_Game/config.ini")
lib.get_max()  # Initiate the max console size

# Initialize main map
game_data.MapData.current_map = game_data.MainMap()
movement_engine.init_coord()

# Intro Script
# time.sleep(2)
# lib.gprint("Hello...")
# time.sleep(1)
# lib.gprint("Due to the fact that you are most likely running this program on a mac, I have very little way of being\n"
#            "able to account for the fact that our monitors' resolutions might be different...\n")
# time.sleep(1)
# lib.gprint("So since I didn't want to write a dedicated file to monitor whether or not this program is in\n"
#            "fullscreen during the entire play through and correct it if it is not, I am going to trust you...\n")
# time.sleep(1.5)
# lib.gprint("Please run this program in fullscreen as if you don't, many things will break and it will make me very sad")
# time.sleep(1.5)
# lib.gprint("I will give you some time to do that now")
# time.sleep(4)
#
#
# os.system("cls")
#
# # Basic Controls tutorial
# time.sleep(2)
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
#
# lib.gprint("Why don't you give that a try now?")
# game_data.MapData.valid_cmd.append("help")
# movement_engine.demo_prompt()
# print()
#
# lib.clear_line(2, 34, False, True)
# game_data.MapData.valid_cmd.clear()
# lib.gprint("Great!")
# lib.gprint(lib.MQ([lib.ck("Now try the "), lib.ck("inventory", "yellow"), " command to display your current items."]))
# movement_engine.demo_prompt()
#
# line_length = len(f"{'':<10}") + len(f"{'*':^25}{'*':^25}{'*':^25}") * 2
# lib.display_inv()
# time.sleep(2)
# lib.clear_line(5, line_length, False, True)
# time.sleep(1)
#

lib.maximize_console()

random_variable_that_has_one_purpose = True
while random_variable_that_has_one_purpose:
    continue
