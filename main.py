import pygame
from math import *
from sequencer import Sequencer

LEFT_BUTTON = 1
RIGHT_BUTTON = 3
SCROLL_UP = 4
SCROLL_DOWN = 5
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

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

while running:
    mouse_pos = pygame.mouse.get_pos()
    row = floor(mouse_pos[1] / square_size)
    col = floor(mouse_pos[0] / square_size)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= row < sequencer.row_count and 0 <= col < sequencer.col_count:
                if event.button == SCROLL_UP:
                    sequencer.set(row, col, clamp(sequencer.get(row,col) + 0.1, 0, 1))
                elif event.button == SCROLL_DOWN:
                    sequencer.set(row, col, clamp(sequencer.get(row,col) - 0.1, 0, 1))
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
    left, _, right = pygame.mouse.get_pressed()
    if left:
        sequencer.set(row, col, 1)
    elif right:
        sequencer.set(row, col, 0)
    time_to_elapse = int(250/(sequencer.tempo/60))
    is_odd_column = sequencer.col_location % 2 == 1
    if is_odd_column:
        time_to_elapse = time_to_elapse + time_to_elapse * (sequencer.swing_percentage / 100)
    if delta_time < time_to_elapse:
        delta_time += clock.get_time()
    elif sequencer.playing: # if all the required time has elapsed, and the sequencer is set to play
        sequencer.play_col()
        delta_time = 0
    screen.fill((0, 0, 0))
    sequencer.draw(screen)
    screen.blit(help_text, (0, square_size * row_count))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()