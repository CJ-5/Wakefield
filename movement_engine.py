import sys
import game_data
from colorama import init
from colorama import Fore, Back, Style
import os
from pynput import keyboard
from threading import Thread
import time
import lib
import random

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


def enemy_move_calc(map_in):  # This was such a simple task, why did I add a enemy movement system?
    """
    Order of operations:
         - Check if any enemy tiles are on the map, if there are none pull the enemy data configuration for the map
        Spawning Script:
            - Calculate valid positions for enemies to make sure enemy is not spawned within certain radius of main
              door and does not spawn on top of player tile. Store list of invalid positions in cache data for map.
            - For each entry of enemy data attempt to initialize the tile on the map in a valid position
    """
    pass


def process_tile(tile_char: str, coord: tuple):  # Process the specified tile
    if tile_char == "1":  # Door Tile
        # Tile type is a door, fetch and process door data
        for d in game_data.MapData.current_map.door_data:
            if d.pos == coord:  # Look for door with matching player current coordinate
                # Door has been found
                if not d.valid:
                    game_data.MapData.map_idle = True
                    lib.gprint(game_data.MQ([lib.ck("The door won't budge. Try Again Later?", 'yellow')]))
                    time.sleep(1)
                    lib.back_line(38)
                    game_data.MapData.map_idle = False
                    return

                old_coord = get_coord(game_data.MapData.current_map)
                old_id = game_data.MapData.current_map.map_id
                game_data.MapData.current_map = lib.map_index(d.map_warp)()  # Set new map and initialize
                init_coord()  # initiate new coordinate values
                init_door()  # initiate all door data
                d.event = False  # Debug line REMOVE THIS LINE IN LIVE VERSION

                # Checks if this door leads to the next floor, if it does trigger the question system
                if d.floor_progress[0] and len(Data.questions[0][d.floor_progress[1]]) > 0:
                    # Trigger the floor progression question system
                    lib.question_handler(d.floor_progress[1])

                if d.event:
                    lib.event_handler(d.door_id, 0)  # Process door event type with event id of door
                else:
                    # Main map entrance view reset
                    if game_data.MapData.current_map.map_id == 0:  # Checks if the map is the main map
                        # Reset to the entrance position
                        lmc = game_data.MapData.lmc
                        cc = get_coord(game_data.MapData.current_map)
                        game_data.MapData.current_map.map_array[::-1][cc[1]][cc[0]] = ""
                        game_data.MapData.current_map.map_array[::-1][lmc[1]][lmc[0]] = 'x'
                        init_coord()
                        game_data.MapData.last_char = '-'

                if old_id == 0:  # If the map the player is coming off of is the main map, pull the coordinates
                    game_data.MapData.lmc = (old_coord[0], old_coord[1])  # Set door entrance map coord

                show_map(game_data.MapData.current_map)
                break  # Data has been found, no need to continue


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
        # Out of boundary check
        if not (new_x > len(map_in.map_array[0]) - 1 or new_x < 0 or new_y > len(map_in.map_array) - 1 or new_y < 0):
            future_char = get_coord_char(map_in, new_x, new_y)
            # Collision Checking to see if the player is allowed to move into this area
            if not Data.movement_blacklist.__contains__(future_char):
                if Data.tile_data.__contains__(future_char):
                    process_tile(future_char, (new_x, new_y))
                else:
                    # Add movement entry
                    game_data.MapData.movement.append((((game_data.MapData.x, game_data.MapData.y), (new_x, new_y)),
                                                       game_data.MapData.last_char))

                    internal_coordinates = [game_data.MapData.x, game_data.MapData.y_max - game_data.MapData.y]  # local
                    game_data.MapData.x += x_m  # Global
                    game_data.MapData.y += y_m  # Global
                    map_in.map_array[internal_coordinates[1]][internal_coordinates[0]] = game_data.MapData.last_char
                    map_in.map_array[::-1][game_data.MapData.y][game_data.MapData.x] = "x"  # Enter new position
                    game_data.MapData.last_char = future_char
                    move_char()
                    # show_map(map_in)


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

        print(f"\x1b[{game_data.MapData.space_buffer + m[0][0][1]}A", end='')
        print(f"\x1b[{m[0][0][0] * Data.map_spacing}C", end='')
        print(last_colour + last_char + Fore.RESET, end='')
        print(f'\x1b[{game_data.MapData.space_buffer + m[0][0][1]}B', end='\r')  # Reset Cursor Y

        # Enter new position
        print(f"\x1b[{game_data.MapData.space_buffer + m[0][1][1]}A", end='')
        print(f"\x1b[{m[0][1][0] * Data.map_spacing}C", end='')
        print(f"{Fore.CYAN}x", end=Fore.RESET)
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


def init_door():
    # Sets the doors on the map
    map_in = game_data.MapData.current_map
    for m in map_in.door_data:
        for e in game_data.EventData.events["door"]:  # Event Binding
            print(m.door_id)
            if e.object_id == m.door_id:
                m.event = True
                break

        if len(m.pos) > 1:
            m.multiple_pos = True  # Door has multiple positions, bypass the discovered door cache
        pos = m.pos[random.randint(0, len(m.pos) - 1)]
        m.pos = pos  # Overwrites coordinate list to selected coord
        map_in.map_array[::-1][pos[1]][pos[0]] = "1"  # Sets the tile type as door data
        if not m.floor_progress:
            m.symbol_color = Fore.GREEN
        if not lib.map_index(m.map_warp):
            m.symbol_color = Fore.RED
            m.valid = False


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
            elif cur_char == '0':  # Can be removed
                cur_char = f"{Style.DIM}{cur_char:<{local_spacing}}{Fore.RESET}"
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
    if not game_data.MapData.map_idle:
        if key == keyboard.Key.up:
            coord_set(game_data.MapData.current_map, 0, 1)
            # Thread(target=coord_set, args=(game_data.MapData.current_map, 0, 1)).start()
        elif key == keyboard.Key.down:
            coord_set(game_data.MapData.current_map, 0, -1)
        elif key == keyboard.Key.right:
            coord_set(game_data.MapData.current_map, 1, 0)
        elif key == keyboard.Key.left:
            coord_set(game_data.MapData.current_map, -1, 0)
        elif key == keyboard.Key.esc:
            game_data.MapData.map_kill = True
            return False  # Test Code, allows code exit mid run
    else:
        pass


def on_press(key):  # For command processing
    if game_data.PlayerData.question_status is True:
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
        except:
            pass

    elif not game_data.MapData.map_idle:
        try:
            if game_data.PlayerData.command_status:
                if key == keyboard.Key.enter:
                    lib.process_command(game_data.MapData.current_command)
                elif key == keyboard.Key.backspace:
                    # Remove last character of both printed message, and the current command string
                    game_data.MapData.current_command = game_data.MapData.current_command[:-1]
                    sys.stdout.write('\b \b')
                else:
                    print(f"{Fore.LIGHTCYAN_EX}{key.char}{Fore.RESET}", end='')
                    game_data.MapData.current_command += key.char
        except:
            pass  # Entered key was a special key
    else:
        pass


# Keyboard Listeners

# Main Input Listener
def kb_listener():
    with keyboard.Listener(on_release=on_release, on_press=on_press) as listener:
        def watcher():
            while True:
                if game_data.MapData.map_kill is True:
                    game_data.MapData.map_kill = False
                    listener.stop()
                    return False  # Kill Watcher Thread
                time.sleep(0.01)  # Probably the most important statement in the entire program
        Thread(target=watcher).start()  # MULTI-THREADING!!!
        listener.join()


# Used for player basic controls tutorial as not to display the active map
def demo_prompt():
    with keyboard.Listener(on_press=on_press) as listener:
        def watcher():
            while True:
                if game_data.MapData.map_kill:
                    game_data.MapData.map_kill = False
                    listener.stop()
                    return False
                time.sleep(0.01)
        Thread(target=watcher).start()
        listener.join()


# Type input only listener (used in question handler)
def question_input():
    with keyboard.Listener(on_press=on_press) as listener:
        def watcher():
            while True:
                if game_data.PlayerData.question_kill:
                    game_data.PlayerData.question_kill = False
                    listener.stop()
                    return False
                time.sleep(0.01)
        Thread(target=watcher).start()
        listener.join()
