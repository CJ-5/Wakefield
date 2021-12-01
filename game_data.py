from colorama import Fore, Back, Style
import sys
from dataclasses import dataclass
import lib


class PlayerData:
    Inventory_Displayed = False  # Is the inventory currently displayed on screen
    cur_inv_display_size = 3  # The amount of characters that the current inventory display takes up
    Health = 100  # Players current health
    Inventory_Space = 13  # Players current max inventory size
    Inventory_Accessible = False  # Is the players inventory currently accessible
    Inventory = []  # Players current inventory populated with InvItem Objects


#  NPC and Enemy classes are NOT done
@dataclass()
class EnemyData:
    Entity_id: int  # The spawn id of the enemy
    Name: str  # The display name of the enemy
    Health: int  # The Health of the enemy
    max_inst: int  # The max amount of this enemy that can spawn on a valid map


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
    max_screen_size = ()  # The max size of the console in rows / columns
    hwnd = None  # PID


class Demo:
    demo_mode = True  # If program is in demo mode
    help_demo = True  # If the help command demo has been completed
    inventory_demo = True
    item_info_demo = True


class MapData:
    # General Map Data
    y = 0
    x = 0
    valid_cmd = []
    demo_mode = False
    current_map = None
    map_kill = False
    last_char = ""
    current_command = ""


class HelpPage:
    __slots__ = ('cmd_list', 'ind_def')

    # cmd_list: Command List
    # ind_def: Individual Definitions
    def __init__(self):
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
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy')  # Total Memory Optimization stuff

    def __init__(self):
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Main Area" + Style.RESET_ALL
        self.npc = []
        self.enemy = None  # No enemies can spawn on this map
        self.map_array = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", ""],
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
                     ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "x", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
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
                     ["X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]]

