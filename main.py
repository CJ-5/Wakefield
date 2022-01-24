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
print(f'\x1b[{num//2}B', end='')  # Reset 
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
lib.get_max()  # Initiate the max console size set to SysData
lib.maximize_console()
init()  # initiate colorama

# Config Pull Script
movement_engine.Data = game_data.StaticData()   # Initialize static data

# Initialize main map
game_data.MapData.current_map = game_data.MainMap()
movement_engine.init_coord()
movement_engine.init_door()
os.system("cls")

# Basic Controls tutorial
lib.print_logo()
lib.gprint(game_data.MQ([lib.ck("WARNING", "yellow"),
                        lib.ck(": This program should only be ran in the python 3.9+ interpreter\n"
                               "and keep in mind that ALL keyboard input is listened to (for game commands)\n")]), 0)
lib.gprint(game_data.MQ([lib.ck("WARNING", "yellow"),
                         lib.ck(": KEEP THIS PROGRAM IN FULLSCREEN FOR THE ENTIRE PLAY THROUGH"
                                "(otherwise things will break, and I will be sad)\n"
                                "The script does everything for you, let it do it's thing\n")]), 0)

time.sleep(5)

# Tutorial Script
os.system('cls')
lib.print_logo()
time.sleep(1)
print('\n\n')
lib.gprint('Welcome to the game... oddly enough I decided after putting all of this work into it that I would not'
           'bother giving it a name...')
time.sleep(1.5)
lib.gprint('Hence the name Adventure Game Stuck.')
time.sleep(2)
os.system('cls')
lib.print_logo()
print('\n\n')
lib.gprint('Originally I would have wrote a fully interactive tutorial script that had you enter all of the different'
           'commands and it would be all cool and fancy, but then I realised...')
time.sleep(1)
lib.gprint('I can just give you a help command that shows tells you the exact same thing!')
time.sleep(1)
lib.gprint('So.')
time.sleep(1)
lib.gprint(game_data.MQ([lib.ck('At any time '), lib.ck('(terms and conditions apply)', 'yellow'),
                         lib.ck(', use the "'), lib.ck('help', 'yellow'), lib.ck('" command to see a list of commands'
                                                                                 'and their individual usages')]))
time.sleep(2)
os.system('cls')
lib.print_logo()
print('\n\n')
lib.gprint('The game is simple. You are an adventurer in the magical land of Wakefield.')
time.sleep(1)
lib.gprint('You all local dungeons have dried up and cleared out ages ago.')
time.sleep(1)
lib.gprint('You thought adventuring would be a sustainable, stable job. Now you realise that it wasn\'t')
time.sleep(1)
lib.gprint('Your only hope now is to find a dungeon that you can clear by yourself and use the loot to sell and support'
           ' yourself.')
time.sleep(3)
os.system('cls')
print('\n\n')
lib.gprint('Now then, lets get started...')
time.sleep(2)
lib.gprint('ill be nice and give you some starter gear.')
time.sleep(1)
lib.gprint('Hmm...', 200)
time.sleep(1)
lib.gprint('How about your grandfathers old broadsword... a Small HP potion, and....... Moldy Bread...')
time.sleep(1.5)
lib.gprint('Generous aren\'t I?')
time.sleep(3)
os.system('cls')
print('\n\n')
lib.gprint('Alright now for controls. Its simple, use arrow keys to move, moving onto a door will activate it,'
           ' all enemies must be cleared to progress to the next floor, once enemies are cleared a question will be'
           ' asked and if you get the answer wrong more than 3 times or the time runs out once you will be returned to'
           ' the main map.')
time.sleep(3)
lib.gprint('\nEnemies will move every second time you move but will not move when you are near. Moving onto an enemy'
           ' will start a battle,  if you lose the battle and die you will be returned to the main map losing 1 random'
           ' item (some items are immune to this).')
time.sleep(2)
lib.gprint('Winning a battle will give you a random (within defined range) amount of exp which will, over time, level '
           'you up. Levels don\'t really do much... On top of the exp you will also get some loot, this includes '
           'weapons and consumables that can be used in battle.')
time.sleep(2)
lib.gprint(game_data.MQ([lib.ck('To use a item, you can use the "use" '
                                'command which is combined with a item id / item name like so', 'yellow'),
                         lib.ck(' use item-name   |   use 0', 'yellow')]))
time.sleep(3)
os.system('cls')
lib.print_logo()
print('\n\n')
lib.gprint('Alright! Now since you are a pro and know everything about the game because of my masterful teaching, '
           'I am going to drop you onto the map.')
time.sleep(3)
os.system('cls')
script = [lib.ck('Good luck! and may the RNG God be with you. Oh and small detail, there are no save files. :)')]
lib.center_cursor(len(script[0][0]))
lib.gprint(game_data.MQ(script))
time.sleep(1)

game_data.PlayerData.Inventory_Accessible = True
game_data.Demo.inventory_demo = False
game_data.Demo.help_demo = False
game_data.Demo.item_info_demo = False
game_data.MapData.valid_cmd = ["inventory", "item-info", "help", 'drop']
movement_engine.show_map(game_data.MapData.current_map)
Thread(target=movement_engine.csq_watch_dog).start()  # Movement listener (Async)
movement_engine.kb_listener()

while game_data.SysData.full_kill is False:  # Debug code to hold in place while testing
    time.sleep(0.1)
    continue

# To-Do:
# - Item Pickup system
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
