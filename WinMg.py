import pygame
import time

pygame.init()

# general window variables
win_title = 'TicTacToe+'
icon = pygame.image.load('C:/Users/Krzysztof/PycharmProjects/tic-tac-toe-plus/graphics/icon2.png')
win_size = 900
bg_color = (230, 230, 230)  # 'white'  # (106, 42, 245)

# thin lines variables
line_quantity = 9
line_width = 2
line_color = (150, 150, 150)  # (4, 57, 107)

# thick lines variables
big_line_quantity = 3
big_line_width = 4
big_line_color = 'black'  # (6, 14, 184)

# symbols general variables
circle_color = 'red'
square_color = 'blue'
symbol_width = int(win_size / 100)

# miscellaneous variables
shadow_color = 'white'  # '(230, 230, 230)

rect_diff = symbol_width

# size variables
tile_size = win_size / line_quantity
sector_size = win_size / big_line_quantity

# screen message variables
info_font_size = 100
info_font = pygame.font.Font("freesansbold.ttf", info_font_size)
info_aa = True
info_color = (0, 0, 0)
info_bg = (255, 255, 255)
info_coords = (win_size/2-(7/5*info_font_size), win_size/2-(1/2*info_font_size-1))

# watermark variables
watermark_font = pygame.font.Font('freesansbold.ttf', 10)
watermark_txt = "Krzysztof Kulak"
watermark_color = (220, 220, 220)
watermark_coords = (10, 0)

# general cursor variables
# cur_img_width = 30
# cur_img_r = cur_img_width/2
# cur_img_ln_width = 5

# symbol cursors variables
# circle
# circle_surf = pygame.Surface((cur_img_width, cur_img_width), pygame.SRCALPHA)
# pygame.draw.circle(circle_surf, 'red', (cur_img_r, cur_img_r), cur_img_r, cur_img_ln_width)
# circle = pygame.cursors.Cursor((int(cur_img_r), int(cur_img_r)), circle_surf)

# square
# square_surf = pygame.Surface((cur_img_width, cur_img_width), pygame.SRCALPHA)
# pygame.draw.rect(square_surf, 'blue', (0, 0, cur_img_width, cur_img_width), cur_img_ln_width)
# square = pygame.cursors.Cursor((int(cur_img_r), int(cur_img_r)), square_surf)

# crayon cursors variables
# circle
circle_img = pygame.image.load('C:/Users/Krzysztof/PycharmProjects/tic-tac-toe-plus/graphics/cursor2.png')
circle = pygame.cursors.Cursor((0, 127), circle_img)

# square
square_img = pygame.image.load('C:/Users/Krzysztof/PycharmProjects/tic-tac-toe-plus/graphics/cursor1.png')
square = pygame.cursors.Cursor((0, 127), square_img)


class Pen:

    def __init__(self):

        self.tiles_rects = {}
        self.sectors_rects = {}

        self.col = None
        self.row = None

        # cursors list
        self.cursors = [circle, square]
        self.cursor_index = 0
        pygame.mouse.set_cursor(self.cursors[self.cursor_index])

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
                left = col * tile_len + rect_len_diff
                top = row * tile_len + rect_len_diff
                side_ln = tile_len - (2 * rect_len_diff)
                target[(col, row)] = pygame.Rect(left, top, side_ln, side_ln)

    # uses 9x9 tiles grid instead of 3x3x3x3
    def draw_symbol(self, symbol, colrow, target=None):
        if target is None:
            target = self.tiles_rects[colrow]
        else:
            target = self.sectors_rects[colrow]

        if symbol == 'o':
            pygame.draw.ellipse(self.screen, circle_color, target, symbol_width)
        elif symbol == 'x':
            # pygame.Rect.inflate_ip(target, (-symbol_width, -symbol_width))
            pygame.draw.rect(self.screen, square_color, target, symbol_width)

        # self.move_outline(colrow)
        pygame.display.update()

        pygame.display.flip()
        return

    def draw_default_board(self, sector=None):
        self.screen.fill(bg_color)

        watermark = watermark_font.render(watermark_txt, info_aa, watermark_color)
        self.screen.blit(watermark, watermark_coords)

        # draw shadow behind active sector
        if sector is not None:
            # print(f"sector: {sector}")
            pygame.Surface.fill(self.screen, shadow_color, self.sectors_rects[sector])

        # rysowanie siatki
        self.draw_lines(line_quantity, line_width, line_color)
        self.draw_rects(line_quantity, self.tiles_rects, rect_diff)
        # print(self.tiles_pos)
        self.draw_lines(big_line_quantity, big_line_width, big_line_color)
        self.draw_rects(big_line_quantity, self.sectors_rects, rect_diff)
        pygame.display.flip()
        return

    # 9x9 <-> 3x3x3x3 translate function
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
        self.screen.blit(info, info_coords)
        pygame.display.flip()

    def refresh(self, written_symbols_dic, next_sector, msg=None, draw_board=None, change_cur=False):

        if change_cur:
            self.cursor_index += 1
            self.cursor_index %= len(self.cursors)
            pygame.mouse.set_cursor(self.cursors[self.cursor_index])

        # for sector in written_symbols_dic:
        #     print(f"{sector}: {written_symbols_dic[sector]}")

        # rysowanie tła
        # TODO: draw only important parts (bg only one time, thick lines only one time,
        #  bg color shadow to recently lightly shadowed sector)
        draw_board_start = time.time()
        if draw_board is None:
            if next_sector == (4, 4):
                next_sector = None
            # print(f"next sector: {next_sector}")
            self.draw_default_board(next_sector)
        else:
            # customowe rysownie
            draw_board()
        board_drawn_time = time.time()

        # draw outline
        # self.draw_symbol()

        # rysowanie symboli
        # TODO: make it so that max two sectors are being updated (thus checked), bg color shadow to the won sector
        symbols_drawing_start = time.time()
        counting = 0
        # there's about 17ms spared for one symbol, so after optimization, max refresh time should be around 306ms
        # which still is not satisfying, but it's not 700ms
        # (recorded highest is 812ms for move 61, but theoretically could be higher)
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
        symbols_drawing_end = time.time()

        # dev stuff
        board_drawing_time = round(((board_drawn_time - draw_board_start)*1000), 4)
        symbols_drawing_time = round(((symbols_drawing_end - symbols_drawing_start)*1000), 4)
        drawing_time = round(((symbols_drawing_end - draw_board_start)*1000), 4)

        # print(f'sec_name: {sec_name}|(col, row): {(col, row)}')
        # print(f'colrow: {colrow}')
        # print(f"tiles checked: {counting}")
        return board_drawing_time, symbols_drawing_time, drawing_time


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
