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
pygame.display.set_caption('Letter Selection Screen')

# Load font
font = pygame.font.Font(font_path, font_size)

# Grid settings
n_rows, n_cols = 4, 4
n_rows += 1  # Add one for the row of indices
n_cols += 1  # Add one for the column of indices
index_row_height = screen_height // (2 * n_rows - 1)  # Half the size for the index row
index_col_width = screen_width // (2 * n_cols - 1)  # Half the size for the index column
row_height = 2 * screen_height // (2 * n_rows - 1)  # Remaining rows
col_width = 2 * screen_width // (2 * n_cols - 1)  # Remaining columns
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


def color_cell(row, col):
    # Create a transparent surface for the highlights
    highlight_surface = pygame.Surface((col_width, row_height), pygame.SRCALPHA)

    # Calculate the top-left position of the cell
    x = index_col_width + (col - 1) * col_width if col > 0 else 0
    y = index_row_height + (row - 1) * row_height if row > 0 else 0

    # Adjust the size for index row and column
    width = index_col_width if col == 0 else col_width
    height = index_row_height if row == 0 else row_height

    # Create the rect for the cell
    rect = pygame.Rect(x, y, width, height)
    # rect = pygame.Rect(col * col_width, row * row_height, col_width, row_height)
    pygame.draw.rect(screen, WHITE, rect)

    # Light grey for the indices
    if row == 0 or col == 0:
        pygame.draw.rect(screen, LIGHT_GREY, rect)
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


def draw_grid_lines(n_rows, n_cols, color):
    # Draw horizontal lines
    for row in range(n_rows):  # +1 to account for the index row
        y = index_row_height + row * row_height
        start_pos = (0, y)
        end_pos = (screen_width, y)
        # Draw a thicker line for the index row
        line_width = 3 if row > 0 else 5
        pygame.draw.line(screen, color, start_pos, end_pos, line_width)

    # Draw vertical lines
    for col in range(n_cols):  # +1 to account for the index column
        x = index_col_width + col * col_width
        start_pos = (x, 0)
        end_pos = (x, screen_height)
        # Draw a thicker line for the index column
        line_width = 3 if col > 0 else 5
        pygame.draw.line(screen, color, start_pos, end_pos, line_width)


def draw_grid(n_rows, n_cols):
    idx = 0

    for row in range(n_rows):
        for col in range(n_cols):
            text = None

            rect = color_cell(row, col)

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
            mx, my = event.pos
            if mx < index_col_width:
                col = 0
            else:
                col = (mx - index_col_width) // col_width + 1
            if my < index_row_height:
                row = 0
            else:
                row = (my - index_row_height) // row_height + 1

            # Highlight only if a valid grid cell (not an index cell) is clicked
            if row > 0 and col > 0:
                highlighted_row = row - 1
                highlighted_col = col - 1
        elif event.type == pygame.VIDEORESIZE:
            # The window has been resized, so resize the grid
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode(
                (screen_width, screen_height), pygame.RESIZABLE
            )

            index_row_height = screen_height // (
                2 * n_rows - 1
            )  # Half the size for the index row
            index_col_width = screen_width // (
                2 * n_cols - 1
            )  # Half the size for the index column
            row_height = 2 * screen_height // (2 * n_rows - 1)  # Remaining rows
            col_width = 2 * screen_width // (2 * n_cols - 1)  # Remaining columns

            # Re-adjust the font size if needed
            font = pygame.font.Font(font_path, font_size)

    # Redraw the screen
    screen.fill(WHITE)
    draw_grid(n_rows, n_cols)
    draw_grid_lines(n_rows, n_cols, VERY_LIGHT_GREY)

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
sys.exit()
