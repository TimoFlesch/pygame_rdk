# random dot motion kinematogram
import pygame
from pygame.locals import *
import random
import numpy as np
import time

# basic parameters
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_NAME = "Random Dots"

COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)

# time
TIME_FIX = 1  # seconds
TIME_RDK = 1
TIME_ITI = 2

# dot parameters
N_DOTS = 100         # max num of simultaneously displayed dots
DOT_SIZE = 3         # size in pixels
DOT_SPEED = 5        # speed in pixels per frame
DOT_ANGLES = [90, 180]  # motion directions
DOT_REPETITIONS = 5  # how many repetitions of same trials?
DOT_COHERENCE = 100  # motion coherence in percent
DOT_COLOR = COL_WHITE

# aperture parameters
APERTURE_RADIUS = 200       # radius in pixels
APERTURE_WIDTH = 4         # line width in pixels
APERTURE_COLOR = COL_WHITE

# fixation parameters
FIX_SIZE = (15, 15)     # width and height of fix cross
FIX_COLOR = COL_WHITE
FIX_WIDTH = 4 # line width


def set_trials(n_reps=10, angles=[0, 90, 135], shuff=True):
    """ creates vectors with trial indices and motion directions """
    all_trials = np.array([])
    for ang in angles:
        all_trials = np.append(all_trials, np.repeat(ang, n_reps), axis=0)
        # n = np.arange(1, len(all_trials)+1)

        if shuff:
            random.shuffle(all_trials)
            # all_trials = np.concatenate((all_trials[np.newaxis, :],
            #             n[np.newaxis, :]), axis=0)
            return all_trials


class RDK(object):
    """implements a random dot stimulus"""

    def __init__(self, display):
        self.display = display

    def draw(self):
        # draws dots
        pass

    def update(self):
        # updates position of dots
        pass
        

class Fixation(object):
    """implements a fixation cross"""

    def __init__(self, display):
        self.display = display
        self.centre = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]
        self.f_col = FIX_COLOR
        self.f_width = FIX_WIDTH
        self.f_size = FIX_SIZE
        self.a_col = APERTURE_COLOR
        self.a_size = APERTURE_RADIUS
        self.a_width = APERTURE_WIDTH

    def draw(self):
        # draw aperture and and fixation cross
        self.fix_x = pygame.draw.line(self.display, self.f_col,
                        [self.centre[0]-self.f_size[0], self.centre[1]],
                        [self.centre[0]+self.f_size[0], self.centre[1]],
                        self.f_width)

        self.fix_y = pygame.draw.line(self.display, self.f_col,
                        [self.centre[0], self.centre[1]-self.f_size[1]],
                        [self.centre[0], self.centre[1]+self.f_size[1]],
                        self.f_width)

        self.aperture = pygame.draw.circle(self.display, self.a_col,
                        self.centre, self.a_size, self.a_width)


def main():

    pygame.init()
    clock = pygame.time.Clock()

    # init screen
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    display.fill(COL_BLACK)
    # init new experiment (fixation and stimulus)
    rdk = RDK(display)
    fix = Fixation(display)

    # define trials
    trials = set_trials(n_reps=DOT_REPETITIONS, angles=DOT_ANGLES)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fix.draw()
        pygame.display.flip()
        print("tick " + str(pygame.time.get_ticks()))
        clock.tick(1)
    #
    # # loop through trials
    # for ii, angle in enumerate(trials):
    #     # randomise dots
    #     rdk.randomise()
    #
    #     # show fixation
    #     fix.draw()
    #
    #     time.sleep(TIME_FIX)
    #     # show RDK
    #     # rdk.draw(angle)
    #     # time.sleep(TIME_RDK)
    #
    #     # show ITI
    #     display.fill(COL_BLACK)
    #     time.sleep(TIME_ITI)
    #     # run at 60pfs
    #     # clock.tick(60)
    #     pass

    time.sleep(2)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
