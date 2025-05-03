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
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves, 'B': self.get_bishop_moves,
                               'Q': self.get_queen_moves, 'K': self.get_king_moves}  # Dictionary to map piece types to their move functions
# The GameState class initializes the chessboard with the starting positions of all pieces.
# The board is represented as a list of lists, where each inner list represents a row on the chessboard.
        self.white_to_move = True  # True if it's white's turn, False
        self.move_log = []  # List to keep track of moves made in the game

    # The make_move method updates the board with the new move. - not works for casting, pawn promotion and en passant yet.
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        print(f"Board after move: {self.board}")  # Debugging
    
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
        moves = self.get_all_possible_moves()
        print("Valid moves:", [move.get_chess_notation() for move in moves])  # Debugging
        return moves

    """
    Moves without considering king is in check
    """
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    print(f"Checking piece {piece} at {r}, {c}")  # Debugging
                    self.move_functions[piece](r, c, moves)  # Call the appropriate move function for the piece

        print(f"Generated moves: {[move.get_chess_notation() for move in moves]}")  # Debugging
        return moves

    """ 
    Below methods are used to get the possible moves for each piece.
    The methods will check if the move is valid and if the move does not put the king in check.
    """
    def get_pawn_moves(self, r, c, moves):
        """
        The legal moves for a pawn are:
        1. Move two squares forward from its starting position (if not blocked).
        2. Move one square forward (if not blocked).
        3. Capture diagonally (if an opponent's piece is present).
        4. En passant (if applicable).
        5. Promotion (if it reaches the opposite end of the board).
        """
        if self.white_to_move:  # White pawns move up
            if self.board[r-1][c] == '--':  # Move one square forward
                moves.append(Move((r, c), (r-1, c), self.board))
            if r == 6 and self.board[r-2][c] == '--' and self.board[r-1][c] == '--':  # Move two squares forward
                moves.append(Move((r, c), (r-2, c), self.board))
            # Diagonal captures
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':  # Capture left
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 < len(self.board[r]) and self.board[r-1][c+1][0] == 'b':  # Capture right
                moves.append(Move((r, c), (r-1, c+1), self.board))
        else:  # Black pawns move down
            if self.board[r+1][c] == '--':  # Move one square forward
                moves.append(Move((r, c), (r+1, c), self.board))
            if r == 1 and self.board[r+2][c] == '--' and self.board[r+1][c] == '--':  # Move two squares forward
                moves.append(Move((r, c), (r+2, c), self.board))
            # Diagonal captures
            if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':  # Capture left
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 < len(self.board[r]) and self.board[r+1][c+1][0] == 'w':  # Capture right
                moves.append(Move((r, c), (r+1, c+1), self.board))

    
    def get_rook_moves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))  # Up, Left, Down, Right movements
        enemy_color = 'b' if self.white_to_move else 'w'  # Determine the enemy color
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i  # Calculate the new row position
                end_col = c + d[1] * i  # Calculate the new column position
                if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[end_row]):  # Check if the position is within the board
                    end_piece = self.board[end_row][end_col]  # Get the piece at the new position
                    if end_piece == '--':  # If the square is empty, add the move
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # If the square has an enemy piece, add the move and break
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # If the square has a friendly piece, break
                        break
                else:  # If the position is out of bounds, break
                    break

    def get_knight_moves(self, r, c, moves):
        knight_moves = ((-2,-1), (-1,-2), (1,-2), (2,-1), (2,1), (1,2), (-1,2), (-2,1))
        enemy_color = 'b' if self.white_to_move else 'w'  # Determine the enemy color
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]  # Calculate the new column position
            if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[end_row]):  # Check if the position is within the board
                end_piece = self.board[end_row][end_col]  # Get the piece at the new position
                if end_piece == enemy_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                elif end_piece == '--':  # If the square is empty, add the move 
                    moves.append(Move((r, c), (end_row, end_col), self.board))
            

    def get_bishop_moves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))  # Up-Left, Up-Right, Down-Left, Down-Right movements
        enemy_color = 'b' if self.white_to_move else 'w'  # Determine the enemy color
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i  # Calculate the new column position
                if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[end_row]):  # Check if the position is within the board
                    end_piece = self.board[end_row][end_col]  # Get the piece at the new position
                    if end_piece == '--':  # If the square is empty, add the move
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # If the square has an enemy piece, add the move and break
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:  # If the position is out of bounds, break
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)  # Combine rook and bishop moves for queen

    def get_king_moves(self, r, c, moves):
        king_moves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        ally_color = 'w' if self.white_to_move else 'b'  # Determine the ally color
        for move in king_moves:
            end_row = r + move[0]  # Calculate the new row position
            end_col = c + move[1]  # Calculate the new column position
            if 0 <= end_row < len(self.board) and 0 <= end_col < len(self.board[end_row]):  # Check if the position is within the board
                end_piece = self.board[end_row][end_col]  # Get the piece at the new position
                if end_piece == '--' or end_piece[0] != ally_color:  # Empty square or enemy piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))
            

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
        print(self.move_id)  # Print the move ID for debugging purposes

    """
    The __eq__ method is used to compare two Move objects.
    It checks if the move_id of both objects is the same i.e. the move made with the mouse and move we have generated.
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


        

    