# pygame-sudoku

A graphical Sudoku game built with Pygame, featuring multiple difficulty levels and an inference engine solver.

## Features
- Play Sudoku with a clean GUI
- Multiple difficulty levels
- Solve the board automatically (with two solver options)
- Get hints

## Requirements
- Python 3.7+
- [Pygame](https://www.pygame.org/)

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/pygame-sudoku.git
   cd pygame-sudoku
   ```
2. **Install dependencies:**
   ```bash
   python3 -m pip install --break-system-packages pygame
   ```
   Or, if you use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pygame
   ```

## Running the Game
```bash
python3 sudoku.py
```

## Controls
- **Mouse:** Select cells and use buttons (Solve, Hint, Reset)
- **Keyboard:**
  - 1-9: Enter numbers
  - Delete/Backspace: Clear cell
  - Enter: Confirm entry

## Files
- `sudoku.py`: Main game file
- `sudoku_solver_IE.py`: Inference engine solver module
- `sudoku_solver.py`: (Optional) Additional solver module

## License
MIT 