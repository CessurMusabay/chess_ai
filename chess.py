import pygame
import sys
from colors import Colors
from chess_piece import Rook, King, Pawn, Queen, Bishop, Knight
from pygame.time import Clock


class Chess:
    def __init__(self):
        self.square_width = 100
        self.size = (self.square_width * 8, self.square_width * 8)
        self.screen = pygame.display.set_mode(self.size)
        self.is_white_turn = True
        self.clock = Clock()
        self.state = [
            [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False),
             Rook(False)],
            [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
            [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
        ]
        self.piece = None
        self.next_steps = []
        self.dead = []

    def draw_tile(self, pos, color, is_index=False):
        if is_index:
            pos = pos[1] * 100 + 25, pos[0] * 100 + 25
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill(color)
            self.screen.blit(surface, pos)
        else:
            pygame.draw.rect(self.screen, color, (pos, (100, 100)))

    def draw_table(self):
        draw = False
        for left in range(0, 800, 100):
            draw = not draw
            for top in range(0, 800, 100):
                if draw:
                    self.draw_tile((left, top), Colors.silver)
                    draw = False
                else:
                    draw = True

    def draw_pieces(self):
        for x in range(0, 8):
            for y in range(0, 8):
                piece = self.state[x][y]
                if piece != None:
                    self.screen.blit(piece.img, (y * 100 + 18, x * 100 + 18))

    def draw_next_steps(self):
        for step in self.next_steps:
            self.draw_tile(step, Colors.n_step, is_index=True)

    def move(self, i=None, j=None):

        if i is None:
            pos = pygame.mouse.get_pos()
            x, y = pos
            i, j = y // 100, x // 100

        piece = self.state[i][j]
        pos = (i, j)
        if piece is not None:
            if (self.piece is not None) and (pos in self.next_steps):
                old_i, old_j = self.piece

                # dead
                self.dead.append(self.state[old_i][old_j])
                self.state[i][j] = None

                self.state[i][j] = self.state[old_i][old_j]
                self.state[old_i][old_j] = None

                self.piece = None
                self.next_steps = []
                self.is_white_turn = not self.is_white_turn
            else:  # choose

                if piece.is_white == self.is_white_turn:
                    self.piece = pos
                    self.next_steps = piece.next_steps((i, j), self.state)

        else:
            if self.piece is not None and pos in self.next_steps:
                old_i, old_j = self.piece
                self.state[i][j] = self.state[old_i][old_j]
                self.state[old_i][old_j] = None
                self.piece = None
                self.next_steps = []
                self.is_white_turn = not self.is_white_turn

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.move()

            self.screen.fill(Colors.coffee)
            self.draw_table()
            self.draw_pieces()
            self.draw_next_steps()

            pygame.display.flip()

