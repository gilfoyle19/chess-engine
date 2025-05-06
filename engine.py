#Its the class which is responsible for storing all the information for the current state of the chess game 
#Also responsible for determining the legality of moves and updating the game state accordingly. 
#It will also keep a move history of the game. - for undo and redo functionality.

class GameState():
    """
    A class representing the current state of a chess game.
    
    This class is responsible for:
    - Storing the current board configuration
    - Tracking game state (whose turn, castling rights, etc.)
    - Validating and making moves
    - Maintaining move history
    - Checking for game end conditions (checkmate, stalemate)
    
    Attributes:
        board (list): 8x8 2D list representing the chess board
        white_to_move (bool): True if it's white's turn, False if black's
        move_log (list): History of moves made in the game
        white_king_location (tuple): Current position of white king (row, col)
        black_king_location (tuple): Current position of black king (row, col)
        check_mate (bool): True if game is in checkmate
        stale_mate (bool): True if game is in stalemate
        en_passant_possible (tuple): Square where en passant capture is possible
        pawn_promotion (bool): True if a pawn can be promoted
        promotion_choice (str): The piece type chosen for pawn promotion
    """
    def __init__(self):
        """
        Initialize a new chess game with the standard starting position.
        Sets up the board and initializes all game state variables.
        """
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
        self.white_king_location = (7, 4)  # Initial position of the white king
        self.black_king_location = (0, 4)  # Initial position of the black king
        self.check_mate = False  # Flag to indicate if the game is in checkmate
        self.stale_mate = False  # Flag to indicate if the game is in stalemate
        # Castling rights
        self.white_king_moved = False
        self.white_queen_rook_moved = False
        self.white_king_rook_moved = False
        self.black_king_moved = False
        self.black_queen_rook_moved = False
        self.black_king_rook_moved = False
        # En passant
        self.en_passant_possible = ()  # Coordinates for the square where en passant capture is possible
        self.en_passant_log = [self.en_passant_possible]  # Log of en passant possibilities
        # Pawn promotion
        self.pawn_promotion = False
        self.promotion_choice = 'Q'  # Default promotion to queen
    # The make_move method updates the board with the new move. - not works for casting, pawn promotion and en passant yet.
    def make_move(self, move):
        """
        Execute a move on the board and update the game state.
        
        Handles special moves including:
        - Castling (both kingside and queenside)
        - En passant captures
        - Pawn promotion
        
        Args:
            move (Move): The move to execute
            
        Side effects:
            - Updates the board configuration
            - Updates game state (turn, castling rights, etc.)
            - Adds move to move history
        """
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        
        # Update king's location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
            self.white_king_moved = True
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
            self.black_king_moved = True
        
        # Update rook moved status for castling
        if move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # Queen's rook
                    self.white_queen_rook_moved = True
                elif move.start_col == 7:  # King's rook
                    self.white_king_rook_moved = True
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # Queen's rook
                    self.black_queen_rook_moved = True
                elif move.start_col == 7:  # King's rook
                    self.black_king_rook_moved = True

        # Pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + self.promotion_choice

        # En passant
        if move.is_en_passant_move:
            self.board[move.start_row][move.end_col] = '--'  # Capture the pawn

        # Update en passant possibility
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:  # Only on 2 square pawn advance
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()
        self.en_passant_log.append(self.en_passant_possible)

        # Castling
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # King side castle
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = '--'
            else:  # Queen side castle
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = '--'

        print(f"Board after move: {self.board}")  # Debugging
    
    def undo_move(self):
        """
        Revert the last move made and restore the previous game state.
        
        Handles undoing special moves including:
        - Castling
        - En passant captures
        - Pawn promotion
        
        Side effects:
            - Restores previous board configuration
            - Restores previous game state
            - Removes last move from move history
        """
        if len(self.move_log) != 0: # to prevent index error when there are no moves made yet
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved #reverse the move by putting the piece back to its original position
            self.board[move.end_row][move.end_col] = move.piece_captured #reverse the piece captured by putting the piece back to its original position
            self.white_to_move = not self.white_to_move  # Switch turns back to the previous player
            
            # Update king's location
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

            # Undo en passant
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured

            # Undo castling
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # King side castle
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else:  # Queen side castle
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'

            # Restore en passant possibility
            self.en_passant_log.pop()
            self.en_passant_possible = self.en_passant_log[-1]
    
    """
    Moves considering king is in check
    """
    def get_valid_moves(self):
        """
        Get all legal moves for the current player.
        
        A move is legal if:
        1. It is a possible move for the piece
        2. It doesn't leave the player's king in check
        
        Returns:
            list: List of legal Move objects
            
        Side effects:
            May update checkmate/stalemate status
        """
        """Get all valid moves for the current player considering checks"""
        moves = []
        self.get_all_possible_moves(moves)
        
        # For each move, make it and see if it puts/leaves our king in check
        for i in range(len(moves)-1, -1, -1):  # Go backwards to safely remove items
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move  # Switch back to our turn
            if self.in_check():  # If we're in check, the move is not valid
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move  # Switch turns back
            self.undo_move()
        
        if len(moves) == 0:  # Either checkmate or stalemate
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        
        return moves

    """
    Determine if the current player's king is in check.
    """
    def in_check(self):
        """
        Determine if the current player is in check.
        
        A player is in check if their king is under attack by any enemy piece.
        
        Returns:
            bool: True if current player is in check, False otherwise
        """
        """Determine if the current player is in check"""
        if self.white_to_move:
            return self.square_under_attack_simple(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack_simple(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack_simple(self, r, c):
        """
        Determine if a square is under attack by any enemy piece.
        
        Checks for attacks from:
        - Pawns
        - Knights
        - Bishops/Queens (diagonal)
        - Rooks/Queens (horizontal/vertical)
        - Kings
        
        Args:
            r (int): Row of square to check
            c (int): Column of square to check
            
        Returns:
            bool: True if square is under attack, False otherwise
        """
        """Determine if a square is under attack by any enemy piece using a simpler approach"""
        opponent_color = 'b' if self.white_to_move else 'w'
        
        # Check for pawn attacks
        if self.white_to_move:
            if r > 0:
                if c > 0 and self.board[r-1][c-1][0] == opponent_color and self.board[r-1][c-1][1] == 'p':
                    return True
                if c < 7 and self.board[r-1][c+1][0] == opponent_color and self.board[r-1][c+1][1] == 'p':
                    return True
        else:
            if r < 7:
                if c > 0 and self.board[r+1][c-1][0] == opponent_color and self.board[r+1][c-1][1] == 'p':
                    return True
                if c < 7 and self.board[r+1][c+1][0] == opponent_color and self.board[r+1][c+1][1] == 'p':
                    return True
        
        # Check for knight attacks
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in knight_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                piece = self.board[end_row][end_col]
                if piece[0] == opponent_color and piece[1] == 'N':
                    return True
        
        # Check for rook/queen attacks (horizontal and vertical)
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    piece = self.board[end_row][end_col]
                    if piece[0] == opponent_color and (piece[1] == 'R' or piece[1] == 'Q'):
                        return True
                    elif piece != '--':
                        break
                else:
                    break
        
        # Check for bishop/queen attacks (diagonals)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    piece = self.board[end_row][end_col]
                    if piece[0] == opponent_color and (piece[1] == 'B' or piece[1] == 'Q'):
                        return True
                    elif piece != '--':
                        break
                else:
                    break
        
        # Check for king attacks
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for move in king_moves:
            end_row = r + move[0]
            end_col = c + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                piece = self.board[end_row][end_col]
                if piece[0] == opponent_color and piece[1] == 'K':
                    return True
        
        return False

    """
    Moves without considering king is in check
    """
    def get_all_possible_moves(self, moves=None):
        """
        Get all possible moves for the current player without considering check.
        
        For each piece of the current player's color:
        1. Identifies the piece type
        2. Calls the appropriate move generation function
        
        Args:
            moves (list, optional): List to store moves in. Creates new list if None.
            
        Returns:
            list: List of all possible Move objects
        """
        if moves is None:
            moves = []
        
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)  # Calls the appropriate move function
        
        return moves

    """ 
    Below methods are used to get the possible moves for each piece.
    The methods will check if the move is valid and if the move does not put the king in check.
    """
    def get_pawn_moves(self, r, c, moves):
        """
        Get all possible moves for a pawn at the given position.
        
        Handles:
        - Single square advances
        - Initial two square advances
        - Diagonal captures
        - En passant captures
        - (Promotion is handled in make_move)
        
        Args:
            r (int): Current row of pawn
            c (int): Current column of pawn
            moves (list): List to add valid moves to
        """
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
                if r == 6 and self.board[r-2][c] == '--':  # Move two squares forward
                    moves.append(Move((r, c), (r-2, c), self.board))
            # Diagonal captures
            if c-1 >= 0:  # Capture left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, is_en_passant_move=True))
            if c+1 < len(self.board[r]):  # Capture right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, is_en_passant_move=True))
        else:  # Black pawns move down
            if self.board[r+1][c] == '--':  # Move one square forward
                moves.append(Move((r, c), (r+1, c), self.board))
            if r == 1 and self.board[r+2][c] == '--' and self.board[r+1][c] == '--':  # Move two squares forward
                moves.append(Move((r, c), (r+2, c), self.board))
            # Diagonal captures
            if c-1 >= 0:  # Capture left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, is_en_passant_move=True))
            if c+1 < len(self.board[r]):  # Capture right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, is_en_passant_move=True))

    
    def get_rook_moves(self, r, c, moves):
        """
        Get all possible moves for a rook at the given position.
        
        Generates moves in four directions:
        - Up (-1, 0)
        - Down (1, 0)
        - Left (0, -1)
        - Right (0, 1)
        
        Args:
            r (int): Current row of rook
            c (int): Current column of rook
            moves (list): List to add valid moves to
        """
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
        """
        Get all possible moves for a knight at the given position.
        
        Generates all eight possible L-shaped moves:
        - 2 squares in one direction and 1 square perpendicular
        
        Args:
            r (int): Current row of knight
            c (int): Current column of knight
            moves (list): List to add valid moves to
        """
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
        """
        Get all possible moves for a bishop at the given position.
        
        Generates moves in four diagonal directions:
        - Up-Left (-1, -1)
        - Up-Right (-1, 1)
        - Down-Left (1, -1)
        - Down-Right (1, 1)
        
        Args:
            r (int): Current row of bishop
            c (int): Current column of bishop
            moves (list): List to add valid moves to
        """
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
        """
        Get all possible moves for a queen at the given position.
        
        Combines rook and bishop moves:
        - All horizontal/vertical moves (rook-like)
        - All diagonal moves (bishop-like)
        
        Args:
            r (int): Current row of queen
            c (int): Current column of queen
            moves (list): List to add valid moves to
        """
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)  # Combine rook and bishop moves for queen

    def get_king_moves(self, r, c, moves):
        """
        Get all possible moves for a king at the given position.
        
        Handles:
        - Regular king moves (one square in any direction)
        - Castling (both kingside and queenside)
        
        Ensures:
        - King doesn't move into check
        - Castling requirements are met (no pieces between, rights available)
        
        Args:
            r (int): Current row of king
            c (int): Current column of king
            moves (list): List to add valid moves to
        """
        """Get all valid moves for a king at the given position"""
        # Define all possible king moves (8 directions)
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        ally_color = 'w' if self.white_to_move else 'b'
        
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Not an ally piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))
        
        # Castling
        if not self.in_check():
            # Kingside castling
            if (self.white_to_move and not self.white_king_moved and not self.white_king_rook_moved) or \
               (not self.white_to_move and not self.black_king_moved and not self.black_king_rook_moved):
                if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                    if not self.square_under_attack_simple(r, c+1) and not self.square_under_attack_simple(r, c+2):
                        moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))
            
            # Queenside castling
            if (self.white_to_move and not self.white_king_moved and not self.white_queen_rook_moved) or \
               (not self.white_to_move and not self.black_king_moved and not self.black_queen_rook_moved):
                if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
                    if not self.square_under_attack_simple(r, c-1) and not self.square_under_attack_simple(r, c-2):
                        moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))

class Move(): # This class is responsible for storing the information of a move made in the game.
    """
    A class representing a chess move.
    
    Stores all information about a move including:
    - Start and end positions
    - Piece moved and captured
    - Special move flags (promotion, en passant, castle)
    - Unique move ID for comparison
    
    Also provides methods for:
    - Move comparison
    - Converting to chess notation
    
    Attributes:
        start_row (int): Starting row of the move
        start_col (int): Starting column of the move
        end_row (int): Ending row of the move
        end_col (int): Ending column of the move
        piece_moved (str): The piece that was moved
        piece_captured (str): The piece that was captured (if any)
        is_pawn_promotion (bool): True if move results in pawn promotion
        is_en_passant_move (bool): True if move is an en passant capture
        is_castle_move (bool): True if move is a castling move
        move_id (int): Unique identifier for the move
    """
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0} # Dictionary to convert ranks to rows
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # Reverse the dictionary to convert rows to ranks
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7} # Dictionary to convert files to columns
    cols_to_files = {v: k for k, v in files_to_cols.items()}  # Reverse the dictionary to convert columns to files
    def __init__(self, start_square, end_square, board, is_en_passant_move=False, is_castle_move=False):
        """
        Initialize a new Move object.
        
        Args:
            start_square (tuple): Starting position (row, col)
            end_square (tuple): Ending position (row, col)
            board (list): Current board configuration
            is_en_passant_move (bool): True if move is en passant
            is_castle_move (bool): True if move is castling
        """
        self.start_row = start_square[0]  # Row of the starting square - tuple
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7)
        self.is_en_passant_move = is_en_passant_move
        if self.is_en_passant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'
        self.is_castle_move = is_castle_move
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col ## Unique ID for the move

    """
    The __eq__ method is used to compare two Move objects.
    It checks if the move_id of both objects is the same i.e. the move made with the mouse and move we have generated.
    """
    def __eq__(self, other):
        """
        Compare this move with another move.
        
        Args:
            other (Move): Another move to compare with
            
        Returns:
            bool: True if moves are the same, False otherwise
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    
    def get_chess_notation(self):
        """
        Convert the move to standard chess notation.
        
        Returns:
            str: Move in chess notation (e.g., 'e2e4')
        """
        # Convert the move to chess notation (e.g., 'e2e4')
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  # Convert the move to chess notation (e.g., 'e2e4') 

    def get_rank_file(self, r, c):
        """
        Convert board coordinates to chess notation coordinates.
        
        Args:
            r (int): Row number (0-7)
            c (int): Column number (0-7)
            
        Returns:
            str: Position in chess notation (e.g., 'e2')
        """
        return self.cols_to_files[c] + self.rows_to_ranks[r]  # Convert the row and column to chess notation (e.g., 'e2' or 'h8')


        

    