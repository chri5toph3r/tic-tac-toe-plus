import pygame

pygame.init()

win_title = 'TicTacToe+'
win_size = 600
bg_color = 'white'  # '(106, 42, 245)

line_quantity = 9
line_width = 3
line_color = (150, 150, 150)  # (4, 57, 107)

big_line_quantity = 3
big_line_width = 3
big_line_color = 'black'  # (6, 14, 184)

circle_color = 'red'
square_color = 'blue'
symbol_width = int(win_size / 100)

outline_color = (206, 252, 3)
outline_width = int(symbol_width/2)

rect_diff = symbol_width

tile_size = win_size / line_quantity
sector_size = win_size / big_line_quantity

info_font = pygame.font.Font('freesansbold.ttf', 40)
info_aa = True
info_color = (0, 0, 0)
info_bg = (255, 255, 255)


class Pen:

    # prev_tile = None

    def __init__(self):
        self.tiles_rect = {}
        # self.prev_tile_obj = {}
        # self.tiles_info = {}
        self.sectors_rect = {}

        self.col = None
        self.row = None

        self.screen = pygame.display.set_mode((win_size, win_size))
        pygame.display.set_caption(win_title)
        self.screen.fill(bg_color)
        pygame.display.flip()

    def draw_lines(self, ln_quantity, ln_width, ln_color):
        tile_len = win_size / ln_quantity
        # rysowanie linii
        for i in range(1, ln_quantity):
            pygame.draw.line(self.screen, ln_color, (tile_len * i, 0),
                             (tile_len * i, win_size), ln_width)
            pygame.draw.line(self.screen, ln_color, (0, tile_len * i),
                             (win_size, tile_len * i), ln_width)
        return

    def draw_rects(self, rect_quantity, target, rect_len_diff):
        tile_len = win_size / rect_quantity
        # tworzenie siatki pól na znaki
        for col in range(rect_quantity):
            for row in range(rect_quantity):
                name = col, row
                left = col * tile_len + rect_len_diff
                top = row * tile_len + rect_len_diff
                side_ln = tile_len - (2 * rect_len_diff)
                target[name] = pygame.Rect(left, top, side_ln, side_ln)
                # if target != self.tiles_info:
                #     target[name] = pygame.Rect(left, top, side_ln, side_ln)
                # else:
                #     target[name] = left, top, side_ln, side_ln

    def draw_symbol(self, symbol, target=None, colrow=None):
        if target is None:
            colrow = self.col, self.row
            target = self.tiles_rect[colrow]
        elif target == 'sector':
            target = self.sectors_rect[colrow]
        # else:
        #     target = self.prev_tile_obj[colrow]

        if symbol == 'o':
            pygame.draw.ellipse(self.screen, circle_color, target, symbol_width)
            # Pen.prev_tile = colrow
        elif symbol == 'x':
            pygame.Rect.inflate_ip(target, (-symbol_width, -symbol_width))
            pygame.draw.rect(self.screen, square_color, target, symbol_width)
            # Pen.prev_tile = colrow
        # elif symbol == 'outline':
        #     pygame.draw.rect(self.screen, outline_color, target, outline_width)

        pygame.display.flip()
        return

    def draw_default_board(self):
        # rysowanie siatki
        self.draw_lines(line_quantity, line_width, line_color)
        # self.draw_rects(line_quantity, self.prev_tile_obj, 0)
        # self.draw_rects(line_quantity, self.tiles_info, 0)
        self.draw_rects(line_quantity, self.tiles_rect, rect_diff)
        self.draw_lines(big_line_quantity, big_line_width, big_line_color)
        self.draw_rects(big_line_quantity, self.sectors_rect, rect_diff)
        pygame.display.flip()
        return

    def pos_translate(self, position):
        x, y = position
        if y > win_size or x > win_size:
            return None
        self.col = x // tile_size
        self.row = y // tile_size
        return self.col, self.row

    def fin_msg(self, msg):

        info = info_font.render(msg, info_aa, info_color, info_bg)
        self.screen.blit(info, (250, 280))
        pygame.display.flip()


if __name__ == '__main__':
    pen = Pen()
    pen.draw_default_board()

    flag = True
    while flag:
        for event in pygame.event.get():
            flag = event.type != pygame.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                pen.pos_translate(pygame.mouse.get_pos())
                pen.draw_symbol('o')
