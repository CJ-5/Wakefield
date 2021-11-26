#  Holds the main functions that operate the backend of the game (e.g battle system)
import movement_engine
import time
from colorama import init
from dataclasses import dataclass
from colorama import Fore, Back, Style
import game_data
import sys


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


def process_command():
    # Pull the Current command value and process it
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


def display_inv():
    # Display the inventory
    reset_cursor = False
    if game_data.PlayerData.Inventory_Displayed is True:
        # Clear the amount of lines that are specified by the cur_inv_display_size value
        reset_cursor = True
        print(f"\x1b[{game_data.PlayerData.cur_inv_display_size}A")

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
        print(f"{'':<10}", end='')

        if i > inv_size:
            # Item is out of total inventory index
            # Print Blank Row
            print(f"{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}", end='')
            if element_num == 2:
                print("\n", end='')
                element_num = 1
            else:
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
                print(f"{item.name:^{item_spacing}}"
                      f"{item.qty:^{item_spacing}}"
                      f"{item.item_id:^{item_spacing}}", end='')
            else:
                print(f"{'*':^{item_spacing}}{'*':^{item_spacing}}{'*':^{item_spacing}}", end='')
            element_num = 1  # Set to first column
            sub_key_num += 1

            print(f"{Fore.RESET}", end='')
            print("\n", end='')
    if reset_cursor is True:
        print(f'\x1b[{game_data.PlayerData.cur_inv_display_size // 2}B')


@dataclass()
class MQ:
    messages: list


def ck(text: str, color: str = None):
    return text, color


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
