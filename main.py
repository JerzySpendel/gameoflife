import pygame
from pygame.locals import *
import sys
import copy
import random

pygame.init()
BLOCK_SIZE = BLOCK_W, BLOCK_H = (8, 8)
BLOCKS = BLOCKS_IN_W, BLOCKS_IN_H = 68*2, 35*2
size = width, height = (BLOCK_W*BLOCKS[0], BLOCK_H*BLOCKS[1])
screen = pygame.display.set_mode(size)


class ChessBoard:
    stopped = False

    def __init__(self, screen):
        self.screen = screen
        self.cells = []
        for _ in range(BLOCKS_IN_W):
            cel = [False]*BLOCKS_IN_H
            self.cells.append(cel)
        self._random()

    def _random(self):
        for x in range(BLOCKS_IN_W):
            for y in range(BLOCKS_IN_H):
                if random.choice([True, False]):
                    self.cells[x][y] = True

    def change_state(self):
        self.stopped = not self.stopped

    def click_at(self, pos):
        if self.stopped:
            x, y = pos
            block_x, block_y = x // BLOCK_W, y // BLOCK_H
            self.cells[block_x][block_y] = not self.cells[block_x][block_y]

    def draw_net(self):
        color = (0, 0, 200)
        for i in range(BLOCKS_IN_W):
            start_pos = (i*BLOCK_W, 0)
            end_pos = (i*BLOCK_W, height)
            pygame.draw.line(self.screen, color, start_pos, end_pos, 1)
        for i in range(BLOCKS_IN_H):
            start_pos = (0, i*BLOCK_H)
            end_pos = (width, i*BLOCK_H)
            pygame.draw.line(self.screen, color, start_pos, end_pos, 1)

    def draw_cells(self):
        for x in range(BLOCKS_IN_W):
            for y in range(BLOCKS_IN_H):
                if self.cells[x][y]:
                    xx, yy = x*BLOCK_W, y*BLOCK_H
                    r = pygame.Rect([xx+1, yy+1, BLOCK_W-1, BLOCK_H-1])
                    pygame.draw.rect(self.screen, (255, 255, 255), r)

    def border_with(self, point):
        borders = 0
        x, y = point
        points = ((x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1),
                  (x, y-1), (x+1, y-1))
        for xx, yy in points:
            try:
                if 0 <= xx < BLOCKS_IN_W and 0 <= yy < BLOCKS_IN_H:
                    if self.cells[xx][yy]:
                        borders += 1
                else:
                    continue
            except IndexError:
                pass
        return borders

    def next_step(self):
        if self.stopped:
            return
        cells = copy.deepcopy(self.cells)
        for x in range(BLOCKS_IN_W):
            for y in range(BLOCKS_IN_H):
                borders = self.border_with((x, y))
                if not self.cells[x][y]:
                    if borders == 3:
                        cells[x][y] = True
                elif self.cells[x][y]:
                    if not 2 <= borders <= 3:
                        cells[x][y] = False
        self.cells = cells

chess = ChessBoard(screen)
clock = pygame.time.Clock()
i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                chess.change_state()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            chess.click_at(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    chess.draw_net()
    chess.draw_cells()
    pygame.display.flip()
    chess.next_step()
    clock.tick(2)
