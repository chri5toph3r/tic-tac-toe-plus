import pygame

pygame.init()

win_title = 'TicTacToe+'
icon = pygame.image.load('C:/Users/Krzysztof/PycharmProjects/tic-tac-toe-plus/icon.png')
win_size = 900
bg_color = 'white'  # '(106, 42, 245)

line_quantity = 9
line_width = 2
line_color = (150, 150, 150)  # (4, 57, 107)

big_line_quantity = 3
big_line_width = 4
big_line_color = 'black'  # (6, 14, 184)

circle_color = 'red'
square_color = 'blue'
symbol_width = int(win_size / 100)

shadow_color = (230, 230, 230)

rect_diff = symbol_width

tile_size = win_size / line_quantity
sector_size = win_size / big_line_quantity

info_font = pygame.font.Font('freesansbold.ttf', 40)
info_aa = True
info_color = (0, 0, 0)
info_bg = (255, 255, 255)


class Pen:

    def __init__(self):

        self.tiles_rect = {}
        self.tiles_pos = {}
        self.sectors_rect = {}

        self.outline_rect = None
        self.cur_outline_x, self.cur_outline_y = -100, -100
        # self.draw_outline(self.cur_outline_x, self.cur_outline_y)

        self.col = None
        self.row = None

        self.screen = pygame.display.set_mode((win_size, win_size))
        pygame.display.set_caption(win_title)
        pygame.display.set_icon(icon)
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
                if target == self.tiles_rect:
                    self.tiles_pos[name] = left, top

    # uses 9x9 tiles grid instead of 3x3x3x3
    def draw_symbol(self, symbol, colrow, target=None):
        if target is None:
            target = self.tiles_rect[colrow]
        else:
            target = self.sectors_rect[colrow]

        if symbol == 'o':
            pygame.draw.ellipse(self.screen, circle_color, target, symbol_width)
        elif symbol == 'x':
            # pygame.Rect.inflate_ip(target, (-symbol_width, -symbol_width))
            pygame.draw.rect(self.screen, square_color, target, symbol_width)

        # self.move_outline(colrow)
        pygame.display.update()

        pygame.display.flip()
        return

    #def draw_outline(self, x, y):
    #    self.outline_rect = pygame.Rect(x, y, tile_size, tile_size)
    #    pygame.draw.rect(self.screen, outline_color, self.outline_rect, outline_width)
    #    self.cur_outline_x, self.cur_outline_y = x, y
    #    return

    #def move_outline(self, colrow):
    #    print('self.tiles_pos', self.tiles_pos[colrow])

    #    xk, yk = self.tiles_pos[colrow]
    #    x_vector, y_vector = int(xk - self.cur_outline_x), int(yk - self.cur_outline_y)
    #    self.outline_rect.move(x_vector, y_vector)

    def draw_default_board(self, sector=None):
        self.screen.fill(bg_color)

        # draw shadow behind active sector
        if sector is not None:
            pygame.Surface.fill(self.screen, shadow_color, self.sectors_rect[sector])

        # rysowanie siatki
        self.draw_lines(line_quantity, line_width, line_color)
        self.draw_rects(line_quantity, self.tiles_rect, rect_diff)
        # print(self.tiles_pos)
        self.draw_lines(big_line_quantity, big_line_width, big_line_color)
        self.draw_rects(big_line_quantity, self.sectors_rect, rect_diff)
        pygame.display.flip()
        return

    # TODO: 9x9 <-> 3x3x3x3 translate function
    @staticmethod
    def pos_system_translate(pos1, pos2=None):

        if pos1 is None:
            # print(f"pos1 is None -> pos1 ({pos1}) returned")
            return pos1

        # 3x3 x 3x3 -> 9x9
        if pos2 is not None:
            sector_col, sector_row = pos1
            tile_col, tile_row = pos2
            # print(f"pos1 = {pos1} & pos2 = {pos2}; return = {sector_col*3 + tile_col, sector_row*3 + sector_row}")
            return sector_col*3 + tile_col, sector_row*3 + tile_row

        # 9x9 -> 3x3 x 3x3
        board_col, board_row = pos1
        # print(f'pos_translate pos1: {pos1}; bc, br: {board_col, board_row}')
        return board_col // 3, board_row // 3, board_col % 3, board_row % 3

    def pos_translate(self, position):
        x, y = position
        if y > win_size or x > win_size:
            return None
        self.col = x // tile_size
        self.row = y // tile_size
        return int(self.col), int(self.row)

    def fin_msg(self, msg):

        info = info_font.render(msg, info_aa, info_color, info_bg)
        self.screen.blit(info, (250, 280))
        pygame.display.flip()

    def refresh(self, written_symbols_dic, next_sector, msg=None, draw_board=None):

        for sector in written_symbols_dic:
            print(f"{sector}: {written_symbols_dic[sector]}")

        # rysowanie tła
        if draw_board is None:
            if next_sector == (4, 4):
                next_sector = None
            self.draw_default_board(next_sector)
        else:
            # customowe rysownie
            draw_board()

        # draw outline
        # self.draw_symbol()

        # rysowanie symboli
        counting = 0
        for sector in range(len(written_symbols_dic)):
            for col in range(3):
                for row in range(3):
                    sec_name = col, row
                    # jeśli sektor jest wygrany to narysuj tylko duży symbol
                    if sec_name in written_symbols_dic[(3, 3)]:
                        self.draw_symbol(written_symbols_dic[(3, 3)][sec_name], sec_name, 'board')
                    # jeśli sektor niewygrany to rysuj małe symbole
                    else:
                        for tile in written_symbols_dic[sec_name]:
                            colrow = self.pos_system_translate(sec_name, tile)
                            # print(f"sec_name: {sec_name}; tile: {tile}\n")
                            counting += 1
                            self.draw_symbol(written_symbols_dic[sec_name][tile], colrow)

        # print(f'sec_name: {sec_name}|(col, row): {(col, row)}')
        # print(f'colrow: {colrow}')
        # print(f"tiles checked: {counting}")


if __name__ == '__main__':
    pen = Pen()
    pen.draw_default_board()

    turn = 1
    symbol = 'o'
    flag = True
    while flag:
        for event in pygame.event.get():
            flag = event.type != pygame.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                pen.pos_translate(pygame.mouse.get_pos())
                pen.draw_symbol('o')
                turn += 1
                turn //= 2
                if turn == 1:
                    symbol = 'o'
                else:
                    symbol = 'x'
