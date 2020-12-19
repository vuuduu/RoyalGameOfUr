"""
File:         board_square.py
Author:       Vu Nguyen
Date:         11/13/2020
Section:      31
E-mail:       vnguye12@umbc.edu
Description:  This is a modified board square
"""


class UrPiece:
    BLACK = 'Black'
    WHITE = 'White'
    CANT_MOVE = 0
    OFF_BOARD_MOVE = 1

    def __init__(self, color, symbol):
        self.color = color
        self.position = None  # <-- This store board square object
        self.exit_pos = None  # <-- This store exit board square object
        self.start_pos = None  # <- This store start board square to piece
        self.complete = False
        self.symbol = symbol

    def can_move(self, num_moves, the_board):

        if num_moves == self.CANT_MOVE:
            return False
        else:

            # This loop find which board_square is the piece is currently on
            for row in the_board:
                for board_square in row:

                    # This condition checks if the piece is on the board
                    if self.position:
                        if self.position == board_square:
                            check_position = self.position
                            if self.color == self.WHITE:

                                # This loop checks position for white piece
                                for steps in range(num_moves):
                                    if check_position == self.exit_pos:

                                        # This function checks for exiting position for white
                                        if num_moves - steps > self.OFF_BOARD_MOVE:
                                            return False
                                        else:
                                            return True
                                    else:
                                        check_position = check_position.next_white

                                # This call function to check the square for pieces and rosette
                                if self.checking_square(check_position):
                                    return True
                                else:
                                    return False

                            elif self.color == self.BLACK:

                                # This loop checks position for black piece
                                for steps in range(num_moves):
                                    if check_position == self.exit_pos:

                                        # This function checks for exiting position for black
                                        if num_moves - steps == self.OFF_BOARD_MOVE:
                                            return True
                                        else:
                                            return False
                                    else:
                                        check_position = check_position.next_black

                                # This call function to check the square for pieces and rosette
                                if self.checking_square(check_position):
                                    return True
                                else:
                                    return False
                    else:
                        # This condition checks if the piece is off the board for white.
                        if board_square.entrance == self.WHITE and self.color == self.WHITE:
                            check_white_position = board_square

                            # This loop find the new position to checks for off board white piece
                            for steps in range(num_moves - self.OFF_BOARD_MOVE):
                                if check_white_position == self.exit_pos:

                                    # This function checks for exiting position for white
                                    if (num_moves - self.OFF_BOARD_MOVE) - steps == self.OFF_BOARD_MOVE:
                                        return True
                                    else:
                                        return False
                                else:
                                    check_white_position = check_white_position.next_white

                            # This call function to check the square for pieces and rosette
                            if self.checking_square(check_white_position):
                                return True
                            else:
                                return False

                        # This condition checks if the piece is off the board for black.
                        elif board_square.entrance == self.BLACK and self.color == self.BLACK:
                            check_black_position = board_square

                            # This loop find the new position to checks for off board white piece
                            for steps in range(num_moves - self.OFF_BOARD_MOVE):
                                if check_black_position == self.exit_pos:

                                    # This function checks for exiting position for white
                                    if (num_moves - self.OFF_BOARD_MOVE) - steps == self.OFF_BOARD_MOVE:
                                        return True
                                    else:
                                        return False
                                else:
                                    check_black_position = check_black_position.next_black

                            # This call function to check the square for pieces and rosette
                            if self.checking_square(check_black_position):
                                return True
                            else:
                                return False

    def checking_square(self, check_position):
        """
        This helper function check whether the new position is empty, different color pieces
        or no rosette square occupied by the different pieces.
        :param check_position: The Board Square that the piece suppose to go on
        :return: Either True or False
        """
        if not check_position.piece:
            return True
        else:
            if check_position.piece.color != self.color:
                if check_position.rosette:
                    return False
                else:
                    return True
            else:
                return False


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
