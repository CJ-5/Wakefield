from colorama import Fore, Back, Style
from dataclasses import dataclass
import colorama


# Because who needs a config file right?


# Coordinates with player stats
class PlayerData:
    question_answer = ""  # The accumulated answer
    question_status = False  # Is the player currently answering a question
    question_processing = False
    question_attempt = 0  # The amount of times the player has tried to answer the question

    # Battle Data
    battles_won = 0  # How many battles have been won
    battles_lost = 0  # How many battles have been lost
    battles = battles_won + battles_lost  # The total amount of battles played  [Needs to be called recursively]
    battle_turn = 0  # How many turns are in the current battle
    in_battle = False  # Whether the player is in a battle
    battle_action: str = ''  # The current action to be processed
    battle_damage_player = 0  # The current total damage dealt to the player from the enemy
    battle_damage_enemy = 0  # The current total damage dealt to the enemy from the player
    battle_inventory = False  # Whether the player is looking at the inventory during battle
    battle_action_processing = False  # Locks thread until the player has entered an action
    battle_run_warning = False  # Listener Lock
    battle_run_response = False  # Player Response

    Inventory_Displayed = False  # Is the inventory currently displayed on screen [Redundant]
    item_info_displayed = False  # Whether the item info screen is displayed or not
    Health = 100  # Players current health
    Health_Max = 100  # The player's max health
    regen_max_warn = False  # Trigger regen over max warning
    regen_max_warn_response = False  # regen over max warning response
    health_recovery = 5  # The amount of hp that the player recovers per move (out of battle)
    jinx_mod = 25  # % Chance of the enemy's attack failing (Nice)
    crit_mod = 10  # Critical Attack modifier. Yes its is overpowered, but I am the developer and you are not. -_-
    crit_chance = 12  # The percent chance of hitting a critical attack
    defense = None  # To be implemented
    player_level = 0  # The players current level
    total_xp = 0
    exp_scaling = 10  # The scaling of exp required to advance to the next level
    exp_lvl = 0  # XP required for next level  [Auto - Generated]
    level_cap = 30  # Player level cap
    Inventory_Space = 23  # Players current max inventory size
    Inventory_Accessible = False  # Is the players inventory currently accessible
    command_status = False  # Whether the player is allowed to enter commands
    Inventory = []  # Players current inventory populated with InvItem Objects
    Detection_Distance = 3  # The distance that the player needs to be within in order to see hidden objects


# Class instance for the creation of a NPC entity
@dataclass()
class NPCData:
    Entity_id: int  # Entity ID of the npc
    Name: str  # Display name of the NPC
    Type: int = 0  # 0: Mass NPC (No shop or extra quest)


@dataclass()
class AttackData:
    name: str = ''  # The name of the attack
    damage: range = range(0, 1)  # Base attack range
    dia: str = ""  # The dialogue when the enemy uses the attack


@dataclass()
class LT:
    # Loot Table class
    common_items: list  # Item IDs of common items
    uncommon_items: list  # Item IDs of uncommon items
    rare_items: list  # Item IDs of rare items
    super_rare_items: list  # Item IDs of super rare items
    common_item_chance: range = range(0, 0)  # The chance of a random common item to be picked
    uncommon_item_chance: range = range(0, 0)  # The chance of a random uncommon item to be picked
    rare_item_chance: range = range(0, 0)  # The chance of a random rare item to be picked
    super_rare_item_chance: range = range(0, 0)  # The chance of a random super rare item to be picked


@dataclass()
class EnemyData:
    Entity_id: int  # The spawn id of the enemy
    Name: str  # The display name of the enemy
    Health: int  # The Health of the enemy
    base_level: int  # Enemy base level
    display_char: str
    display_colour: colorama.Fore
    Attacks: list  # Holds attack data from attack class
    xp_drop: tuple  # The amount of xp that the enemy drops when killed
    loot_table: LT  # Use Loot Table Class (LT)
    loot_range: range  # How many items the enemy will drop on death
    move: bool  # If the enemy can move
    escape: bool = True
    cur_lvl: int = 0  # [Auto Generated] The calculated temporary level of the enemy


class LootTables:
    base_loot = LT([2, 3, 4, 5, 6, 7, 23, 24, 26, 31, 12, 17, 18], [0, 21, 29, 9], [], [],
                   common_item_chance=range(0, 80), uncommon_item_chance=range(80, 100))
    mid_level = LT(base_loot.common_items, base_loot.uncommon_items + [14, 16], [1, 22, 19], [],
                   common_item_chance=range(0, 30), uncommon_item_chance=range(30, 80), rare_item_chance=range(80, 100))
    high_level = LT(base_loot.common_items, mid_level.uncommon_items, mid_level.rare_items + [14, 11, 27, 28],
                    [], common_item_chance=range(0, 30), uncommon_item_chance=range(30, 80),
                    rare_item_chance=range(80, 100))
    boss = LT([], [], [], [32], super_rare_item_chance=range(20, 100))


class StaticData:  # Core Game Data
    __slots__ = ("movement_blacklist", "tile_data", "map_spacing", "game_items", "enemies", "lib_spacing_size",
                 "questions")

    def __init__(self):
        self.tile_data = ["1", "2"]  # Specifies which tile types have data
        self.movement_blacklist = ["X", "0"]  # The spots the player is not allowed to move onto
        self.map_spacing = 2  # The amount of spacing between each character on the map
        self.lib_spacing_size = 160  # Equivalent to 1 inventory row worth of characters
        self.game_items = [  # The in game item data
            InvItem('Small HP Potion', 0, 1, 5, 2, health_regen=(30, 35), desc='Small Healing Potion, increases hp.'),
            InvItem('Medium HP Potion', 1, 1, 3, 2, health_regen=(40, 43), desc='Medium Healing Potion, increases hp.'),
            InvItem('Sausage', 2, 1, 10, 1, health_regen=(15, 16), desc='Meat with questionable ingredients.'),
            InvItem('Pretzel', 3, 1, 10, 1, health_regen=(12, 13), desc='It\'s gone a little stale.'),
            InvItem('Bread', 4, 1, 5, 2, health_regen=(14, 16), desc='This is a whole loaf of bread. '
                                                                     'At least its not moldy'),
            InvItem('Meat', 5, 1, 5, 1, health_regen=(10, 14), desc='Keep in mind this dropped from a monster'),
            InvItem('Moldy Bread', 6, 1, 3, 2, health_regen=(-2, 1), desc='A little penicillin (mostly) never hurts.'),
            InvItem('Apple', 7, 1, 8, 1, health_regen=(12, 14), desc='Keeps the doctor away'),
            InvItem('Meat Sandwich', 21, 1, 5, 1, health_regen=(16, 18), desc='Two pieces of bread '
                                                                              'with raw meat in between'),
            InvItem('Veal', 22, 1, 3, 2, health_regen=(32, 42), desc='This poor deer...'),
            InvItem('Carrot', 23, 1, 10, 1, health_regen=(3, 4), desc='Fresh from the ground'),
            InvItem('Potato', 24, 1, 10, 1, health_regen=(2, 3), desc='One of the most versatile vegetables.'),
            InvItem('Double Baked Potato', 25, 1, 10, 1, health_regen=(6, 7), desc='Baked not once... BUT TWICE!'),
            InvItem('Bun', 26, 1, 8, 1, health_regen=(3, 5), desc='Fresh from the local dungeon floor'),
            InvItem('Cheese Bread', 27, 1, 10, 1, health_regen=(25, 26), desc='Bread but with cheese'),
            InvItem('Soup', 28, 1, 5, 1, health_regen=(22, 23), desc='Full of nutrients such as, such as potato, and '
                                                                     'uh... Potato.'),
            InvItem('Water Flask', 29, 1, 3, 1, health_regen=(12, 14), desc='A conveniently filled flask.'),
            InvItem('Cheese Wheel', 30, 1, 2, 1, health_regen=(12, 14), desc='cheese.'),
            InvItem('Rotten Meat', 31, 1, 5, 1, health_regen=(-13, 1), desc='You tore this from a monsters corpse. '
                                                                            'Let that set in.'),

            InvItem('Hero\'s Sword', 8, 1, 1, 3, type='weapon', damage=(500, 550), desc='That\'s a lot of damage'),
            InvItem('Iron Broadsword', 9, 1, 1, 2, type='weapon', damage=(14, 16), desc='Pretty sharp for a '
                                                                                      'hunk of raw metal'),
            InvItem('Steel Broadsword', 10, 1, 1, 2, type='weapon', damage=(15, 17), desc='Nice sword bro'),
            InvItem('Titanium Broadsword', 11, 1, 1, 2, type='weapon', damage=(18, 25), desc='Means business'),
            InvItem('Wood Training Sword', 12, 1, 1, 2, type='weapon', damage=(1, 2), desc='Used for children to '
                                                                                           'practice with'),
            InvItem('Rusty Broadsword', 13, 1, 1, 2, type='weapon', damage=(8, 11), desc='It has a lot of chips in it, '
                                                                                        'and most of the blade is '
                                                                                        'rusted out too.'),
            InvItem('Bandit Knife', 14, 1, 1, 1, type='weapon', damage=(6, 9), desc='Short enough to have in a belt '
                                                                                    'loop '
                                                                                    'and not appear suspicious'),
            InvItem('Kitchen Cleaver', 15, 1, 1, 1, type='weapon', damage=(6, 8),
                    desc='Is this from the butchers shop?'),
            InvItem('Wooden Club', 16, 1, 1, 2, type='weapon', damage=(4, 7), desc='Is this a tree branch with a '
                                                                                   'handle?'),
            InvItem('Log', 17, 1, 1, 3, type='weapon', damage=(5, 6), desc='This is literally a branch from a tree'),
            InvItem('Rusty Pole', 18, 1, 1, 2, type='weapon', damage=(4, 5), desc='Looks like reba-... Totally not '
                                                                                  'rebar.'),
            InvItem('Machete', 19, 1, 1, 2, type='weapon', damage=(18, 20), desc='Cut down your way through jungles.'),
            InvItem('Katana', 32, 1, 1, 2, type='weapon', damage=(80, 150), desc='Used by samurai in ancient times, '
                                                                                 'how did it get here?'),
            InvItem('null', 20, 0, 1, 0, type='weapon', damage=(8888, 9999), desc='Cut the Earth in half.'),
        ]  # Max ID: 32

        self.enemies = [
            EnemyData(0, 'Slime', 3, 1, '◉', Fore.WHITE, [AttackData('Jump Attack', range(2, 3))], (4, 6),
                      loot_table=LootTables.base_loot, move=True, loot_range=range(1, 2)),
            EnemyData(1, 'Ghost', 5, 2, '•', Fore.WHITE, [AttackData('Phase', range(4, 6)),
                                                          AttackData('Haunt', range(5, 8))], (3, 7),
                      loot_table=LootTables.base_loot, move=True, loot_range=range(2, 3)),
            EnemyData(2, 'Undead', 4, 2, 'µ', Fore.WHITE, [AttackData('Flail', range(3, 7)),
                                                           AttackData('Rot', range(4, 6))], (5, 8),
                      loot_table=LootTables.base_loot, move=True, loot_range=range(2, 3)),
            EnemyData(3, 'Shade', 5, 4, 'Ä', Fore.WHITE, [AttackData('Summon', range(6, 8)),
                                                          AttackData('Phase', range(8, 10))], (6, 9),
                      loot_table=LootTables.mid_level, move=True, loot_range=range(1, 3)),
            EnemyData(4, 'Brute', 8, 4, '*', Fore.WHITE, [AttackData('Smash', range(8, 10)),
                                                          AttackData('Rage', range(12, 13))], (8, 11),
                      loot_table=LootTables.mid_level, move=True, loot_range=range(2, 4)),
            EnemyData(5, 'Reaper', 24, 8, '>', Fore.CYAN, [AttackData('Slash', range(12, 15)),
                                                           AttackData('Death Incarnate', range(20, 25))], (9, 10),
                      loot_table=LootTables.high_level, move=True, loot_range=range(2, 5)),
            EnemyData(6, 'Giant', 20, 10, '=', Fore.CYAN, [AttackData('Rock Throw', range(14, 22)),
                                                           AttackData('Tree Javelin', range(15, 22))], (10, 13),
                      loot_table=LootTables.high_level, move=True, loot_range=range(2, 5)),
            EnemyData(7, 'Gate Keeper', 100, 30, '╬', Fore.RED, [AttackData('Block', range(40, 50)),
                                                                 AttackData('Shield', range(40, 45)),
                                                                 AttackData('Slash', range(10, 15))], (80, 100),
                      escape=False, loot_table=LootTables.boss, move=False, loot_range=range(0, 1)),
            EnemyData(8, 'Pozzebun', 110, 25, 'Д', Fore.GREEN, [AttackData('Opera Singer Summons', range(30, 50)),
                                                                AttackData('Pop Quiz', range(60, 70)),
                                                                AttackData('Paper Cut', range(30, 45)),
                                                                AttackData('Cipher', range(35, 40))], (300, 600),
                      escape=False, move=False, loot_table=LT([], [], [], [8], super_rare_item_chance=range(0, 100)),
                      loot_range=range(0, 1))
        ]  # Holds enemy data

        # Questions are divided up into different difficulty tiers and have a corresponding timeouts
        # Questions should be in tuples that list the answer(s)
        self.questions = ([[Q('How many bits is in a byte? / A. 10 / B. 1024 / C. 8', ['c', '8']),
                            Q('What does cpu stand for? / A. Center Process Unit / B. Central Processing Unit / '
                              'C. No Meaning', ['b', 'central processing unit']),
                            Q('What does DPI stand for? / A. Dots Per Increment / B. Dots Per Inch / C. No Meaning',
                              ['b', 'dots per inch']),
                            Q('What are hard drives used for? / A. Storing Short Term Data / B. Instruction Execution /'
                              ' C. Storing Long Term Data', ['c', 'storing long term data']),
                            Q('A Motherboard is used to. / A. House Components / B. Act as the data highway between '
                              'components / C. Make Computer function faster',
                              ['a', 'b', 'house components', 'act as the data highway between components']),
                            Q('Mac OS was created by. / A. Tim Apple / B. Nerds / C. Tim Cook / D. Steve Jobs',
                              ['b', 'nerds']),
                            Q('ISP Stands for. / A. Internet Still Paid / B. Internet Service Provider / C.'
                              ' Internet Stands Perpetual', ['b', 'internet service provider']),
                            Q('What is a URL. / A. a virtual address that directs a computer on where '
                              'to find a resource online / B. Random scary thing in my browser',
                              ['a', 'a virtual address that directs a computer on where '
                               'to find a resource online']),
                            Q('How do dial up connections connect to the internet? / A. Demonic Sounds / '
                              'B. By using audio signals to decode \\ encode data. / C. Black Magic',
                              ['b', 'By using audio signals to decode / encode data']),
                            Q('An example of malware is. / A. This program / B. System 32 / C. Rat',
                              ['c', 'rat'])], [], []], [15000, 10000, 6000])  # I never want to write this again


class SysData:
    max_screen_size = ()  # The max size of the console in rows / columns (x, y)
    hwnd = None  # PID
    full_kill = False
    main_listener = None
    demo_listener = None
    question_listener = None


@dataclass()
class Q:
    question: str
    answer: list[str]


@dataclass()
class EP:  # Enemy Package
    enemy_id: int  # The id of the enemy that is to be spawned
    pos: list  # The positions on the map that the player can spawn on
    last_char: str = ''  # [Auto Generated] The display char of the spot the enemy is on before it moved there


@dataclass()
class Event:
    object_id: int  # The ID of the door/item/npc to bind the event to when the map loads
    event_dialogue: list  # Change events to be intractable in the future ("Text", Delay)


class StoryData:  # Event trigger data
    town_entered = False
    dungeon_final_boss = False  # Will stop the final boss from spawning again after it has been defeated.


class EventData:  # Event Dialogue Data  [Door_ID [(DIALOGUE)]]
    events = {
        "door": [Event(0, [("You found it", 1000), ("You actually found a new dungeon entrance, that looks "
                                                    "like it hasn't been touched in thousands of years!", 1000),
                           ("Now then...", 1000), ("Its time you start your Adventure!", 2000)])],
        "npc": [],
        "item": [Event(32, [('Once used by the noble samurai, this sword carries the burden of all of those it has'
                             'cut through.', 1600), ('You now carry the burden of this pristine blade.', 1400)]),
                 Event(8, [('Once used by a noble Hero.', 1100),
                           ('What they did for this world will forever remain unknown.', 1100),
                           ('The legend of the hero is unknown', 1300),
                           ('You carry the burden of the hero with this pristine blade.', 1100),
                           ('Take care of it', 1300)])],
        "enemy": [Event(7, [('A formidable foe stands in your way', (1600, 'yellow')),
                            ('\"I am the Gatekeeper\"', (1800, 'red')),
                            ('\"I am the protector of the final room\"', (2100, 'red')),
                            ('\"I have defeated all who have come before you... You will be no exception...\"',
                             (2300, 'red'))]),
                  Event(8, [('The final floor, the final boss', 1800), ('This is it.', 2300),
                            ('After this boss has been defeated you are able to restart the game by going through'
                             ' the door after the boss has been defeated', 2100)])]
    }


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
    map_kill = False  # Bad idea to use
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
    enemy_movement = False  # Toggles to run enemy movement script every second player movement


@dataclass()
class MQ:
    messages: list


# Inventory Functions
@dataclass()
class InvItem:
    name: str
    item_id: int
    qty: int = 1
    max_qty: int = 0
    item_size: int = 1
    type: str = "consumable"  # The type of the item [weapon / consumable / clothing]
    damage: tuple = (0, 0)  # Damage range items deals (does not apply to non-weapon type items)
    health_regen: tuple = (0, 0)
    stamina_regen: tuple = (0, 0)
    desc: str = None  # Description of item
    death_drop: bool = True  # Can the item drop on death?
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
    floor_entrance: bool = False  # Triggers run warn script
    event: bool = False  # [AUTO GENERATED] Whether the door has an event bound to it (Automatically assigned)
    valid: bool = True  # [AUTO GENERATED] Declares if the player can access this door


class HelpPage:
    __slots__ = ('cmd_list', 'ind_def')

    # cmd_list: Command List
    # ind_def: Individual Definitions
    def __init__(self):
        self.cmd_list = ["help", "?", "inventory", "item-info", "drop"]
        self.ind_def = {"use": "Usage (use [item name / item id]): Uses the specified item "
                               "(if it is valid for the situation)",
                        "inventory / inv": "Usage (inventory) | (inv): Displays your current inventory",
                        "item-info": "Usage (item-info [item name / item id] | Displays info on the specified item",
                        "drop": 'Usage (drop [item name / item id] | Removes the specified item from your inventory'}


class MainMap:  # Main starting area Map
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 0
        self.map_desc = "The main area of Wakefield!"
        self.map_name = Fore.GREEN + "Main Area" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = []  # No enemies can spawn on this map
        self.door_data = [DoorData(0, 1, chr(9688), "-", Fore.BLUE, Fore.GREEN, True, [(9, 25)], (True, 0)),
                          DoorData(1, 99, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(24, 7)])]
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
            ["-", "-", "-", "-", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "1", "", "", "T", "", "O", "", "W", "", "N", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X"],
            ["X", "X", "x", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]]


class Floor0:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 1
        self.map_desc = "Dungeon Floor 1"
        self.map_name = Fore.GREEN + "Floor 0" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = []  # No enemies can spawn on this map
        self.door_data = [DoorData(2, 0, chr(9688), "-", Fore.BLUE, Fore.GREEN, False, [(0, 14)], floor_entrance=True),
                          DoorData(3, 2, chr(9688), "", Fore.BLUE, Fore.BLACK, True, [(20, 11), (18, 15)], (True, 0))]
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
        self.map_desc = "Dungeon Floor 2"
        self.map_name = Fore.GREEN + "Floor 1" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(0, [(7, 16)]), EP(3, [(8, 10)])]
        self.door_data = [DoorData(4, 0, chr(9688), "-", Fore.BLUE, Fore.GREEN, False, [(0, 12)], floor_entrance=True),
                          DoorData(5, 3, chr(9688), "", Fore.BLUE, Fore.BLACK, False, [(23, 11)], (True, 1))]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "2", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", ""],
            ["1", "x", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "1"],
            ["", "", "X", "X", "X", "X", "", "", "2", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
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


class Floor2:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')
    # x: 23 y: 19

    def __init__(self):
        self.map_id = 3
        self.map_desc = ""
        self.map_name = Fore.GREEN + "Dungeon Floor 3" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(0, [(1, 9)]), EP(1, [(6, 11)]), EP(2, [(6, 2)]),
                      EP(4, [(16, 6)]), EP(6, [(19, 12)])]
        self.door_data = [DoorData(7, 0, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(11, 19)],
                                   floor_entrance=True),
                          DoorData(8, 4, chr(9688), '', Fore.BLUE, Fore.WHITE, True, [(3, 0), (1, 10), (3, 9)],
                                   (True, 1), True)]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "", "", "", "", "", "", "", "x", "", "", "", "", "", "", "", "X", "", "", "", ""],
            ["", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", ""],
            ["", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "X", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", ""],
            ["", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", ""],
            ["", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", ""],
            ["", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]


class Floor3:
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    # x: 23 y: 19
    def __init__(self):
        self.map_id = 4
        self.map_desc = ""
        self.map_name = Fore.GREEN + "Dungeon Floor 4" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(6, [(1, 4)]), EP(5, [(2, 18)]), EP(3, [(20, 3)]), EP(4, [(10, 2)]), EP(4, [(20, 19)])]
        self.door_data = [DoorData(10, 0, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(10, 19)],
                                   floor_entrance=True),
                          DoorData(11, 5, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(1, 3), (22, 8)],
                                   (True, 2), True)]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "x", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "X", "X", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["X", "X", "X", "X", "X", "", "", "", "", "X", "X", "", "", "", "", "", "X", "", "", "", "", "", "", ""],
            ["X", "X", "X", "X", "X", "X", "", "", "", "X", "X", "", "", "", "", "X", "X", "", "", "", "", "", "", ""],
            ["", "X", "X", "X", "X", "X", "", "", "", "X", "X", "X", "", "", "", "X", "X", "X", "", "", "", "", "", ""],
            ["", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", ""],
            ["", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", ""],
            ["", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", ""],
            ["", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "", "", ""],
            ["", "", "", "", "X", "X", "X", "X", "X", "", "", "", "", "", "", "X", "X", "X", "X", "X", "", "", "", ""],
            ["", "", "", "", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", ""],
            ["", "", "", "", "", "X", "X", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "X", "", "", "", "X", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "X", "X", "", ""],
            ["", "X", "X", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "X", "X", "", ""],
            ["X", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", "", "", "X", "", ""]]


class Floor4:  # Template Floor
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    # x: 23 y: 17
    def __init__(self):
        self.map_id = 5
        self.map_desc = ""
        self.map_name = Fore.GREEN + "Dungeon Floor 6" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(6, [(5, 5), (2, 3)]), EP(5, [(10, 5), (5, 17)]), EP(5, [(9, 17), (8, 15)]),
                      EP(4, [(20, 5), (15, 5)]), EP(3, [(1, 1), (20, 10)])]
        self.door_data = [DoorData(12, 0, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(23, 12)],
                                   floor_entrance=True),
                          DoorData(13, 6, chr(9688), '', Fore.BLUE, Fore.WHITE, True, [(0, 17), (15, 0), (10, 17)],
                                   (True, 2), True)]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", "", ""],
            ["", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "", "", "", "x", "1"],
            ["", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "", "", "", ""],
            ["", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "X", "", "", "", "", "", ""],
            ["", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]


class GateKeeper:  # Gate Keeper's Floor
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 6
        self.map_desc = "Dungeon Floor 7"
        self.map_name = Fore.GREEN + "Gate Keepers Floor" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(7, [(12, 11)])]
        self.door_data = [DoorData(6, 7, chr(9688), chr(9688), Fore.LIGHTMAGENTA_EX, Fore.WHITE, False, [(12, 0)],
                                   floor_progress=(True, 2))]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "X", "X", "X", "x", "X", "X", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "X", "X", "X", "", "X", "X", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "X", "X", "X", "", "", "", "X", "X", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "X", "X", "X", "X", "", "X", "X", "X", "X", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "X", "X", "", "X", "", "X", "", "X", "X", "X", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "X", "X", "X", "X", "", "", "", "", "X", "X", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "", "", "", "", "X", "X", "X", "X", "", "X", "", "X", "", "", "", "", "", "", "", ""],
            ["", "X", "X", "X", "X", "", "", "", "X", "X", "X", "X", "", "X", "X", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "", "", "", "", "", "", "X", "X", "", "X", "X", "X", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "X", "", "X", "X", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "X", "2", "X", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "X", "X", "X", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "X", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "", "", ""]]


class FinalFloor:  # Final Floor
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 7
        self.map_desc = "The Final Floor"
        self.map_name = Fore.GREEN + "Finale" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = [EP(8, [(12, 5)])]
        self.door_data = [DoorData(9, 0, chr(9688), chr(9688), Fore.BLUE, Fore.BLUE, False, [(11, 11)],
                                   floor_entrance=True)]
        self.map_array = [
            ["", "", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "x", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]


class Template:  # Template Floor
    __slots__ = ('map_name', 'map_array', 'map_desc', 'npc', 'enemy', 'map_id', 'door_data')

    def __init__(self):
        self.map_id = 0
        self.map_desc = ""
        self.map_name = Fore.GREEN + "" + Style.RESET_ALL
        self.npc = []  # NPC DATA [NEED TO WORK ON]
        self.enemy = []
        self.door_data = []
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
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

