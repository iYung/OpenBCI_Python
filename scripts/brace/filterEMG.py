import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import time
import timeit

# Filters a sampled EMG signal


def filterEMG(time, emg, sfreq=1600, low_band=50, high_band=15, low_pass=10):

    # Notch filter at 60Hz
    b1, a1 = sp.signal.iirnotch(60, 30, sfreq)
    emg_notched = sp.signal.filtfilt(b1, a1, emg)


    # create bandpass filter, runs the notch filtered signal through it
    high_band = high_band/(1.0*sfreq/2)
    low_band = low_band/(1.0*sfreq/2)
    b, a = sp.signal.butter(4, [high_band, low_band], btype='bandpass')
    emg_bandpassed = sp.signal.filtfilt(b, a, emg_notched)

    return emg_bandpassed
