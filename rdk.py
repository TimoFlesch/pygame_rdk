# random dot motion kinematogram
# timo flesch, 2019


import pygame
from pygame.locals import *
import random
import numpy as np
from math import cos, sin, atan2, radians, degrees
import time
import matplotlib.pyplot as plt
from array2gif import write_gif

# basic parameters
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 250
WINDOW_NAME = "Random Dot Kinematogram"

COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)


# time
TICK_RATE = 60
TIME_FIX = 20  # frames
TIME_ISI = 30
TIME_RDK = 60
TIME_ITI = 60

# dot parameters
N_DOTS = 200         # max num of simultaneously displayed dots
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
FIX_SIZE = (15, 15)  # width and height of fix cross
FIX_COLOR = COL_WHITE
FIX_WIDTH = 4  # line width


def polar2cartesian(phi, r):
    """ helper function. converts polar coordinates to cartesian coordinates"""
    phi_radians = radians(phi)
    x = r*cos(phi_radians)
    y = r*sin(phi_radians)
    return x, y


def cartesian2polar(x, y):
    """ helper function. converts cartesian to polar coordinates"""
    r = (x**2+y**2)**.5
    phi = atan2(y, x)
    return phi, r


def set_trials(n_reps=10, angles=[0, 90, 135], shuff=True):
    """ creates vector of all motion directions """
    all_trials = np.array([])

    for thisAngle in angles:
        all_trials = np.append(all_trials, np.repeat(thisAngle, n_reps),
                                axis=0)

    if shuff:
        random.shuffle(all_trials)

    return all_trials


class RandDot(pygame.sprite.Sprite):
    """ implements a single random dot. """

    def __init__(self, display, centre,
                radius=random.randint(0, APERTURE_RADIUS),
                motiondir=180):
        super(RandDot, self).__init__()
        self.surf = pygame.Surface((DOT_SIZE, DOT_SIZE))
        self.surf.fill((DOT_COLOR))
        self.centre = centre
        self.angle = random.randint(0, 360)
        self.radius = radius
        self.speed = DOT_SPEED
        self.coherence = DOT_COHERENCE
        if random.random() < self.coherence:
            self.motiondir = motiondir
        else:
            self.motiondir = random.randint(0, 360)
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
        self.angle, self.radius = cartesian2polar(self.rect.x - self.centre[0],
                                    self.rect.y - self.centre[1])

    def reset_pos(self):
        self.angle = self.motiondir - 180 + random.randint(-90, 90)
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
        self.ndots = N_DOTS
        self.maxrad = APERTURE_RADIUS-DOT_SIZE
        self.duration = TIME_RDK
        self.dots = pygame.sprite.Group()
        self.motiondir = motiondir
        self.dots = self.sample_dots(self.maxrad, self.ndots)
        self.clock = pygame.time.Clock()
        # self.fix = Fixation(self.display)

    def draw(self):
        # draws dots
        for dot in self.dots:
            dot.draw()

    def show(self):
        allframes = np.zeros((self.duration, WINDOW_WIDTH, WINDOW_HEIGHT))
        ii = 0
        while self.duration > 0:
            self.clock.tick(TICK_RATE)
            self.display.fill(COL_BLACK)
            # self.fix.draw()
            self.draw()
            pygame.display.update()
            frame = self.collect_frame()
            frame = frame.astype('float32')
            frame *= (255.0/frame.max())
            allframes[ii, :, :] = frame
            ii += 1
            self.duration -= 1
            self.update()
        self.duration = TIME_RDK
        self.hide()
        return allframes

    def update(self):
        # updates position of dots
        for dot in self.dots:
            dot.move()

    def hide(self):
        self.display.fill(COL_BLACK)
        pygame.display.update()

    def new_sample(self, angle):
        self.motiondir = angle
        self.dots = self.sample_dots(self.maxrad, self.ndots)

    def sample_dots(self, maxrad, ndots):
        # use weighted sampling distribution to avoid
        # dots clustering close to centre of screen:
        weights = np.arange(maxrad)/sum(np.arange(maxrad))
        radii = np.random.choice(maxrad, ndots, p=weights)
        dots = pygame.sprite.Group()
        [dots.add(RandDot(self.display, self.centre, radii[ii],
                            self.motiondir)) for ii in range(ndots)]
        return dots

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,
                            (WINDOW_WIDTH, WINDOW_HEIGHT), 'RGB')
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
                        [self.centre[0] - self.f_size[0], self.centre[1]],
                        [self.centre[0] + self.f_size[0], self.centre[1]],
                        self.f_width)

        self.fix_y = pygame.draw.line(self.display, self.f_col,
                        [self.centre[0], self.centre[1] - self.f_size[1]],
                        [self.centre[0], self.centre[1] + self.f_size[1]],
                        self.f_width)

        self.aperture = pygame.draw.circle(self.display, self.a_col,
                        self.centre, self.a_size, self.a_width)

    def show(self):
        pygame.display.flip()
        allframes = np.zeros((self.f_duration, WINDOW_WIDTH, WINDOW_HEIGHT))
        ii = 0
        while self.f_duration > 0:
            self.clock.tick(TICK_RATE)
            self.draw()
            pygame.display.flip()
            frame = self.collect_frame()
            frame = frame.astype('float32')
            frame *= (255.0/frame.max())
            allframes[ii, :, :] = frame
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
        string_image = pygame.image.tostring(self.display, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,
                        (WINDOW_WIDTH, WINDOW_HEIGHT), 'RGB')
        return pygame.surfarray.array2d(temp_surf)


class BlankScreen(object):
    """displays a blank screen. returns an n-D array of all displayed frames"""

    def __init__(self, display, time=TIME_ITI):
        self.display = display
        self.duration = time
        self.duration_init = time
        self.clock = pygame.time.Clock()

    def show(self):
        self.display.fill(COL_BLACK)
        allframes = np.zeros((self.duration, WINDOW_WIDTH, WINDOW_HEIGHT))
        ii = 0
        while self.duration > 0:
            self.clock.tick(TICK_RATE)
            pygame.display.update()
            frame = self.collect_frame()
            frame = frame.astype('float32')
            frame *= (255.0/frame.max())
            allframes[ii, :, :] = frame
            ii += 1
            self.duration -= 1
        self.duration = self.duration_init
        return allframes

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,
                             (WINDOW_WIDTH, WINDOW_HEIGHT), 'RGB')
        return pygame.surfarray.array2d(temp_surf)


class TrialSequence(object):
    """defines the sequence of events within a trial.
       returns a n-D matrix with all displayed frames as greyscale images (2D)
    """

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
        frames_iti = self.iti.show()

        return np.concatenate((frames_fix, frames_rdk, frames_iti), axis=0)


def main():
    trials = set_trials(n_reps=DOT_REPETITIONS, angles=DOT_ANGLES)
    # trial_seq = TrialSequence()
    # allframes = np.array([])
    # for ii, thisAngle in enumerate(trials[0:5]):
    #     frames = trial_seq.run(thisAngle)
    #     allframes = np.concatenate((allframes,frames),axis=0) if len(allframes) else frames

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    display.fill(COL_BLACK)
    rdk = RDK(display)

    rdk.new_sample(20)
    frames = rdk.show()
    pygame.quit()
    # print(allframes.shape)
    frame_list = [np.squeeze(np.stack((frames[ii,:,:],) * 3, axis=0)) for ii in range(frames.shape[0])]

    # print(len(frame_list))
    # print(frame_list[0].shape)
    # print(np.max(frame_list[0]))
    # print(np.min(frame_list[0]))
    write_gif(list(frame_list),'smallandmany.gif',fps=60)


    quit()


if __name__ == "__main__":
    main()
