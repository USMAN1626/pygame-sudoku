# pygame-sudoku

#Output<img width="535" height="6<img width="538" height="639" alt="Screenshot 2025-07-18 at 11 37 38 PM" src="https://github.com/user-attachments/assets/852b421c-9532-4946-b313-1333ba438666" />
38" alt="Screenshot 2025-07-18<img width="539" height="640" alt="Screenshot 2025-07-18 at 11 37 49 PM" src="https://github.com/user-attachments/assets/42378672-82c5-4a00-b339-fed13fd2605a" />
 at 11 37 12 PM" src="https://github.com/user-attachments/assets/7be99c2d-7989-4186-8e13-be6d2f16c8a7" />
 


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
