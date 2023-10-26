import pygame
from math import *
from sequencer import Sequencer
from sequencer import BEATEVENT

running = True
square_size = 50
row_count = 4
col_count = 16
screen_size = (square_size * col_count, square_size * row_count)

pygame.init()
pygame.mixer.pre_init()
pygame.display.set_caption("Beat Sequencer")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_size)
sequencer = Sequencer(row_count, col_count, square_size, clock)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = floor(mouse_pos[1] / square_size)
            col = floor(mouse_pos[0] / square_size)
            sequencer.set(row, col, 1 if sequencer.get(row, col) == 0 else 0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sequencer.set_tempo(sequencer.tempo - 5)
            elif event.key == pygame.K_UP:
                sequencer.set_tempo(sequencer.tempo + 5)
            elif event.key == pygame.K_SPACE:
                if sequencer.playing:
                    sequencer.stop()
                else:
                    sequencer.play()
        elif event.type == BEATEVENT:
            sequencer.play_col()
    screen.fill((0,0,0))
    sequencer.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()