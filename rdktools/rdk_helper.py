# random dot motion kinematogram
# timo flesch, 2019


import random
import numpy as np
from math import cos, sin, atan2, radians, degrees



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
