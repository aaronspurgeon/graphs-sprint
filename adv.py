from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
backtrack_path = []
rooms = {}


def flip_direction(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "w":
        return "e"
    if dir == "e":
        return "w"


rooms[player.current_room.id] = player.current_room.get_exits()


while len(rooms) < len(room_graph)-1:
    if player.current_room.id not in rooms:
        rooms[player.current_room.id] = player.current_room.get_exits()
        last_room = backtrack_path[-1]
        rooms[player.current_room.id].remove(last_room)
    while len(rooms[player.current_room.id]) < 1:
        backtrack = backtrack_path.pop()
        player.travel(backtrack)
        traversal_path.append(backtrack)
    else:
        last_exit = rooms[player.current_room.id].pop()
        traversal_path.append(last_exit)
        backtrack_path.append(flip_direction(last_exit))
        player.travel(last_exit)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
