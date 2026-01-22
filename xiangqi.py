import pygame
import sys
from xiangqi_rules import XiangqiRules

# Initialize Pygame
pygame.init()

# Constants
BOARD_WIDTH = 9  # 9 columns (files)
BOARD_HEIGHT = 10  # 10 rows (ranks) - but row 4 and 5 form the river
SQUARE_SIZE = 60
WINDOW_WIDTH = BOARD_WIDTH * SQUARE_SIZE
WINDOW_HEIGHT = (BOARD_HEIGHT - 1) * SQUARE_SIZE + 40  # -1 because river takes no space

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (210, 180, 140)  # Lighter brown for board
BLUE = (100, 149, 237)  # Cornflower blue for river
GOLD = (212, 175, 55)  # Gold for palace
GRAY = (128, 128, 128)  # For menu


# Xiangqi Game Class
class XiangqiGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = "red"
        self.selected_piece = None
        self.valid_moves = []
        self.rules = XiangqiRules()

    def initialize_board(self):
        board = [[None for _ in range(9)] for _ in range(10)]
        # Place red pieces (bottom half)
        board[9][0] = ("rook", "red")
        board[9][1] = ("horse", "red")
        board[9][2] = ("elephant", "red")
        board[9][3] = ("advisor", "red")
        board[9][4] = ("general", "red")
        board[9][5] = ("advisor", "red")
        board[9][6] = ("elephant", "red")
        board[9][7] = ("horse", "red")
        board[9][8] = ("rook", "red")
        board[7][1] = ("cannon", "red")
        board[7][7] = ("cannon", "red")
        for col in [0, 2, 4, 6, 8]:
            board[6][col] = ("soldier", "red")

        # Place black pieces (top half)
        board[0][0] = ("rook", "black")
        board[0][1] = ("horse", "black")
        board[0][2] = ("elephant", "black")
        board[0][3] = ("advisor", "black")
        board[0][4] = ("general", "black")
        board[0][5] = ("advisor", "black")
        board[0][6] = ("elephant", "black")
        board[0][7] = ("horse", "black")
        board[0][8] = ("rook", "black")
        board[2][1] = ("cannon", "black")
        board[2][7] = ("cannon", "black")
        for col in [0, 2, 4, 6, 8]:
            board[3][col] = ("soldier", "black")
        return board

    def is_valid_move(self, piece_type, color, start, end):
        # Can't move to river rows
        if end[0] == 4 or end[0] == 5:
            return False
        return XiangqiRules.is_valid_move(self.board, piece_type, color, start, end)

    def get_valid_moves(self, piece_type, color, start):
        return XiangqiRules.get_valid_moves(self.board, piece_type, color, start)

    def make_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Move the piece
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None

        # Switch turns
        self.current_turn = "black" if self.current_turn == "red" else "red"


# GUI Class
class XiangqiGUI:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Xiangqi (Chinese Chess)")
        self.font = pygame.font.Font(None, 36)
        self.menu_font = pygame.font.Font(None, 24)
        self.use_chinese = True  # Toggle for character display

        self.piece_icons_chinese = {
            ("general", "red"): "帥",  # General (red)
            ("general", "black"): "將",  # General (black)
            ("advisor", "red"): "仕",  # Advisor (red)
            ("advisor", "black"): "士",  # Advisor (black)
            ("elephant", "red"): "相",  # Elephant (red)
            ("elephant", "black"): "象",  # Elephant (black)
            ("horse", "red"): "傌",  # Horse (red)
            ("horse", "black"): "馬",  # Horse (black)
            ("rook", "red"): "俥",  # Chariot/Rook (red)
            ("rook", "black"): "車",  # Chariot/Rook (black)
            ("cannon", "red"): "炮",  # Cannon (red)
            ("cannon", "black"): "砲",  # Cannon (black)
            ("soldier", "red"): "兵",  # Soldier (red)
            ("soldier", "black"): "卒",  # Soldier (black)
        }

        self.piece_icons_english = {
            ("general", "red"): "G",
            ("general", "black"): "G",
            ("advisor", "red"): "A",
            ("advisor", "black"): "A",
            ("elephant", "red"): "E",
            ("elephant", "black"): "E",
            ("horse", "red"): "H",
            ("horse", "black"): "H",
            ("rook", "red"): "R",
            ("rook", "black"): "R",
            ("cannon", "red"): "C",
            ("cannon", "black"): "C",
            ("soldier", "red"): "S",
            ("soldier", "black"): "S",
        }

        # Try to load a font that supports Chinese characters
        try:
            self.chinese_font = pygame.font.SysFont('simsun', 36)  # SimSun font for Chinese characters
            if not self.chinese_font:
                self.chinese_font = pygame.font.SysFont('arial unicode ms', 36)
        except:
            self.chinese_font = self.font  # Fallback to default font
            self.use_chinese = False  # Disable Chinese if font not available

    def draw_menu_bar(self):
        """Draw the menu bar at the top of the screen"""
        # Draw menu background
        pygame.draw.rect(self.screen, GRAY, (0, 0, WINDOW_WIDTH, 40))
        pygame.draw.line(self.screen, BLACK, (0, 40), (WINDOW_WIDTH, 40), 2)

        # Draw language toggle button
        button_width = 120
        button_height = 30
        button_x = WINDOW_WIDTH - button_width - 10
        button_y = 5

        # Button background
        button_color = WHITE
        pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, BLACK, (button_x, button_y, button_width, button_height), 2)

        # Button text
        button_text = "中文" if self.use_chinese else "English"
        text_surface = self.menu_font.render(button_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.screen.blit(text_surface, text_rect)

        # Draw turn indicator
        turn_text = self.font.render(f"Turn: {self.game.current_turn.capitalize()}", True,
                                     RED if self.game.current_turn == "red" else BLACK)
        self.screen.blit(turn_text, (10, 5))

        return (button_x, button_y, button_width, button_height)  # Return button bounds for click detection

    def draw_board(self):
        # Clear screen
        self.screen.fill(BROWN)

        # Draw menu bar and get button bounds
        self.language_button_rect = self.draw_menu_bar()

        # Offset the board drawing by menu height
        board_offset_y = 40

        # Draw the river between rows 4 and 5
        river_y = 4 * SQUARE_SIZE + board_offset_y
        river_rect = pygame.Rect(0, river_y, WINDOW_WIDTH, SQUARE_SIZE)
        pygame.draw.rect(self.screen, BLUE, river_rect)

        # Draw "楚河" and "漢界" in the river
        if self.use_chinese:
            try:
                chu_text = self.chinese_font.render("楚河", True, WHITE)
                han_text = self.chinese_font.render("漢界", True, WHITE)
                self.screen.blit(chu_text, (WINDOW_WIDTH // 4 - 30, river_y + SQUARE_SIZE // 2 - 15))
                self.screen.blit(han_text, (3 * WINDOW_WIDTH // 4 - 30, river_y + SQUARE_SIZE // 2 - 15))
            except:
                river_text = self.font.render("River", True, WHITE)
                self.screen.blit(river_text, (WINDOW_WIDTH // 2 - 30, river_y + SQUARE_SIZE // 2 - 15))
        else:
            river_text = self.menu_font.render("RIVER", True, WHITE)
            self.screen.blit(river_text, (WINDOW_WIDTH // 2 - 25, river_y + SQUARE_SIZE // 2 - 10))

        # Draw grid lines
        for row in range(BOARD_HEIGHT):
            if row == 4 or row == 5:
                continue  # Skip river rows

             # Adjust y position - rows after river are shifted up

            if row < 4:
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y
            else:
                y = (row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y


            pygame.draw.line(self.screen, BLACK, (SQUARE_SIZE // 2, y),
                                      (WINDOW_WIDTH - SQUARE_SIZE // 2, y), 2)
        for col in range(BOARD_WIDTH):
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(self.screen, BLACK, (x, SQUARE_SIZE // 2 + board_offset_y),
                                    (x, WINDOW_HEIGHT - SQUARE_SIZE // 2), 2)
        # Draw palaces (3x3 areas in the center of each side)
        palace_x = 3 * SQUARE_SIZE + SQUARE_SIZE // 2
        palace_width = 2 * SQUARE_SIZE

        # Black palace (top)
        palace_y_top = SQUARE_SIZE // 2 + board_offset_y
        palace_height = 2 * SQUARE_SIZE

        # Draw palace diagonals for black
        pygame.draw.line(self.screen, GOLD, (palace_x, palace_y_top),
                         (palace_x + palace_width, palace_y_top + palace_height), 2)
        pygame.draw.line(self.screen, GOLD, (palace_x + palace_width, palace_y_top),
                         (palace_x, palace_y_top + palace_height), 2)

        # Red palace (bottom)
        palace_y_bottom = 6 * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y  # Rows 7,8,9 visually

        # Draw palace diagonals for red
        pygame.draw.line(self.screen, GOLD, (palace_x, palace_y_bottom),
                         (palace_x + palace_width, palace_y_bottom + palace_height), 2)
        pygame.draw.line(self.screen, GOLD, (palace_x + palace_width, palace_y_bottom),
                         (palace_x, palace_y_bottom + palace_height), 2)

        # Draw position markers
        self.draw_position_markers(board_offset_y)

        # Draw pieces
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                piece = self.game.board[row][col]
                if piece:
                    piece_type, color = piece
                    self.draw_piece(piece_type, color, row, col, board_offset_y)

        # Highlight selected piece
        if self.game.selected_piece:
            row, col = self.game.selected_piece
            x = col * SQUARE_SIZE
            if row < 4:
                y = row * SQUARE_SIZE + board_offset_y
            else:
                y = (row - 1) * SQUARE_SIZE + board_offset_y
            pygame.draw.rect(self.screen, YELLOW, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

        # Highlight valid moves
        for move in self.game.valid_moves:
            row, col = move
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            if row < 4:
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y
            else:
                y = (row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y
            pygame.draw.circle(self.screen, GREEN, (x, y), SQUARE_SIZE // 4, 3)

        pygame.display.flip()

    def draw_position_markers(self, offset_y):
        """Draw small corner markers at key positions"""
        # Positions that need markers
        marker_positions = [
            # Cannon positions
            (2, 1), (2, 7), (7, 1), (7, 7),
            # Soldier positions
            (3, 0), (3, 2), (3, 4), (3, 6), (3, 8),
            (6, 0), (6, 2), (6, 4), (6, 6), (6, 8)
        ]

        for row, col in marker_positions:
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            # Adjust y for visual position
            # Skip river rows
            if row == 4 or row == 5:
                continue
            # Adjust y for visual position
            if row < 4:
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset_y
            else:
                y = (row - 1) * SQUARE_SIZE + SQUARE_SIZE // 2 + offset_y

            # Draw small corner markers
            marker_size = 5
            marker_offset = 15

            # Don't draw markers that would go off the board
            corners = []
            if col > 0 and row > 0:
                corners.append((-1, -1))  # top-left
            if col < 8 and row > 0:
                corners.append((1, -1))  # top-right
            if col > 0 and row < 9:
                corners.append((-1, 1))  # bottom-left
            if col < 8 and row < 9:
                corners.append((1, 1))  # bottom-right

            for dx, dy in corners:
                # Draw L-shaped corner
                start_x = x + dx * marker_offset
                start_y = y + dy * marker_offset

                # Horizontal part
                pygame.draw.line(self.screen, BLACK,
                                 (start_x, start_y),
                                 (start_x - dx * marker_size, start_y), 2)
                # Vertical part
                pygame.draw.line(self.screen, BLACK,
                                 (start_x, start_y),
                                 (start_x, start_y - dy * marker_size), 2)

    def draw_piece(self, piece_type, color, row, col, offset_y):
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset_y
        radius = SQUARE_SIZE // 2 - 5

        # Draw piece background
        bg_color = WHITE
        pygame.draw.circle(self.screen, bg_color, (x, y), radius)
        pygame.draw.circle(self.screen, RED if color == "red" else BLACK, (x, y), radius, 2)

        # Choose character set based on toggle
        if self.use_chinese:
            piece_icons = self.piece_icons_chinese
            font_to_use = self.chinese_font
        else:
            piece_icons = self.piece_icons_english
            font_to_use = self.font

        # Draw the character
        piece_text = font_to_use.render(piece_icons[(piece_type, color)], True,
                                        RED if color == "red" else BLACK)
        text_rect = piece_text.get_rect(center=(x, y))
        self.screen.blit(piece_text, text_rect)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if language button was clicked
                    button_x, button_y, button_w, button_h = self.language_button_rect
                    if button_x <= x <= button_x + button_w and button_y <= y <= button_y + button_h:
                        self.use_chinese = not self.use_chinese
                    else:
                        # Handle board clicks
                        board_y = y - 40  # Account for menu bar
                        col = x // SQUARE_SIZE
                        # Convert visual position to board row
                        visual_row = board_y // SQUARE_SIZE

                        if visual_row < 4:
                            row = visual_row
                        elif visual_row == 4:
                            continue  # Click on river, ignore
                        else:
                            row = visual_row + 1  # Account for river gap

                        if 0 <= row < 10 and row != 4 and row != 5 and 0 <= col < BOARD_WIDTH:
                            if self.game.selected_piece:
                                start_row, start_col = self.game.selected_piece
                                piece = self.game.board[start_row][start_col]
                                if piece and self.game.is_valid_move(piece[0], piece[1], (start_row, start_col),
                                                                     (row, col)):
                                    self.game.make_move((start_row, start_col), (row, col))
                                self.game.selected_piece = None
                                self.game.valid_moves = []
                            else:
                                piece = self.game.board[row][col]
                                if piece and piece[1] == self.game.current_turn:
                                    self.game.selected_piece = (row, col)
                                    self.game.valid_moves = self.game.get_valid_moves(piece[0], piece[1], (row, col))

            self.draw_board()
            clock.tick(30)


if __name__ == "__main__":
    game = XiangqiGame()
    gui = XiangqiGUI(game)
    gui.run()