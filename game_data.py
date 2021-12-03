from colorama import Fore, Back, Style
import sys
from dataclasses import dataclass
import lib
import colorama
# Because who needs a config file right?


# Coordinates with player stats
class PlayerData:
    Inventory_Displayed = False  # Is the inventory currently displayed on screen
    cur_inv_display_size = 3  # The amount of characters that the current inventory display takes up
    Health = 100  # Players current health
    Inventory_Space = 13  # Players current max inventory size
    Inventory_Accessible = False  # Is the players inventory currently accessible
    command_status = False  # Whether or not the player is allowed to enter commands
    Inventory = []  # Players current inventory populated with InvItem Objects
    Detection_Distance = 3  # The distance that the player needs to be within in order to see hidden objects


@dataclass()
class AK:
    id: int  # The id of the attack
    name: str  # The name of the attack
    attack_msg: list  # What is message is displayed when the attack hits you


#  NPC and Enemy classes are NOT done, in fact the are shit
@dataclass()
class EnemyData:
    Entity_id: int  # The spawn id of the enemy
    Name: str  # The display name of the enemy
    Health: int  # The Health of the enemy
    Max_inst: int  # The max amount of this enemy that can spawn on a valid map
    Attacks = []


# Class instance for the creation of a NPC entity
@dataclass()
class NPCData:
    Entity_id: int  # Entity ID of the npc
    Name: str  # Display name of the NPC
    Type: int = 0  # 0: Mass NPC (No shop or extra quest)


class StaticData:
    __slots__ = ("movement_blacklist", "map_spacing", "game_items", "enemies", "lib_spacing_size")

    def __init__(self):
        self.movement_blacklist = ["X", "0"]  # The spots the player is not allowed to move onto
        self.map_spacing = 2  # The amount of spacing between each character on the map
        self.lib_spacing_size = 160  # Equivalent to 1 inventory row worth of characters
        self.game_items = [  # The in game item data
            lib.InvItem("Ol' Reliable Broad Sword", 0, 1, 1, 3, "weapon", (3, 6), 0, 0, "Its your sword a bit rusty but"
                                                                                        "has always been reliable"),
            lib.InvItem("Apple", 1, 1, 10, 1, "consumable", (0, 0), 10, 5, "Its an apple"),
            lib.InvItem("Bread", 2, 1, 5, 2, "consumable", (0, 0), 15, 10, "Its bread, at least it is not moldy"),
            lib.InvItem("Sword", 3, 1, 1, 3, "weapon", (3, 6), 0, 0, "Its your sword a bit rusty but"
                                                                     "has always been reliable"),
        ]
        self.enemies = [EnemyData(0, "Test_Enemy", 100, 5)]  # Holds enemy data


class SysData:
    max_screen_size = ()  # The max size of the console in rows / columns (x, y)
    hwnd = None  # PID


class Demo:
    demo_mode = True  # If program is in demo mode
    help_demo = True  # If the help command demo has been completed
    inventory_demo = True
    item_info_demo = True
    stats_demo = True


class MapDataCache:
    doors_found = {}  # Which maps the player has found the door on
    main_area_city = False  # The access status of the city area of the main map


class MapData:
    # General Map Data
    y = 0
    x = 0
    valid_cmd = []
    map_displayed = False
    current_map = None
    map_kill = False
    last_char = ""
    current_command = ""
    y_max = 0  # The max y coordinate  [Used for proximity calculations]


@dataclass()
class TileData:
    # Tile data, I hate this
    tile_type: int  # 0: door


@dataclass()
class DoorData:
    map_warp: int  # id of the map this door leads to
    symbol: str  # The symbol of the actual door
    symbol_alt: str  # The symbol displayed in the doors place (if prox_check is True)
    prox_check: bool  # Whether or not to display the door only when the player is within detection distance
    pos: tuple


class HelpPage:
    __slots__ = ('cmd_list', 'ind_def')

    # cmd_list: Command List
    # ind_def: Individual Definitions
    def __init__(self):
        self.cmd_list = ["help", "?", "inventory", "item_info", "stats"]
        self.ind_def = {"use": "Usage (use [item name / item id]): Uses the specified item "
                               "(if it is valid for the situation)",
                        "inventory / inv": "Usage (inventory) | (inv): Displays your current inventory",
                        "item_info": "Usage (item_info [item name / item id] | Displays info on the specified item"}

# def test():
#     class A:
#         __slots__ = ('x', 'y')
#
#         def __init__(self):  # Is run automatically
#             self.x = "test"


class MainMap:  # Main starting area Map
    # Blank Row ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'door_alt', 'map_id', 'door_pos', 'door_type',
                 'extra_doors')

    def __init__(self):
        self.map_id = 0
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Main Area" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = None  # No enemies can spawn on this map
        self.extra_doors = []
        self.door_alt = ('-', Fore.GREEN)
        self.door_pos = [(9, 25)]
        self.door_type = "1"
        self.map_array = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "1", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
                     ["X", "X", "x", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]]


class Floor0:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'door_alt', 'map_id', 'door_function')

    def __init__(self):
        self.map_id = 1
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Floor 0" + Style.RESET_ALL
        self.npc = []
        self.enemy = None  # No enemies can spawn on this map
        self.door_alt = ('-', Fore.GREEN)
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]
