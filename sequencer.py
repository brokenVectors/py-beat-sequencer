import numpy as np
import pygame
row_colours = [
    (234, 196, 53),
    (52, 89, 149),
    (3, 206, 164),
    (251, 77, 61)
]
def clamp(n, smallest, largest): return max(smallest, min(n, largest))
class Sequencer:
    # TODO: Make a version of the beat sequencer with a basic piano roll
    # TODO: Add an export feature (use the wave module)
    def __init__(self, row_count, col_count, square_size, clock, tempo=120):
        self.playing = False
        self.square_size = square_size
        self.row_count = row_count
        self.col_count = col_count
        self.col_location = 0
        self.tempo = 120
        self.swing_percentage = 90
        self.clock = clock
        self.beats = np.zeros([row_count, col_count])
        self.row_sounds = [
            pygame.mixer.Sound("sounds/hat.wav"),
            pygame.mixer.Sound("sounds/clap.wav"),
            pygame.mixer.Sound("sounds/snare.wav"),
            pygame.mixer.Sound("sounds/kick.wav"),
        ]
        self.channels = [
            pygame.mixer.Channel(0),
            pygame.mixer.Channel(1),
            pygame.mixer.Channel(2),
            pygame.mixer.Channel(3),
        ]
    def set(self, row, col, value):
        self.beats[row][col] = value
    def get(self, row, col):
        return self.beats[row][col]
    def draw(self, surface):
        for row in range(0, self.row_count):
            for col in range(0, self.col_count):
                value = self.get(row, col)
                if value > 0:
                    color = (row_colours[row][0] * value, row_colours[row][1] * value, row_colours[row][2] * value)
                elif col % 4 == 0:
                    color = (20, 20, 20)
                else:
                    color = (0,0,0)
                if col == self.col_location:
                    color = (clamp(color[0] + 100, 0, 255), clamp(color[1] + 100, 0, 255), clamp(color[2] + 100, 0, 255))
                pygame.draw.rect(surface, color, pygame.Rect(col*self.square_size,row*self.square_size,self.square_size,self.square_size))
    def play_col(self):
        for row in range(0, self.row_count):
            value = self.get(row, self.col_location)
            if value > 0:
                self.row_sounds[row].set_volume(1.0 * value)
                self.channels[row].play(self.row_sounds[row])
        if self.col_location < self.col_count - 1:
            self.col_location = self.col_location + 1
        else:
            self.col_location = 0
    def play(self):
        self.playing = True
    def stop(self):
        self.playing = False
    def set_tempo(self, tempo):
        self.tempo = tempo
        self.play()
    def set_swing_percentage(self, swing):
        self.swing_percentage = swing