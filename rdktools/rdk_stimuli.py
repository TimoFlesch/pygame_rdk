# random dot motion kinematogram
# timo flesch, 2019


import pygame
from pygame.locals import *
import random
import numpy as np
from math import cos, sin, atan2, radians, degrees
import matplotlib.pyplot as plt
from array2gif import write_gif

import rdktools.rdk_params as params
from rdktools.rdk_helper import polar2cartesian, cartesian2polar


class Fixation(object):
    """implements a fixation cross"""

    def __init__(self, display,
                    win_width=params.WINDOW_WIDTH,
                    win_height=params.WINDOW_HEIGHT,
                    f_col=params.FIX_COLOR,
                    f_width=params.FIX_WIDTH,
                    f_size=params.FIX_SIZE,
                    f_duration=params.TIME_FIX,
                    a_col=params.APERTURE_COLOR,
                    a_size=params.APERTURE_RADIUS,
                    a_width=params.APERTURE_WIDTH,
                    win_colour=params.WINDOW_COLOUR,
                    tick_rate=params.TICK_RATE):
        self.display = display
        self.win_width = win_width
        self.win_height = win_height
        self.win_colour = win_colour
        self.centre = [self.win_width//2, self.win_height//2]
        self.f_col = f_col
        self.f_width = f_width
        self.f_size = f_size
        self.f_duration = f_duration
        self.f_duration_init = f_duration
        self.a_col = a_col
        self.a_size = a_size
        self.a_width = a_width
        self.tick_rate = tick_rate
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
        allframes = np.zeros((self.f_duration, self.win_width, self.win_height))
        ii = 0
        while self.f_duration > 0:
            self.clock.tick(self.tick_rate)
            self.draw()
            pygame.display.flip()
            frame = self.collect_frame()
            frame = frame.astype('float32')
            frame *= (255.0/frame.max())
            allframes[ii, :, :] = frame
            ii += 1
            self.f_duration -= 1
        self.f_duration = self.f_duration_init
        self.hide()
        return allframes

    def wait(self):
        time.sleep(self.f_duration)

    def hide(self):
        self.display.fill(self.win_colour)
        pygame.display.update()

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,
                        (self.win_width, self.win_height), 'RGB')
        return pygame.surfarray.array2d(temp_surf)



class RDK(object):
    """implements a random dot stimulus"""

    def __init__(self, display,
                motiondir=180,
                win_width=params.WINDOW_WIDTH,
                win_height=params.WINDOW_HEIGHT,
                n_dots=params.N_DOTS,
                win_colour=params.WINDOW_COLOUR,
                dot_colour=params.DOT_COLOR,
                dot_size=params.DOT_SIZE,
                dot_speed=params.DOT_SPEED,
                duration=params.TIME_RDK,
                dot_coherence=params.DOT_COHERENCE,
                aperture_radius=params.APERTURE_RADIUS,
                radius=random.randint(0, params.APERTURE_RADIUS),
                tick_rate=params.TICK_RATE):
        self.display = display
        self.win_width = win_width
        self.win_height = win_height
        self.win_colour = win_colour
        self.centre = [win_width//2, win_height//2]
        self.aperture_radius = aperture_radius
        self.ndots = n_dots
        self.dot_size = dot_size
        self.duration_init = duration
        self.duration = duration
        self.angle = random.randint(0,360)
        self.radius = radius
        self.max_radius = self.aperture_radius - self.dot_size
        self.dot_speed = dot_speed
        self.dot_colour = dot_colour
        self.tick_rate = tick_rate
        self.coherence = dot_coherence
        if random.random() < self.coherence:
            self.motiondir = motiondir
        else:
            self.motiondir = random.randint(0, 360)

        self.dots = pygame.sprite.Group()
        self.dots = self.sample_dots(self.max_radius, self.ndots)
        self.clock = pygame.time.Clock()
        self.fix = Fixation(self.display)

    def draw(self):
        # draws dots
        for dot in self.dots:
            dot.draw()

    def show(self):
        allframes = np.zeros((self.duration, self.win_width, self.win_height))
        ii = 0
        while self.duration > 0:
            self.clock.tick(self.tick_rate)
            self.display.fill(self.win_colour)
            self.fix.draw()
            self.draw()
            pygame.display.update()
            frame = self.collect_frame()
            frame = frame.astype('float32')
            frame *= (255.0/frame.max())
            allframes[ii, :, :] = frame
            ii += 1
            self.duration -= 1
            self.update()
        self.duration = self.duration_init
        self.hide()
        return allframes

    def update(self):
        # updates position of dots
        for dot in self.dots:
            dot.move()

    def hide(self):
        self.display.fill(self.win_colour)
        pygame.display.update()

    def new_sample(self, angle):
        self.motiondir = angle
        self.dots = self.sample_dots(self.max_radius, self.ndots)

    def sample_dots(self, max_radius, ndots):
        # use weighted sampling distribution to avoid
        # dots clustering close to centre of screen:
        weights = np.arange(max_radius)/sum(np.arange(max_radius))
        radii = np.random.choice(max_radius, ndots, p=weights)
        dots = pygame.sprite.Group()
        [dots.add(RandDot(self.display, self.centre, radius=radii[ii],
                            motiondir=self.motiondir,
                            dot_colour=self.dot_colour,
                            dot_size=self.dot_size,
                            dot_speed=self.dot_speed,
                            dot_coherence=self.coherence,
                            aperture_radius=self.aperture_radius
                            )) for ii in range(ndots)]
        return dots

    def collect_frame(self):
        string_image = pygame.image.tostring(self.display, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,
                            (self.win_width, self.win_height), 'RGB')
        return pygame.surfarray.array2d(temp_surf)


class BlankScreen(object):
    """displays a blank screen. returns an n-D array of all displayed frames"""

    def __init__(self, display, time=params.TIME_ITI,
                    win_width=params.WINDOW_WIDTH,
                    win_height=params.WINDOW_HEIGHT,
                    win_colour=params.WINDOW_COLOUR,
                    tick_rate=params.TICK_RATE):
        self.display = display
        self.duration = time
        self.duration_init = time
        self.win_width = win_width
        self.win_height = win_height
        self.win_colour = win_colour
        self.tick_rate = tick_rate
        self.clock = pygame.time.Clock()

    def show(self):
        self.display.fill(self.win_colour)
        allframes = np.zeros((self.duration, self.win_width, self.win_height))
        ii = 0
        while self.duration > 0:
            self.clock.tick(self.tick_rate)
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
                             (self.win_width, self.win_height), 'RGB')
        return pygame.surfarray.array2d(temp_surf)



class RandDot(pygame.sprite.Sprite):
    """ implements a single random dot. """

    def __init__(self, display, centre,
                dot_colour=params.DOT_COLOR,
                dot_size=params.DOT_SIZE,
                dot_speed=params.DOT_SPEED,
                dot_coherence=params.DOT_COHERENCE,
                aperture_radius=params.APERTURE_RADIUS,
                radius=random.randint(0, params.APERTURE_RADIUS),
                motiondir=180):
        super(RandDot, self).__init__()
        self.dot_size = dot_size
        self.dot_colour = dot_colour
        self.surf = pygame.Surface((self.dot_size, self.dot_size))
        self.surf.fill((self.dot_colour))
        self.centre = centre
        self.angle = random.randint(0,360)
        self.radius = radius
        self.max_radius = aperture_radius-dot_size
        self.dot_speed = dot_speed
        self.coherence = dot_coherence
        if random.random() < self.coherence:
            self.motiondir = motiondir
        else:
            self.motiondir = random.randint(0, 360)
        self.x_0, self.y_0 = polar2cartesian(self.angle, self.radius)
        self.dx, self.dy = polar2cartesian(self.motiondir, self.dot_speed)
        self.rect = self.surf.get_rect(center=(self.x_0 + self.centre[0],
                                        self.y_0 + self.centre[1]))
        self.display = display

    def move(self):
        if self.radius >= self.max_radius:
            self.reset_pos()
        self.x_0 += self.dx
        self.y_0 += self.dy
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.angle, self.radius = cartesian2polar(self.rect.x - self.centre[0],
                                    self.rect.y - self.centre[1])

    def reset_pos(self):
        self.angle = self.motiondir - 180 + random.randint(-90, 90)
        self.radius = self.max_radius
        self.x_0, self.y_0 = polar2cartesian(self.angle, self.radius)
        self.rect.x = self.x_0 + self.centre[0]
        self.rect.y = self.y_0 + self.centre[1]

    def draw(self):
        self.surf.fill(self.dot_colour)
        self.display.blit(self.surf, self.rect)
