import time
import copy
import numpy as np
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CELL_SIZE = WIDTH // 8
KING_RED = (200, 0, 0)
KING_BLUE = (0, 0, 200)
AI_DEPTH = 4

class Checkers:
    def __init__(self):
        self.board = self.create_board()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.selected_piece = None
        self.current_player = 'R'
        self.draw_board()

    def create_board(self):
        board = np.full((8, 8), '-', dtype=object)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'B'
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'R'
        return board

    def draw_board(self):
        self.window.fill(WHITE)
        for row in range(8):
            for col in range(8):
                color = BLACK if (row + col) % 2 == 0 else WHITE
                pygame.draw.rect(self.window, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                piece = self.board[row][col]
                if piece in ['R', 'B']:
                    pygame.draw.circle(self.window, RED if piece == 'R' else BLUE,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 5)
                elif piece in ['RK', 'BK']:
                    pygame.draw.circle(self.window, KING_RED if piece == 'RK' else KING_BLUE,
                                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 5)
        pygame.display.update()

    def valid_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        is_king = 'K' in piece
        directions = [(-1, -1), (-1, 1)] if piece.startswith('R') else [(1, -1), (1, 1)]
        if is_king:
            directions += [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        jump_moves = []

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == '-':
                    moves.append(((row, col), (new_row, new_col)))
                elif self.board[new_row][new_col][0] != piece[0] and self.board[new_row][new_col] != '-':
                    jump_row, jump_col = new_row + drow, new_col + dcol
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board[jump_row][jump_col] == '-':
                        jump_moves.append(((row, col), (jump_row, jump_col)))

        return jump_moves if jump_moves else moves

    def move_piece(self, move):
        (old_row, old_col), (new_row, new_col) = move
        self.board[new_row][new_col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = '-'

        if abs(new_row - old_row) == 2:
            mid_row, mid_col = (new_row + old_row) // 2, (new_col + old_col) // 2
            self.board[mid_row][mid_col] = '-'

        if new_row == 0 and self.board[new_row][new_col] == 'R':
            self.board[new_row][new_col] = 'RK'
        elif new_row == 7 and self.board[new_row][new_col] == 'B':
            self.board[new_row][new_col] = 'BK'

        self.current_player = 'B' if self.current_player == 'R' else 'R'

    def get_all_moves(self, player):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col].startswith(player):
                    moves.extend(self.valid_moves(row, col))
        return moves

    def minimax(self, depth, maximizing, alpha, beta):
        if depth == 0 or not self.get_all_moves('B' if maximizing else 'R'):
            return self.evaluate_board()

        if maximizing:
            max_eval = float('-inf')
            for move in self.get_all_moves('B'):
                board_copy = copy.deepcopy(self.board)
                self.move_piece(move)
                eval = self.minimax(depth - 1, False, alpha, beta)
                self.board = board_copy
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_all_moves('R'):
                board_copy = copy.deepcopy(self.board)
                self.move_piece(move)
                eval = self.minimax(depth - 1, True, alpha, beta)
                self.board = board_copy
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self):
        return (
                np.count_nonzero(self.board == 'B') - np.count_nonzero(self.board == 'R') +
                3 * (np.count_nonzero(self.board == 'BK') - np.count_nonzero(self.board == 'RK'))
        )

    def make_ai_move(self):
        time.sleep(0.5)  # AI moves naturally
        moves = self.get_all_moves('B')
        if not moves:
            return
        best_move = max(moves, key=lambda move: self.minimax(AI_DEPTH, False, float('-inf'), float('inf')))
        self.move_piece(best_move)
        self.draw_board()


if __name__ == "__main__":
    game = Checkers()
    running = True
    while running:
        if game.current_player == 'B':
            game.make_ai_move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                moves = game.get_all_moves('R')
                for move in moves:
                    if move[0] == (row, col):
                        game.move_piece(move)
                        break
                game.draw_board()
    pygame.quit()
