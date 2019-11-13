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
        self.piece = Piece(vitals=random.choice(self.shape_list),
                           board_obj=self.board)
        self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                board_obj=self.board)
        self.piece.spawn_piece()
        self.game_over = False

    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')

    def display_score(self, screen):
        font = pg.font.SysFont(None, 40)
        text = font.render('Lines: '+str(self.board.lines_cleared), True, BLACK)
        text_rect = text.get_rect(topleft = (0,0))
        screen.blit(text, text_rect)

    def display_next_box(self, screen):
        font = pg.font.SysFont(None, NEXT_TEXT_SIZE)
        text = font.render('NEXT', True, BLACK)
        text_rect = text.get_rect(center=(NEXT_TEXT_X, NEXT_TEXT_Y))
        screen.blit(text, text_rect)
        self.next_piece.draw_next(screen)

    def game_over_check(self):
        if self.piece.valid_spawn == False:
            self.game_over = True

    def handle_game_over(self):
        print('Handling game over')
        self.board.reset_board()
        self.piece = Piece(vitals=random.choice(self.shape_list),
                           board_obj=self.board)
        self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                board_obj=self.board)
        self.piece.spawn_piece()
        self.game_over = False



    def game_logic(self):
        if self.piece.landed == True:
            self.piece = self.next_piece
            self.piece.spawn_piece()
            self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                    board_obj=self.board)
            self.game_over_check()
            if self.game_over == True:
                self.handle_game_over()
            self.piece.landed = False
            self.piece.check_collision()
            self.board.print_board()


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.piece.movement_controls(event)
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)
        self.piece.check_collision()
        self.game_logic()


    def draw(self, screen):
        screen.fill((WHITE2))
        self.board.draw_board(screen)
        self.piece.draw_piece(screen)
        self.display_next_box(screen)
        self.display_score(screen)
