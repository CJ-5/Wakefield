#  Holds the main functions that operate the backend of the game (e.g battle system)
import movement_engine
import time
from colorama import init
from dataclasses import dataclass
from colorama import Fore, Back, Style
import game_data


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
    damage: int = None  # Damage items deals (does not apply to non-weapon type items)
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
                    game_data.PlayerData.Inventory[idx].qty += 1
                    ind = idx
                    dupe = True

            if dupe is False:
                game_data.PlayerData.Inventory.append(item_data)
            print(game_data.PlayerData.Inventory[ind])

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
