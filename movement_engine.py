import sys

import pynput.keyboard

import game_data
from colorama import init
from colorama import Fore, Back, Style
import os
from pynput import keyboard
from threading import Thread
import time
import lib
import random
import copy

init()
global Data  # Holds static system data (Initiated by the main file)


# Note: Create map then use reverse operation for coordinate reading otherwise everything will be confusing
def get_coord(map_in):  # Find and return the coordinates of the player
    map_in = map_in.map_array[::-1]  # Reverse the map
    for y in range(len(map_in)):
        for x in range(len(map_in[y])):
            if map_in[y][x] == "x":
                return [x, y]

    return False


def get_coord_char(map_in, x, y):
    # Checks what character is in the specified position
    return map_in.map_array[::-1][y][x]


# Coordinate init code: (Resets system coordinate values to accommodate the current map)
def init_coord():
    init_coordinates = get_coord(game_data.MapData.current_map)
    game_data.MapData.y = init_coordinates[1]
    game_data.MapData.x = init_coordinates[0]
    game_data.MapData.last_char = ""
    game_data.MapData.y_max = len(game_data.MapData.current_map.map_array) - 1


def enemy_move_calc(map_in):  # This was such a simple task, why did I add an enemy movement system?
    """
    Order of operations:
         - Check if any enemy tiles are on the map, if there are none pull the enemy data configuration for the map
        Spawning Script:
            - Calculate valid positions for enemies to make sure enemy is not spawned within certain radius of main
              door and does not spawn on top of player tile. Store list of invalid positions in cache data for map.
            - For each entry of enemy data attempt to initialize the tile on the map in a valid position
    """
    pass


def map_check():
    # Map Specific events
    if game_data.MapData.current_map.map_id == 0\
            and game_data.MapData.lmc != (0, 0):  # Checks if the map is the main map
        # Reset to the entrance position
        lmc = game_data.MapData.lmc  # Last Map Coordinate
        cc = get_coord(game_data.MapData.current_map)  # Get coordinate of player
        game_data.MapData.last_char = \
            game_data.MapData.current_map.map_array[::-1][lmc[1]][lmc[0]]  # Set replacement char
        game_data.MapData.current_map.map_array[::-1][cc[1]][cc[0]] = ""
        game_data.MapData.current_map.map_array[::-1][lmc[1]][lmc[0]] = 'x'
        init_coord()  # Reset the coordinate backend


def process_tile(tile_char: str, coord: tuple):  # Process the specified tile
    # tile_char : The character of the tile to process
    # coord : the coordinate of that tile

    if tile_char == "1":  # Door Tile
        # Tile type is a door, fetch and process door data
        for d in game_data.MapData.current_map.door_data:
            if d.pos == coord:  # Look for door with matching player current coordinate
                # Door has been found
                if len(game_data.MapData.current_map.enemy) > 0:
                    game_data.MapData.map_idle = True
                    lib.gprint(game_data.MQ([lib.ck("The door won't move, all enemies must be defeated first.",
                                                    'yellow')]))
                    time.sleep(1)
                    lib.back_line(56)
                    game_data.MapData.map_idle = False
                    return

                if not d.valid:
                    game_data.MapData.map_idle = True
                    lib.gprint(game_data.MQ([lib.ck("The door won't budge. Try Again Later?", 'yellow')]))
                    time.sleep(1)
                    lib.back_line(38)
                    game_data.MapData.map_idle = False
                    return

                if d.floor_entrance:
                    os.system('cls')
                    script = [lib.ck('This door goes back to the main map. Do you want to continue? ', 'yellow'),
                              lib.ck('['), lib.ck('Y / N', 'red'), lib.ck(']')]

                    sl = 0
                    for s in script:
                        sl += len(s[0])

                    lib.center_cursor(sl)
                    lib.gprint(game_data.MQ(script))

                    game_data.PlayerData.battle_run_warning = True  # Set to only accept Y / N
                    any_key()

                    while game_data.SysData.demo_listener.running:
                        continue

                    if not game_data.PlayerData.battle_run_response:
                        show_map(game_data.MapData.current_map)
                        return

                old_coord = get_coord(game_data.MapData.current_map)
                old_id = game_data.MapData.current_map.map_id
                game_data.MapData.current_map = lib.map_index(d.map_warp)()  # Set new map and initialize
                init_coord()  # initiate new coordinate values
                init_door()  # initiate all door data
                d.event = False  # Debug line REMOVE THIS LINE IN LIVE VERSION Overrides the event status

                # Checks if this door leads to the next floor, if it does trigger the question system
                if d.floor_progress[0] and len(Data.questions[0][d.floor_progress[1]]) > 0:
                    # Trigger the floor progression question system
                    lib.question_handler(d.floor_progress[1])

                if d.event:
                    lib.event_handler(d.door_id, 0)  # Process door event type with event id of door
                else:
                    # Main map entrance view reset
                    map_check()

                if old_id == 0:  # If the map the player is coming off of is the main map, pull the coordinates
                    game_data.MapData.lmc = (old_coord[0], old_coord[1])  # Set door entrance map coord

                show_map(game_data.MapData.current_map)
                break  # Data has been found, no need to continue
    elif tile_char == "2":
        # Player Has encountered an enemy.
        game_data.MapData.map_idle = True
        enemy = None
        enemy_data_pos = None
        ui_ss = 20  # UI Side Spacing
        ss = 5  # Side Spacing
        aso = 15  # Action Space Out

        # Fetch Enemy data using current coordinates
        map_data = game_data.MapData.current_map
        if map_data.enemy is None:
            # Clear the invalid enemy tile
            map_data.map_array[::-1][coord[1]][coord[0]] = ''

        for x, e in enumerate(map_data.enemy):
            if e.pos == coord:
                for _e in Data.enemies:
                    if _e.Entity_id == e.enemy_id:
                        # Enemy data found. Set Data
                        enemy_data_pos = x  # used to remove the enemy entry from the list
                        enemy = copy.copy(_e)  # Create copy of local data without editing main copy
                        break
                break

        if enemy is None:  # enemy was found in map data but the id referenced non-existent data
            map_data.map_array[::-1][coord[1]][coord[0]] = ''

        # Enemy Level Curve
        enemy.cur_lvl = \
            enemy.base_level + random.randint(0, game_data.MapData.current_map.map_id) * random.randint(0, 2)

        # Enemy Health Curve
        enemy_curve_health = enemy.Health + round((enemy.Health * 0.15) * (enemy.cur_lvl - enemy.base_level))
        enemy.Health = enemy_curve_health

        # Check Event data
        enemy_events = [x.object_id for x in game_data.EventData.events['enemy']]
        if enemy.Entity_id in enemy_events:
            os.system('cls')
            lib.event_handler(enemy.Entity_id, 3, False)  # Starts enemy type event
            time.sleep(1)

        # Initiate battle script
        os.system("cls")
        time.sleep(1)
        script = [lib.ck('A wild Lvl.'), lib.ck(f"{enemy.cur_lvl} {enemy.Name}", "yellow"),
                  lib.ck(" has appeared")]
        sl = len(script[0][0]) + len(script[1][0]) + len(script[2][0])
        print("\n" * (game_data.SysData.max_screen_size[1] // 2) +  # Text Centering Vertical
              " " * ((game_data.SysData.max_screen_size[0] // 2) - (sl // 2)), end='')  # Text Centering Horizontal
        lib.gprint(game_data.MQ(script))
        time.sleep(2)
        print(f"\x1b[{(game_data.SysData.max_screen_size[0] // 2) - (sl // 2)}C", end='')
        lib.back_line(sl)
        time.sleep(0.5)

        # Set Valid Commands
        game_data.MapData.valid_cmd = ["inventory", "use", "item-info", 'run']
        game_data.PlayerData.in_battle = True
        while game_data.PlayerData.in_battle:
            do_enemy_attack = False
            os.system("cls")
            form = f'{enemy.Name} Lvl. {enemy.cur_lvl}'  # Because PEP-8 that's why
            print(f"{f'{Fore.YELLOW}  {form}{Fore.RESET}  ':-^{game_data.SysData.max_screen_size[0] // 2}}\n")
            print(f"{'':<{ss}}", f"{Fore.YELLOW}Turn{Fore.RESET}: {Fore.RED}{game_data.PlayerData.battle_turn}\n")
            print(f"{'':<{ss}}", f"{Fore.YELLOW}{f'Enemy Health{Fore.RESET}: ':<{ui_ss}} {Fore.RED}{enemy.Health}"
                                 f"{Fore.YELLOW}/ {Fore.GREEN}{enemy_curve_health}")
            print(f"{'':<{ss}}", f"{Fore.YELLOW}{f'Player Health{Fore.RESET}: ':<{ui_ss}} "
                                 f"{Fore.RED}{game_data.PlayerData.Health} {Fore.YELLOW}/{Fore.GREEN} "
                                 f"{game_data.PlayerData.Health_Max}")
            print(Fore.RESET, end='')
            print(f"{f'  {Fore.YELLOW}Actions{Fore.RESET}  ':-^{game_data.SysData.max_screen_size[0] // 2}}\n\n")

            action_printout = ''
            for i, a in enumerate(game_data.MapData.valid_cmd):
                action_printout += f'{a:^{aso}}'
                if i == len(game_data.MapData.valid_cmd) - 1 or (i % 3 == 0 and i != 0):
                    action_printout += '\n\n'  # Create 2 New Lines
            print(f'{action_printout:^{game_data.SysData.max_screen_size[0] // 2}}')
            # I don't feel like getting this to be perfectly centered. Deal with it

            print(f"  {Fore.RED}:{Fore.RESET}> ", end='')
            game_data.PlayerData.battle_action = ""

            # since the main keyboard listener is still active but the movement module is idle
            # this changes the mode to process battle actions instead of game movements / commands
            game_data.PlayerData.battle_action_processing = True
            while game_data.PlayerData.battle_action_processing:
                time.sleep(0.1)
                continue

            action = str(game_data.PlayerData.battle_action).split(" ")

            if action[0] not in game_data.MapData.valid_cmd:
                os.system("cls")
                if action[0].isspace() or action[0] == '':
                    msg = [lib.ck(""), lib.ck("Please enter a command")]
                else:
                    msg = [lib.ck(action[0], "red"), lib.ck(" is not a valid command")]

                sl = len(msg[0][0]) + len(msg[1][0])
                print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                      " " * (game_data.SysData.max_screen_size[0] // 2 - (sl // 2)), end='')
                lib.gprint(game_data.MQ(msg))
                time.sleep(2)
                print(f"\x1b[{(game_data.SysData.max_screen_size[0] // 2) - (sl // 2)}C", end='')
                lib.back_line(sl)
                # Exits and returns to top of while loop
            elif action[0] == "use":
                do_enemy_attack = True
                if len(action) != 2:
                    os.system('cls')
                    print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                          " " * (game_data.SysData.max_screen_size[0] // 2 - (sl // 2)), end='')
                    lib.gprint(game_data.MQ([lib.ck("Use", "yellow"), lib.ck(" requires ", "red"),
                                             lib.ck("1", "yellow"), lib.ck(" argument. Usage: "),
                                             lib.ck("use [item_name / item_id]")]))
                    time.sleep(5)
                elif len(action[1]) > 15:
                    os.system('cls')
                    sl = "Stop, no item has a name that long"
                    print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                          " " * (game_data.SysData.max_screen_size[0] // 2 - (len(sl) // 2)), end='')
                    lib.gprint(sl)  # No Formatting used print raw without MQ class
                    time.sleep(2)
                else:
                    # Fetch item data
                    item_data = lib.has_item(action[1], True)
                    if item_data is False:
                        os.system('cls')
                        sl = [lib.ck(f"Could not find item with the {['name', 'id'][action[1].isnumeric()]} ", "red"),
                              lib.ck("["), lib.ck(action[1], "yellow"), lib.ck("]")]

                        print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                              " " * (game_data.SysData.max_screen_size[0] // 2 -
                                     ((len(sl[0][0]) + len(sl[2][0]) + 2) // 2)),
                              end='')
                        lib.gprint(game_data.MQ(sl))
                        sl = [lib.ck("When trying to use an item with a space " +
                                     "in its name replace the space with a dash", "yellow")]

                        print("\n" + " " * (game_data.SysData.max_screen_size[0] // 2 -
                                            len(sl[0][0]) // 2), end='')
                        lib.gprint(game_data.MQ(sl))
                        time.sleep(3)
                    else:
                        # you have the item data do damage calculations
                        if item_data.type == "clothing":
                            pass  # Clothing has not been implemented
                        elif item_data.type == "weapon":
                            critical = False
                            sl = 0
                            damage = random.randint(item_data.damage[0], item_data.damage[1])
                            if random.randint(0, 100) <= game_data.PlayerData.crit_chance:  # Calculate critical
                                damage = damage + damage * game_data.PlayerData.crit_mod
                                critical = True

                            if critical:
                                script = [lib.ck(f'Critical Hit!', 'yellow'), lib.ck(' Your ', 'red'),
                                          lib.ck(str(item_data.name), 'yellow'), lib.ck(' dealt ', 'red'),
                                          lib.ck(str(damage), 'yellow'), lib.ck(' damage to ', 'red'),
                                          lib.ck(enemy.Name)]
                            else:
                                script = [lib.ck(' Your ', 'red'),
                                          lib.ck(item_data.name, 'yellow'), lib.ck(' dealt ', 'red'),
                                          lib.ck(str(damage), 'yellow'), lib.ck(' damage to ', 'red'),
                                          lib.ck(enemy.Name)]

                            for i in script:  # Calculate offset
                                sl += len(i[0])

                            # Position cursor
                            os.system('cls')
                            lib.center_cursor(sl)

                            lib.gprint(game_data.MQ(script))
                            enemy.Health -= damage
                            time.sleep(3)
                            pass
                        elif item_data.type == "consumable":
                            consume = False
                            """
                            Currently only implements healing / food items. Add potions that add skill buffs (later)
                            version 2 maybe. Stick with simplicity for now.
                            """
                            os.system('cls')
                            regen = random.randint(item_data.health_regen[0], item_data.health_regen[1])
                            if (game_data.PlayerData.Health + regen) > game_data.PlayerData.Health_Max:
                                # Ask the player if they still wish to use the item
                                script = [lib.ck('Consuming a ', 'yellow'), lib.ck(item_data.name, 'red'),
                                          lib.ck(' will bring you over max health. Your health will be maxed at ',
                                                 'yellow'),
                                          lib.ck(str(game_data.PlayerData.Health_Max), 'red'), lib.ck(' and', 'yellow'),
                                          lib.ck(' ' + str(game_data.PlayerData.Health + (regen -
                                                           game_data.PlayerData.Health_Max)), "red"),
                                          lib.ck(' HP will be wasted.',
                                                 "yellow")]
                                sl = 0
                                for d in script:
                                    sl += len(d[0])

                                print('\n' * (game_data.SysData.max_screen_size[1] // 2) + ' ' *
                                      ((game_data.SysData.max_screen_size[0] // 2) - (sl // 2)), end='')
                                lib.gprint(game_data.MQ(script))

                                script = "Do you wish to continue? (Y / N)"
                                print(' ' * ((game_data.SysData.max_screen_size[0] // 2) - (len(script) // 2)), end='')
                                lib.gprint(game_data.MQ([lib.ck(script, "yellow")]))
                                game_data.PlayerData.regen_max_warn = True
                                any_key()
                                while game_data.SysData.demo_listener.running:
                                    continue

                                if game_data.PlayerData.regen_max_warn_response:
                                    consume = True
                            else:
                                consume = True

                            if consume:
                                game_data.PlayerData.Health += regen
                                os.system('cls')
                                script = [lib.ck('You consume the ', 'yellow'), lib.ck(item_data.name, 'green'),
                                          lib.ck(' your health is now at ', 'yellow'),
                                          lib.ck(str(game_data.PlayerData.Health), 'green'), lib.ck(' HP')]
                                sl = 0
                                for i in script:
                                    sl += len(i[0])

                                lib.remove_item(item_data.item_id)
                                lib.center_cursor(sl)
                                lib.gprint(game_data.MQ(script))
                                time.sleep(2)

            elif action[0] == "inventory":
                game_data.PlayerData.battle_inventory = True
                lib.display_inv()
                lib.gprint("\nPress any key to exit...")
                any_key()
                while game_data.SysData.demo_listener.running is True:
                    continue
            elif action[0] == "item-info":
                # Display item info regardless of whether the player has the item
                # Fetch item data
                if len(action) != 2:
                    os.system('cls')
                    print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                          " " * (game_data.SysData.max_screen_size[0] // 2 - (sl // 2)), end='')
                    lib.gprint(game_data.MQ([lib.ck("item-info", "yellow"), lib.ck(" requires ", "red"),
                                             lib.ck("1", "yellow"), lib.ck(" argument. Usage: ", "yellow"),
                                             lib.ck("item-info [item_name / item_id]", "red")]))
                    time.sleep(5)
                elif len(action[1]) > 15:
                    os.system('cls')
                    sl = "Stop, no item has a name that long"
                    print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                          " " * (game_data.SysData.max_screen_size[0] // 2 - (len(sl) // 2)), end='')
                    lib.gprint(sl)  # No Formatting used print raw without MQ class
                    time.sleep(2)
                else:
                    item_data = lib.item_info(action[1])
                    os.system("cls")

                    if item_data is False:
                        os.system('cls')
                        sl = [lib.ck(f"Could not find item with the {['name', 'id'][action[1].isnumeric()]} ", "red"),
                              lib.ck("["), lib.ck(action[1], "yellow"), lib.ck("]")]

                        print("\n" * (game_data.SysData.max_screen_size[1] // 2) +
                              " " * (game_data.SysData.max_screen_size[0] // 2 -
                                     ((len(sl[0][0]) + len(sl[2][0]) + 2) // 2)),
                              end='')
                        lib.gprint(game_data.MQ(sl))
                        sl = [lib.ck("When trying to use an item with a space " +
                                     "in its name replace the space with a dash", "yellow")]
                        print("\n" + " " * (game_data.SysData.max_screen_size[0] // 2 -
                                            len(sl[0][0]) // 2), end='')
                        lib.gprint(game_data.MQ(sl))
                        time.sleep(3)
                    else:

                        lib.display_item_info(item_data)
                        lib.gprint("\nPress any key to exit...")

                        game_data.PlayerData.battle_inventory = True  # Same idea as the inventory display
                        any_key()
                        while game_data.SysData.demo_listener.running is True:
                            continue

            elif action[0] == 'run':
                os.system('cls')
                if enemy.escape:
                    script = [lib.ck('Running from this battle will return you to the main map. '
                                     'Do you wish to continue? [',
                                     'yellow'), lib.ck(' Y ', "red"), lib.ck('/', 'yellow'), lib.ck(' N ', "green"),
                              lib.ck(']', 'yellow')]
                else:
                    script = [lib.ck('You cannot run from this enemy', 'red')]

                sl = 0
                for i in script:
                    sl += len(i[0])
                lib.center_cursor(sl)
                lib.gprint(game_data.MQ(script))

                if not enemy.escape:
                    time.sleep(2)
                else:
                    game_data.PlayerData.battle_run_warning = True
                    any_key()
                    while game_data.SysData.demo_listener.running:
                        continue

                    if game_data.PlayerData.battle_run_response:
                        # Player wants to run
                        game_data.MapData.current_map = game_data.MainMap()
                        init_coord()
                        init_door()
                        map_check()
                        game_data.PlayerData.in_battle = False
                        return

            # End of game actions
            if game_data.PlayerData.Health <= 0:
                """
                Player has died, drop random item and return player to main map
                """
                valid_items = [i for i in game_data.PlayerData.Inventory if i.death_drop is True]
                item = random.choice(valid_items)
                lib.remove_item(item.item_id)
                os.system('cls')
                script = [lib.ck('You have passed out. A passing adventurer drags your unconscious body out of the '
                                 'dungeon, upon waking you discovered that you no longer have your ', 'yellow'),
                          lib.ck(item.name, 'red')]

                sl = 0
                for i in script:
                    sl += len(i[0])

                lib.center_cursor(sl)
                time.sleep(1)
                lib.gprint(game_data.MQ(script))
                time.sleep(3)
                game_data.MapData.current_map = game_data.MainMap()
                init_coord()
                init_door()
                map_check()
                game_data.PlayerData.in_battle = False
                return
            elif enemy.Health <= 0:  # Player won battle
                # XP Calculation
                xp = random.randint(enemy.xp_drop[0], enemy.xp_drop[1])  # add level advantage scaling
                game_data.PlayerData.total_xp += xp
                os.system('cls')
                script = [lib.ck(enemy.Name, 'yellow'), lib.ck(' fainted! You earned ', 'green'),
                          lib.ck(str(xp), 'yellow'), lib.ck(' xp', 'green')]
                sl = 0
                for i in script:
                    sl += len(i[0])

                lib.center_cursor(sl)
                lib.gprint(lib.MQ(script))
                time.sleep(2)

                # Recursive level up system
                lvl_change = 0  # amount of times player leveled up
                while True:
                    game_data.PlayerData.exp_lvl = game_data.PlayerData.exp_scaling * game_data.PlayerData.player_level
                    if game_data.PlayerData.player_level >= game_data.PlayerData.level_cap:
                        break
                    elif game_data.PlayerData.total_xp > game_data.PlayerData.exp_lvl:
                        game_data.PlayerData.player_level += 1
                        lvl_change += 1
                    else:
                        break

                os.system('cls')
                if lvl_change > 0:
                    if lvl_change == 1:
                        lvl = "level"
                    else:
                        lvl = "levels"
                    script = [lib.ck("You leveled up ", 'green'), lib.ck(str(lvl_change), 'yellow'),
                              lib.ck(f' {lvl}, ', 'green'), lib.ck('you are now level ', 'green'),
                              lib.ck(str(game_data.PlayerData.player_level) + ['', ' (Max Level)']
                              [game_data.PlayerData.player_level == game_data.PlayerData.level_cap], 'yellow')]
                    sl = 0
                    for i in script:
                        sl += len(str(i[0]))

                    lib.center_cursor(sl)
                    lib.gprint(game_data.MQ(script))
                    time.sleep(3)

                # Loot Drop Calculations
                rng_roll = random.randint(0, 100)
                loot_drop = []
                for m in range(0, random.choice(enemy.loot_range) + 1):
                    if rng_roll in enemy.loot_table.super_rare_item_chance:
                        item = random.choice(enemy.loot_table.super_rare_items)
                        loot_drop.append(item)
                        lib.add_item(item)
                    elif rng_roll in enemy.loot_table.rare_item_chance:
                        item = random.choice(enemy.loot_table.rare_items)
                        loot_drop.append(item)
                        lib.add_item(item)
                    elif rng_roll in enemy.loot_table.uncommon_item_chance:
                        item = random.choice(enemy.loot_table.uncommon_items)
                        loot_drop.append(item)
                        lib.add_item(item)
                    elif rng_roll in enemy.loot_table.common_item_chance:
                        item = random.choice(enemy.loot_table.common_items)
                        loot_drop.append(item)
                        lib.add_item(item)
                    else:
                        # Choose random item from entire base table
                        item = random.choice(Data.game_items).item_id
                        loot_drop.append(item)
                        lib.add_item(item)

                os.system('cls')
                detail_comp = [x.name for x in (list(map(lib.item_info, loot_drop)))]

                script = [lib.ck(enemy.Name, 'green'), lib.ck(' dropped ', 'yellow')]

                # Add item list to print-out
                for x, i in enumerate(detail_comp):
                    script.append(lib.ck(i, 'red'))
                    if x != len(detail_comp) - 1:
                        script.append(lib.ck(', ', 'yellow'))

                sl = 0
                for x in script:
                    sl += len(str(x[0]))

                lib.center_cursor(sl)
                lib.gprint(game_data.MQ(script))

                time.sleep(2)
                game_data.PlayerData.in_battle = False
            elif do_enemy_attack:  # Avoids the attack script triggering on turn that was used for non-use action
                attack = random.choice(enemy.Attacks)  # Choose random attack
                attack_damage = random.choice(attack.damage)  # Random attack damage
                os.system('cls')
                script = [lib.ck(enemy.Name, 'red'), lib.ck(' uses ', 'yellow'), lib.ck(attack.name),
                          lib.ck(' attack deals ', 'yellow'), lib.ck(str(attack_damage), 'red'),
                          lib.ck(' damage', 'yellow')]

                sl = 0
                for i in script:
                    sl += len(i[0])

                lib.center_cursor(sl)
                lib.gprint(game_data.MQ(script))
                game_data.PlayerData.Health -= attack_damage  # Deal enemy damage to player
                time.sleep(3)

        game_data.MapData.current_map.enemy.pop(enemy_data_pos)  # Remove data
        game_data.MapData.current_map.map_array[::-1][coord[1]][coord[0]] = ' '  # Remove enemy from map
        game_data.MapData.map_idle = False
        show_map(game_data.MapData.current_map)


def coord_set(map_in, x_m, y_m):  # Main Movement Engine
    # Move point to a certain position on the map

    # x_m = Amount to move on x plane
    # y_m = Amount to move on y plane

    # Check to see if next coordinate pairs is an illegal movement if it is, don't move
    # if it is not, get the current coordinates and reset the position to a blank spot
    # move the players char to the new set of coordinates

    if game_data.PlayerData.Inventory_Displayed:
        # Ignore all movement calculations and exit back out to map
        game_data.PlayerData.Inventory_Displayed = False
        show_map(map_in)
    else:
        new_x = game_data.MapData.x + x_m
        new_y = game_data.MapData.y + y_m
        y_max = len(map_in.map_array) - 1
        x_max = len(map_in.map_array[0]) - 1
        # Out of boundary check
        if not (new_x > x_max or new_x < 0 or new_y > y_max or new_y < 0):
            future_char = get_coord_char(map_in, new_x, new_y)
            # Collision Checking to see if the player is allowed to move into this area
            if not Data.movement_blacklist.__contains__(future_char):
                if Data.tile_data.__contains__(future_char):
                    process_tile(future_char, (new_x, new_y))
                else:
                    # Add movement entry  (Current Coordinates) (New Coordinates) (Old Characters)
                    game_data.MapData.movement.append((((game_data.MapData.x, game_data.MapData.y),
                                                        (new_x, new_y)), game_data.MapData.last_char, ('x', Fore.CYAN)))

                    internal_coordinates = [game_data.MapData.x, game_data.MapData.y_max - game_data.MapData.y]  # local
                    game_data.MapData.x += x_m  # Global
                    game_data.MapData.y += y_m  # Global
                    map_in.map_array[internal_coordinates[1]][internal_coordinates[0]] = game_data.MapData.last_char
                    map_in.map_array[::-1][game_data.MapData.y][game_data.MapData.x] = "x"  # Enter new position
                    game_data.MapData.last_char = future_char
                    move_char()  # Update movements

                    # Enemy movement calculations
                    if game_data.MapData.enemy_movement:

                        invalid = Data.tile_data + Data.movement_blacklist + ['x']
                        game_data.MapData.enemy_movement = False  # Skip the script on next turn
                        m = map_in.map_array[::-1]
                        for e in game_data.MapData.current_map.enemy:
                            # Check each direction to get list of valid directions

                            valid_moves = []  # Compiled list of valid moves

                            def check(x, y):
                                if not ((e.pos[0] + x) > x_max or (e.pos[0] + x) < 0 or (e.pos[1] + y) > y_max
                                        or (e.pos[1] + y) < 0):
                                    if m[e.pos[1] + y][e.pos[0] + x] not in invalid:
                                        valid_moves.append((e.pos[0] + x, e.pos[1] + y))  # Add valid move

                            check(0, 1)  # Check Above
                            check(0, -1)  # Check Below
                            check(1, 0)  # Check Right
                            check(-1, 0)  # Check Left
                            check(1, 1)  # Check Above Right
                            check(-1, 1)  # Check Above Left
                            check(1, -1)  # Check Below Right
                            check(-1, -1)  # Check Below Left

                            if len(valid_moves) > 0:
                                d = Data.enemies[e.enemy_id]
                                _m = random.choice(valid_moves)  # Select Move
                                game_data.MapData.movement.append((((e.pos[0], e.pos[1]), (_m[0], _m[1])), e.last_char,
                                                                   (d.display_char, d.display_colour)))
                                m[e.pos[1]][e.pos[0]] = e.last_char
                                e.pos = _m  # Set the enemy's new position on backend
                                e.old_char = m[_m[1]][_m[0]]
                                m[_m[1]][_m[0]] = '2'  # Set the binder position

                    else:
                        game_data.MapData.enemy_movement = True  # Run script on next turn


def csq_watch_dog():  # Movement manager
    while True:
        for x in game_data.MapData.csq:
            coord_set(game_data.MapData.current_map, x[0], x[1])
        game_data.MapData.csq.clear()
        time.sleep(0.001)  # do not remove this


def move_char():  # Map display script version 2
    # Isolates movements down into individual requests rather than reprinting the entire map every time.
    # All backend calculations remain the same, that way the ability to perform collision checking and prox checks
    # remain unaffected
    for m in game_data.MapData.movement:

        # Clear old position
        last_colour = Fore.WHITE
        last_char = m[1]
        if last_char == '':
            last_char = ' '
        elif last_char in game_data.MapData.ici.keys():
            last_colour = game_data.MapData.ici[last_char]

        print('\033[?25l', end="")  # Hide Cursor
        print(f"\x1b[{game_data.MapData.space_buffer + m[0][0][1]}A", end='')
        print(f"\x1b[{m[0][0][0] * Data.map_spacing}C", end='')
        print(last_colour + last_char + Fore.RESET, end='')
        print(f'\x1b[{game_data.MapData.space_buffer + m[0][0][1]}B', end='\r')  # Reset Cursor Y

        # Enter new position
        print(f"\x1b[{game_data.MapData.space_buffer + m[0][1][1]}A", end='')
        print(f"\x1b[{m[0][1][0] * Data.map_spacing}C", end='')
        print(f"{m[2][1]}{m[2][0]}", end=Fore.RESET)
        print(f"\x1b[{game_data.MapData.space_buffer + m[0][1][1]}B", end='\r')  # Reset Cursor X

    # Door prox check
    for d in game_data.MapData.current_map.door_data:
        if d.prox_check and d.door_id not in \
                game_data.MapDataCache.doors_found[str(game_data.MapData.current_map.map_id)]:
            if lib.check_proximity(d.pos):
                # Display the door
                print(f"\x1b[{game_data.MapData.space_buffer + d.pos[1]}A", end='')
                print(f"\x1b[{d.pos[0] * Data.map_spacing}C", end='')
                print(d.symbol_color + d.symbol + Fore.RESET, end='')
                print(f"\x1b[{game_data.MapData.space_buffer + d.pos[1]}B", end='\r')

    # Display coordinates
    game_data.MapData.movement.clear()
    print(f"\x1b[1A", end=f"{' ' * game_data.SysData.max_screen_size[0]}\r")
    print(f"Your current position is {get_coord(game_data.MapData.current_map)} "
          f"(Represented by the {Fore.CYAN + 'x' + Style.RESET_ALL})")
    print('\033[?25h', end="")  # Show Cursor


def init_door():
    # Initiates door and enemy event data / core data
    map_in = game_data.MapData.current_map
    if len(map_in.door_data) > 0 and map_in.door_data is not None:
        door_events = [x.object_id for x in game_data.EventData.events['door']]
        for m in map_in.door_data:
            if m.door_id in door_events:
                m.event = True

            if len(m.pos) > 1:
                m.multiple_pos = True  # Door has multiple positions, bypass the discovered door cache
            m.pos = random.choice(m.pos)  # Select random pre-defined position
            map_in.map_array[::-1][m.pos[1]][m.pos[0]] = "1"  # Sets the tile type as door data
            if not m.floor_progress:  # if the door is an extra non progression floor
                m.symbol_color = Fore.GREEN
            if not lib.map_index(m.map_warp):
                m.symbol_color = Fore.RED
                m.valid = False

    if len(map_in.enemy) > 0 and map_in.enemy is not None:
        # Place enemy packages on map
        for e in map_in.enemy:
            e.pos = random.choice(e.pos)  # Overwrite multiple positions with selected one
            map_in.map_array[::-1][e.pos[1]][e.pos[0]] = '2'  # Place enemy binder


# Print the entire map
def show_map(map_in):
    # Map display processing
    # Does not affect any backend MAP data

    local_spacing = Data.map_spacing  # Stops code from fetching value from outside class
    map_out = ""
    game_data.PlayerData.command_status = True  # Player can enter commands
    for yi, y in enumerate(map_in.map_array):
        cur_row = ""  # Reset the line print out
        for xi, x in enumerate(y):
            # Get Current Character and add it to the formatted line
            cur_char = x
            if cur_char == "":
                cur_char = f"{' ':<{local_spacing}}"
            elif cur_char == "X":
                cur_char = f"{Fore.YELLOW}{cur_char:<{local_spacing}}{Fore.RESET}"
            elif cur_char == "x":
                cur_char = f"{Fore.CYAN}{cur_char:<{local_spacing}}{Fore.RESET}"
            elif cur_char == "-":
                cur_char = f"{Fore.LIGHTGREEN_EX}{cur_char:<{local_spacing}}{Fore.RESET}"
            elif cur_char == '2':  # Enemy tile
                # Not going to bother writing failsafe script, enemy data is mostly static
                cur_coord = (xi, game_data.MapData.y_max - yi)
                if map_in.enemy is not None:
                    for e in map_in.enemy:
                        if e.pos == cur_coord:
                            for _e in Data.enemies:
                                if _e.Entity_id == e.enemy_id:
                                    cur_char = f"{_e.display_colour}{_e.display_char:<{local_spacing}}{Fore.RESET}"
                                    break
            elif cur_char == "1":
                # Tile type is a door, check door data for that pos
                data_fail = True
                cur_coord = (xi, game_data.MapData.y_max - yi)  # Reverses y coordinate keeps x coord the same

                # Attempt to fetch doors data
                for m in map_in.door_data:
                    if not data_fail:
                        break
                    # Note: Yes I know that I could have made the ID into a tuple and indexed the id of the door
                    # or just contained all the door data in that tile, but it would look messy and in reality
                    # the performance impact that it would have would not equate to much
                    if m.pos == cur_coord:
                        # Door data has been found, use it to print
                        data_fail = False
                        if str(map_in.map_id) not in game_data.MapDataCache.doors_found.keys():
                            # Create dict entry for current map
                            game_data.MapDataCache.doors_found[str(map_in.map_id)] = []

                        if m.prox_check and m.door_id not in game_data.MapDataCache.doors_found[str(map_in.map_id)]:
                            if lib.check_proximity(cur_coord):  # Check if player is within detection distance of door
                                # Door is accessible
                                # Check for door events
                                if not m.multiple_pos:  # Only add bypass entry for doors without multiple positions
                                    game_data.MapDataCache.doors_found[str(map_in.map_id)].append(m.door_id)
                                cur_char = f"{m.symbol_color}{m.symbol:<{local_spacing}}{Fore.RESET}"
                            else:
                                cur_char = f"{m.symbol_alt_color}{m.symbol_alt:<{local_spacing}}{Fore.RESET}"
                        else:
                            cur_char = f"{m.symbol_color}{m.symbol:<{local_spacing}}{Fore.RESET}"
                        break

                if data_fail:
                    # No door data, remove door from origin map
                    # This shouldn't happen as the doors' location is automatically initiated by a separate system
                    map_in.map_array[yi][xi] = " "
                    cur_char = f"{Fore.RED}{'@':<{local_spacing}}{Fore.RESET}"

            else:
                cur_char = f"{cur_char:<{local_spacing}}"

            cur_row += cur_char
        map_out += f"{cur_row}{Fore.RED}|{Fore.RESET}\n"

    # Printing
    os.system("cls")
    print("{:^50}".format(map_in.map_name))
    print(f"{Fore.RED}{'/':^{local_spacing}}{Fore.RESET}" * len(map_in.map_array[0]))
    print(map_out, flush=True, end='')
    print(f"{Fore.RED}{'/':^{local_spacing}}{Fore.RESET}" * len(map_in.map_array[0]))
    print(f"Your current position is {get_coord(map_in)} "
          f"(Represented by the {Fore.CYAN + 'x' + Style.RESET_ALL})")


def on_release(key):  # For movement processing
    if not game_data.MapData.map_idle and not game_data.MapData.movement_idle:
        if key == keyboard.Key.up:
            # coord_set(game_data.MapData.current_map, 0, 1)
            game_data.MapData.csq.append((0, 1))
            # Thread(target=coord_set, args=(game_data.MapData.current_map, 0, 1)).start()
        elif key == keyboard.Key.down:
            # coord_set(game_data.MapData.current_map, 0, -1)
            game_data.MapData.csq.append((0, -1))
        elif key == keyboard.Key.right:
            # coord_set(game_data.MapData.current_map, 1, 0)
            game_data.MapData.csq.append((1, 0))
        elif key == keyboard.Key.left:
            # coord_set(game_data.MapData.current_map, -1, 0)
            game_data.MapData.csq.append((-1, 0))
        elif key == keyboard.Key.esc:
            game_data.MapData.map_kill = True
            return False  # Test Code, allows code exit mid run
    else:
        return


# CLEAN THIS UP
def on_press(key):  # For command processing
    if game_data.PlayerData.regen_max_warn or game_data.PlayerData.battle_run_warning:
        try:
            if key.char == 'y':
                if game_data.PlayerData.regen_max_warn:
                    game_data.PlayerData.regen_max_warn_response = True
                else:
                    game_data.PlayerData.battle_run_response = True

                game_data.PlayerData.battle_run_warning = False
                game_data.PlayerData.regen_max_warn = False
                game_data.SysData.demo_listener.stop()
            elif key.char == 'n':
                if game_data.PlayerData.regen_max_warn:
                    game_data.PlayerData.regen_max_warn_response = False
                else:
                    game_data.PlayerData.battle_run_response = False

                game_data.PlayerData.battle_run_warning = False
                game_data.PlayerData.regen_max_warn = False
                game_data.SysData.demo_listener.stop()
        except:
            return
    elif game_data.PlayerData.battle_action_processing:
        # Pull keys
        try:
            if key == keyboard.Key.space:
                if len(game_data.PlayerData.battle_action) == 0:
                    return
                key.char = " "
            if key == keyboard.Key.enter:
                # Close listener and resume thread processing
                game_data.PlayerData.battle_action_processing = False
            elif key == keyboard.Key.backspace and len(game_data.PlayerData.battle_action) > 0:
                game_data.PlayerData.battle_action = game_data.PlayerData.battle_action[:-1]
                print('\b \b', end='')
            else:
                print(f"{Fore.LIGHTCYAN_EX}{key.char}{Fore.RESET}", end='')
                game_data.PlayerData.battle_action += key.char
        except:
            return
    elif game_data.PlayerData.battle_inventory is True:
        game_data.PlayerData.battle_inventory = False
        game_data.SysData.demo_listener.stop()
    elif game_data.PlayerData.question_status is True:
        # The question system is active, pass all input to this handler
        try:
            if key == keyboard.Key.enter:
                # Check if answer is valid
                pass
            elif key == keyboard.Key.backspace:
                game_data.PlayerData.question_answer = game_data.PlayerData.question_answer[:-1]
            else:
                print(f"{Fore.LIGHTCYAN_EX}{key.char}{Fore.RESET}", end='')
                game_data.PlayerData.question_answer += key.char
        except AttributeError:
            return  # Special key was entered

    elif not game_data.MapData.map_idle:
        try:
            if game_data.PlayerData.command_status:  # Checks if player is allowed to enter commands
                if key == keyboard.Key.space:
                    if len(game_data.MapData.current_command) == 0:
                        return
                    key.char = " "
                if key == keyboard.Key.enter:
                    lib.process_command(game_data.MapData.current_command)
                elif key == keyboard.Key.backspace:
                    # Remove last character of both printed message, and the current command string
                    game_data.MapData.current_command = game_data.MapData.current_command[:-1]
                    sys.stdout.write('\b \b')
                else:
                    print(f"{Fore.LIGHTCYAN_EX}{key.char}{Fore.RESET}", end='')
                    game_data.MapData.current_command += key.char
        except AttributeError:
            return  # Entered key was a special key


# Keyboard Listeners  CLEAN THESE UP AND MERGE

# Main Input Listener
def kb_listener():
    game_data.SysData.main_listener = keyboard.Listener(on_release=on_release, on_press=on_press)
    game_data.SysData.main_listener.start()

    # Watcher Thread
    def watcher():
        while game_data.MapData.map_kill is False:
            time.sleep(0.1)
            continue
        game_data.MapData.map_kill = False
        game_data.SysData.main_listener.stop()
        return False

    Thread(target=watcher).start()


# Used for player basic controls tutorial as not to display the active map
def demo_prompt():
    with keyboard.Listener(on_press=on_press) as listener:
        def watcher():
            while True:
                if game_data.MapData.map_kill or game_data.MapData.demo_kill:
                    game_data.MapData.map_kill = False
                    game_data.MapData.demo_kill = False
                    listener.stop()
                    return False
                time.sleep(0.1)

        Thread(target=watcher).start()
        listener.join()


def any_key():
    game_data.SysData.demo_listener = keyboard.Listener(on_press=on_press)
    game_data.SysData.demo_listener.start()

    # Watcher Thread
    def watcher():
        while game_data.MapData.demo_kill is False:
            time.sleep(0.1)
            continue
        game_data.MapData.demo_kill = False
        game_data.SysData.demo_listener.stop()
        return False

    Thread(target=watcher).start()
