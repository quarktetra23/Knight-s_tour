import pygame
import sys
import numpy as np

# Set the dimensions of the circular board
BOARD_RADIUS = 8
CELL_SIZE = 45
WIDTH = HEIGHT = 2 * BOARD_RADIUS * CELL_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def is_valid_move(x, y):
    # Check if the move is within the circular board
    return np.sqrt((x - BOARD_RADIUS) ** 2 + (y - BOARD_RADIUS) ** 2) < BOARD_RADIUS

def draw_board(screen, knight_positions):
    screen.fill(WHITE)

    # Draw circular board with chess pattern
    for i in range(BOARD_RADIUS * 2):
        for j in range(BOARD_RADIUS * 2):
            color = WHITE if (i + j) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw yellow outlines for the circular board
    pygame.draw.circle(screen, (255, 255, 0), (BOARD_RADIUS * CELL_SIZE, BOARD_RADIUS * CELL_SIZE), BOARD_RADIUS * CELL_SIZE, 3)

    # Draw lines and hollow points for the knight's tour
    for i in range(len(knight_positions) - 1):
        current_x, current_y = knight_positions[i]
        next_x, next_y = knight_positions[i + 1]

        # Draw line
        pygame.draw.line(screen, RED,
                         (current_y * CELL_SIZE + CELL_SIZE // 2, current_x * CELL_SIZE + CELL_SIZE // 2),
                         (next_y * CELL_SIZE + CELL_SIZE // 2, next_x * CELL_SIZE + CELL_SIZE // 2), 3)

        # Draw hollow point
        pygame.draw.circle(screen, RED, (current_y * CELL_SIZE + CELL_SIZE // 2, current_x * CELL_SIZE + CELL_SIZE // 2), 5, 0)

    # Draw hollow point for the last position
    last_x, last_y = knight_positions[-1]
    pygame.draw.circle(screen, RED, (last_y * CELL_SIZE + CELL_SIZE // 2, last_x * CELL_SIZE + CELL_SIZE // 2), 5, 0)

    pygame.display.flip()

def solve_knights_tour(screen, x, y, move_number, knight_positions):
    if move_number == (2 * BOARD_RADIUS) ** 2 + 1:
        return True

    for move in [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]:
        next_x = x + move[0]
        next_y = y + move[1]

        if is_valid_move(next_x, next_y):
            knight_positions.append((next_x, next_y))
            draw_board(screen, knight_positions)
            pygame.display.flip()
            pygame.time.wait(50)  # Adjust the delay here

            if solve_knights_tour(screen, next_x, next_y, move_number + 1, knight_positions):
                return True

            # Backtrack
            knight_positions.pop()
            draw_board(screen, knight_positions)
            pygame.display.flip()
            pygame.time.wait(50)  # Adjust the delay here

    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight's Tour - Circular Board")

    # Get user input for the starting position
    start_x = BOARD_RADIUS
    start_y = BOARD_RADIUS

    knight_positions = [(start_x, start_y)]  # Track knight's positions

    draw_board(screen, knight_positions)
    pygame.display.flip()

    solve_knights_tour(screen, start_x, start_y, 2, knight_positions)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
