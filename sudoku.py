import pygame
import random
import time
pygame.font.init()
from sudoku_solver_IE import get_solved_board

WIDTH, HEIGHT=540,610
BUTTON_HEIGHT=45
BUTTON_MARGIN=30
BACKGROUND_COLOR = (240, 248, 255)
GRID_COLOR = (70, 130, 180)
BUTTON_COLOR = (100, 149, 237)
SELECTED_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (220, 220, 220)
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("sans-serif",25)
    def draw(self, win):
        pygame.draw.rect(win, BUTTON_COLOR, self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 3)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                             self.rect.y + (self.rect.height - text_surf.get_height()) // 2))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    def update_hover(self, pos):
        pass
class Cube:
    rows = 9
    cols = 9
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.is_initial = value != 0
    def draw(self, win, selected_cell):
        fnt = pygame.font.SysFont("sans-serif", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        if selected_cell:
            sel_row, sel_col = selected_cell
            if self.row == sel_row or self.col == sel_col or (self.row//3 == sel_row//3 and self.col//3 == sel_col//3):
                pygame.draw.rect(win, HIGHLIGHT_COLOR, (x, y, gap, gap))
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, SELECTED_COLOR, (x, y, gap, gap), 3)
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("sans-serif", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, BACKGROUND_COLOR, (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        color = (0, 255, 0) if g else (255, 0, 0)
        pygame.draw.rect(win, color, (x, y, gap, gap), 3)
    def set(self, val):
        self.value = val
    def set_temp(self, val):
        self.temp = val
class Grid:
    initial_board1 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    initial_board2 = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    initial_board3 = [
        [0, 0, 0, 0, 0, 0, 6, 8, 0],
        [0, 0, 0, 0, 4, 6, 0, 0, 0],
        [7, 0, 0, 0, 0, 3, 0, 0, 9],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0],
        [1, 0, 0, 5, 0, 0, 0, 0, 3],
        [0, 0, 0, 2, 6, 0, 0, 0, 0],
        [0, 4, 2, 0, 0, 0, 0, 0, 0]
    ]
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.initial_board = random.choice([self.initial_board1, self.initial_board2, self.initial_board3])
        self.reset()
        self.selected = None
    def reset(self):
        self.cubes = [[Cube(self.initial_board[i][j], i, j, self.width, self.height) 
                      for j in range(self.cols)] for i in range(self.rows)]
        self.update_model()
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    def draw(self):
        gap = self.width / 9
        for i in range(self.rows+1):
            thick = 5 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(self.win, GRID_COLOR, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, GRID_COLOR, (i * gap, 0), (i * gap, self.height), thick)
        for row in self.cubes:
            for cube in row:
                cube.draw(self.win, self.selected)
    def select(self, row, col):
        for r in self.cubes:
            for c in r:
                c.selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = int(pos[0] // gap)
            y = int(pos[1] // gap)
            return (y, x)
        return None
    def is_finished(self):
        for r in self.cubes:
            for c in r:
                if c.value == 0:
                    return False
        return True
    def place(self, val):
        if not self.selected:
            return False
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    def sketch(self, val):
        if not self.selected:
            return
        row, col = self.selected
        self.cubes[row][col].set_temp(val)
    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.initial_board[row][col] == 0:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
    def find_empty_cell(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.model[i][j] == 0:
                    possible = []
                    for num in range(1, 10):
                        if valid(self.model, num, (i, j)):
                            possible.append(num)
                    empty_cells.append((len(possible), (i, j), possible))
        if not empty_cells:
            return None, None, None
        empty_cells.sort()
        return empty_cells[0][1], empty_cells[0][2], len(empty_cells)
    def solve(self):
        pos, possible, _ = self.find_empty_cell()
        if not pos:
            return True
        row, col = pos
        for num in possible:
            if valid(self.model, num, (row, col)):
                self.model[row][col] = num
                if self.solve():
                    return True
                self.model[row][col] = 0
        return False
    def solve_gui(self):
        pos, possible, remaining = self.find_empty_cell()
        if not pos:
            return True
        row, col = pos
        for num in possible:
            if valid(self.model, num, (row, col)):
                self.model[row][col] = num
                self.cubes[row][col].set(num)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                if self.solve_gui():
                    return True
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
        return False
def valid(board, num, pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True
def redraw_window(win, board, strikes, lives, buttons, game_over=False, game_won=False):
    win.fill(BACKGROUND_COLOR)
    lives_font = pygame.font.SysFont("comicsans", 30)
    lives_text = lives_font.render(f"Lives: {lives}", True, (0, 0, 255))
    win.blit(lives_text, (WIDTH - 130, 550))
    board.draw()
    for button in buttons:
        button.draw(win)
    if game_won:
        font = pygame.font.SysFont("sans-serif", 70)
        text = font.render("YOU WIN!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH//2, WIDTH//2))
        win.blit(text, text_rect)
    elif game_over:
        font = pygame.font.SysFont("sans-serif", 70)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, WIDTH//2))
        win.blit(text, text_rect)
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Game")
    board = Grid(9, 9, WIDTH, WIDTH, win)
    key = None
    run = True
    strikes = 0
    lives = 5
    game_over = False
    game_won = False
    solve_btn = Button(20, 550, 80, BUTTON_HEIGHT, "Solve", "solve")
    ie_solve_btn = Button(105, 550, 110, BUTTON_HEIGHT, "Solve (IE)", "ie_solve")
    hint_btn = Button(220, 550, 80, BUTTON_HEIGHT, "Hint", "hint")
    reset_btn = Button(305, 550, 80, BUTTON_HEIGHT, "Reset", "reset")
    buttons = [solve_btn, ie_solve_btn, hint_btn, reset_btn]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and not game_over and not game_won:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                if event.key == pygame.K_RETURN:
                    if board.selected and board.cubes[board.selected[0]][board.selected[1]].temp != 0:
                        row, col = board.selected
                        val = board.cubes[row][col].temp
                        if board.place(val):
                            print("Success")
                            if board.is_finished():
                                print("Game won!")
                                game_won = True
                        else:
                            print("Wrong")
                            strikes += 1
                            lives -= 1
                            if lives <= 0:
                                print("Game over - out of lives!")
                                game_over = True
                        key = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.action == "solve":
                            start_time = time.time()
                            board.solve_gui()
                            end_time = time.time()
                            print(f"Solved in {end_time - start_time:.2f} seconds")
                            if board.is_finished():
                                game_won = True
                        elif button.action == "ie_solve":
                            start_time = time.time()
                            current_board = [[cube.value for cube in row] for row in board.cubes]
                            solved_board = get_solved_board(current_board)
                            if solved_board:
                                for i in range(9):
                                    for j in range(9):
                                        board.cubes[i][j].set(solved_board[i][j])
                                board.update_model()
                                end_time = time.time()
                                print(f"Solved in {end_time - start_time:.2f} seconds")
                                if board.is_finished():
                                    game_won = True
                                print("Solved with inference engine!")
                            else:
                                print("No solution found by inference engine.")
                        elif button.action == "hint":
                            if board.selected:
                                row, col = board.selected
                                if board.cubes[row][col].value == 0:
                                    temp_model = [row[:] for row in board.model]
                                    def solve_temp(board_temp):
                                        pos, possible, _ = find_empty_cell_mrv(board_temp)
                                        if not pos:
                                            return True
                                        row, col = pos
                                        for num in possible:
                                            if valid(board_temp, num, (row, col)):
                                                board_temp[row][col] = num
                                                if solve_temp(board_temp):
                                                    return True
                                                board_temp[row][col] = 0
                                        return False
                                    solve_temp(temp_model)
                                    correct_val = temp_model[row][col]
                                    if correct_val != 0:
                                        board.cubes[row][col].set(correct_val)
                                        board.update_model()
                                        if board.is_finished():
                                            game_won = True
                        elif button.action == "reset":
                            board.reset()
                            strikes = 0
                            lives = 5
                            game_over = False
                            game_won = False
                        break
                else:
                    if not game_over and not game_won:
                        clicked = board.click(pos)
                        if clicked:
                            board.select(clicked[0], clicked[1])
                            key = None
        if board.selected and key != None and not game_over and not game_won:
            board.sketch(key)
        redraw_window(win, board, strikes, lives, buttons, game_over, game_won)
        pygame.display.update()
    pygame.quit()
def find_empty_cell_mrv(board):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible = []
                for num in range(1, 10):
                    if valid(board, num, (i, j)):
                        possible.append(num)
                empty_cells.append((len(possible), (i, j), possible))
    if not empty_cells:
        return None, None, None
    empty_cells.sort()
    return empty_cells[0][1], empty_cells[0][2], len(empty_cells)
if __name__ == "__main__":
    main()

