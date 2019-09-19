# basic parameters
COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)


WINDOW_WIDTH = 250
WINDOW_HEIGHT = 250
WINDOW_NAME = "Random Dot Kinematogram"
WINDOW_COLOUR = COL_BLACK



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
