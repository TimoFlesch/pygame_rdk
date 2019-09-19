# random dot motion kinematogram
# timo flesch, 2019

import pygame
from pygame.locals import *
import random
import numpy as np
import rdktools.rdk_params as params

from rdktools.rdk_stimuli import RDK, Fixation, BlankScreen


def set_trials(n_reps=10, angles=[0, 90, 135], shuff=True):
    """ creates vector of all motion directions """
    all_trials = np.array([])

    for thisAngle in angles:
        all_trials = np.append(all_trials, np.repeat(thisAngle, n_reps),
                                axis=0)

    if shuff:
        random.shuffle(all_trials)

    return all_trials


class TrialSequence(object):
    """defines the sequence of events within a trial.
       returns a n-D matrix with all displayed frames as greyscale images (2D)
    """

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((params.WINDOW_WIDTH,
                            params.WINDOW_HEIGHT))
        pygame.display.set_caption(params.WINDOW_NAME)
        self.display.fill(params.COL_BLACK)
        self.rdk = RDK(self.display)
        self.fix = Fixation(self.display)
        self.iti = BlankScreen(self.display, params.TIME_ITI)

    def run(self, trial=90):
        frames_fix = self.fix.show()
        self.rdk.new_sample(trial)
        frames_rdk = self.rdk.show()
        frames_iti = self.iti.show()

        return np.concatenate((frames_fix, frames_rdk, frames_iti), axis=0)
