import sys
from os import path

import pygame

# Initialize Pygame
pygame.init()

# Set the font and size
font_path = path.join(path.abspath(__file__), '..', 'materials', 'EsseGrotesk.otf')
font_size = 48

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (37, 122, 196)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (114, 232, 114)
LIGHT_GREY = (211, 211, 211)
VERY_LIGHT_GREY = (220, 220, 220)

# Initial Screen size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Interactive Grid')

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

# Set the font and size for the numbers
number_font_size = font_size // 2
number_font = pygame.font.Font(font_path, number_font_size)

# Load the tick image
tick_image_path = path.join(path.abspath(__file__), '..', 'materials', 'tick.png')
tick_image = pygame.image.load(tick_image_path)
# Adjust the size as needed
tick_size = min(row_height // 2, col_width // 2)
tick_image = pygame.transform.scale(tick_image, (tick_size, tick_size))


def color_cell(row, col, highlight_surface):
    color = WHITE
    rect = pygame.Rect(col * col_width, row * row_height, col_width, row_height)
    pygame.draw.rect(screen, color, rect)

    # Light grey for the indices
    if row == 0 or col == 0:
        color = LIGHT_GREY  # A different color for indices
        pygame.draw.rect(screen, color, rect)
    # Green for the selected row and column
    else:
        # Selected cell
        if row - 1 == highlighted_row and col - 1 == highlighted_col:
            highlight_surface.fill((*LIGHT_GREEN, 242))  # 90% alpha
            screen.blit(highlight_surface, rect.topleft)

        # Selected row and column
        elif row - 1 == highlighted_row or col - 1 == highlighted_col:
            highlight_surface.fill((*LIGHT_GREEN, 64))  # 25% alpha
            screen.blit(highlight_surface, rect.topleft)

    return rect


def draw_cell(screen, rect, idx):
    letter_list = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        '.',
        '?',
        ' ',
        ' ',
        ' ',
        ' ',
    ]

    # Define the vertical padding between the letter and the number
    padding = 15

    # Calculate the center for the entire cell content (letters and numbers)
    cell_content_center = rect.centerx, rect.centery - number_font_size // 3

    # Draw the first letter and its index
    letter_1 = letter_list[idx]
    text_1 = font.render(letter_1, True, BLACK)
    text_1_rect = text_1.get_rect(
        center=(
            cell_content_center[0] - col_width // 4,
            cell_content_center[1],
        )
    )

    number_1 = number_font.render('1', True, BLUE)
    number_1_rect = number_1.get_rect(
        center=(text_1_rect.centerx, text_1_rect.bottom + padding)
    )

    # Draw the second letter and its index
    letter_2 = letter_list[idx + 1]
    text_2 = font.render(letter_2, True, BLACK)
    text_2_rect = text_2.get_rect(
        center=(
            cell_content_center[0] + col_width // 4,
            cell_content_center[1],
        )
    )

    number_2 = number_font.render('2', True, BLUE)
    number_2_rect = number_2.get_rect(
        center=(text_2_rect.centerx, text_2_rect.bottom + padding)
    )

    # Display the letters and numbers
    screen.blit(text_1, text_1_rect.topleft)
    screen.blit(number_1, number_1_rect.topleft)
    screen.blit(text_2, text_2_rect.topleft)
    screen.blit(number_2, number_2_rect.topleft)


def draw_space_symbol(screen, rect):
    # Draw a wide underscore or another appropriate symbol to represent a space
    underscore_width = rect.width // 3
    underscore_height = 5  # The thickness of the underscore
    underscore_start = (
        rect.centerx - underscore_width // 2,
        rect.centery + rect.height // 4,
    )
    underscore_end = (underscore_start[0] + underscore_width, underscore_start[1])
    pygame.draw.line(screen, BLACK, underscore_start, underscore_end, underscore_height)


def draw_tick(rect):
    # Calculate the position to center the tick image in the rect
    image_rect = tick_image.get_rect(center=rect.center)

    # Blit the image onto the screen
    screen.blit(tick_image, image_rect.topleft)


def draw_grid_lines(n_rows, n_cols, row_height, col_width, color):
    # Draw horizontal lines
    for row in range(1, n_rows):
        pygame.draw.line(
            screen, color, (0, row * row_height), (screen_width, row * row_height), 3
        )

    # Draw vertical lines
    for col in range(1, n_cols):
        pygame.draw.line(
            screen, color, (col * col_width, 0), (col * col_width, screen_height), 3
        )


def draw_grid(n_rows, n_cols, row_height, col_width):
    idx = 0

    # Create a transparent surface for the highlights
    highlight_surface = pygame.Surface((col_width, row_height), pygame.SRCALPHA)

    for row in range(n_rows):
        for col in range(n_cols):
            text = None
            rect = color_cell(row, col, highlight_surface)

            # Column indices
            if row == 0 and col > 0:
                text = font.render(str(col), True, (0, 0, 0))

            # Row indices
            elif col == 0 and row > 0:
                text = font.render(str(row), True, (0, 0, 0))

            # Space symbol
            elif row == n_rows - 1 and col == n_cols - 2:
                draw_space_symbol(screen, rect)

            # Tick symbol
            elif row == n_rows - 1 and col == n_cols - 1:
                draw_tick(rect)

            # Grid cells
            elif row > 0 and col > 0:
                draw_cell(screen, rect, idx)
                idx += 2

            # Skip the top-left corner
            else:
                continue

            if text:
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
    draw_grid_lines(n_rows, n_cols, row_height, col_width, VERY_LIGHT_GREY)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
sys.exit()
