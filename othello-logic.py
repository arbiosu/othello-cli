# Author: Arberim Ame
# Description: Othello game logic - originally written for Intro to Computer Science II at Oregon State University

class Player:
    """Represents a player in a game of Othello"""

    def __init__(self, name, piece_color):

        self.name = name
        self.piece_color = piece_color


class Othello:
    """Represents a game of Othello. Initializes the board to the standard Othello opening, and player_list to []"""

    def __init__(self, board=None, player_list=None):

        self._board = [
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
            ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ]

        self._player_list = []

    def print_board(self):
        """Prints out the current board"""

        return print('\n'.join(['    '.join(element) for element in self._board]))
        #  returns the board with each element separated by a tab space, w/o brackets or commas

    def create_player(self, player_name: str, color: str) -> None:
        """
        Creates a player in an Othello game: records their name and the piece color they represent.
        Adds the Player to the player_list
        """

        self._player_list.append(Player(player_name, color))

    def return_winner(self):
        """Tallies the total number of white and black pieces and returns the winner of the game"""

        white_pieces = len(self.current_positions('white'))
        black_pieces = len(self.current_positions('black'))

        if white_pieces > black_pieces:
            winner = [player.name for player in self._player_list if player.piece_color == 'white']
            return f"The winner is white player: {winner[0]}"

        if white_pieces < black_pieces:
            winner = [player.name for player in self._player_list if player.piece_color == 'black']
            return f"The winner is black player: {winner[0]}"

        return f"It's a tie"

    def return_available_positions(self, color: str) -> list[tuple[int, int]]:
        """Returns a list of possible positions a player can place their piece"""

        color = 'O' if color == 'white' else 'X'

        all_positions = [[(row_ind, index) for index, element in enumerate(row)]
                         for row_ind, row in enumerate(self._board)]

        all_positions_flat = [element for sub_list in all_positions for element in sub_list]

        available_positions = [position for position in all_positions_flat if self.check_if_valid(position, color)]

        return available_positions

    def current_positions(self, color: str) -> list[tuple[int, int]]:
        """Returns a list of the positions of each piece on the game board given a piece color"""

        piece = 'O' if color == 'white' else 'X'

        current_positions = [[(row_ind, index) for index, element in enumerate(row) if element == piece]
                             for row_ind, row in enumerate(self._board)]
        #  gets the current positions of a given piece color
        filtered_positions = [pos for pos in current_positions if pos]  # removes the empty sub-lists

        filtered_pos_flattened = [element for sub_list in filtered_positions for element in sub_list]

        return filtered_pos_flattened

    def check_if_valid(self, piece_pos: tuple[int, int], color: str) -> bool:
        """
        Helper function for return_available_positions: checks if given move is valid by determining whether pieces
        can be flipped in a direction. Once a direction is found to be valid, breaks loop.
        """

        row, column = piece_pos
        board = list(self._board)

        if board[row][column] != '.':
            return False
        # if the position is not equal to an empty space, it is not valid
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'X' if color == 'O' else 'O'

        for coordinates in directions:
            coord_row, coord_col = coordinates
            new_row, new_col = row + coord_row, column + coord_col
            #  adds the directional coordinates to the given move
            if board[new_row][new_col] != opponent:
                continue
            #  checks if the direction is == to an opponent's piece. If not, check the next direction
            while 1 <= new_row <= len(board) - 2 and 1 <= new_col <= len(board) - 2:
                if board[new_row][new_col] == '.':
                    break
                # if an empty space is encountered, break the loop, check next direction
                elif board[new_row][new_col] == color:
                    return True
                # if the player's piece is encountered, return True
                new_row += coord_row
                new_col += coord_col
                # if opponent piece is encountered, keep checking this direction
        return False

    def make_move(self, color: str, piece_position: tuple[int, int]) -> list[list[str]]:
        """Places the specified color piece onto the desired position, flips pieces, and returns updated game board"""

        color = 'O' if color == 'white' else 'X'
        row, column = piece_position

        self._board[row][column] = color
        directions = self.flip_pieces(color, piece_position)
        opponent = 'X' if color == 'O' else 'O'

        for coordinates in directions:
            coord_row, coord_col = coordinates
            new_row, new_col = row + coord_row, column + coord_col

            while self._board[new_row][new_col] == opponent:
                self._board[new_row][new_col] = color
                new_row += coord_row
                new_col += coord_col
            #  flips the pieces
        return self._board

    def play_game(self, player_color: str, piece_position: tuple[int, int]) -> str:
        """
        Evaluates whether a move is legal. If legal, makes the move and returns an updated game board. Else,
        returns an error message
        """

        opponent = 'black' if player_color == 'white' else 'white'

        available_pos = self.return_available_positions(player_color)
        if piece_position not in available_pos:
            print(f'Here are the valid moves: {available_pos}')
            return "Invalid move"
        else:
            self.make_move(player_color, piece_position)
            available_pos = self.return_available_positions(player_color)
            if available_pos == [] and self.return_available_positions(opponent) == []:
                white_pieces = len(self.current_positions('white'))
                black_pieces = len(self.current_positions('black'))
                return f'Game is ended white piece: {white_pieces} black piece: {black_pieces}' + '\n' + \
                    self.return_winner()

    def flip_pieces(self, color: str, piece_position: tuple[int, int]) -> list[tuple[int, int]]:
        """Gets all directions where a move is valid based on the piece color and position"""

        row, column = piece_position

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        opponent = 'X' if color == 'O' else 'O'
        legal_directions = []

        for coordinates in directions:
            coord_row, coord_col = coordinates
            new_row, new_col = row + coord_row, column + coord_col
            #  adds the directional coordinates to the given move
            if self._board[new_row][new_col] != opponent:
                continue
            #  checks if the direction is == to an opponent's piece. If not, check the next direction
            while 1 <= new_row <= len(self._board) - 2 and 1 <= new_col <= len(self._board) - 2:
                if self._board[new_row][new_col] == '.':
                    break
                # if an empty space is encountered, break the loop, check next direction
                elif self._board[new_row][new_col] == color:
                    legal_directions.append((coordinates))
                    break
                # if the player's piece is encountered, append coordinate
                new_row += coord_row
                new_col += coord_col
                # if opponent piece is encountered, keep checking this direction
        return legal_directions
