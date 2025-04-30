#Its the class which is responsible for storing all the information for the current state of the chess game 
#Also responsible for determining the legality of moves and updating the game state accordingly. 
#It will also keep a move history of the game. - for undo and redo functionality.

class GameState():
    def __init__(self):
        self.board = [ 
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
# The GameState class initializes the chessboard with the starting positions of all pieces.
# The board is represented as a list of lists, where each inner list represents a row on the chessboard.
        self.white_to_move = True  # True if it's white's turn, False
        self.move_log = []  # List to keep track of moves made in the game

    # The make_move method updates the board with the new move.
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--' # make the start square empty as the piece has moved from there
        self.board[move.end_row][move.end_col] = move.piece_moved  # Move the piece to the end square
        self.move_log.append(move)  # Add the move to the move log
        self.white_to_move = not self.white_to_move  # Switch turns

class Move():
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0} # Dictionary to convert ranks to rows
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # Reverse the dictionary to convert rows to ranks
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7} # Dictionary to convert files to columns
    cols_to_files = {v: k for k, v in files_to_cols.items()}  # Reverse the dictionary to convert columns to files
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]  # Row of the starting square - tuple
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_chess_notation(self):
        # Convert the move to chess notation (e.g., 'e2e4')
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  # Convert the move to chess notation (e.g., 'e2e4') 

    
    def get_rank_file(self, r, c ):
        return self.cols_to_files[c] + self.rows_to_ranks[r]  # Convert the row and column to chess notation (e.g., 'e2' or 'h8')


        

    