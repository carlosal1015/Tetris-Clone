'''
mainGameState.py
'''

from gameStates import States
import pygame as pg
from pyVariables import *
import random
from tetrisObjects import Block, Piece, Board

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.board = Board()
        self.shape_list = TETRIS_PIECES
        self.piece = Piece(shape=BLOCK_PIECE[0])
        self.next_piece = Piece(shape=BLOCK_PIECE[0])

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')

    def display_score(self, screen):
        font = pg.font.SysFont(None, 40)
        text = font.render('Lines: '+str(self.board.lines_cleared), True, BLACK)
        text_rect = text.get_rect(topleft = (0,0))
        screen.blit(text, text_rect)

    def game_logic(self):
        if self.piece.landed == True:
            self.piece = self.next_piece
            self.next_piece = Piece(shape=BLOCK_PIECE[0])
            self.piece.landed = False
            self.piece.check_collision(self.board)
            self.board.print_board()


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.piece.movement_controls(event, self.board)
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)
        self.piece.check_collision(self.board)
        self.game_logic()


    def draw(self, screen):
        screen.fill((WHITE2))
        self.board.draw_board(screen)
        self.piece.draw_piece(screen)
        self.display_score(screen)
