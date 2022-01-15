from colorama import Fore, Back, Style
from dataclasses import dataclass
import lib
import colorama


# Because who needs a config file right?


# Coordinates with player stats
class PlayerData:
    Inventory_Displayed = False  # Is the inventory currently displayed on screen [Redundant]
    question_answer = ""  # The accumulated answer
    question_status = False  # Is the player currently answering a question
    question_attempt = 0  # The amount of times the player has tried to answer the question

    battles_won = 0  # How many battles have been won
    battles_lost = 0  # How many battles have been lost
    battles = battles_won + battles_lost  # The total amount of battles played
    battle_turn = 0  # How many turns are in the current battle
    in_battle = False  # Whether the player is in a battle
    battle_action: str = ''  # The current action to be processed
    battle_damage_player = 0  # The current total damage dealt to the player from the enemy
    battle_damage_enemy = 0  # The current total damage dealt to the enemy from the player
    battle_inventory = False  # Whether the player is looking at the inventory during battle
    battle_action_processing = False

    item_info_displayed = False  # Whether the item info screen is displayed or not
    cur_inv_display_size = 3  # The amount of characters that the current inventory display takes up
    Health = 100  # Players current health
    health_recovery = 5  # The amount of hp that the player recovers per move (out of battle)
    crit_mod = 25  # Critical Modifier increases damage by x % when attacking
    crit_chance = 3  # The percent chance of hitting a critical attack
    defense = None  # To be implemented
    player_level = 0  # The players current level
    total_xp = 0
    exp_scaling = 6  # The scaling of exp required to advance to the next level
    exp_lvl = player_level * exp_scaling  # XP required for next level
    level_cap = 10  # Player level cap
    Inventory_Space = 13  # Players current max inventory size
    Inventory_Accessible = False  # Is the players inventory currently accessible
    command_status = False  # Whether the player is allowed to enter commands
    Inventory = []  # Players current inventory populated with InvItem Objects
    Inv0 = []
    Inv1 = []
    Detection_Distance = 3  # The distance that the player needs to be within in order to see hidden objects


@dataclass()
class EnemyData:
    Entity_id: int  # The spawn id of the enemy
    Name: str  # The display name of the enemy
    Health: int  # The Health of the enemy
    base_level: int  # Enemy base level
    display_char: str
    display_colour: colorama.Fore
    Attacks: list  # Holds attack data from attack class
    xp_drop: tuple = (0, 0)  # The amount of xp that the enemy drops when killed
    cur_lvl: int = 0  # Auto Generated


# Class instance for the creation of a NPC entity
@dataclass()
class NPCData:
    Entity_id: int  # Entity ID of the npc
    Name: str  # Display name of the NPC
    Type: int = 0  # 0: Mass NPC (No shop or extra quest)


class StaticData:  # Core Game Data
    __slots__ = ("movement_blacklist", "tile_data", "map_spacing", "game_items", "enemies", "lib_spacing_size",
                 "questions")

    def __init__(self):
        self.tile_data = ["1", "2"]  # Specifies which tile types have data
        self.movement_blacklist = ["X", "0"]  # The spots the player is not allowed to move onto
        self.map_spacing = 2  # The amount of spacing between each character on the map
        self.lib_spacing_size = 160  # Equivalent to 1 inventory row worth of characters
        self.game_items = [  # The in game item data
            lib.InvItem("Ol' Reliable Broad Sword", 0, 1, 1, 3, "weapon", (3, 6), 0, 0, "Its your sword a bit rusty but"
                                                                                        "has always been reliable"),
            lib.InvItem("Apple", 1, 1, 10, 1, "consumable", (0, 0), 10, 5, "Its an apple"),
            lib.InvItem("Bread", 2, 1, 5, 2, "consumable", (0, 0), 15, 10, "Its bread, at least it is not moldy"),
            lib.InvItem("God Sword", 3, 1, 1, 3, "weapon", (99, 120), 0, 0, "Infinite Damage"),
        ]
        self.enemies = [EnemyData(0, "Test_Enemy", 100, 10, "☻", Fore.RED, [], (3, 10))]  # Holds enemy data

        # Questions are divided up into different difficulty tiers and have a corresponding timeouts
        # Questions should be in tuples that list the answer(s)
        self.questions = ([[], [], []], [15000, 10000, 6000])


class SysData:
    max_screen_size = ()  # The max size of the console in rows / columns (x, y)
    hwnd = None  # PID
    full_kill = False
    main_listener = None
    demo_listener = None
    question_listener = None


@dataclass()
class Event:
    object_id: int  # The ID of the door/item/npc to bind the event to when the map loads
    event_dialogue: list  # Change events to be intractable in the future


class StoryData:  # Event trigger data
    town_entered = False
    dungeon_final_boss = False


class EventData:  # Event Dialogue Data
    events = {
        "door": [Event(0, [("You found it", 1000), ("You actually found a new dungeon entrance, that looks "
                                                    "like it hasn't been touched in thousands of years!", 1000),
                           ("Now then...", 1000), ("Its time you start your Adventure!", 2000)])],
        "npc": [],
        "item": []
    }


class Demo:
    demo_mode = True  # If program is in demo mode
    help_demo = True  # If the help command demo has been completed
    inventory_demo = True
    item_info_demo = True
    stats_demo = True


class MapDataCache:
    doors_found = {}  # Which doors the player has found (for doors that do not have multiple positions)
    main_area_city = False  # The access status of the city area of the main map
    event_cache = []  # Which events have been triggered and are to be ignored


class MapData:
    # General Map Data
    y = 0
    x = 0
    space_buffer = 3
    valid_cmd = []  # Which commands are valid in the current situation
    map_displayed = False
    current_map = None  # Holds the entirety of all current map data
    map_idle = False  # Put map listener into sleep mode without fully killing it
    movement_idle = False
    d_exit_rest = True  # The player has just left the dungeon, override the last_char calculation
    map_kill = False
    demo_kill = False
    lmc = (0, 0)  # The coordinate of the entrance to the dungeon  (Only valid for main map entrances)
    last_char = ""
    current_command = ""
    y_max = 0  # The max y coordinate  [Used for proximity calculations]
    ici = {'-': colorama.Fore.GREEN
           }  # Icon color index, declares what the icons display colour should be when shown (Only include valid icons)
    # Note: ici is part of the gen 2 movement script aka 'move_char()'
    movement = []  # should contain tuples of movement to display, so it can be cleared and moved to a new location
    csq = []


@dataclass()
class MQ:
    messages: list


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
    InvID: int = 0  # Which column the item will appear in. [Auto-Generated]


@dataclass()
class DoorData:
    door_id: int
    map_warp: int  # id of the map this door leads to
    symbol: str  # The symbol of the actual door (used in map data)
    symbol_alt: str  # The symbol displayed in the doors place (if prox_check is True)
    symbol_color: colorama.Fore  # Color of symbol when displayed
    symbol_alt_color: colorama.Fore  # Color of alt symbol when displayed
    prox_check: bool  # Whether to perform proximity check or not
    pos: list[tuple]  # valid positions for the doors
    floor_progress: tuple = (False, 0)  # Whether the door is a floor door and therefore triggers the question system
    # int represents the difficulty of the question
    multiple_pos: bool = False  # Auto generated by the door init function, no need to manually assign
    event: bool = False  # Whether the door has an event bound to it (Automatically assigned)
    valid: bool = True  # Declares if the player can access this door


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


class MainMap:  # Main starting area Map
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 0
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Main Area" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = None  # No enemies can spawn on this map
        self.door_data = [DoorData(0, 1, chr(9688), "-", Fore.BLUE, Fore.GREEN, True, [(9, 25)], (True, 0))]
        self.map_array = [
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "-", "-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["-", "-", "-", "-", "", "", "", "", "", "", "", "x", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
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
            ["X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]]


class Floor0:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 1
        self.map_desc = "Dungeon Floor 0"
        self.map_name = Fore.GREEN + "Floor 0" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = None  # No enemies can spawn on this map
        self.door_data = [DoorData(1, 0, chr(9688), "-", Fore.BLUE, Fore.GREEN, False, [(0, 14)]),
                          DoorData(2, 2, chr(9688), "", Fore.BLUE, Fore.BLACK, True, [(20, 11), (18, 15)], (True, 0))]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["1", "x", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]


class Floor1:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 2
        self.map_desc = "Dungeon Floor 1"
        self.map_name = Fore.GREEN + "Floor 1" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [(0, (7, 16))]
        self.door_data = [DoorData(3, 1, chr(9688), "-", Fore.BLUE, Fore.GREEN, False, [(0, 12)]),
                          DoorData(4, 3, chr(9688), "", Fore.BLUE, Fore.BLACK, False, [(23, 11)], (True, 1))]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "2", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "x", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", ""],
            ["1", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "1"],
            ["", "", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]
