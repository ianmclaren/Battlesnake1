# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "BigMac27",
        "color": "#105c1b",
        "head": "caffeine", 
        "tail": "swoop",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print(game_state)

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    ####    Prevent your Battlesnake from moving out of bounds    ####
    move_left = {'x': my_head["x"] - 1, 'y': my_head["y"]}
    move_right = {'x': my_head["x"] + 1, 'y': my_head["y"]}
    move_up = {'x': my_head["x"], 'y': my_head["y"] + 1}
    move_down = {'x': my_head["x"], 'y': my_head["y"] - 1}

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False

    #Prevent your Battlesnake from colliding with itself
    #TODO: -Stop from trapping myself around my own body
    my_body = game_state['you']['body']
    my_tail = find_tail(my_body)
    for coords in my_body:
        if coords['x'] == my_tail['x'] and coords['y'] == my_tail['y']:
            continue
        if coords['x'] == move_down['x'] and coords['y'] == move_down['y']:
            is_move_safe["down"] = False
        if coords['x'] == move_up['x'] and coords['y'] == move_up['y']:
            is_move_safe["up"] = False
        if coords['x'] == move_left['x'] and coords['y'] == move_left['y']:
            is_move_safe["left"] = False
        if coords['x'] == move_right['x'] and coords['y'] == move_right['y']:
            is_move_safe["right"] = False


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    print(opponents)
    for snake in opponents:
        #if snake is me, ignore
        if snake['name'] == game_state['you']['name']:
            continue
        else:
            #avoid head if snake is same size of larger
            for possible_head_pos in find_possible_head_pos(snake):
                if possible_head_pos['x'] == move_down['x'] and possible_head_pos['y'] == move_down['y']:
                    is_move_safe["down"] = False
                if possible_head_pos['x'] == move_up['x'] and possible_head_pos['y'] == move_up['y']:
                    is_move_safe["up"] = False
                if possible_head_pos['x'] == move_left['x'] and possible_head_pos['y'] == move_left['y']:
                    is_move_safe["left"] = False
                if possible_head_pos['x'] == move_right['x'] and possible_head_pos['y'] == move_right['y']:
                    is_move_safe["right"] = False
            
            for coords in snake['body']:
                if coords['x'] == move_down['x'] and coords['y'] == move_down['y']:
                    is_move_safe["down"] = False
                if coords['x'] == move_up['x'] and coords['y'] == move_up['y']:
                    is_move_safe["up"] = False
                if coords['x'] == move_left['x'] and coords['y'] == move_left['y']:
                    is_move_safe["left"] = False
                if coords['x'] == move_right['x'] and coords['y'] == move_right['y']:
                    is_move_safe["right"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up")
        return {"move": "up"}

    # Choose a random move from the safe ones
    next_move = best_move(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def find_tail(body):
    return list(body)[-1]

def find_possible_head_pos(snake):
    return [{'x': snake['head']["x"] - 1, 'y': snake['head']["y"]}, {'x': snake['head']["x"] + 1, 'y': snake['head']["y"]}, {'x': snake['head']["x"], 'y': snake['head']["y"] + 1}, {'x': snake['head']["x"], 'y': snake['head']["y"] - 1}]


def best_move(safe_moves):
    return random.choice(safe_moves)


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
