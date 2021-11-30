#  Holds the main functions that operate the backend of the game (e.g battle system)
import os
from os import system
import movement_engine
import time
from colorama import init
from dataclasses import dataclass
from colorama import Fore, Back, Style
import game_data
import sys
from ctypes import windll
import win32gui
import win32gui, win32com.client
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


def process_command(cmd):
    # Process command
    cmd = cmd.lower().split(' ')
    if game_data.MapData.valid_cmd.__contains__(cmd[0]):
        if cmd[0] == "help":  # Print the help page
            if game_data.Demo.help_demo is True:
                game_data.MapData.map_kill = True
                game_data.Demo.help_demo = False
            display_help()
        elif cmd[0] == "item_info":  # Print the specified items info
            print(cmd)  # Debug Code
        elif cmd[0] == "inventory":  # print the players inventory
            print(cmd)  # Debug Code
        elif cmd[0] == "stats":  # print system & player statistics
            print(cmd)  # Debug Code
    else:
        gprint(MQ([ck("Invalid Command")]))


user32 = windll.user32
user32.SetProcessDPIAware()  # optional, makes functions return real pixel numbers instead of scaled values

full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


def is_full_screen():
    try:
        hwnd = user32.GetForegroundWindow()
        rect = win32gui.GetWindowRect(hwnd)  # Get the size of the
        print(rect)
        print(full_screen_rect)
        return rect == full_screen_rect
    except:
        return False


def maximize_console(lines=None):
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    SW_MAXIMIZE = 3
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
            subprocess.check_call('mode.com con cols={} lines={}'.format(
                                    cols, lines))
            user32.ShowWindow(hwnd, SW_MAXIMIZE)
    finally:
        os.close(fd)


def clear_line(num: int, max_line_length: int, reset: bool, multiple: bool = True, direction: str = 'A'):
    # Clear the specified amount of lines
    # Num = The amount of line to clear
    # Max_Line_Length = The length of the largest line amongst the lines being cleared
    # Reset = Whether or not to reset the cursor after clearing specified line amount
    # Multiple = whether or not to clear all lines specified by num
    # direction = The direction to clear the lines (default: A [Up])

    if multiple is True:
        for i in range(num):
            print(f'\x1b[{1}{direction.upper()}', end='')
            print(f'\r{Fore.RED}{" "*max_line_length}{Fore.RESET}', end='')
    else:
        print(f'\x1b[{num}{direction.upper()}')
    if reset is True:
        print(f'\x1b[{num // 2}B')  # Reset the cursor to the original position with magic


def display_help(cmd: str = None):
    help_page = game_data.HelpPage()
    # Display the help page for all or just one command
    if cmd is None:
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


def item_info(item_id: int, item_name: str = None):
    # Create Instance of game items

    if item_id is None and item_name is None:
        print("Error: No Item specified @ InvItemInfo Call")
    elif item_id is None:  # Look for item info by name (Slower)
        for n in movement_engine.Data.game_items:
            if n.name == item_name:
                return n
    elif item_name is None:  # Directly index the item by the index (equivalent to the id) (Faster)
        return movement_engine.Data.game_items[item_id]


def clear_inventory_display():
    # Clear the inventory print out
    game_data.PlayerData.Inventory_Displayed = False
    print(game_data.PlayerData.cur_inv_display_size)
    clear_line(game_data.PlayerData.cur_inv_display_size, len(game_data.MapData.current_map.map_array[0]), True, True)
    game_data.PlayerData.cur_inv_display_size = 0


def display_inv():
    # Display the inventory
    if game_data.PlayerData.Inventory_Displayed is True:
        # Clear the amount of lines that are specified by the cur_inv_display_size value
        clear_inventory_display()

    game_data.PlayerData.Inventory_Displayed = True

    # Note Only for use in display_inv()
    item_spacing = 25
    # print the inventory
    element_num = 1  # Which side of the array is printing
    key_num = 0  # The current item to print in the first column
    sub_key_num = 0  # The current item to print in the second column
    inv_size = len(game_data.PlayerData.Inventory) - 1
    row1 = game_data.PlayerData.Inventory_Space // 2

    if game_data.PlayerData.Inventory_Space % 2 == 1:
        # If the inventory space num is odd, the first column will print 1 more than the second column
        row1 += 1

    print(f"{'':<10}", end='')
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
                print(f"{'':<10}", end='')
                print(f"{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}", end='')
                element_num = 2
        elif element_num == 1:
            item = game_data.PlayerData.Inventory[key_num]
            print(f"{Fore.RED}", end='')
            # Check to see if requested item exists if so print
            print(f"{item.name:^{item_spacing}}"
                  f"{item.qty:^{item_spacing}}"
                  f"{item.item_id:^{item_spacing}}", end='')
            element_num = 2  # Set to second column
            print(f"{Fore.RESET}", end='')
            key_num += 1

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
            game_data.PlayerData.cur_inv_display_size += 1
    print()  # Create newline at end of printout


@dataclass()
class MQ:
    messages: list


def ck(text: str, color: str = None):
    return text, color


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
            print(colors_list[msg[1]], end='')
            for char in msg[0]:
                print(char, end='')
                time.sleep(delay)
            print(Fore.RESET, end='')
        else:
            for char in msg[0]:
                print(char, end='')
                time.sleep(delay)
    print()
