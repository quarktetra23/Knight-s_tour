import pygame
import sys

# Set the dimensions of the board
BOARD_SIZE = 8
CELL_SIZE = 50
WIDTH = BOARD_SIZE * CELL_SIZE
HEIGHT = BOARD_SIZE * CELL_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Knight moves
MOVES = [
    (2, 1),
    (1, 2),
    (-1, 2),
    (-2, 1),
    (-2, -1),
    (-1, -2),
    (1, -2),
    (2, -1)
]


def is_valid_move(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == -1


def warnsdorff_order(x, y, board):
    # Return moves ordered by the number of accessible neighbors
    move_scores = [(move, count_accessible_neighbors(x + move[0], y + move[1], board)) for move in MOVES]
    sorted_moves = sorted(move_scores, key=lambda x: x[1])
    return [move[0] for move in sorted_moves]


def count_accessible_neighbors(x, y, board):
    return sum(1 for move in MOVES if is_valid_move(x + move[0], y + move[1], board))


def draw_board(screen, board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            color = WHITE if (i + j) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[i][j] != -1:
                font = pygame.font.Font(None, 36)
                text = font.render(str(board[i][j]), True, RED)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)


def outline_boxes(screen, start_x, start_y, end_x, end_y):
    # Outline the first position with a green rectangle
    pygame.draw.rect(screen, GREEN, (start_y * CELL_SIZE, start_x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    # Outline the last position with a red rectangle
    pygame.draw.rect(screen, RED, (end_y * CELL_SIZE, end_x * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    pygame.display.flip()


def get_user_input():
    while True:
        try:
            start_x = int(input("Enter the starting row (0 to 7): "))
            start_y = int(input("Enter the starting column (0 to 7): "))
            if 0 <= start_x < BOARD_SIZE and 0 <= start_y < BOARD_SIZE:
                return start_x, start_y
            else:
                print("Invalid input. Row and column must be between 0 and 7.")
        except ValueError:
            print("Invalid input. Please enter valid integers.")


def solve_knights_tour(screen, board, x, y, move_number, start_x, start_y):
    if move_number == BOARD_SIZE ** 2 + 1:
        return True

    for move in warnsdorff_order(x, y, board):
        next_x = x + move[0]
        next_y = y + move[1]

        if is_valid_move(next_x, next_y, board):
            board[next_x][next_y] = move_number
            draw_board(screen, board)
            outline_boxes(screen, start_x, start_y, next_x, next_y)
            pygame.display.flip()
            pygame.time.wait(100)  # Adjust the delay here

            if solve_knights_tour(screen, board, next_x, next_y, move_number + 1, start_x, start_y):
                return True

            # Backtrack
            board[next_x][next_y] = -1
            draw_board(screen, board)
            pygame.display.flip()
            pygame.time.wait(100)  # Adjust the delay here

    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour")

    # Initialize the chessboard with -1
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Get user input for the starting position
    start_x, start_y = get_user_input()
    board[start_x][start_y] = 1

    draw_board(screen, board)
    outline_boxes(screen, start_x, start_y, start_x, start_y)
    pygame.display.flip()

    solve_knights_tour(screen, board, start_x, start_y, 2, start_x, start_y)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
