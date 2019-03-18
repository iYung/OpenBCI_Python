import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import time
import timeit

# Filters a sampled EMG signal
def filterEMG(time, emg, low_pass=10, sfreq=200, high_band=20, low_band=99):
    # create bandpass filter for EMG
    high_band = high_band/(1.0*sfreq/2)
    low_band = low_band/(1.0*sfreq/2)
    b, a = sp.signal.butter(4, [high_band, low_band], btype='bandpass')
    # normalize the signal
    emg_norm = [i / 500.0 for i in emg]

    emg_filtered = sp.signal.filtfilt(b, a, emg_norm)
    return emg_filtered
