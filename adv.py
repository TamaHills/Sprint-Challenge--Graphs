from room import Room
from player import Player
from world import World
from hashlib import sha256
from os import system
import random
from ast import literal_eval
from sys import maxsize, argv, platform
# Load world
world = World()

# ascii escape sequence helpers to control console output
PURPLE = "\033[95m"
CYAN ="\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BRIGHT = '\033[97m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

def clear():
    if platform == 'win32':
        system('cls')
    else:
        system('clear')

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# topseeds
# 980 - 93d2f3322e2f7d67f24b69284c71be245b164b0a5b41ee48bbe3b8d9606ff7f0
# 984 - 477ae527d38391cac075c65ff292ffd3bbb1132ee68901f994db6babc690508d
# 986 - ba9f9df2af8aeb073add0f65be5cd95cad5d3f60bfafd42e8f09ada65f2906f7
# 987 - cee41f2318ec12cef2b69755d634d25b7f73a0d4a5ab7fc268236a3d36195c94
# 994 - b3361043b83e8bdf4e909465f6eeb191c52c199fddeb10ccf4ea9ab32be5e279

# 1.1
# 953 - 5f86c9d0588ff690e9d9622fc29e80358075b39b42a4239b9d92809256b97f69
# 969 - d6c91c41896f5abadc62bf0815bb639fd273fbef534bccf707d10aa2f0552ac2
# 976 - d5e247e9fcd939c3ea19306caa0394231c470532a740d5770c6165ad34b1648f
# 981 - 9b66d50dc29043f8954ba8318cc2562a505ab55bff88264d18e5d1d6ec1d97a4
# 985 - c1e2efc3be1dc0464445c9dc6d5ffb0c15ebf27b5f687ee891d5f6837aca52bf
# 986 - 588b972d443d8e7e46f05265f05cc7c327f1aa8ffee3d286511e7f9df53fe8c3
# 987 - 3b731fdff8d25ae9d5ca6bf2bf7d4c762be19c19975ae92766bf69cce56773d6
# 990 - 8b2f4767fe18ae9feb57c31efc760de67d3af137cc345143238b5097d9d87f32


# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
topseed = '5f86c9d0588ff690e9d9622fc29e80358075b39b42a4239b9d92809256b97f69'
player = Player(world.starting_room)

def new_seed():return sha256(f'{random.randint(0, maxsize)}'.encode()).hexdigest()

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
reverse_map = {'n':'s','e':'w','s':'n','w':'e'}

def traverse_graph(starting_room, seed, path=None, visited=None ):

    if not visited:
        visited = set()
    if not path:
        path = []

    room = starting_room
    visited.add(starting_room.id)
    rooms = room.get_exits()
    # seed = f'{seed}{room.id}' # old algo
    room_seed = sha256(f'{seed}{room.id}'.encode()).hexdigest()
    random.seed(room_seed)
    random.shuffle(rooms)
    for direction in rooms:
        next_room = room.get_room_in_direction(direction)
        if next_room.id not in visited:
            path.append(direction)
            traverse_graph(next_room, room_seed, path, visited)
            if len(visited) != len(room_graph):
                path.append(reverse_map[direction])
    
    
    return path

# def main():
#     if len(argv) >= 2:
#         if argv[1] == 'random':
#             fresh_seed = new_seed()
#             traversal_path = traverse_graph(world.starting_room)
#             print(fresh_seed)
        
#         if argv[1] == 'mine':
#             if len(argv) == 3:
#                 global topseed
#                 topseed = argv[2]
#             path = traverse_graph(world.starting_room, topseed)
#             count = 0
#             lowest = len(path)
#             best_seed = '0'
#             try: 
#                 while True:
#                     path = []
#                     fresh_seed = new_seed()
#                     path = traverse_graph(world.starting_room, fresh_seed)
#                     if len(path) < lowest:
#                         lowest = len(path)
#                         topseed = fresh_seed
#                         clear()
#                         print(f'{GREEN}Best Seed: {topseed}{END}')
#                         print(f'{BLUE}Lowest: {lowest}{END}')
#                         print(f'{RED}Count: {count}{END}')
#                     if count % 1000 == 0:
#                         clear()
#                         print(f'{GREEN}Best Seed: {topseed}{END}')
#                         print(f'{BLUE}Lowest: {lowest}{END}')
#                         print(f'{RED}Count: {count}{END}')
#                     count += 1
#             except KeyboardInterrupt:
#                 traversal_test()
#                 exit()

#         else:
#             topseed = argv[1]
#             traversal_path = traverse_graph(world.starting_room, topseed)
#     else:
#         traversal_path = traverse_graph(world.starting_room, topseed)

#   traversal_test()

def traversal_test():
    # TRAVERSAL TEST
    traversal_path = traverse_graph(world.starting_room, topseed)
    world.print_rooms()
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        print(f"{GREEN}TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited{END}")
        print(f'{BOLD}TOPSEED: {YELLOW}{topseed}{END}')
    else:
        print("{RED}TESTS FAILED: INCOMPLETE TRAVERSAL{END}")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


if __name__ == '__main__':
    try:
        # main()
        traversal_test
    except KeyboardInterrupt:
        clear()
        print('topseed:', topseed)
        exit(0)