#Its the class which is responsible for storing all the information for the current state of the chess game 
#Also responsible for determining the legality of moves and updating the game state accordingly. 
#It will also keep a move history of the game. - for undo and redo functionality.

class GameState():
    def __init__(self):
        self.board = [
            list("bRbNbBbQbKbBbNbR"),
            list("bP" * 8),
            ["--"] * 8,
            ["--"] * 8,
            ["--"] * 8,
            ["--"] * 8,
            list("wP" * 8),
            list("wRwNwBwQwKwBwNwR")
        ]
# The GameState class initializes the chessboard with the starting positions of all pieces.
# The board is represented as a list of lists, where each inner list represents a row on the chessboard.
        self.white_to_move = True  # True if it's white's turn, False
        self.move_log = []  # List to keep track of moves made in the game