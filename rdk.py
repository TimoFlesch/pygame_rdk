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

# dot parameters
N_DOTS = 100         # max num of simultaneously displayed dots
DOT_SIZE = 3         # size in pixels
DOT_SPEED = 5        # speed in pixels per frame
DOT_DIRECITON = 90   # direcion in degrees
DOT_COHERENCE = 100  # motion coherence in percent
DOT_COLOR = COL_WHITE

# aperture parameters
APERTURE_RADIUS = 200       # radius in pixels
APERTURE_WIDTH = 4         # line width in pixels
APERTURE_COLOR = COL_WHITE

# fixation parameters
FIX_SIZE = (40, 40)     # width and height of fix cross
FIX_COLOR = COL_WHITE


class Experiment(object):
    """initialises screen and loops through fixation and stimulus pairs"""

    def __init__(self, arg):
        self.arg = arg

    def show_fixation():
        pass

    def show_rdk():
        pass

    def hide_all():
        pass

    def run_trial():
        # loop through content of trial (as defined by parameter vect)
        pass


class RDK(object):
    """represents a random dot stimulus"""

    def __init__(self, arg):
        self.arg = arg


class Aperture(object):
    """a circular aperture"""

    def __init__(self, arg):
        super(Aperture, self).__init__()
        self.arg = arg


class Fixation(object):
    """a fixation cross"""

    def __init__(self, arg):
        super(Fixation, self).__init__()
        self.arg = arg
