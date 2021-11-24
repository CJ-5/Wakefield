from colorama import Fore, Back, Style
import sys
from dataclasses import dataclass
import lib


class PlayerData:
    # Dynamic Data, DO NOT SLOT
    Inventory_Displayed = False  # Is the inventory currently displayed on screen
    cur_inv_display_size = None  # The amount of characters that the current inventory display takes up
    Health = 100  # Players current health
    Inventory_Space = 26  # Players current max inventory size
    Inventory_Accessible = False  # Is the players inventory currently accessible
    Inventory = []  # Players current inventory populated with InvItem Objects


class StaticData:
    __slots__ = ("movement_blacklist", "map_spacing", "game_items")

    def __init__(self):
        self.movement_blacklist = ["X"]  # The spots the player is not allowed to move onto
        self.map_spacing = 2  # The amount of spacing between each character on the map
        self.game_items = [  # The in game item data
            lib.InvItem("Ol' Reliable Broad Sword", 0, 1, 1, 3, "weapon", (3, 6), "Its your sword a bit rusty but"
                                                                                  "has always been reliable")
        ]


class MapData:
    y = 0
    x = 0
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
        self.ind_def = {"use": "Usage (use [item]): Uses the specified item (if it is valid for the situation)",
                        "inventory / inv": "Usage (inventory) | (inv): Displays your current inventory"}

# def test():
#     class A:
#         __slots__ = ('x', 'y')
#
#         def __init__(self):  # Is run automatically
#             self.x = "test"


class MainMap:  # Main starting area Map
    # Blank Row ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    __slots__ = ('map_name', 'map_array', 'map_desc', 'valid_moves')  # Total Memory Optimization stuff

    def __init__(self):
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Main Area" + Style.RESET_ALL
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

