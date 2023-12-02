# %%
import sys
import time
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
BOX_COLOR = (173, 216, 230)  # Light blue color


class LetterSelectionScreen(object):
    def __init__(self):
        pygame.init()
        self.font_path = path.join(
            path.abspath(__file__), '..', 'materials', 'EsseGrotesk.otf'
        )
        self.font_size = 36
        self.number_font_size = self.font_size // 2

        self.screen_width, self.screen_height = 1400, 600

        self.header_height = 60  # Height of the header space to display selected keys
        # Increase overall screen height to accommodate the header
        self.screen_height += self.header_height

        self.circle_positions = [
            (20, self.header_height // 2),
            (60, self.header_height // 2),
            (100, self.header_height // 2),
        ]

        self.n_boxes = 4
        self.box_padding = 10
        self.letter_padding = 5
        self.box_width = (
            self.screen_width - ((self.n_boxes + 1) * self.box_padding)
        ) / self.n_boxes
        self.box_height = 2 * self.screen_height / 3
        self.box_top_margin = (
            ((self.screen_height - self.header_height) / 2)
            - (self.box_height / 2)
            + self.header_height
        )

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )
        pygame.display.set_caption('Letter Selection Screen')

        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.number_font = pygame.font.Font(self.font_path, self.number_font_size)

        self.image_size = min(self.box_height // 2, self.box_width // 2)

        self.tick_image_path = path.join(
            path.abspath(__file__), '..', 'materials', 'tick.png'
        )
        self.tick_image = pygame.image.load(self.tick_image_path)
        self.tick_image = pygame.transform.scale(
            self.tick_image, (self.image_size, self.image_size)
        )

        self.back_image_path = path.join(
            path.abspath(__file__), '..', 'materials', 'backspace.png'
        )
        self.back_image = pygame.image.load(self.back_image_path)
        aspect_ratio = self.back_image.get_width() / self.back_image.get_height()
        new_height = int(self.image_size / aspect_ratio)
        self.back_image = pygame.transform.scale(
            self.back_image, (self.image_size, new_height)
        )

        self.space_image_path = path.join(
            path.abspath(__file__), '..', 'materials', 'space.png'
        )
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

        self.letter_list = [
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
        ]

        self.letter_groups = self.split_letters_into_groups(self.letter_list)

    def get_letter(self, keys):
        for letter, key_combo in self.letter_dict.items():
            if key_combo == keys:
                return letter
        return ''  # Return None if no matching letter is found

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

    def split_letters_into_groups(self, letters):
        # Calculate the base size for each group
        group_size = len(letters) // self.n_boxes
        # Initialize a list to hold all groups
        groups = []

        # Calculate the number of groups that will have an extra letter
        extra_letter_groups = len(letters) % self.n_boxes

        # Start index for slicing letters
        start_idx = 0

        for i in range(self.n_boxes):
            # If there are still extra letters to distribute, add one more letter to the group
            size = group_size + (1 if i < extra_letter_groups else 0)
            # Slice the letters to create a new group and append to the groups list
            groups.append(letters[start_idx : start_idx + size])
            # Move the start index for the next group
            start_idx += size

        return groups

    def draw_boxes(self):
        letter_slot_heights = [
            (self.box_height) / (len(group) + 1) for group in self.letter_groups
        ]

        for i, group in enumerate(self.letter_groups):
            # Define the x position of the box
            box_x = self.box_padding + i * (self.box_width + self.box_padding)

            # Draw the box
            pygame.draw.rect(
                self.screen,
                BOX_COLOR,
                (
                    box_x,
                    self.box_top_margin,
                    self.box_width,
                    self.box_height,
                ),
            )

            # Center the letters vertically within each box
            for j, letter in enumerate(group):
                # Calculate the y position for each letter to be centered in its slot
                text_x = box_x + (self.box_width - 10) // 2
                text_y = self.box_top_margin + (j + 1) * letter_slot_heights[i]

                # Render the letter
                text_surface = self.font.render(letter, True, BLACK)
                text_rect = text_surface.get_rect()

                # Center the text horizontally in the box
                text_rect.center = (text_x, text_y)

                # Blit the text surface onto the screen at the calculated x, y coordinates
                self.screen.blit(text_surface, text_rect)

    def handle_mouse_click(self, pos):
        """Handle the mouse click event."""
        # Determine which box has been clicked
        box_index = int(pos[0] // (self.box_width + self.box_padding))
        print(len(self.letter_groups[box_index]))
        if box_index < len(self.letter_groups):
            if len(self.letter_groups[box_index]) == 0:
                # Ignore empty boxes
                pass
            elif len(self.letter_groups[box_index]) != 1:
                # Split the letters in the clicked box into four groups
                self.letter_groups = self.split_letters_into_groups(
                    self.letter_groups[box_index]
                )
                # Flatten the list and filter out any empty subgroups
                self.letter_list = [
                    letter for subgroup in self.letter_groups for letter in subgroup
                ]
            else:
                # If the clicked box only has one letter, add it to the word list
                self.word_list.append(self.letter_groups[box_index][0])
                # Reset the letter groups
                self.letter_list = [
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
                ]
                self.letter_groups = self.split_letters_into_groups(self.letter_list)

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
                    self.handle_mouse_click(event.pos)

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
            # self.draw_grid(self.n_rows, self.n_cols)
            # self.draw_grid_lines(self.n_rows, self.n_cols, VERY_LIGHT_GREY)
            self.draw_boxes()
            self.draw_circles()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = LetterSelectionScreen()
    game.run()
