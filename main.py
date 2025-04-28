#Responsible for the user input and gamestate object information 

"""
Todo: 
1. Add a functionality in the LoadImages function to change the themes. 
2. Add in piece highlighting functionality in DrawGame function.
3. Move suggestions in the DrawGame function.

"""

import pygame as p
import engine


p.init()  # Initialize the pygame library
WIDTH = HEIGHT = 512  # Set the width and height of the window
DIMENSION = 8 # Set the number of rows and columns on the chessboard
SQUARE_SIZE = HEIGHT // DIMENSION  # Set the size of each square on the chessboard
MAX_FPS = 15
IMAGES = {}  # Dictionary to hold the images of the chess pieces

'''
Load images of chess pieces into the IMAGES dictionary. This function is called once at the start of the program.
'''
def LoadImages():
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("C:/Users/Chivukula/100daysofcode/Chess/chess_engine/images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))  # Load and scale the image to fit the square size
    # Load the images for the chess pieces and store them in the IMAGES dictionary.


"""
Main function to run the chess game. Initializes the game, sets up the graphics, and handles user input.
"""
def main():
    p.init()    # Initialize the pygame library
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Create a window with the specified width and height
    clock = p.time.Clock()  #to control the frame rate
    screen.fill(p.Color("white")) 
    state = engine.GameState()  # Create a new GameState object to manage the game state
    LoadImages() # Load the images of the chess pieces
    running = True  # Flag to control the main loop
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Check if the user has closed the window
                running = False
                print("Game Over")
        
        clock.tick(MAX_FPS)  # Control the frame rate of the game
        p.display.flip() # Update the display

"""
Responsible for all the graphics within the current game state 
"""

def DrawGame(screen, state):
    DrawBoard(screen)  # Draw the chessboard
    DrawPieces(screen, state.board)  # Draw the pieces on the board

"""
Draw the chessboard on the screen. The board is drawn in a checkerboard pattern with alternating colors."""
def DrawBoard(screen):
    pass

# Draw the chessboard on the screen. The board is drawn in a checkerboard pattern with alternating colors.
def DrawPieces(screen, board):
    pass 

if __name__ == "__main__":
    main()  # Run the main function to start the game