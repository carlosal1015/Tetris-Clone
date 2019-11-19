'''
mainGameState.py
'''
from assets.pyAssets import *
from gameStates import States
import pygame as pg
from pyShapes import *
from pyVariables import *
import random
from tetrisObjects import Block, Piece, Board

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.board = Board()
        self.piece_count = {'O':0,'I':0, 'S':0,'Z':0,'J':0,'L':0, 'T':0}
        self.shape_list = TETRIS_PIECES
        self.piece = Piece(vitals=random.choice(self.shape_list),
                           board_obj=self.board)
        self.update_piece_stats(self.piece.name)
        self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                board_obj=self.board)
        self.piece.spawn_piece()
        self.game_over = False
        self.high_score = 0


    def cleanup(self):
        print('cleaning up Game state stuff')

    def startup(self):
        print('starting Game state stuff')


    '''-----STATISTICS HUD-----'''
    def update_piece_stats(self, piece):
        self.piece_count[str(piece)] += 1

    def reset_piece_stats(self):
        for piece, value in self.piece_count.items():
            self.piece_count[piece] = 0

    def create_stat_pieces(self):
        stat_pieces = []
        for i in range(len(self.shape_list)):
            P = Piece(vitals=self.shape_list[i], board_obj=self.board)
            stat_pieces.append(P)

        return stat_pieces

    def display_stat_text(self, screen):
        font = pg.font.Font(PIXEL_FONT, 50)
        text = font.render('STATISTICS', True, WHITE)
        text_rect = text.get_rect(center=(STAT_TEXT_X, STAT_TEXT_Y))
        screen.blit(text, text_rect)

    def display_piece_values(self, screen):
        piece_stats = SHAPE_LIST
        for i in range(len(piece_stats)):
            font = pg.font.Font(PIXEL_FONT, 40)
            text = font.render(str(
                               self.piece_count[str(piece_stats[i])]).zfill(3),
                               True, WHITE)
            text_rect = text.get_rect(topleft=(STAT_X_VALUES,
                                      STAT_Y_VALUES + i*50))
            screen.blit(text,text_rect)

    def draw_piece_stats(self,screen):
        pg.draw.rect(screen, BLACK, (STAT_BOX_RECT))
        pieces = self.create_stat_pieces()
        for piece_num in range(len(pieces)):
            pieces[piece_num].draw_stat(screen, piece_num)

    '''-----SCORE BOARD-----'''
    def calculate_high_score(self):
        if self.board.points > self.high_score:
            self.high_score = self.board.points
        else:
            self.high_score = self.high_score

    def create_score_board(self, screen):
        pg.draw.rect(screen, BLACK, (SCORE_BOX_RECT))

    def display_score_text(self,screen):
        score_text = ('SCORE', str(self.board.points).zfill(6))
        x = SCORE_TEXT_X
        y = SCORE_TEXT_Y
        for i in range(len(score_text)):
            font = pg.font.Font(PIXEL_FONT, 60)
            text = font.render(score_text[i], True, WHITE)
            text_rect = text.get_rect(topleft=(x,y+i*40))
            screen.blit(text, text_rect)

    def display_high_score_text(self, screen):
        score_text = ('TOP', str(self.high_score).zfill(6))
        x = SCORE_TEXT_X
        y = SCORE_TEXT_Y - 90
        for i in range(len(score_text)):
            font = pg.font.Font(PIXEL_FONT, 60)
            text = font.render(score_text[i], True, WHITE)
            text_rect = text.get_rect(topleft=(x,y+i*40))
            screen.blit(text, text_rect)


    '''-----HEADS UP DISPLAY-----'''
    def display_lines(self, screen):
        pg.draw.rect(screen, BLACK, (LINE_BOX_RECT))
        font = pg.font.SysFont(None, 60)
        text = font.render('LINES - '+str(self.board.lines_cleared).zfill(3),
                          True, WHITE)
        text_rect = text.get_rect(center = (LINE_TEXT_COORD))
        screen.blit(text, text_rect)

    def display_statistics(self, screen):
        self.draw_piece_stats(screen)
        self.display_piece_values(screen)
        self.display_stat_text(screen)

    def display_score(self,screen):
        self.create_score_board(screen)
        self.display_score_text(screen)
        self.calculate_high_score()
        self.display_high_score_text(screen)



    def display_next_box(self, screen):
        pg.draw.rect(screen, BLACK, (NEXT_BOX_RECT))
        font = pg.font.SysFont(None, NEXT_TEXT_SIZE)
        text = font.render('NEXT', True, WHITE)
        text_rect = text.get_rect(center=(NEXT_TEXT_X, NEXT_TEXT_Y))
        screen.blit(text, text_rect)
        self.next_piece.draw_next(screen)

    def display_hud(self, screen):
        self.display_lines(screen)
        self.display_score(screen)
        self.display_next_box(screen)
        self.display_statistics(screen)

    def draw_tetris_board(self, screen):
        self.board.draw_board(screen)

    def game_over_check(self):
        if self.piece.valid_spawn == False:
            self.game_over = True

    def handle_game_over(self):
        self.next = 'gameover'
        self.done = True
        self.board.reset_board()
        self.piece = Piece(vitals=random.choice(self.shape_list),
                           board_obj=self.board)
        self.reset_piece_stats()
        self.update_piece_stats(self.piece.name)
        self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                board_obj=self.board)
        self.piece.spawn_piece()
        self.game_over = False



    def game_logic(self):
        if self.piece.landed == True:
            self.piece = self.next_piece
            self.update_piece_stats(self.piece.name)
            self.piece.spawn_piece()
            self.next_piece = Piece(vitals=random.choice(self.shape_list),
                                    board_obj=self.board)
            self.game_over_check()
            if self.game_over == True:
                self.handle_game_over()
            self.piece.landed = False
            self.piece.check_collision()


    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            self.next = 'pause'
            self.done = True
        elif event.type == pg.KEYDOWN:
            self.piece.movement_controls(event)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)
        self.piece.check_collision()
        self.game_logic()


    def draw(self, screen):
        screen.fill((LAVENDER_MIST))
        self.board.draw_board(screen)
        self.piece.draw_piece(screen)
        self.display_hud(screen)
