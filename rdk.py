# random dot motion kinematogram
# timo flesch, 2019
# todo

import pygame
from pygame.locals import *
import random
import numpy as np
from math import cos, sin, atan2, radians, degrees
import time
import matplotlib.pyplot as plt

# basic parameters
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 250
WINDOW_NAME = "Random Dot Kinematogram"

COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)

TICK_RATE = 60

# time
TIME_FIX = 60  # frames
TIME_ISI = 30
TIME_RDK = 60
TIME_ITI = 120

# dot parameters
N_DOTS = 100         # max num of simultaneously displayed dots
DOT_SIZE = 3         # size in pixels
DOT_SPEED = 4        # speed in pixels per frame
DOT_ANGLES = [0, 45, 90, 112, 240, 315]  # motion directions
DOT_REPETITIONS = 5  # how many repetitions of same trials?
DOT_COHERENCE = 1  # motion coherence (between 0 and 1)
DOT_COLOR = COL_WHITE

# aperture parameters
APERTURE_RADIUS = 100       # radius in pixels
APERTURE_WIDTH = 4         # line width in pixels
APERTURE_COLOR = COL_WHITE

# fixation parameters
FIX_SIZE = (15, 15)     # width and height of fix cross
FIX_COLOR = COL_WHITE
FIX_WIDTH = 4  # line width


def polar2cartesian(phi, r):
    phi_radians = radians(phi)
    x = r*cos(phi_radians)
    y = r*sin(phi_radians)
    return x, y


def cartesian2polar(x, y):
    r = (x**2+y**2)**.5
    phi = atan2(y, x)
    return phi, r


def set_trials(n_reps=10, angles=[0, 90, 135], shuff=True):
    """ creates vectors with trial indices and motion directions """
    all_trials = np.array([])

    for thisAngle in angles:
        print(thisAngle)
        all_trials = np.append(all_trials, np.repeat(thisAngle, n_reps), axis=0)

    if shuff:
        random.shuffle(all_trials)

    return all_trials


class RandDot(pygame.sprite.Sprite):

    def __init__(self, display, centre,
                radius=random.randint(0, APERTURE_RADIUS),
                motiondir=180):
        super(RandDot, self).__init__()
        self.surf = pygame.Surface((DOT_SIZE, DOT_SIZE))
        self.surf.fill((DOT_COLOR))
        self.centre = centre
        self.angle = random.randint(0, 360)
        self.radius = radius
        # TODO make trial specific
        self.speed = DOT_SPEED
        self.coherence = DOT_COHERENCE
        if random.random() < self.coherence:
            self.motiondir = motiondir
        else:
            self.motiondir = random.randint(0,360)
        self.x_0, self.y_0 = polar2cartesian(self.angle, self.radius)
        self.dx, self.dy = polar2cartesian(self.motiondir, self.speed)
        self.rect = self.surf.get_rect(center=(self.x_0 + self.centre[0],
                        self.y_0 + self.centre[1]))
        self.display = display

    def move(self):
        if self.radius >= APERTURE_RADIUS-DOT_SIZE:
            self.reset_pos()
        self.x_0 += self.dx
        self.y_0 += self.dy
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.angle, self.radius = cartesian2polar(self.rect.x-self.centre[0],
                                    self.rect.y-self.centre[1])

    def reset_pos(self):
        self.angle = self.motiondir - 180 + random.randint(-90,90)
        self.radius = APERTURE_RADIUS-DOT_SIZE
        self.x_0, self.y_0 = polar2cartesian(self.angle, self.radius)
        self.rect.x = self.x_0 + self.centre[0]
        self.rect.y = self.y_0 + self.centre[1]

    def draw(self):
        self.surf.fill(COL_WHITE)
        self.display.blit(self.surf, self.rect)


class RDK(object):
    """implements a random dot stimulus"""

    def __init__(self, display, motiondir=180):
        self.display = display
        self.centre = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
        self.ndots  = N_DOTS
        self.maxrad = APERTURE_RADIUS-DOT_SIZE
        self.duration = TIME_RDK
        self.dots = pygame.sprite.Group()
        self.motiondir = motiondir
        self.dots = self.sample_dots(self.maxrad, self.ndots)
        self.clock = pygame.time.Clock()
        self.fix = Fixation(self.display)

    def draw(self):
        # draws dots
        # self.hide()
        for dot in self.dots:
            dot.draw()

    def show(self):
        allframes = np.zeros((self.duration,WINDOW_WIDTH,WINDOW_HEIGHT))
        ii = 0
        while self.duration > 0:
            self.clock.tick(TICK_RATE)
            self.display.fill(COL_BLACK)
            self.fix.draw()
            self.draw()
            pygame.display.update()
            allframes[ii,:,:] = self.collect_frame()
            ii += 1
            self.duration -= 1
            self.update()
        self.duration = TIME_RDK
        self.hide()
        return allframes


    def update(self):
        # updates position of dots
        for dot in self.dots:
            # dot.hide()
            dot.move()
            # dot.show()

    def hide(self):
        self.display.fill(COL_BLACK)
        pygame.display.update()

    def wait(self):
        time.sleep(self.duration)

    def new_sample(self, angle):
        self.motiondir = angle
        self.dots = self.sample_dots(self.maxrad, self.ndots)

    def sample_dots(self, maxrad, ndots):
        # use weighted sampling distribution to avoid overpresence of
        # dots close to centre of screen:
        weights = np.arange(maxrad)/sum(np.arange(maxrad))
        radii = np.random.choice(maxrad, ndots, p=weights)
        dots = pygame.sprite.Group()
        [dots.add(RandDot(self.display, self.centre, radii[ii], self.motiondir))
                for ii in range(ndots)]
        return dots

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display,'RGB')
        temp_surf = pygame.image.fromstring(string_image,(WINDOW_WIDTH, WINDOW_HEIGHT),'RGB')
        return pygame.surfarray.array2d(temp_surf)


class Fixation(object):
    """implements a fixation cross"""

    def __init__(self, display):
        self.display = display
        self.centre = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
        self.f_col = FIX_COLOR
        self.f_width = FIX_WIDTH
        self.f_size = FIX_SIZE
        self.f_duration = TIME_FIX
        self.a_col = APERTURE_COLOR
        self.a_size = APERTURE_RADIUS
        self.a_width = APERTURE_WIDTH
        self.clock = pygame.time.Clock()

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

    def show(self):
        pygame.display.flip()
        allframes = np.zeros((self.f_duration,WINDOW_WIDTH,WINDOW_HEIGHT))
        ii = 0
        while self.f_duration > 0:
            self.clock.tick(TICK_RATE)
            self.draw()
            pygame.display.flip()
            allframes[ii,:,:] = self.collect_frame()
            ii += 1
            self.f_duration -= 1
        self.f_duration = TIME_FIX
        self.hide()
        return allframes

    def wait(self):
        time.sleep(self.f_duration)

    def hide(self):
        self.display.fill(COL_BLACK)
        pygame.display.update()

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display,'RGB')
        temp_surf = pygame.image.fromstring(string_image,(WINDOW_WIDTH, WINDOW_HEIGHT),'RGB')
        return pygame.surfarray.array2d(temp_surf)


class BlankScreen(object):
    """docstring for BlankScren."""

    def __init__(self, display, time=TIME_ITI):
        self.display = display
        self.duration = time
        self.duration_init = time
        self.clock = pygame.time.Clock()

    def show(self):
        self.display.fill(COL_BLACK)
        allframes = np.zeros((self.duration,WINDOW_WIDTH,WINDOW_HEIGHT))
        ii = 0
        while self.duration > 0:
            self.clock.tick(TICK_RATE)
            pygame.display.update()
            allframes[ii:,:] = self.collect_frame()
            ii += 1
            self.duration -= 1
        self.duration = self.duration_init

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display,'RGB')
        temp_surf = pygame.image.fromstring(string_image,(WINDOW_WIDTH, WINDOW_HEIGHT),'RGB')
        return pygame.surfarray.array2d(temp_surf)


class TrialSequence(object):
    "docstring for TrialSequence."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_NAME)
        self.display.fill(COL_BLACK)
        self.rdk = RDK(self.display)
        self.fix = Fixation(self.display)
        self.iti = BlankScreen(self.display, TIME_ITI)

    def run(self, trial=90):
        frames_fix = self.fix.show()
        self.rdk.new_sample(trial)
        frames_rdk = self.rdk.show()
        self.iti.show()
        # todo return frames from each funct above, stitched together as
        # single matrix
        return frames_fix,frames_rdk


def main():
    # define trials
    trials = set_trials(n_reps=DOT_REPETITIONS, angles=DOT_ANGLES)
    trial_seq = TrialSequence()
    # _,frames_rdk = trial_seq.run(trials[0])
    # plt.imshow(frames_rdk[0,:,:])
    # plt.show()
    for ii, thisAngle in enumerate(trials):
        trial_seq.run(thisAngle)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
