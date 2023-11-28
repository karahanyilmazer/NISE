# %%
import socket
import sys
from os import path

import pygame

# %%
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (37, 122, 196)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (114, 232, 114)
LIGHT_GREY = (211, 211, 211)
VERY_LIGHT_GREY = (220, 220, 220)


class LetterSelectionScreen(object):
    def __init__(self):
        pygame.init()
        current_dir = path.dirname(path.abspath(__file__))

        # Construct the path to the font file
        self.font_path = path.join(current_dir, 'materials', 'EsseGrotesk.otf')
        self.font_size = 48
        self.number_font_size = self.font_size // 2

        self.screen_width, self.screen_height = 1800, 1000 #2000, 1600     
        self.header_height = 60  # Height of the header space to display selected keys
        # Increase overall screen height to accommodate the header
        self.screen_height += self.header_height

        self.circle_positions = [
            (20, self.header_height // 2),
            (60, self.header_height // 2),
            (100, self.header_height // 2),
        ]

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )
        pygame.display.set_caption('Letter Selection Screen')

        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.number_font = pygame.font.Font(self.font_path, self.number_font_size)

        self.n_rows, self.n_cols = 5, 5  # Including index rows and columns

        # Recalculate the grid size based on the new screen height
        self.index_row_height = (self.screen_height - self.header_height) // (
            2 * self.n_rows - 1
        )
        self.row_height = (
            2 * (self.screen_height - self.header_height) // (2 * self.n_rows - 1)
        )

        self.index_col_width = self.screen_width // (2 * self.n_cols - 1)
        self.col_width = 2 * self.screen_width // (2 * self.n_cols - 1)

        self.selecting_col = True
        self.highlighted_row = None
        self.highlighted_col = None

        self.image_size = min(self.row_height // 2, self.col_width // 2)

        self.tick_image_path = path.join(current_dir, 'materials', 'tick.png')
        self.tick_image = pygame.image.load(self.tick_image_path)
        self.tick_image = pygame.transform.scale(
            self.tick_image, (self.image_size, self.image_size)
        )

        self.back_image_path = path.join(current_dir, 'materials', 'backspace.png')
        self.back_image = pygame.image.load(self.back_image_path)
        aspect_ratio = self.back_image.get_width() / self.back_image.get_height()
        new_height = int(self.image_size / aspect_ratio)
        self.back_image = pygame.transform.scale(
            self.back_image, (self.image_size, new_height)
        )

        self.space_image_path = path.join(current_dir, 'materials', 'space.png')

        self.space_image = pygame.image.load(self.space_image_path)
        aspect_ratio = self.space_image.get_width() / self.space_image.get_height()
        new_height = int(self.image_size / aspect_ratio)
        self.space_image = pygame.transform.scale(
            self.space_image, (self.image_size, new_height)
        )

        self.running = True

        self.key_list = []
        self.word_list = []

        self.letter_dict = {
            'A': [1, 1, 1],
            'B': [1, 1, 2],
            'C': [2, 1, 1],
            'D': [2, 1, 2],
            'E': [3, 1, 1],
            'F': [3, 1, 2],
            'G': [4, 1, 1],
            'H': [4, 1, 2],
            'I': [1, 2, 1],
            'J': [1, 2, 2],
            'K': [2, 2, 1],
            'L': [2, 2, 2],
            'M': [3, 2, 1],
            'N': [3, 2, 2],
            'O': [4, 2, 1],
            'P': [4, 2, 2],
            'Q': [1, 3, 1],
            'R': [1, 3, 2],
            'S': [2, 3, 1],
            'T': [2, 3, 2],
            'U': [3, 3, 1],
            'V': [3, 3, 2],
            'W': [4, 3, 1],
            'X': [4, 3, 2],
            'Y': [1, 4, 1],
            'Z': [1, 4, 2],
            '.': [2, 4, 1],
            '?': [2, 4, 2],
            ' ': [3, 4, 1],
            'backspace': [3, 4, 2],
            'send': [4, 4, 1],
        }

    def get_letter(self, keys):
        for letter, key_combo in self.letter_dict.items():
            if key_combo == keys:
                return letter
        return ''  # Return None if no matching letter is found

    def color_cell(self, row, col):
        # Create a transparent surface for the highlights
        highlight_surface = pygame.Surface(
            (self.col_width, self.row_height), pygame.SRCALPHA
        )

        # Calculate the top-left position of the cell
        x = self.index_col_width + (col - 1) * self.col_width if col > 0 else 0
        y = (
            self.header_height + self.index_row_height + (row - 1) * self.row_height
            if row > 0
            else self.header_height
        )

        # Adjust the size for index row and column
        width = self.index_col_width if col == 0 else self.col_width
        height = self.index_row_height if row == 0 else self.row_height

        # Create the rect for the cell
        rect = pygame.Rect(x, y, width, height)
        # rect = pygame.Rect(col * col_width, row * row_height, col_width, row_height)
        pygame.draw.rect(self.screen, WHITE, rect)

        # Light grey for the indices
        if row == 0 or col == 0:
            pygame.draw.rect(self.screen, LIGHT_GREY, rect)
        # Green for the selected row and column
        else:
            # Selected cell
            if row - 1 == self.highlighted_row and col - 1 == self.highlighted_col:
                highlight_surface.fill((*LIGHT_GREEN, 242))  # 90% alpha
                self.screen.blit(highlight_surface, rect.topleft)

            # Selected row and column
            elif row - 1 == self.highlighted_row or col - 1 == self.highlighted_col:
                highlight_surface.fill((*LIGHT_GREEN, 64))  # 25% alpha
                self.screen.blit(highlight_surface, rect.topleft)

        return rect

    def draw_cell(self, screen, rect, idx):
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
            '_',
            ' ',
            ' ',
            ' ',
        ]

        # Define the vertical padding between the letter and the number
        padding = 15

        # Calculate the center for the entire cell content (letters and numbers)
        cell_content_center = rect.centerx, rect.centery - self.number_font_size // 3

        # Draw the first letter and its index
        letter_1 = letter_list[idx]
        text_1 = self.font.render(letter_1, True, BLACK)
        text_1_rect = text_1.get_rect(
            center=(
                cell_content_center[0] - self.col_width // 4,
                cell_content_center[1],
            )
        )

        number_1 = self.number_font.render('1', True, BLUE)
        number_1_rect = number_1.get_rect(
            center=(text_1_rect.centerx, text_1_rect.bottom + padding)
        )

        # Draw the second letter and its index
        letter_2 = letter_list[idx + 1]
        text_2 = self.font.render(letter_2, True, BLACK)
        text_2_rect = text_2.get_rect(
            center=(
                cell_content_center[0] + self.col_width // 4,
                cell_content_center[1],
            )
        )

        number_2 = self.number_font.render('2', True, BLUE)
        number_2_rect = number_2.get_rect(
            center=(text_2_rect.centerx, text_2_rect.bottom + padding)
        )

        # Display the letters and numbers
        screen.blit(text_1, text_1_rect.topleft)
        screen.blit(number_1, number_1_rect.topleft)
        screen.blit(text_2, text_2_rect.topleft)
        screen.blit(number_2, number_2_rect.topleft)

    def draw_image(self, rect, image, pos=None):
        # Define the vertical padding between the letter and the number
        padding = 15

        # Calculate the center for the entire cell content (letters and numbers)
        cell_content_center = rect.centerx, rect.centery - self.number_font_size // 3

        if pos == 'left':
            offset = -self.col_width // 4
            idx = '1'
        elif pos == 'right':
            offset = self.col_width // 4
            idx = '2'
        else:
            offset = 0
            idx = None

        # Calculate the position to center the tick image in the rect
        image_rect = image.get_rect(
            center=(
                cell_content_center[0] + offset,
                cell_content_center[1],
            )
        )

        number = self.number_font.render(idx, True, BLUE)
        number_rect = number.get_rect(
            center=(image_rect.centerx, image_rect.bottom + padding)
        )

        # Blit the image onto the screen
        self.screen.blit(image, image_rect.topleft)
        self.screen.blit(number, number_rect.topleft)

    def draw_grid_lines(self, n_rows, n_cols, color):
        # Draw horizontal lines
        for row in range(n_rows):  # +1 to account for the index row
            y = self.header_height + self.index_row_height + row * self.row_height
            # y = self.index_row_height + row * self.row_height
            start_pos = (0, y)
            end_pos = (self.screen_width, y)
            # Draw a thicker line for the index row
            line_width = 3 if row > 0 else 5
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)

        # Draw vertical lines
        for col in range(n_cols):  # +1 to account for the index column
            x = self.index_col_width + col * self.col_width
            start_pos = (x, self.header_height)
            end_pos = (x, self.screen_height)
            # Draw a thicker line for the index column
            line_width = 3 if col > 0 else 5
            pygame.draw.line(self.screen, color, start_pos, end_pos, line_width)

    def draw_grid(self, n_rows, n_cols):
        idx = 0

        for row in range(n_rows):
            for col in range(n_cols):
                text = None

                rect = self.color_cell(row, col)

                # Column indices
                if row == 0 and col > 0:
                    text = self.font.render(str(col), True, (0, 0, 0))

                # Row indices
                elif col == 0 and row > 0:
                    text = self.font.render(str(row), True, (0, 0, 0))

                # Space and backspace symbols
                elif row == n_rows - 1 and col == n_cols - 2:
                    # self.draw_space_symbol(self.screen, rect)
                    self.draw_image(rect, self.space_image, pos='left')
                    self.draw_image(rect, self.back_image, pos='right')

                # Tick symbol
                elif row == n_rows - 1 and col == n_cols - 1:
                    self.draw_image(rect, self.tick_image)

                # Grid cells
                elif row > 0 and col > 0:
                    self.draw_cell(self.screen, rect, idx)
                    idx += 2

                # Skip the top-left corner
                else:
                    continue

                if text:
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def render_text(self, text, position, color=WHITE, background=None):
        text_surface = self.font.render(text, True, color, background)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def draw_circles(self):
        for i, position in enumerate(self.circle_positions):
            if i < len(self.key_list):
                # Draw filled circle
                pygame.draw.circle(self.screen, LIGHT_GREEN, position, 10)
                if i == 2:
                    pygame.draw.circle(self.screen, BLUE, position, 10)
            else:
                # Draw hollow circle
                pygame.draw.circle(self.screen, LIGHT_GREEN, position, 10, 2)
                if i == 2:
                    pygame.draw.circle(self.screen, BLUE, position, 10, 2)

    def run(self):
        # Set up the client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'  # Change this to the IP address of your server
        port = 12345  # Choose the same port number as in the server

        client_socket.connect((host, port))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    # The window has been resized, so resize the grid
                    self.screen_width, self.screen_height = event.size
                    self.screen = pygame.display.set_mode(
                        (self.screen_width, self.screen_height), pygame.RESIZABLE
                    )

                    self.index_row_height = (
                        self.screen_height - self.header_height
                    ) // (2 * self.n_rows - 1)
                    self.row_height = (
                        2
                        * (self.screen_height - self.header_height)
                        // (2 * self.n_rows - 1)
                    )

                    self.index_col_width = self.screen_width // (2 * self.n_cols - 1)
                    self.col_width = 2 * self.screen_width // (2 * self.n_cols - 1)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Adjust to account for the additional row and column
                    mx, my = event.pos
                    if mx < self.index_col_width:
                        col = 0
                    else:
                        col = (mx - self.index_col_width) // self.col_width + 1
                    if my < self.index_row_height + self.header_height:
                        row = 0
                    else:
                        row = (
                            my - (self.index_row_height + self.header_height)
                        ) // self.row_height + 1

                    # Highlight only if a valid grid cell (not an index cell) is clicked
                    if row > 0 and col > 0:
                        self.highlighted_row = row - 1
                        self.highlighted_col = col - 1

                    # Re-adjust the font size if needed
                    self.font = pygame.font.Font(self.font_path, self.font_size)

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        self.key_list.append(event.key - 48)

                        index = int(event.unicode) - 1  # Convert key to 0-based index
                        if self.selecting_col:
                            self.highlighted_col = index
                        else:
                            self.highlighted_row = index

                        if len(self.key_list) == 3:
                            letter = self.get_letter(self.key_list)
                            if letter not in ('backspace', 'send'):
                                self.word_list.append(letter)
                            elif letter == 'backspace':
                                self.word_list.pop()
                            elif letter == 'send':
                                pass

                            self.key_list = []
                            self.highlighted_row = None
                            self.highlighted_col = None
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            # Receive a message from the server
            data_from_server = client_socket.recv(4)
            index = int.from_bytes(data_from_server, byteorder='big')

            print(f"Received from server: {index}")

            if index != 0:
                self.key_list.append(index)
                if self.selecting_col:
                    self.highlighted_col = index - 1
                else:
                    self.highlighted_row = index - 1
                if len(self.key_list) == 3:
                    letter = self.get_letter(self.key_list)
                    if self.key_list[2] == '3' or self.key_list[2] == '4':
                        pass
                    elif letter not in ('backspace', 'send'):
                        self.word_list.append(letter)
                    elif letter == 'backspace':
                        self.word_list.pop()
                    elif letter == 'send':
                        pass
                    self.key_list = []
                    self.highlighted_row = None
                    self.highlighted_col = None
            index = 0

            # Check if we are selecting a row or column
            if len(self.key_list) in (0, 2):
                self.selecting_col = True
            elif len(self.key_list) == 1:
                self.selecting_col = False

            # Clear the screen
            self.screen.fill(WHITE)
            # Draw the header background
            pygame.draw.rect(
                self.screen, BLACK, (0, 0, self.screen_width, self.header_height)
            )
            self.render_text(
                ''.join(self.word_list),
                (self.screen_width // 2, self.header_height // 2),
            )
            self.draw_grid(self.n_rows, self.n_cols)
            self.draw_grid_lines(self.n_rows, self.n_cols, VERY_LIGHT_GREY)
            self.draw_circles()

            pygame.display.flip()

        client_socket.close()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = LetterSelectionScreen()
    game.run()

# %%
