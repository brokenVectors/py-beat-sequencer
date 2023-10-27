import pygame
from math import *
from sequencer import Sequencer

running = True
square_size = 50
row_count = 4
col_count = 16
screen_size = (square_size * col_count, square_size * row_count + 100)

pygame.init()
pygame.mixer.pre_init()
pygame.display.set_caption("Beat Sequencer")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_size)
sequencer = Sequencer(row_count, col_count, square_size, clock)
font = pygame.font.SysFont("arialunicode", 24)
help_text = font.render('''↑: +5 BPM          ↓: -5 BPM         SPACE: Play/Pause''', True, (255,255,255))

delta_time = 0
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
    time_to_elapse = int(250/(sequencer.tempo/60))
    if sequencer.col_location % 2 == 1:
        time_to_elapse = time_to_elapse + time_to_elapse * (sequencer.swing_percentage / 100)
    if delta_time < time_to_elapse:
        delta_time += clock.get_time()
    elif sequencer.playing:
        sequencer.play_col()
        delta_time = 0
    screen.fill((0, 0, 0))
    sequencer.draw(screen)
    screen.blit(help_text, (0, square_size * row_count))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()