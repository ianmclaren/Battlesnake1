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
    #print(game_state)
    BOARD_WIDTH, BOARD_HEIGHT = 11, 11
    fake_board = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    risky_moves = dict() # ranked by how risky - moving into opponent's tail square: 1, moving into possible opponents head location: 2

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

    #Prevent Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    my_tail = find_tail(my_body)
    #TODO: Change this to only avoid tail if snake has just eaten
    for coords in my_body:
        if coords['x'] == my_tail['x'] and coords['y'] == my_tail['y']:
            if my_tail['x'] == move_down['x'] and my_tail['y'] == move_down['y']:
                is_move_safe["down"] = False
                risky_moves['down'] = 1
            if my_tail['x'] == move_up['x'] and my_tail['y'] == move_up['y']:
                is_move_safe["up"] = False
                risky_moves['up'] = 1
            if my_tail['x'] == move_left['x'] and my_tail['y'] == move_left['y']:
                is_move_safe["left"] = False
                risky_moves['left'] = 1
            if my_tail['x'] == move_right['x'] and my_tail['y'] == move_right['y']:
                is_move_safe["right"] = False
                risky_moves['right'] = 1
        else:
            if coords['x'] == move_down['x'] and coords['y'] == move_down['y']:
                is_move_safe["down"] = False
            if coords['x'] == move_up['x'] and coords['y'] == move_up['y']:
                is_move_safe["up"] = False
            if coords['x'] == move_left['x'] and coords['y'] == move_left['y']:
                is_move_safe["left"] = False
            if coords['x'] == move_right['x'] and coords['y'] == move_right['y']:
                is_move_safe["right"] = False

    #Prevent collisions with opponents
    opponents = game_state['board']['snakes']
    #print(opponents)
    for snake in opponents:
        #if snake is me, ignore
        if snake['name'] == game_state['you']['name']:
            continue
        else:
            #avoid head if snake is same size of larger
            for possible_head_pos in find_possible_head_pos(snake):
                if len(snake['body']) >= len(my_body):
                    if possible_head_pos['x'] == move_down['x'] and possible_head_pos['y'] == move_down['y']:
                        is_move_safe["down"] = False
                        risky_moves['down'] = 2
                    if possible_head_pos['x'] == move_up['x'] and possible_head_pos['y'] == move_up['y']:
                        is_move_safe["up"] = False
                        risky_moves['up'] = 2
                    if possible_head_pos['x'] == move_left['x'] and possible_head_pos['y'] == move_left['y']:
                        is_move_safe["left"] = False
                        risky_moves['left'] = 2
                    if possible_head_pos['x'] == move_right['x'] and possible_head_pos['y'] == move_right['y']:
                        is_move_safe["right"] = False
                        risky_moves['right'] = 2
            
            for coords in snake['body']:
                #If this is the tail, set as risky move in case its eaten
                if coords == list(snake['body'][-1]):
                    if coords['x'] == move_down['x'] and coords['y'] == move_down['y']:
                        risky_moves['down'] = 1
                    if coords['x'] == move_up['x'] and coords['y'] == move_up['y']:
                        risky_moves['up'] = 1
                    if coords['x'] == move_left['x'] and coords['y'] == move_left['y']:
                        risky_moves['left'] = 1
                    if coords['x'] == move_right['x'] and coords['y'] == move_right['y']:
                        risky_moves['right'] = 1
                else:
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
        #print("RISKY MOVES ************")
        #print(risky_moves)
        if len(risky_moves) != 0:
            least_risky = min(risky_moves, key=risky_moves.get)
            print("Least risky: " + str(least_risky))
            return {"move": least_risky}
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up")

        return {"move": "up"}

    #Checking board
    for snake in opponents:
        for coords in snake['body']:
            fake_board[coords['x']][coords['y']] = 1

    next_move = best_move(safe_moves, my_body, fake_board)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def find_tail(body):
    return list(body)[-1]

def find_possible_head_pos(snake):
    return [{'x': snake['head']["x"] - 1, 'y': snake['head']["y"]}, {'x': snake['head']["x"] + 1, 'y': snake['head']["y"]}, {'x': snake['head']["x"], 'y': snake['head']["y"] + 1}, {'x': snake['head']["x"], 'y': snake['head']["y"] - 1}]


def best_move(safe_moves, my_body, fake_board):
    if len(safe_moves) == 1:
        return random.choice(safe_moves)

    second_order_safe_moves = second_order_safe(safe_moves, my_body[0], fake_board)
    
    
    #BFS_moves = FloodFill(possible_moves, my_body[0], fake_board)
    #print("Moves after flood fill: " + str(BFS_moves))
    #max_counts = [k for k, v in BFS_moves.items() if v >= 15]
    #if len(max_counts) > 1:
    #    return random.choice(max_counts)
    #else:
    #best_fill = max(BFS_moves, key=BFS_moves.get)
        #print("Best move: " + str(best_fill))
    #return best_fill
    
    return random.choice(second_order_safe_moves)

def second_order_safe(moves, head, board):
    for move in moves:
        if move == 'up':
            check_four_sides(board, head['x'], head['y'] + 1, moves, move)
        if move == 'down':
            check_four_sides(board, head['x'], head['y'] - 1, moves, move)
        if move == 'left':
            check_four_sides(board, head['x'] - 1, head['y'], moves, move)
        if move == 'right':
            check_four_sides(board, head['x'] + 1, head['y'], moves, move)
    return moves
        
def check_four_sides(board, newX, newY, moves, move):
    pos = board[newX][newY]
    if check_board(board, newX + 1, newY) != 0 and check_board(board, newX - 1, newY) != 0 and check_board(board, newX, newY + 1) != 0 and check_board(board, newX, newY - 1) != 0:
        moves.remove(move)


def check_board(board, X, Y):
    if 0 <= X and X < 11 and 0 <= Y and Y < 11:
        return board[X][Y] 
    else: 
        return -1
        

def FloodFill(moves, my_head, fake_board):
    moves_dict = dict.fromkeys(moves, 0)
    #print("Moves: " + str(moves))
    
    #print('Moves dictionary: ' + str(moves_dict))
    for move in moves:
        temp_board = fake_board
        #print(move)
        prevValue = fake_board[my_head['x']][my_head['y']]
        if move == 'up':
            newValue = 2
            print(temp_board)
            FloodFillRecursive(moves_dict, my_head['x'], my_head['y'] + 1, prevValue, newValue, temp_board, 0, move)
            print(temp_board)
        if move == 'down':
            newValue = 3
            print(temp_board)
            FloodFillRecursive(moves_dict, my_head['x'], my_head['y'] - 1, prevValue, newValue, temp_board, 0, move)
            print(temp_board)
        if move == 'right':
            newValue = 4
            FloodFillRecursive(moves_dict, my_head['x'] + 1, my_head['y'], prevValue, newValue, temp_board, 0, move)
        if move == 'left':
            newValue = 5
            FloodFillRecursive(moves_dict, my_head['x'] - 1, my_head['y'], prevValue, newValue, temp_board, 0, move)
    return moves_dict

def FloodFillRecursive(moves_dict, x, y, prevValue, newValue, board, count, move):
    # Base cases
    #print(board)
    if (x < 0 or x >= 4 or y < 0 or
        y >= 4 or board[x][y] != prevValue or
        board[x][y] == newValue):
        moves_dict[move] = max(count, moves_dict[move])
        return 
    #if count > 15:
        #moves_dict[move] = 15
        #return
 
    # Replace the value at (x, y)
    board[x][y] = newValue
    count = count + 1
 
    # Recur for up, down, right and left
    FloodFillRecursive(moves_dict, x + 1, y, prevValue, newValue, board, count, move)
    FloodFillRecursive(moves_dict, x - 1, y, prevValue, newValue, board, count, move)
    FloodFillRecursive(moves_dict, x, y + 1, prevValue, newValue, board, count, move)
    FloodFillRecursive(moves_dict, x, y - 1, prevValue, newValue, board, count, move)



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
