import sys
import game_data
from colorama import init
from colorama import Fore, Back, Style
import os
from pynput import keyboard
from threading import Thread
import time
import lib


init()
global Data


# Note: Create map then use reverse operation for coordinate reading otherwise everything will be confusing
def get_coord(map_in):
    map_in = map_in.map_array[::-1]  # Reverse the map
    for y in range(len(map_in)):
        for x in range(len(map_in[y])):
            if map_in[y][x] == "x":
                return [x, y]
    return False


def get_coord_char(map_in, x, y):
    # Checks what character is in the specified position
    return map_in.map_array[::-1][y][x]


# Coordinate init code:
def init_coord():
    init_coordinates = get_coord(game_data.MapData.current_map)
    game_data.MapData.y = init_coordinates[1]
    game_data.MapData.x = init_coordinates[0]


def enemy_move_calc(map_in):  # This was such a simple task, why did I add a enemy movement system?
    pass


def coord_set(map_in, x_m, y_m):  # Main Movement Engine
    # Move point to a certain position on the map
    # Collision Checking

    # x_m = Amount to move on x plane
    # y_m = Amount to move on y plane

    # Check to see if next coordinate pairs is an illegal movement if it is, don't move
    # if it is not, get the current coordinates and reset the position to a blank spot
    # move the players char to the new set of coordinates
    new_x = game_data.MapData.x + x_m
    new_y = game_data.MapData.y + y_m
    if not (new_x > len(map_in.map_array[0]) - 1 or new_x < 0 or new_y > len(map_in.map_array) - 1 or new_y < 0):
        future_char = get_coord_char(map_in, new_x, new_y)
        if not Data.movement_blacklist.__contains__(future_char):
            internal_coordinates = []
            for yi, y in enumerate(map_in.map_array):
                for xi, x in enumerate(y):
                    if x == "x":
                        internal_coordinates = [xi, yi]

            os.system("cls")
            game_data.MapData.x += x_m
            game_data.MapData.y += y_m
            map_in.map_array[internal_coordinates[1]][internal_coordinates[0]] = game_data.MapData.last_char
            map_in.map_array[::-1][game_data.MapData.y][game_data.MapData.x] = "x"  # Enter new position
            show_map(map_in)
            # Fix this BS
            game_data.MapData.last_char = future_char


def show_map(map_in):
    # Print the map

    print("{:^50}".format(map_in.map_name))
    print(f"{Fore.RED}{'/':^{Data.map_spacing}}{Fore.RESET}" * len(map_in.map_array[0]))
    map_out = ""
    for y in map_in.map_array:
        cur_row = ""  # Reset the line print out
        for x in y:
            # Get Current Character and add it to the formatted line
            cur_char = x
            if cur_char == "":
                cur_char = f"{' ':<{Data.map_spacing}}"
            elif cur_char == "X":
                cur_char = f"{Fore.YELLOW}{cur_char:<{Data.map_spacing}}{Fore.RESET}"
            elif cur_char == "x":
                cur_char = f"{Fore.CYAN}{cur_char:<{Data.map_spacing}}{Fore.RESET}"
            elif cur_char == "-":
                cur_char = f"{Fore.LIGHTGREEN_EX}{cur_char:<{Data.map_spacing}}{Fore.RESET}"

            cur_row += cur_char
        map_out += f"{cur_row}{Fore.RED}/{Fore.RESET}\n"
    print(map_out, end='')  # Reduces the flashing of the console
    print(f"{Fore.RED}{'/':^{Data.map_spacing}}{Fore.RESET}" * len(map_in.map_array[0]))
    print(f"Your current position is {get_coord(map_in)} "
          f"(Represented by the {Fore.GREEN + 'x' + Style.RESET_ALL})")


def on_release(key):
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


def on_press(key):
    try:
        if key == keyboard.Key.enter:
            lib.process_command()
        elif key == keyboard.Key.backspace:
            # Remove last character of both printed message, and the current command string
            game_data.MapData.current_command = game_data.MapData.current_command[:-1]
            sys.stdout.write('\b \b')
        else:
            print(key.char, end='')
            game_data.MapData.current_command += key.char
    except AttributeError:
        pass  # Entered key was a special key


def kb_listener():
    def listener_start():
        with keyboard.Listener(on_release=on_release, on_press=on_press) as listener:
            def watcher():
                while True:
                    if game_data.MapData.map_kill is True:
                        game_data.MapData.map_kill = False
                        listener.stop()
                        return False  # Kill Watcher Thread
                    time.sleep(0.1)  # Probably the most important statement in the entire program
            Thread(target=watcher).start()  # MULTI-THREADING!!!
            listener.join()

            print("Listener Ended")
    Thread(target=listener_start).start()


def demo_prompt():
    # Raw Keyboard input for commands
    def listener_start():
        with keyboard.Listener(on_press=on_press) as Listener:
            Listener.start()
    Thread(target=listener_start()).start()
