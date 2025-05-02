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

    # The make_move method updates the board with the new move. - not works for casting, pawn promotion and en passant yet.
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--' # make the start square empty as the piece has moved from there
        self.board[move.end_row][move.end_col] = move.piece_moved  # Move the piece to the end square
        self.move_log.append(move)  # Add the move to the move log
        self.white_to_move = not self.white_to_move  # Switch turns
    
    def undo_move(self):
        if len(self.move_log) != 0: # to prevent index error when there are no moves made yet
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved #reverse the move by putting the piece back to its original position
            self.board[move.end_row][move.end_col] = move.piece_captured #reverse the piece captured by putting the piece back to its original position
            self.white_to_move = not self.white_to_move  # Switch turns back to the previous player
    """
    Moves considering king is in check
    """
    def get_valid_moves(self):
        return self.get_all_possible_moves()  # Get all possible moves for the current game state

    """
    Moves without considering king is in check
    """
    def get_all_possible_moves(self):
        """
        This is how the function will work:
        1. Go throuugh all the pieces on the board
        2. Check the color of the piece 
        3. If the color is the same as the player to move, get all the possible moves for that piece
        4. If the color is not the same, skip that piece
    
        """
        moves = [Move((6,4), (4,4), self.board)]  # List to store all possible moves
        for r in range(len(self.board)):  # Loop through all rows
            for c in range(len(self.board[r])):  # Loop through all columns in the row
                turn = self.board[r][c][0]  # Get the color of the piece by accessing the first character of the string
                if (turn == 'w'and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1] # Get the type of the piece by accessing the second character of the string
                    if piece == 'P':  # If the piece is a pawn
                        self.get_pawn_moves(r, c, moves)  # Get all possible moves for the pawn
                    elif piece == 'R':  # If the piece is a rook
                        self.get_rook_moves(r, c, moves)
        return moves

    """ 
    Below methods are used to get the possible moves for each piece.
    The methods will check if the move is valid and if the move does not put the king in check.
    """
    def get_pawn_moves(self, r, c, moves):
        pass
    def get_rook_moves(self, r, c, moves):
        pass
            

class Move(): # This class is responsible for storing the information of a move made in the game.
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
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col ## Unique ID for the move

    """
    The __str__ method is used to convert the move to a string representation.
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    
    def get_chess_notation(self):
        # Convert the move to chess notation (e.g., 'e2e4')
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  # Convert the move to chess notation (e.g., 'e2e4') 

    
    def get_rank_file(self, r, c ):
        return self.cols_to_files[c] + self.rows_to_ranks[r]  # Convert the row and column to chess notation (e.g., 'e2' or 'h8')


        

    