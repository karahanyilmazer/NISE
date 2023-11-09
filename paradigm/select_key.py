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
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)

# Initial Screen size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Grid")

# Load font
font = pygame.font.Font(font_path, font_size)

# Grid settings
n_rows, n_cols = 4, 4
row_height = screen_height // n_rows
col_width = screen_width // n_cols
highlighted_row = None
highlighted_col = None


# Function to draw the grid
def draw_grid(n_rows, n_cols, row_height, col_width):
    for row in range(n_rows):
        for col in range(n_cols):
            if row == highlighted_row:
                color = LIGHTBLUE
            elif col == highlighted_col:
                color = LIGHTGREEN
            else:
                color = WHITE

            rect = pygame.Rect(col * col_width, row * row_height, col_width, row_height)
            pygame.draw.rect(screen, color, rect)

            letter = chr(65 + row)
            text = font.render(f"{letter}{col + 1}", True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the index of the row and column that was clicked
            col = event.pos[0] // col_width
            row = event.pos[1] // row_height

            # Highlight the clicked row and column
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
