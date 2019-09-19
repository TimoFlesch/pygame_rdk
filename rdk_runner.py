# random dot motion kinematogram
# timo flesch, 2019


# import matplotlib.pyplot as plt
# from array2gif import write_gif

import rdktools.rdk_params as params
from rdktools.rdk_experiment import set_trials, TrialSequence




def main():
    trials = set_trials(n_reps=params.DOT_REPETITIONS,
                        angles=params.DOT_ANGLES)
    trial_seq = TrialSequence()
    for ii, thisAngle in enumerate(trials):
        frames = trial_seq.run(thisAngle)

    quit()


if __name__ == "__main__":
    main()
