import pygame
import sys

# Set the dimensions of the board
BOARD_WIDTH = 24
BOARD_HEIGHT = 8
CELL_SIZE = 30
WIDTH = BOARD_WIDTH * CELL_SIZE
HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Knight moves
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def is_valid_move(x, y, board):
    return 0 <= x < BOARD_HEIGHT and 0 <= y < BOARD_WIDTH and board[x][y] == -1


def warnsdorff_order(x, y, board):
    # Return moves ordered by the number of accessible neighbors
    move_scores = [(move, count_accessible_neighbors(x + move[0], y + move[1], board)) for move in MOVES]
    sorted_moves = sorted(move_scores, key=lambda x: x[1])
    return [move[0] for move in sorted_moves]


def count_accessible_neighbors(x, y, board):
    return sum(1 for move in MOVES if is_valid_move(x + move[0], y + move[1], board))


def draw_board(screen, board, knight_positions):
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            color = WHITE if (i + j) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw lines for the knight's tour
    for i in range(len(knight_positions) - 1):
        pygame.draw.line(screen, RED,
                         (knight_positions[i][1] * CELL_SIZE + CELL_SIZE // 2,
                          knight_positions[i][0] * CELL_SIZE + CELL_SIZE // 2),
                         (knight_positions[i + 1][1] * CELL_SIZE + CELL_SIZE // 2,
                          knight_positions[i + 1][0] * CELL_SIZE + CELL_SIZE // 2), 5)

    # Draw circles for knight's positions
    for pos in knight_positions:
        pygame.draw.circle(screen, RED,
                           (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4, 1)

    pygame.display.flip()


def draw_structure(screen, knight_positions):
    # Create a new window to display the structure
    structure_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour Structure")

    # Draw lines for the structure
    for i in range(len(knight_positions) - 1):
        pygame.draw.line(structure_screen, RED,
                         (knight_positions[i][1] * CELL_SIZE + CELL_SIZE // 2,
                          knight_positions[i][0] * CELL_SIZE + CELL_SIZE // 2),
                         (knight_positions[i + 1][1] * CELL_SIZE + CELL_SIZE // 2,
                          knight_positions[i + 1][0] * CELL_SIZE + CELL_SIZE // 2), 5)

    # Draw circles for knight's positions
    for pos in knight_positions:
        pygame.draw.circle(structure_screen, RED,
                           (pos[1] * CELL_SIZE + CELL_SIZE // 2, pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4, 1)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


def solve_knights_tour(screen, board, x, y, move_number, knight_positions):
    if move_number == BOARD_HEIGHT * BOARD_WIDTH + 1:
        draw_structure(screen, knight_positions)
        return True

    for move in warnsdorff_order(x, y, board):
        next_x = x + move[0]
        next_y = y + move[1]

        if is_valid_move(next_x, next_y, board):
            board[next_x][next_y] = move_number
            knight_positions.append((next_x, next_y))
            draw_board(screen, board, knight_positions)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.wait(50)  # Adjust the delay here

            if solve_knights_tour(screen, board, next_x, next_y, move_number + 1, knight_positions):
                return True

            # Backtrack
            board[next_x][next_y] = -1
            knight_positions.pop()
            draw_board(screen, board, knight_positions)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.wait(50)  # Adjust the delay here

    return False


def get_user_input():
    while True:
        try:
            start_x = int(input("Enter the starting row (0 to 7): "))
            start_y = int(input("Enter the starting column (0 to 23): "))
            if 0 <= start_x < BOARD_HEIGHT and 0 <= start_y < BOARD_WIDTH:
                return start_x, start_y
            else:
                print("Invalid input. Row must be between 0 and 7, and column must be between 0 and 23.")
        except ValueError:
            print("Invalid input. Please enter valid integers.")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour")

    # Initialize the chessboard with -1
    board = [[-1 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    # Get user input for the starting position
    start_x, start_y = get_user_input()
    board[start_x][start_y] = 1

    knight_positions = [(start_x, start_y)]

    draw_board(screen, board, knight_positions)
    pygame.display.flip()

    solve_knights_tour(screen, board, start_x, start_y, 2, knight_positions)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
