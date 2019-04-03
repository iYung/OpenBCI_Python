import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import time
import timeit

# Filters a sampled EMG signal


def filterEMG(time, emg, sfreq=800, low_band=50, high_band=15, low_pass=10):
    # create bandpass filter for EMG
    high_band = high_band/(1.0*sfreq/2)
    low_band = low_band/(1.0*sfreq/2)
    b, a = sp.signal.butter(4, [high_band, low_band], btype='bandpass')
    emg_bandpassed = sp.signal.filtfilt(b, a, emg)

    #simulating a notch filter
    #this is the lower freq part of it
    high_band1 = 0/(1.0*sfreq/2)
    low_band1 = 58/(1.0*sfreq/2)
    b1, a1 = sp.signal.butter(5, [high_band1, low_band1], btype='bandpass')
    #this is the higher freq part of it
    high_band2 = 62/(1.0*sfreq/2)
    low_band2 = sfreq/(1.0*sfreq/2)
    b1, a1 = sp.signal.butter(5, [high_band2, low_band2], btype='bandpass')

    # b1, a1 = signal.iirnotch(60, 30, sfreq)
    # normalize the signal
    #emg_norm = [i / 500.0 for i in emg]

    emg_filtered = sp.signal.filtfilt(b, a, emg_bandpassed) + sp.signal.filtfilt(b, a, emg_bandpassed)
    # emg_bandpass = sp.signal.filtfilt(b, a, emg)
    # emg_notch_low = sp.signal.filtfilt(b1, a1, emg_bandpass)
    # return emg_filtered
    return emg_filtered
