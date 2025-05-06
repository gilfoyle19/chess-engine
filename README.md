# Chess Game

A Python chess game implementation using Pygame.

## Installation

1. Install the required package:
```bash
pip install pygame
```

## Running the Game

2. Run the game:
```bash
python main.py
```

## How to Play

### Mouse Controls
- **Select a Piece**: Left-click on the piece you want to move
- **Move a Piece**: Left-click on a valid destination square
- **Cancel Selection**: Right-click anywhere on the board
- **Pawn Promotion**: When a pawn reaches the opposite end, click on your desired piece (Queen, Rook, Bishop, or Knight)

### Keyboard Controls
- **Undo Move**: Press 'z' to undo the last move
- **Reset Game**: Press 'r' to reset the game to the starting position
- **Quit Game**: Press 'q' or 'ESC' to exit the game

### Game Rules
- White moves first, followed by Black
- Pieces can only move according to standard chess rules
- The game will automatically detect:
  - Check (when your king is under attack)
  - Checkmate (when no legal moves can prevent check)
  - Stalemate (when no legal moves are available but the king is not in check)
