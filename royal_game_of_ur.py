""" This is the Royal Game of UR """
import numpy as np


class UrBoard:

    def __init__(self):
        self.board_string = "W0WWWWWWWBBBBBBB123456789abcdef"
        self.board = {}
        self.board[0] = {"W": 7, "B": 7}
        for i in range(1, 16, 1):
            self.board[i] = {"W": 0, "B": 0}
        self.turn = "W"
        self.player_space = [1, 2, 3, 4, 13, 14]
        self.shared_space = [5, 6, 7, 8, 9, 10, 11, 12]
        self.special = [4, 8, 14]
        self.dice = Dice()

    def roll_dice(self):
        self.dice.roll()
        return self.dice.value

    def board_to_string(self):
        saver = self.turn
        for i in range(16):
            saver += f"{i:x}"
            saver += self.board[i]["W"] * "W" + self.board[i]["B"] * "B"
        self.board_string = saver
        return saver
    
    def string_to_board(self):
        saver = {i: {"W": 0 , "B": 0} for i in range(16)}
        tile = 0
        self.turn = self.board_string[0]
        for c in self.board_string[1:]:
            if c in "".join([f"{i:x}" for i in range(16)]):
                tile = int(c, base=16)
            elif c in ["W", "B"]:
                saver[tile][c] += 1
        self.board = dict(saver)
        return saver

    def possible_moves(self):
        moves = []
        roll = self.dice.value
        if roll == 0:
            return []
        for key in self.board:
            if roll + key < 16:
                loc = self.board[key][self.turn]
                dest = self.board[key + roll][self.turn]
                dest_opponent = self.board[key + roll][self.opponent()]
                if loc > 0:
                    if key + roll in [0, 15]:
                        moves.append(key)
                    elif dest == 0:
                        if key + roll in list(set(self.shared_space) & set(self.special)):
                            if dest_opponent == 0:
                                moves.append(key)
                        else:
                            moves.append(key)
        return moves

    def make_move(self, move: int):
        roll = self.dice.value
        if roll == 0 or move < 0:
            self.turn = self.opponent()
            return
        self.board[move][self.turn] -= 1
        self.board[move + roll][self.turn] += 1
        opp_pieces = self.board[move+roll][self.opponent()]
        if move + roll in self.shared_space and opp_pieces > 0:
            self.board[move + roll][self.opponent()] = 0
            self.board[0][self.opponent()] += opp_pieces
            assert opp_pieces in [0, 1], "Cannot have multiple opponent pieces on shared space!"

        if not move + roll in self.special:
            self.turn = self.opponent()
        
        self.board_string = self.board_to_string()
    
    def opponent(self):
        return "".join(chrctr for chrctr in "WB" if chrctr != self.turn)



class Dice:
    def __init__(self):
        self.value = 0
        self.dice_config = [0, 0, 0, 0]
    
    def roll(self):
        self.dice_config = np.random.randint(0, high=2, size=4)
        self.value = sum(self.dice_config)


class Player:
    def __init__(self, name):
        self.name = name
        self.stones = np.zeros((7), dtype=int)


def display_board(board_string):
    
    displayed = " " * (9 + 8 + 16) + "\n"
    line_length = len(displayed)
    displayed += "-" * (1 + 4 * 4) + " " * (4 + 3) + "-" * (1 + 2 * 4) + "\n"
    displayed += "|% %| " + "  | " * 3 + " " * (1 + 3 + 1) + " |% %|   |" + "\n"
    displayed += "-" * (1 + 8 * 4) + "\n"
    displayed += "|" + "   |" * 3 + "% %|" + "   |" * 4 + "\n"
    displayed += "-" * (1 + 8 * 4) + "\n"
    displayed += "|% %| " + "  | " * 3 + " " * (1 + 3 + 1) + " |% %|   |" + "\n"
    displayed += "-" * (1 + 4 * 4) + " " * (4 + 3) + "-" * (1 + 2 * 4) + "\n"
    displayed += " " * (9 + 8 + 16) + "\n"

    white_positions_dict = {
        1: (2 + 4 * 3) + line_length * 2,
        2: (2 + 4 * 2) + line_length * 2,
        3: (2 + 4) + line_length * 2,
        4: 2 + line_length * 2,
        5: 2 + line_length * 4,
        6: 2 + 4 * 1 + line_length * 4,
        7: 2 + 4 * 2 + line_length * 4,
        8: 2 + 4 * 3 + line_length * 4,
        9: 2 + 4 * 4 + line_length * 4,
        10: 2 + 4 * 5 + line_length * 4,
        11: 2 + 4 * 6 + line_length * 4,
        12: 2 + 4 * 7 + line_length * 4,
        13: 2 + 4 * 7 + line_length * 2,
        14: 2 + 4 * 6 + line_length * 2,
    }

    black_positions_dict = {
        1: (2 + 4 * 3) + line_length*6,
        2: (2 + 4 * 2) + line_length*6,
        3: (2 + 4) + line_length*6,
        4: 2 + line_length*6,
        5: 2 + line_length * 4,
        6: 2 + 4 * 1 + line_length * 4,
        7: 2 + 4 * 2 + line_length * 4,
        8: 2 + 4 * 3 + line_length * 4,
        9: 2 + 4 * 4 + line_length * 4,
        10: 2 + 4 * 5 + line_length * 4,
        11: 2 + 4 * 6 + line_length * 4,
        12: 2 + 4 * 7 + line_length * 4,
        13: 2 + 4 * 7 + line_length * 6,
        14: 2 + 4 * 6 + line_length * 6,
    }

    displayed_list = list(displayed)
    idx_start = board_string.find("0") + 1
    idx_end = board_string.find("1")
    pieces = board_string[idx_start:idx_end]
    black_home = 0
    white_home = 0
    for p in pieces:
        if p == "W":
            white_home += 1
            displayed_list[ 2 * white_home ] = "W"
        elif p == "B":
            black_home += 1
            displayed_list[ 2 * black_home + line_length * 8 ] = "B"
    idx_start = board_string.find("f") + 1
    pieces = board_string[idx_start:]
    black_converted = 0
    white_converted = 0
    for p in pieces:
        if p == "W":
            white_converted += 1
            displayed_list[ line_length - 2 * white_converted ] = "W"
        elif p == "B":
            black_converted += 1
            displayed_list[ line_length - 2 * black_converted + line_length * 8 ] = "B"

    for i in range(1, 15, 1):
        idx_start = board_string.find(f"{i:x}") + 1
        idx_end = board_string.find(f"{i+1:x}")
        pieces = board_string[idx_start:idx_end]
        if "W" in pieces:
            print(i)
            displayed_list[white_positions_dict.get(i)] = "W"
        if "B" in pieces:
            displayed_list[black_positions_dict.get(i)] = "B"
    displayed = "".join(displayed_list)

    print(displayed)

    if white_converted >= 7:
        print("Player White wins! Congratulations.")
        return True
    elif black_converted >= 7:
        print("Player Black wins! Congratulations.")
        return True
    return False


def main():
    print("\n\n\n\n\n\n\n\n")
    # Game setup
    quit_game = False
    values = np.zeros((5), dtype=int)
    game_board = UrBoard()
    players = [
        Player("Black"),
        Player("White"),
    ]

    # Game loop
    loop_counter = 0
    quit_game = display_board(game_board.board_string)
    game_board.roll_dice()
    while True:
        if quit_game:
            break
        loop_counter += 1
        print(f"Move {loop_counter}: {game_board.turn} rolled a {game_board.dice.value}")
        possible_moves = game_board.possible_moves()
        if possible_moves:

            print(f"Possible moves are {possible_moves}")

            # process input
            in_string = input("What move to make? ")
            if in_string == 'q':
                quit_game = True
                continue
            elif not in_string in [f"{i}" for i in range(16)]:
                print("Not a possible move. Please select again or press 'q' to quit.")
                continue


            chosen_move = int(in_string, base=10)
            if chosen_move in possible_moves:
                print(f"Making move {in_string}")
            else:
                print(f"The selected move is not possible! Please choose again!")
                loop_counter -= 1
                continue
        else:
            chosen_move = -1

        # update game status
        values[game_board.dice.value] += 1
        game_board.make_move(chosen_move)
        game_board.roll_dice()

        # render
        quit_game = display_board(game_board.board_string)

    print()

    # clean up the game 
    print("Check RNG:")
    print("0:{:3.02f} 1:{:3.02f} 2:{:3.02f} 3:{:3.02f} 4:{:3.02f}".format(*values/loop_counter))


if __name__ == "__main__":
    main()
