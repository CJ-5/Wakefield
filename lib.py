#  Holds the main functions that operate the backend of the game (e.g battle system)
import os
from os import system

import lib
import movement_engine
import time
from colorama import Fore, Style
import game_data
import random
import math
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes
from game_data import MQ, InvItem
import threading
from threading import Thread
import websocket
import _thread



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
        print(f'\r{Fore.RED}{" " * max_line_length}{Fore.RESET}\r', end='')

    if reset is True:
        print(f'\x1b[{num // 2}B')  # Reset the cursor to the original position with magic


def back_line(num: int, delay: int = 10, index: int = 1):
    # Clear specified line in a typing backspace fashion
    print(f'\x1b[{index}A' + f'\x1b[{num}C', end=' ')
    for i in range(num):
        print(f'\x1b[2D ', end='')
        time.sleep(delay / 1000)
    print('\r', end='')


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


def get_distance(object_pos0: tuple, object_pos1: tuple):
    return math.sqrt(abs((object_pos0[0] - object_pos1[0]) ** 2 + (object_pos0[1] - object_pos1[1]) ** 2))


def check_proximity(object_pos: tuple):
    # Return the distance of the player to an object
    return math.sqrt(abs((object_pos[0] - game_data.MapData.x) ** 2 + (object_pos[1] - game_data.MapData.y) ** 2)) <= \
        game_data.PlayerData.Detection_Distance


def add_item(item_id: int):
    # Add an item by id to a players inventory
    if game_data.PlayerData.Inventory_Accessible:
        item_data = item_info(str(item_id))
        size_calc = game_data.PlayerData.Inventory_Space - item_data.item_size
        if size_calc >= 0:

            # Check for duplicate entries and combine their qty
            dupe = False
            for idx, inv_item in enumerate(game_data.PlayerData.Inventory):
                if inv_item.item_id == item_data.item_id:
                    if not game_data.PlayerData.Inventory[idx].qty + 1 > inv_item.max_qty:
                        # Makes sure to not add items that can't have multiple instances in the inventory
                        dupe = True
                        game_data.PlayerData.Inventory[idx].qty += 1

                        break

            if not dupe:
                game_data.PlayerData.Inventory.append(item_data)
                # print(game_data.PlayerData.Inventory[ind])

        elif size_calc < 0:
            print("Could not add item(s) to your inventory due to lack of space")
    else:
        print("Error: Player Inventory is inaccessible")


def remove_item(item_id: int, qty: int = 1):
    if game_data.PlayerData.Inventory_Accessible:
        for i in game_data.PlayerData.Inventory[::-1]:  # Reverse order search
            if i.item_id == item_id:
                if i.qty > 1:
                    i.qty -= qty
                else:
                    game_data.PlayerData.Inventory.remove(i)
                break


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


def has_item(item_search: str, data_return: bool = False):
    # Check if the player has the item in their inventory
    if str(item_search).isnumeric():  # Check if the player specified an id
        for n in game_data.PlayerData.Inventory:
            if n.item_id == int(item_search):
                if data_return:
                    return n
                else:
                    return True
    else:
        item_search = item_search.replace("-", " ")
        for n in game_data.PlayerData.Inventory:
            if n.name.lower() == item_search.lower():
                if data_return:
                    return n
                else:
                    return True
    return False  # item not found


def item_info(item: str):
    if str(item).isnumeric():
        for i in movement_engine.Data.game_items:
            if i.item_id == int(item):
                return i
        return False
    else:
        for i in movement_engine.Data.game_items:
            if i.name.lower() == item.lower():
                return i  # Item found by name
        return False  # Item not found


def cmove(num: int = 1, direction: str = 'A'):  # Dunno, seems kinda useless, but who will actually read all of this?
    # Move the console cursor
    print(f"\x1b[{num}{direction}", end='')


def map_index(map_id: int):
    # Find and return the map data for the specified id
    maps = [game_data.MainMap, game_data.Floor0, game_data.Floor1, game_data.Floor2, game_data.Floor3,
            game_data.Floor4, game_data.GateKeeper, game_data.FinalFloor]

    if not map_id > len(maps) - 1:
        return maps[map_id]
    else:
        return False


def display_inv():
    # if the map is displayed, clear the map and then display the inventory
    # Display the inventory
    os.system("cls")
    item_spacing = 25
    side_spacing = 5
    element_num = 1  # Which side of the array is printing
    key_num = 0  # The current item to print in the first column
    sub_key_num = 0  # The current item to print in the second column
    # inv_size = len(game_data.PlayerData.Inventory) - 1
    row1 = game_data.PlayerData.Inventory_Space // 2
    inv0 = []
    inv1 = []

    if game_data.PlayerData.Inventory_Space % 2 == 1:
        # If the inventory space num is odd, the first column will print 1 more than the second column
        row1 += 1

    # Initialize the inventory columns
    for x, i in enumerate(game_data.PlayerData.Inventory):
        if x > row1 - 1:
            inv1.append(i)
        else:
            inv0.append(i)

    print(f"{'':<{side_spacing}}", end='')  # Title Side Spacing
    print(f"{Fore.RED}{'Item Name':^{item_spacing}}{'Item QTY':^{item_spacing}}{'Item ID':^{item_spacing}}"
          f"{'Item Name':^{item_spacing}}{'Item QTY':^{item_spacing}}{'Item ID':^{item_spacing}}{Fore.RESET}\n")

    for i in range(game_data.PlayerData.Inventory_Space):
        if element_num == 1:
            print(f"{'':<{side_spacing}}", end='')
            if key_num > len(inv0) - 1:
                # No Item to print
                print(f"{Style.BRIGHT}{Fore.BLACK}{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}"
                      f"{Fore.RESET}", end='')
            else:
                # There is an item to print
                item = inv0[key_num]
                print(f"{item.name:^{item_spacing}}{item.qty:^{item_spacing}}{item.item_id:^{item_spacing}}", end='')
                key_num += 1
            element_num = 2
        elif element_num == 2:
            # Print second row, check to see if requested item exists if so print
            # Check to see if the second column has anything to print

            if sub_key_num > len(inv1) - 1:
                print(f"{Style.BRIGHT}{Fore.BLACK}{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}"
                      f"{Fore.RESET}", end='')
            else:
                item = inv1[sub_key_num]
                print(f"{item.name:^{item_spacing}}{item.qty:^{item_spacing}}{item.item_id:^{item_spacing}}", end='')
                sub_key_num += 1
            element_num = 1  # Set to first column
            print(f"{Fore.RESET}\n", end='')
    print(Fore.RESET + Style.RESET_ALL)  # Create newline at end of printout
    # print([x.name for x in game_data.PlayerData.Inventory])
    # print([x.name for x in inv0])
    # print([x.name for x in inv1])
    game_data.PlayerData.Inventory_Displayed = True
    game_data.PlayerData.command_status = False  # Disable command input


def display_stats():  # Display stats of system and player
    pass


def display_item_info(item_data):  # Get raw item info and display it in formatted statement
    spacing = 30

    item_has = has_item(item_data.item_id)
    print('\n' * 3 + f'{item_data.name:-^20}')
    print(f'{Fore.YELLOW}{"Player has item:":<{spacing}}{[Fore.RED, Fore.GREEN][item_has]}{item_has}')
    print(f'{Fore.YELLOW}{"Item: ":<{spacing}}{item_data.item_id}/{Fore.RED}{len(movement_engine.Data.game_items) - 1}'
          f'{Fore.RESET}')
    print(f'{Fore.YELLOW}{"Item ID:":<{spacing}}{Fore.RESET}{item_data.item_id}')
    print(f'{Fore.YELLOW}{"Item Type:":<{spacing}}{Fore.RESET}{item_data.type}')
    print(f'{Fore.YELLOW}{"Item Max Quantity:":<{spacing}}{Fore.RESET}{item_data.max_qty}')
    print(f'{Fore.YELLOW}{"Item Size:":<{spacing}}{Fore.RESET}{item_data.item_size}')
    print(f'{Fore.YELLOW}{"Damage: ":<{spacing}}{Fore.RESET}{item_data.damage[0]} {Fore.YELLOW}-> '
          f'{Fore.RESET}{item_data.damage[1]}')
    print(f'{Fore.YELLOW}{"Health Regeneration:":<{spacing}}{Fore.RESET}{item_data.health_regen}')
    # print(f'{"Stamina Regeneration:":<{spacing}}{item_data.stamina_regen}')  # Not Implemented yet
    print(f'{Fore.YELLOW}{"Description:":<{spacing}}{Fore.RESET}{item_data.desc}')


def ck(text: str, color: str = None):  # Kind of useless
    return text, color


def process_command(cmd_raw):
    # Process command
    cmd = cmd_raw.lower().split(' ')
    if (len(cmd_raw) > 0 and game_data.HelpPage().cmd_list.__contains__(cmd[0])
            and game_data.MapData.valid_cmd.__contains__(cmd[0])) or cmd[0] == "exit":

        cmd_latter = " ".join(cmd[1:])  # Isolates content after command header
        if cmd[0] == "help" or cmd[0] == "?":  # Print the help page
            system('cls')
            game_data.PlayerData.Inventory_Displayed = True
            display_help(cmd_latter)
        elif cmd[0] == "inventory":  # print the players inventory
            system('cls')
            display_inv()
            gprint(game_data.MQ([ck("\nMove to exit...")]))
        elif cmd[0] == "item-info":  # Print the specified items info
            system('cls')
            # game_data.PlayerData.command_status = False  # Disable command input
            game_data.PlayerData.Inventory_Displayed = True
            game_data.PlayerData.command_status = False
            info = item_info(cmd_latter)
            if info is False:
                err_msg('Invalid Item')
            else:
                display_item_info(info)
                gprint(game_data.MQ([ck("\nMove to exit...")]))
        elif cmd[0] == "stats":  # print system & player statistics
            system('cls')
            display_stats()
        elif cmd[0] == 'drop':  # Remove the specified item from the players inventory
            item = item_info(cmd_latter)
            if item is False:
                err_msg('Invalid Item')
            elif not has_item(item.item_id):
                err_msg('You don\'t have this item')
            else:  # Remove the item from players inventory
                remove_item(item.item_id)
                script = [ck('Dropped', 'yellow'), ck('['), ck(item.name, 'red'), ck(']')]
                sl = 0
                for i in script:
                    sl += len(i[0])

                game_data.MapData.map_idle = True
                system('cls')
                center_cursor(sl)
                gprint(game_data.MQ(script))
                time.sleep(1)
                game_data.MapData.map_idle = False
                movement_engine.show_map(game_data.MapData.current_map)
        elif cmd[0] == "exit":
            game_data.MapData.map_kill = True  # Exit listener thread
            os.system('cls')
            reset_sys_font(30)
            get_max()
            print(f"{'':<{game_data.SysData.max_screen_size[0] // 2}}", end='')
            gprint(MQ([ck("Goodbye :(")]))
            time.sleep(1)
            system('exit')
            game_data.SysData.full_kill = True
        elif cmd[0] == "mp":  # Multiplayer command header

            operations = ["start", "stop", "join", "info"]
            os.system('cls')
            if cmd_latter not in operations:
                script = [ck('Invalid operation.', 'red'), ck(' valid operations are: '),
                          ck(', '.join([x[0] for x in operations]))]
                center_cursor(len(''.join([x[0] for x in operations])))
                gprint(game_data.MQ([script]))
                return

            # Lock Down
            game_data.MapData.map_idle = True

            # Operation Switch
            game_data.SysData.management_operation.append(("con_start", cmd_latter))
    else:
        err_msg('Invalid Command')
    game_data.MapData.current_command = ""  # Reset the inputted command


def management_thread():
    # I probably could have used this many months ago ._.
    operation_index = {
        "con_start": connection_prompt,
    }
    while True:
        if len(game_data.SysData.management_operation) > 0:
            for x in game_data.SysData.management_operation:
                if x[0] in operation_index.keys():
                    Thread(target=operation_index[x[0]](x[1])).start()  # Run function
            game_data.SysData.management_operation.clear()
        time.sleep(0.1)


def connection_prompt(cmd_latter):
    if cmd_latter == "start":
        """
        Order of operations:
            - Pause Map Activity
            - Switch Listener to prompt user to enter server address
            - Attempt connection to server
        """

        game_data.PlayerData.mp_join = True
        # Prompt user for the server address
        gprint(game_data.MQ([ck("Please enter the server address...")]))
        print(f"\n  {Fore.CYAN}>{Fore.GREEN}: {Fore.RESET}", end=' ')
        time.sleep(0.1)

        # Try to hijack main listener capabilities
        game_data.PlayerData.mp_server_address = ""

        while game_data.PlayerData.mp_join:
            time.sleep(0.1)
            continue

        os.system("cls")
        script = [ck('Attempting connection to '), ck(game_data.PlayerData.mp_server_address, 'cyan')]
        center_cursor(len(''.join([x[0] for x in script])))
        gprint(game_data.MQ(script))
        time.sleep(0.4)
        game_data.multiplayer.socket_initial_connect = True
        Thread(target=open_socket, args=(game_data.PlayerData.mp_server_address,)).start()
        while game_data.multiplayer.socket_open_message_status is False:
            continue

        # Socket connection has finished, check to see if the client is connected if not display error message
        if game_data.multiplayer.socket_timeout:
            err_msg("Error: Could not connect to specified server. "
                    "Please check your connection and the server's status")
    elif cmd_latter == "stop":  # Stop the public / private session
        pass
    elif cmd_latter == "leave":  # Leave the global session
        pass
    elif cmd_latter == "join":  # Join the specified session (sessions can be viewed via the 'mp list' command)
        pass
    elif cmd_latter == "info":  # View info on the current connection
        pass
    elif cmd_latter == "list":  # View the list of publicly hosted sessions
        pass

    pass


def err_msg(msg: str):
    game_data.MapData.map_idle = True
    game_data.PlayerData.command_status = False
    system('cls')
    center_cursor(len(msg))
    gprint(MQ([ck(msg, "red")]))
    time.sleep(2)
    movement_engine.show_map(game_data.MapData.current_map)
    game_data.MapData.map_idle = False
    game_data.PlayerData.command_status = True


def center_cursor(x_offset: int, y_offset: int = 0):  # Move the cursor to the middle of the screen with optional offset
    # Maybe change to use /x1b[#A/B/C/D exit code to move cursor
    game_data.MapData.current_command = ""
    print('\n' * ((game_data.SysData.max_screen_size[1] // 2) - y_offset) +
          ' ' * ((game_data.SysData.max_screen_size[0] // 2) - (x_offset // 2)), end='')


def event_handler(event_id: int, event_type: int, reset_map: bool = True):
    if event_id not in game_data.MapDataCache.event_cache:  # Make sure not to duplicate events
        game_data.MapData.map_idle = True  # Stop keyboard listener and printout
        game_data.PlayerData.command_status = False  # Disable command input
        system('cls')
        time.sleep(2)

        # Pull event data
        for x, m in enumerate(game_data.EventData.events[list(game_data.EventData.events.keys())[event_type]]):
            if m.object_id == event_id:
                event_id = x
                break

        # Fetch event data
        for m in game_data.EventData.events[list(game_data.EventData.events.keys())
                                            [event_type]][event_id].event_dialogue:
            if type(m[1]) is tuple:
                delay = m[1][0]
                colour = m[1][1]
            else:
                delay = m[1]
                colour = 'white'

            center_cursor(len(m[0]))
            gprint(game_data.MQ([ck(m[0], colour)]))  # Print specified dialogue
            time.sleep(delay / 1000)  # Pause for specified delay in MS
            system('cls')
        game_data.MapDataCache.event_cache.append(event_id)  # Avoids the event being triggered again
        game_data.MapData.map_idle = False  # Resume the map listener
        game_data.PlayerData.command_status = True  # Re-Enable user command input
        if reset_map:
            movement_engine.show_map(game_data.MapData.current_map)


def question_handler(question_diff: int):
    """
    Order of operations:
        1. Set map movement system into idle
        2. Pull a random question of the specified difficulty
        3. Ask and open input (kb_listener on_press thread will handle question accumulation)
        4. if the user got the question right progress to the next map (return True), if the user got it wrong
           give them the option to retry or to leave (leaving will leave them on the same floor, adds number of tries
           to total to avoid a leave and retry loophole) 3 wrong questions spawns them outside the mine
    """

    question = movement_engine.Data.questions[0][question_diff][
               random.randint(0, len(movement_engine.Data.questions[0][0]))][0]

    # Find the longest line
    question_cache = question.split("\n")
    max_l = 0
    for line in question_cache:
        if len(line) > max_l:
            max_l = len(line)

    os.system("cls")
    print("\n" * (game_data.SysData.max_screen_size[1] // 2) + " " *
                 (game_data.SysData.max_screen_size[0] - (max_l // 2)), end='')

    print(question)
    game_data.PlayerData.question_status = True  # set the input listener to accumulate the answer
    while game_data.PlayerData.question_status:  # Lock the script here until the question input has been satisfied
        time.sleep(0.1)
        continue

    answer = game_data.PlayerData.question_answer


def gprint(queue, speed: int = 25):
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


# Multiplayer Connection Backend
def socket_message(ws, message):  # Socket has received message
    print('Message')


def socket_error(ws, error):  # Socket has encountered error
    print(error)


def socket_close(ws, close_status_code, close_msg):  # Socket has closed
    if game_data.multiplayer.socket_initial_connect:
        game_data.multiplayer.socket_timeout = True
        game_data.multiplayer.socket_initial_connect = False


def socket_open(ws):  # Socket has opened
    if game_data.SysData.connection_status is False:
        game_data.SysData.connection_status = True
        game_data.SysData.multiplayer_socket = ws
        os.system('cls')
        script = [ck('Server Connection Successfully Established')]
        lib.center_cursor(len(''.join([x[0] for x in script])))
        lib.gprint(game_data.MQ(script))



def open_socket(ws_addr):
    websocket.enableTrace(True)
    game_data.SysData.multiplayer_socket = websocket.WebSocketApp(ws_addr,
                                                                  on_open=socket_open,
                                                                  on_message=socket_message,
                                                                  on_close=socket_close,
                                                                  on_error=socket_error,)
    websocket.setdefaulttimeout(2)
    game_data.SysData.multiplayer_socket.run_forever()

