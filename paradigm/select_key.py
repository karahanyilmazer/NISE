import sys
from os import path

import pygame

# Initialize Pygame
pygame.init()

# Set the font and size
font_path = path.join(path.abspath(__file__), "..", "materials", "EsseGrotesk.otf")
font_size = 48

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_GREY = (211, 211, 211)

# Initial Screen size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Grid")

# Load font
font = pygame.font.Font(font_path, font_size)

# Grid settings
n_rows, n_cols = 4, 4
n_rows += 1  # Add one for the row of indices
n_cols += 1  # Add one for the column of indices
row_height = screen_height // n_rows
col_width = screen_width // n_cols
highlighted_row = None
highlighted_col = None


def draw_grid(n_rows, n_cols, row_height, col_width):
    for row in range(n_rows):
        for col in range(n_cols):
            if row == 0 or col == 0:  # Check for the first row or column
                color = LIGHT_GREY  # A different color for indices
            elif row - 1 == highlighted_row and col - 1 == highlighted_col:
                color = LIGHT_GREEN
            elif row - 1 == highlighted_row:
                color = LIGHT_BLUE
            elif col - 1 == highlighted_col:
                color = LIGHT_GREEN
            else:
                color = WHITE

            rect = pygame.Rect(col * col_width, row * row_height, col_width, row_height)
            pygame.draw.rect(screen, color, rect)

            # Determine what text to render
            if row == 0 and col > 0:
                # Column indices
                text = font.render(str(col), True, (0, 0, 0))
            elif col == 0 and row > 0:
                # Row indices
                text = font.render(str(row), True, (0, 0, 0))
            elif row > 0 and col > 0:
                # Grid cells
                letter = chr(64 + row)
                text = font.render(f"{letter}{col}", True, (0, 0, 0))
            else:
                continue  # Skip the top-left corner

            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Adjust to account for the additional row and column
            col = event.pos[0] // col_width - 1
            row = event.pos[1] // row_height - 1

            if row >= 0 and col >= 0:
                # Highlight only if a valid grid cell (not an index cell) is clicked
                highlighted_row = row
                highlighted_col = col
        elif event.type == pygame.VIDEORESIZE:
            # The window has been resized, so resize the grid
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode(
                (screen_width, screen_height), pygame.RESIZABLE
            )

            row_height = screen_height // n_rows
            col_width = screen_width // n_cols

            font = pygame.font.Font(
                font_path, font_size
            )  # Re-create the font to adjust the size if needed

    # Redraw the screen
    screen.fill(WHITE)
    draw_grid(n_rows, n_cols, row_height, col_width)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
sys.exit()
