#  Holds the main functions that operate the backend of the game (e.g battle system)
import os
from os import system
import movement_engine
import time
from dataclasses import dataclass
from colorama import Fore, Back, Style
import game_data
import sys
import random
import math
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes


class Logo:
    __slots__ = ("logo_a", "logo_b")

    # logo_a: equivalent to "Adventure"
    # logo_b: equivalent to "Game"
    def __init__(self):
        self.logo_a = [10, 32, 32, 32, 32, 10, 32, 9608, 9608, 9608, 9608, 9608, 9559, 32, 9608, 9608, 9608, 9608, 9608,
                       9608, 9559, 32, 9608, 9608, 9559, 32, 32, 32, 9608, 9608, 9559, 9608, 9608, 9608, 9608, 9608,
                       9608, 9608, 9559, 9608, 9608, 9608, 9559, 32, 32, 32, 9608, 9608, 9559, 9608, 9608, 9608, 9608,
                       9608, 9608, 9608, 9608, 9559, 9608, 9608, 9559, 32, 32, 32, 9608, 9608, 9559, 9608, 9608, 9608,
                       9608, 9608, 9608, 9559, 32, 9608, 9608, 9608, 9608, 9608, 9608, 9608, 9559, 10, 9608, 9608, 9556,
                       9552, 9552, 9608, 9608, 9559, 9608, 9608, 9556, 9552, 9552, 9608, 9608, 9559, 9608, 9608, 9553,
                       32, 32, 32, 9608, 9608, 9553, 9608, 9608, 9556, 9552, 9552, 9552, 9552, 9565, 9608, 9608, 9608,
                       9608, 9559, 32, 32, 9608, 9608, 9553, 9562, 9552, 9552, 9608, 9608, 9556, 9552, 9552, 9565, 9608,
                       9608, 9553, 32, 32, 32, 9608, 9608, 9553, 9608, 9608, 9556, 9552, 9552, 9608, 9608, 9559,
                       9608, 9608, 9556, 9552, 9552, 9552, 9552, 9565, 10, 9608, 9608, 9608, 9608, 9608, 9608, 9608,
                       9553, 9608, 9608, 9553, 32, 32, 9608, 9608, 9553, 9608, 9608, 9553, 32, 32, 32, 9608, 9608, 9553,
                       9608, 9608, 9608, 9608, 9608, 9559, 32, 32, 9608, 9608, 9556, 9608, 9608, 9559, 32, 9608, 9608,
                       9553, 32, 32, 32, 9608, 9608, 9553, 32, 32, 32, 9608, 9608, 9553, 32, 32, 32, 9608, 9608, 9553,
                       9608, 9608, 9608, 9608, 9608, 9608, 9556, 9565, 9608, 9608, 9608, 9608, 9608, 9559, 32, 32, 10,
                       9608, 9608, 9556, 9552, 9552, 9608, 9608, 9553, 9608, 9608, 9553, 32, 32, 9608, 9608, 9553, 9562,
                       9608, 9608, 9559, 32, 9608, 9608, 9556, 9565, 9608, 9608, 9556, 9552, 9552, 9565, 32, 32, 9608,
                       9608, 9553, 9562, 9608, 9608, 9559, 9608, 9608, 9553, 32, 32, 32, 9608, 9608, 9553, 32, 32, 32,
                       9608, 9608, 9553, 32, 32, 32, 9608, 9608, 9553, 9608, 9608, 9556, 9552, 9552, 9608, 9608,
                       9559, 9608, 9608, 9556, 9552, 9552, 9565, 32, 32, 10, 9608, 9608, 9553, 32, 32, 9608, 9608, 9553,
                       9608, 9608, 9608, 9608, 9608, 9608, 9556, 9565, 32, 9562, 9608, 9608, 9608, 9608, 9556, 9565, 32,
                       9608, 9608, 9608, 9608, 9608, 9608, 9608, 9559, 9608, 9608, 9553, 32, 9562, 9608, 9608, 9608,
                       9608, 9553, 32, 32, 32, 9608, 9608, 9553, 32, 32, 32, 9562, 9608, 9608, 9608, 9608, 9608, 9608,
                       9556, 9565, 9608, 9608, 9553, 32, 32, 9608, 9608, 9553, 9608, 9608, 9608, 9608, 9608, 9608, 9608,
                       9559, 10, 9562, 9552, 9565, 32, 32, 9562, 9552, 9565, 9562, 9552, 9552, 9552, 9552, 9552, 9565,
                       32, 32, 32, 9562, 9552, 9552, 9552, 9565, 32, 32, 9562, 9552, 9552, 9552, 9552, 9552, 9552, 9565,
                       9562, 9552, 9565, 32, 32, 9562, 9552, 9552, 9552, 9565, 32, 32, 32, 9562, 9552, 9565,
                       32, 32, 32, 32, 9562, 9552, 9552, 9552, 9552, 9552, 9565, 32, 9562, 9552, 9565, 32, 32, 9562,
                       9552, 9565, 9562, 9552, 9552, 9552, 9552, 9552, 9552, 9565, 10, 32, 32, 32, 32, 32, 32, 32, 32,
                       32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
                       32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
                       32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 10]

        self.logo_b = [10, 32, 9608, 9608, 9608, 9608, 9608, 9608, 9559, 32, 32, 9608, 9608, 9608, 9608, 9608,
                       9559, 32, 9608, 9608, 9608, 9559, 32, 32, 32, 9608, 9608, 9608, 9559, 9608, 9608, 9608, 9608,
                       9608, 9608, 9608, 9559, 10, 9608, 9608, 9556, 9552, 9552, 9552, 9552, 9565, 32, 9608, 9608,
                       9556, 9552, 9552, 9608, 9608, 9559, 9608, 9608, 9608, 9608, 9559, 32, 9608, 9608, 9608, 9608,
                       9553, 9608, 9608, 9556, 9552, 9552, 9552, 9552, 9565, 10, 9608, 9608, 9553, 32, 32, 9608, 9608,
                       9608, 9559, 9608, 9608, 9608, 9608, 9608, 9608, 9608, 9553, 9608, 9608, 9556, 9608, 9608, 9608,
                       9608, 9556, 9608, 9608, 9553, 9608, 9608, 9608, 9608, 9608, 9559, 32, 32, 10, 9608, 9608, 9553,
                       32, 32, 32, 9608, 9608, 9553, 9608, 9608, 9556, 9552, 9552, 9608, 9608, 9553, 9608, 9608, 9553,
                       9562, 9608, 9608, 9556, 9565, 9608, 9608, 9553, 9608, 9608, 9556, 9552, 9552, 9565, 32, 32, 10,
                       9562, 9608, 9608, 9608, 9608, 9608, 9608, 9556, 9565, 9608, 9608, 9553, 32, 32, 9608, 9608,
                       9553, 9608, 9608, 9553, 32, 9562, 9552, 9565, 32, 9608, 9608, 9553, 9608, 9608, 9608, 9608, 9608,
                       9608, 9608, 9559, 10, 32, 9562, 9552, 9552, 9552, 9552, 9552, 9565, 32, 9562, 9552, 9565, 32, 32,
                       9562, 9552, 9565, 9562, 9552, 9565, 32, 32, 32, 32, 32, 9562, 9552, 9565, 9562, 9552, 9552, 9552,
                       9552, 9552, 9552, 9565, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
                       32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
                       32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 10]


def print_logo():
    # Print the Logo
    logo_instance = Logo()
    for logo_char in logo_instance.logo_a:
        if logo_char == 10:  # Check for new line
            print(f"{chr(logo_char):<10}", end='')  # Spacing so text is not left-aligned
        else:
            print(chr(logo_char), end='')
    for logo_char in logo_instance.logo_b:
        if logo_char == 10:
            print(f"{chr(logo_char):<30}", end='')
        else:
            print(chr(logo_char), end='')
    print('\n')


def get_max():
    # Initiate the max size of the console
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    kernel32.GetConsoleWindow.restype = wintypes.HWND
    kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
    kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
    user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

    fd = os.open('CONOUT$', os.O_RDWR)

    try:
        hcon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hcon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        cols = max_size.X
        hwnd = kernel32.GetConsoleWindow()
        if cols and hwnd:
            lines = max_size.Y
            game_data.SysData.max_screen_size = (cols, lines)
    finally:
        os.close(fd)


def is_full_screen():
    try:
        col, row = os.get_terminal_size()
        print((col, row))
        print(game_data.SysData.max_screen_size)
        print((col, row) == get_max())
        return (col, row) == game_data.SysData.max_screen_size
    except:
        return False


def maximize_console(lines=None):
    #  I hate how long this took to figure out
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    SW_MAXIMIZE = 3  # specifies to maximize the window
    kernel32.GetConsoleWindow.restype = wintypes.HWND
    kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
    kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
    user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hcon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hcon)

        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        cols = max_size.X
        hwnd = kernel32.GetConsoleWindow()

        if cols and hwnd:
            if lines is None:
                lines = max_size.Y
            else:
                lines = max(min(lines, 9999), max_size.Y)
            game_data.SysData.max_screen_size = (cols, lines)
            subprocess.check_call('mode.com con cols={} lines={}'.format(cols, lines))
            user32.ShowWindow(hwnd, SW_MAXIMIZE)
    finally:
        os.close(fd)


def clear_line(num: int, max_line_length: int = None,
               reset: bool = False, direction: str = 'A'):
    # Clear the specified amount of lines from the console
    # Num = The amount of line to clear
    # Max_Line_Length = The length of the largest line amongst the lines being cleared
    # Reset = Whether or not to reset the cursor after clearing specified line amount
    # direction = The direction to clear the lines (default: A [Up])
    if max_line_length is None:
        max_line_length = game_data.SysData.max_screen_size[0]
    for i in range(num):
        print(f'\x1b[{1}{direction.upper()}', end='')
        print(f'\r{Fore.RED}{" "*max_line_length}{Fore.RESET}\r', end='')

    if reset is True:
        print(f'\x1b[{num // 2}B')  # Reset the cursor to the original position with magic


def display_help(cmd: str = None):
    help_page = game_data.HelpPage()
    # Display the help page for all or just one command
    if cmd.isspace() or cmd is cmd == "":
        # Display the full help page
        print("Game Command List\n")
        for cmd_info in help_page.ind_def:
            print(f"{cmd_info:<20}", end='')
            print(f":  {help_page.ind_def[cmd_info]}")
    else:
        # Index the command info from the command info list
        pass


# Inventory Functions
@dataclass()
class InvItem:
    name: str
    item_id: int
    qty: int = 1
    max_qty: int = None
    item_size: int = 1
    type: str = "consumable"  # The type of the item [weapon / consumable / clothing]
    damage: tuple = (0, 0)  # Damage range items deals (does not apply to non-weapon type items)
    health_regen: int = 0
    stamina_regen: int = 0
    desc: str = None  # Description of item


def check_proximity(object_pos: tuple):
    # Check if the player is within distance of the object
    return math.sqrt(abs((object_pos[0] - game_data.MapData.x) ** 2 + (object_pos[1] - game_data.MapData.y) ** 2)) <= \
        game_data.PlayerData.Detection_Distance


def add_item(item_id: int):
    # Add a item by id to a players inventory
    if game_data.PlayerData.Inventory_Accessible is True:
        item_data = item_info(item_id)
        size_calc = game_data.PlayerData.Inventory_Space - item_data.item_size
        if size_calc >= 0:
            #
            # Check for duplicate entries and combine their qty
            dupe = False
            ind = 0
            for idx, inv_item in enumerate(game_data.PlayerData.Inventory):
                if inv_item.item_id == item_data.item_id:
                    if not game_data.PlayerData.Inventory[idx].qty + 1 > inv_item.max_qty:
                        # Makes sure to not add items that cant have multiple instances in the inventory
                        dupe = True
                        game_data.PlayerData.Inventory[idx].qty += 1
                        ind = idx
                        break

            if dupe is False:
                game_data.PlayerData.Inventory.append(item_data)
                # print(game_data.PlayerData.Inventory[ind])

        elif size_calc < 0:
            print("Could not add item(s) to your inventory due to lack of space")
    else:
        print("Error: Player Inventory is inaccessible")


def reset_sys_font(font_size: int = 18):

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.dwFontSize.Y = font_size  # The actual scalable size of the font
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "NSimSun"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))


def item_info(item_id: int, item_name: str = None):
    if item_id is None and item_name is None:
        print("Error: No Item specified @ InvItemInfo Call")
    elif item_id is None:  # Look for item info by name (Slower)
        for n in movement_engine.Data.game_items:
            if n.name == item_name:
                return n
    elif item_name is None:  # Directly index the item by the index (equivalent to the id) (Faster)
        return movement_engine.Data.game_items[item_id]


def cmove(num: int = 1, dir: str = 'A'):  # Dunno, seems kinda useless, but who will actually read all of this?
    # Move the console cursor
    print(f"\x1b[{num}{dir}", end='')


def map_index(map_id: int):
    # Find and return the map data for the specified id
    maps = [game_data.MainMap, game_data.Floor0]
    if not map_id > len(maps) - 1:
        return maps[map_id]
    else:
        os.system("cls")
        print(f"{Fore.RED}Error: Failed to find map based off of specified id{Fore.RESET}")


def clear_inventory_display(line: int = 0):
    # Clear the inventory print out
    game_data.PlayerData.Inventory_Displayed = False
    print(game_data.PlayerData.cur_inv_display_size)
    clear_line(game_data.PlayerData.cur_inv_display_size, len(game_data.MapData.current_map.map_array[0]), False)
    game_data.PlayerData.cur_inv_display_size = 0


def display_inv():
    # if the map is displayed, clear the map and then display the inventory
    # Display the inventory
    game_data.PlayerData.Inventory_Displayed = True
    game_data.PlayerData.command_status = False
    os.system("cls")
    item_spacing = 25
    side_spacing = 5
    element_num = 1  # Which side of the array is printing
    key_num = 0  # The current item to print in the first column
    sub_key_num = 0  # The current item to print in the second column
    inv_size = len(game_data.PlayerData.Inventory) - 1
    row1 = game_data.PlayerData.Inventory_Space // 2

    if game_data.PlayerData.Inventory_Space % 2 == 1:
        # If the inventory space num is odd, the first column will print 1 more than the second column
        row1 += 1

    print(f"{'':<{side_spacing}}", end='')  # Title Side Spacing
    print(f"{'Item Name':^{item_spacing}}{'Item QTY':^{item_spacing}}{'Item ID':^{item_spacing}}"
          f"{'Item Name':^{item_spacing}}{'Item QTY':^{item_spacing}}{'Item ID':^{item_spacing}}\n")
    for i in range(game_data.PlayerData.Inventory_Space):

        if i > inv_size:
            # Item is out of total inventory index
            # Print Blank Row
            if element_num == 2:
                print(f"{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}", end='')
                print("\n", end='')
                game_data.PlayerData.cur_inv_display_size += 1
                element_num = 1
            else:
                print(f"{'':<{side_spacing}}", end='')
                print(f"{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}", end='')
                element_num = 2
        elif element_num == 1:
            print(f"{'':<{side_spacing}}", end='')
            item = game_data.PlayerData.Inventory[key_num]
            print(f"{Fore.RED}", end='')
            # Check to see if requested item exists if so print
            print(f"{item.name:^{item_spacing}}"
                  f"{item.qty:^{item_spacing}}"
                  f"{item.item_id:^{item_spacing}}", end='')
            element_num = 2  # Set to second column
            print(f"{Fore.RESET}", end='')
            key_num += 1
            game_data.PlayerData.cur_inv_display_size += 1
        elif element_num == 2:
            print(f"{Fore.GREEN}", end='')
            # Print second row, check to see if requested item exists if so print
            # Attempt to index item that is out of index of the first row

            if not row1 + sub_key_num > inv_size - 1:
                item = game_data.PlayerData.Inventory[row1 + sub_key_num]
                print(f"{item.name:>{item_spacing}}"
                      f"{item.qty:>{item_spacing}}"
                      f"{item.item_id:>{item_spacing}}", end='')
            else:
                print(f"{'*':<{item_spacing}}{'*':<{item_spacing}}{'*':<{item_spacing}}", end='')
            element_num = 1  # Set to first column
            sub_key_num += 1

            print(f"{Fore.RESET}\n", end='')
    print()  # Create newline at end of printout


def display_stats():  # Display stats of system and player
    pass


def display_item_info(cmd):  # Get raw item info and display it in formatted statement
    pass


@dataclass()
class MQ:
    messages: list


def ck(text: str, color: str = None):
    return text, color


def process_command(cmd_raw):
    # Process command
    cmd = cmd_raw.lower().split(' ')
    if (len(cmd_raw) > 0 and game_data.HelpPage().cmd_list.__contains__(cmd[0])
            and game_data.MapData.valid_cmd.__contains__(cmd[0])) or cmd[0] == "exit":

        cmd_latter = " ".join(cmd[1:])  # Removes the command keyword
        print(cmd_latter)
        if cmd[0] == "help" or cmd[0] == "?":  # Print the help page
            if game_data.Demo.help_demo is True:
                game_data.MapData.map_kill = True
                game_data.Demo.help_demo = False
                print()
            display_help(cmd_latter)
        elif cmd[0] == "inventory":  # print the players inventory
            if game_data.Demo.inventory_demo is True:
                game_data.MapData.map_kill = True
                game_data.Demo.inventory_demo = False
                print()
            display_inv()
        elif cmd[0] == "item_info":  # Print the specified items info
            if game_data.Demo.item_info_demo is True:
                game_data.MapData.map_kill = True
                game_data.Demo.item_info_demo = False
                print("ITEM INFO")
            display_item_info(cmd_latter)
        elif cmd[0] == "stats":  # print system & player statistics
            if game_data.Demo.stats_demo is True:
                game_data.MapData.map_kill = True
                game_data.Demo.stats_demo = False
                print("STATS DISPLAY")
            display_stats()
        elif cmd[0] == "exit":
            game_data.MapData.map_kill = True  # Exit listener thread
            os.system('cls')
            reset_sys_font(30)
            get_max()
            print(f"{'':<{game_data.SysData.max_screen_size[0] // 2}}", end='')
            gprint(MQ([ck("Goodbye :(")]))
            system('exit')
    else:
        gprint(MQ([ck("\nInvalid Command", "red")]))

    game_data.MapData.current_command = ""  # Reset the inputted command


def event_handler(event_id: int, event_type: int):
    if event_id not in game_data.MapDataCache.event_cache:  # Make sure not to duplicate events
        game_data.MapData.map_idle = True  # Stop keyboard listener and printout
        game_data.PlayerData.command_status = False  # Disable command input
        system('cls')
        time.sleep(2)
        # Fetch event data
        for m in game_data.EventData.events[list(game_data.EventData.events.keys())
                                            [event_type]][event_id].event_dialogue:
            gprint(m[0])  # Print specified dialogue
            time.sleep(m[1] / 1000)  # Pause for specified delay in MS
        time.sleep(3)
        game_data.MapDataCache.event_cache.append(event_id)
        movement_engine.show_map(game_data.MapData.current_map)
        game_data.MapData.map_idle = False  # Resume the map listener
        game_data.PlayerData.command_status = True  # Re-Enable user command input


def question_handler(question_diff: int):
    # Kill main listener
    game_data.MapData.map_kill = True

    # Get random set of questions
    question = movement_engine.Data.questions[0][question_diff]
    question = question[random.randint(0, len(question))]

    # Ask Question and initiate the input
    gprint(question)


def gprint(queue, speed: int = 35):
    # Print as if the text was being typed
    if type(queue) is not MQ:
        # Converts raw string into MQ format
        queue = MQ([(queue, None)])
    delay = speed / 1000  # Seconds to milliseconds conversion
    # Used to index color by string key
    colors_list = {"red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW, "blue": Fore.BLUE,
                   "magenta": Fore.MAGENTA, "cyan": Fore.CYAN, "white": Fore.WHITE}
    for msg in queue.messages:
        if msg[1] is not None:
            # if color printing is specified
            print(colors_list[msg[1].lower()], end='')
            for char in msg[0]:
                print(char, end='')
                time.sleep(delay)
            print(Fore.RESET, end='')
        else:
            for char in msg[0]:
                print(char, end='')
                time.sleep(delay)
    print()  # Create new line
