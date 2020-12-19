from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece
"""
File:         royal_ur.py
Author:       Vu Nguyen
Date:         11/13/2020
Section:      31
E-mail:       vnguye12@umbc.edu
Description:  This a Royal Game of Ur Program that let users
              chose there players name and given pre-made 
              pieces (black and white). 
"""


class RoyalGameOfUr:
    # Constant
    WHITE = 'White'
    BLACK = 'Black'
    TURN = 'Turn'
    PIECES = 'Pieces'
    STARTING_PIECES = 7
    NUM_OF_PLAYER = 2

    def __init__(self, board_file_name):
        self.p1_list = None
        self.p2_list = None
        self.board = None
        self.players_info = None
        self.player_one = None
        self.player_two = None
        self.load_board(board_file_name)

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'],
                                                         rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        self.setting_up_player_and_pieces()

        self.set_exit_position()
        self.set_start_position()

        # THE LOOP #
        game_over = False

        while not game_over:
            self.display_board()

            num_moves = self.roll_d4_dice()
            print("\nYou rolled a", num_moves)

            # This loop checks for player turn
            for player in self.players_info:
                if self.players_info[player][self.TURN]:
                    chosen_piece = self.movable_piece(self.players_info[player][self.PIECES], num_moves)

                    # Check to see if the piece is available and if land on rosette go again
                    if chosen_piece:
                        self.set_piece_position(chosen_piece, num_moves)

                        # This condition checks to see if the piece left the board.
                        if chosen_piece.position:
                            if not chosen_piece.position.rosette:
                                self.players_info[player][self.TURN] = False
                                if player == self.player_two:
                                    self.players_info[self.player_one][self.TURN] = True
                        else:
                            self.players_info[player][self.TURN] = False
                            if player == self.player_two:
                                self.players_info[self.player_one][self.TURN] = True

                    else:
                        self.players_info[player][self.TURN] = False
                        if player == self.player_two:
                            self.players_info[self.player_one][self.TURN] = True
                else:
                    if player == self.player_two and not self.players_info[self.player_one][self.TURN]:
                        self.players_info[player][self.TURN] = True

            # This loop remove pieces that completed its path
            for person in self.players_info:
                for pieces in self.players_info[person][self.PIECES]:
                    if pieces.complete:
                        self.players_info[person][self.PIECES].remove(pieces)

            # This condition checks to see who wins.
            if not self.players_info[self.player_one][self.PIECES]:
                print("{} WINS!".format(self.player_one))
                game_over = True
            elif not self.players_info[self.player_two][self.PIECES]:
                print("{} WINS!".format(self.player_two))
                game_over = True

    def setting_up_player_and_pieces(self):
        """
        This helper function ask each players for their name and also create
        7 piece for each player.
        :return: players_info
        """
        self.p1_list = []
        self.p2_list = []
        self.players_info = {}

        # This loop creates 7 pieces for each players
        for pieces in range(self.STARTING_PIECES):
            self.p1_list.append(UrPiece(self.WHITE, "W" + str(pieces)))
            self.p2_list.append(UrPiece(self.BLACK, "B" + str(pieces)))

        self.player_one = input("What is your name? ")
        print(self.player_one, 'you will play as white.')

        self.player_two = input("What is your name? ")
        print(self.player_two, 'you will play as black.')

        # This loop create a dictionary of two players and it information.
        for i in range(self.NUM_OF_PLAYER):
            temporary_player_info = {}
            if i == 0:
                temporary_player_info[self.TURN] = True
                temporary_player_info[self.PIECES] = self.p1_list
                self.players_info[self.player_one] = temporary_player_info
            else:
                temporary_player_info[self.TURN] = False
                temporary_player_info[self.PIECES] = self.p2_list
                self.players_info[self.player_two] = temporary_player_info

    def movable_piece(self, player_pieces, num_moves):
        """
        This helper function takes in all the piece that the current
        player have and display all the piece that it can be moved.
        It also asked the player which piece they want to move and
        return that piece.
        :param player_pieces: A list of all the current player pieces.
        :param num_moves: the number of allowable moves rolled by dice.
        :return: the user_chosen piece
        """
        can_move_piece = []
        option_pieces = []

        # This loop append all the movable pieces to a list.
        for pieces in player_pieces:
            if not pieces.complete and pieces.can_move(num_moves, self.board):
                can_move_piece.append(pieces)

        # This loops display all the available piece that user can move
        for index, piece in enumerate(can_move_piece):
            if not piece.position:
                print("{}: {} currently off the board".format(index + 1, piece.symbol))
                option_pieces.append(str(index + 1))
            else:
                print("{}: {} {}".format(index + 1, piece.symbol, piece.position.position))
                option_pieces.append(str(index + 1))

        # This loops checks to see if the user input a correct available pieces
        correct_input = False
        chosen_piece = None
        if not can_move_piece:
            return chosen_piece
        else:
            while not correct_input:
                chosen_piece = input("Which move do you want to make? ")
                if chosen_piece in option_pieces:
                    correct_input = True
                    chosen_piece = can_move_piece[int(chosen_piece) - 1]
                else:
                    print("Incorrect input!")

            return chosen_piece

    def set_exit_position(self):
        """
        This helper function cycle through each board_square
        and check for the exit position of. If the b_s exit
        is black, all the black piece exit_pos will be assign
        that b_s. Same goes for white pieces.
        :return: set up the exit position for all the pieces
        """
        for row in self.board:
            for board_square in row:
                for white_piece in self.p1_list:
                    if board_square.exit == white_piece.color:
                        white_piece.exit_pos = board_square
                for black_piece in self.p2_list:
                    if board_square.exit == black_piece.color:
                        black_piece.exit_pos = board_square

    def set_start_position(self):
        """
        THis helper function cycle through each board_square
        and check for the entrance (aka start_pos). If b_s
        entrance is white all white start_pos will be assign
        that b_s. Same goes for black pieces.
        :return: set up the start position for all the pieces
        """
        for row in self.board:
            for board_square in row:
                for white_piece in self.p1_list:
                    if board_square.entrance == white_piece.color:
                        white_piece.start_pos = board_square
                for black_piece in self.p2_list:
                    if board_square.entrance == black_piece.color:
                        black_piece.start_pos = board_square

    def set_piece_position(self, chosen_piece, num_moves):
        """
        This helper function capture and update the piece position.
        :param chosen_piece: The pieces that player wanted to move
        :param num_moves: The number or move player can take
        :return: set up the chosen piece position and capture any piece on the square
        """

        if chosen_piece.color == self.WHITE:

            # This condition checks if it on or off the board for white
            if not chosen_piece.position:
                change_square = chosen_piece.start_pos

                for steps in range(num_moves - 1):
                    change_square = change_square.next_white

            else:
                change_square = chosen_piece.position

                for steps in range(num_moves):
                    change_square = change_square.next_white

            # This condition checks to see if the piece complete it path
            if not change_square:
                chosen_piece.complete = True
                chosen_piece.position.piece = None
                chosen_piece.position = None
            else:
                self.update_piece(change_square, chosen_piece)

        elif chosen_piece.color == self.BLACK:

            # This condition checks if it on or off the board for black
            if not chosen_piece.position:
                change_square = chosen_piece.start_pos

                for steps in range(num_moves - 1):
                    change_square = change_square.next_black

            else:
                change_square = chosen_piece.position

                for steps in range(num_moves):
                    change_square = change_square.next_black

            if not change_square:
                chosen_piece.complete = True
                chosen_piece.position.piece = None
                chosen_piece.position = None
            else:
                self.update_piece(change_square, chosen_piece)

    def update_piece(self, change_square, chosen_piece):

        # This condition checks to see if there a white pieces in the square
        if not change_square.piece:
            if chosen_piece.position:
                chosen_piece.position.piece = None  # This clear out the old b_s of the piece

            chosen_piece.position = change_square  # This update the moving piece position
            change_square.piece = chosen_piece  # This update the new position for the moving piece
        else:
            if chosen_piece.position:
                chosen_piece.position.piece = None  # This remove the moving piece from the old square

            change_square.piece.position = None  # This remove the old piece from the new square
            chosen_piece.position = change_square  # This update the moving piece position
            change_square.piece = chosen_piece  # This update the new_square to the moving piece


if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
