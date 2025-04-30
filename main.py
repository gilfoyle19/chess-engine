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
Main function to run the chess game. Initializes the game, sets up the graphics, and handles user input. Call all the helper functions into the main function.
The main loop handles events, updates the game state, and draws the game on the screen.
"""
def main():
    p.init()    # Initialize the pygame library
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Create a window with the specified width and height
    clock = p.time.Clock()  #to control the frame rate
    screen.fill(p.Color("white")) 
    state = engine.GameState()  # Create a new GameState object to manage the game state
    LoadImages() # Load the images of the chess pieces
    running = True  # Flag to control the main loop
    #Intialize the variables to keep track of the last click of the player and the coordinates of the player's clicks - outside of the while loop as we can reuse them.
    square_selected = ()  # Tuple to keep track of the last click of the player (row,column)
    player_clicks = []  # List to store the coordinates of the player's clicks [(row1, column1), (row2, column2)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Check if the user has closed the window
                running = False
                print("Game Over")
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x,y coordinates of the mouse click
                col = location[0] // SQUARE_SIZE  # Calculate the column based on the mouse click position [0] is the x coordinate
                row = location[1] // SQUARE_SIZE  # Calculate the row based on the mouse click position [1] is the y coordinate
                if square_selected == (row, col): # If the user clicks on the same square again, deselect it
                    square_selected = ()
                    player_clicks = []  # Reset the player clicks   
                else:
                    square_selected = (row, col)  # Update the square selected by the player
                    player_clicks.append(square_selected)  # Add the selected square to the player clicks
                if len(player_clicks) == 2:  # If the player has made two clicks
                    move = engine.Move(player_clicks[0], player_clicks[1], state.board)  # Create a Move object with the selected squares and the current board state
                    print(move.get_chess_notation())  # Print the move in chess notation - for debugging
                    state.make_move(move)  # Update the game state with the new move
                    square_selected = ()  # Reset the square selected
                    player_clicks = []  # Reset the player clicks   
                    print(state.move_log)  # Print the move log - for debugging
                    print(state.board)  # Print the current board state - for debugging
       
       
        DrawGame(screen, state) # call the DrawGame function to draw the current game state on the screen
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
    colors = [p.Color("white"), p.Color("gray")] #list for colors on the checkerboard 
    #Creating a nested for loop visualizing the board:start with a white square 
    for r in range(DIMENSION): 
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)] # Calculate the color of the square based on its position
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # Draw the square on the screen




# Draw the chessboard on the screen. The board is drawn in a checkerboard pattern with alternating colors.
def DrawPieces(screen, board):
    for r in range(DIMENSION):  # Loop through each row of the board
        for c in range(DIMENSION): # Loop through each column of the board
            piece = board[r][c] # Get the piece at the current position (row, column)
            #if the piece is not empty (not "--"), draw the piece on the screen
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) # Draw the piece on the same square

if __name__ == "__main__":
    main()  # Run the main function to start the game