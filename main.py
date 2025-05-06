#Responsible for the user input and gamestate object information 

"""
Todo: 
1. Add a functionality in the LoadImages function to change the themes. 
2. Add in piece highlighting functionality in DrawGame function - Completed.
3. Move suggestions in the DrawGame function.
4. Make a version without mouse clicks - only keyboard input

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
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))  # Load and scale the image to fit the square size
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
    valid_moves = state.get_valid_moves()  # Get the valid moves for the current game state
    move_made = False  # Flag to check if a move has been made
    game_over = False  # Flag to check if the game is over
    
    LoadImages() # Load the images of the chess pieces
    running = True  # Flag to control the main loop
    #Intialize the variables to keep track of the last click of the player and the coordinates of the player's clicks - outside of the while loop as we can reuse them.
    square_selected = ()  # Tuple to keep track of the lastest click of the player (row,column)
    player_clicks = []  # List to store the coordinates of the player's clicks [(row1, column1), (row2, column2)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                print("Game Over")
            elif e.type == p.MOUSEBUTTONDOWN and not game_over:
                location = p.mouse.get_pos()  # x, y coordinates of the mouse click
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_selected == (row, col):  # Deselect if the same square is clicked
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)  # Append the selected square
                if len(player_clicks) == 2:  # After two clicks, attempt a move
                    move = engine.Move(player_clicks[0], player_clicks[1], state.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:  # Check if the move is valid
                        state.make_move(move)
                        move_made = True
                        square_selected = ()  # Reset selection
                        player_clicks = []
                        # Handle pawn promotion
                        if move.is_pawn_promotion:
                            promotion_piece = handle_pawn_promotion(screen)
                            if promotion_piece:
                                state.promotion_choice = promotion_piece
                                state.board[move.end_row][move.end_col] = move.piece_moved[0] + promotion_piece
                    else:
                        player_clicks = [square_selected]  # Keep the last selected square
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo move
                    state.undo_move()
                    move_made = True
                    game_over = False
                elif e.key == p.K_r:  # Reset the game
                    state = engine.GameState()
                    valid_moves = state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False

        if move_made:
            valid_moves = state.get_valid_moves()  # Recalculate valid moves
            move_made = False
        
        if state.check_mate:
            game_over = True
            if state.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif state.stale_mate:
            game_over = True
            draw_text(screen, "Stalemate")
        
        DrawGame(screen, state) # call the DrawGame function to draw the current game state on the screen
        clock.tick(MAX_FPS)  # Control the frame rate of the game
        p.display.flip() # Update the display

def handle_pawn_promotion(screen):
    # Draw promotion menu
    menu_rect = p.Rect(WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    p.draw.rect(screen, p.Color("white"), menu_rect)
    p.draw.rect(screen, p.Color("black"), menu_rect, 2)
    
    # Draw piece options
    pieces = ['Q', 'R', 'B', 'N']
    piece_size = SQUARE_SIZE
    for i, piece in enumerate(pieces):
        piece_rect = p.Rect(menu_rect.left + (menu_rect.width - piece_size) // 2,
                          menu_rect.top + (menu_rect.height - piece_size) // 2 + i * piece_size,
                          piece_size, piece_size)
        screen.blit(IMAGES['w' + piece], piece_rect)
    
    p.display.flip()
    
    # Wait for user selection
    while True:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                for i, piece in enumerate(pieces):
                    piece_rect = p.Rect(menu_rect.left + (menu_rect.width - piece_size) // 2,
                                      menu_rect.top + (menu_rect.height - piece_size) // 2 + i * piece_size,
                                      piece_size, piece_size)
                    if piece_rect.collidepoint(mouse_pos):
                        return piece
            elif e.type == p.QUIT:
                return None

def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))

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