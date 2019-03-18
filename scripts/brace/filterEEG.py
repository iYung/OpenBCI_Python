import numpy as np
import scipy as sp
import scipy
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import time
import timeit
import pyrem as pr

def bandpower(x, fs, fmin, fmax):
    f, Pxx = scipy.signal.periodogram(x, fs=fs)
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    return scipy.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


#Filters a sampled EEG signal
def filterEEG(time, eeg, low_pass=10, sfreq=200, high_band=30, low_band=8):

    # create bandpass filter for EEG
    high_band = high_band/(1.0*sfreq/2)
    low_band = low_band/(1.0*sfreq/2)
    b, a = sp.signal.butter(4, [low_band,high_band], btype='bandpass')

    #eeg_correctmean = eeg - np.mean(eeg)
    eeg_norm = [(i-50) /250.0 for i in eeg]

    # eeg_filtered = sp.signal.filtfilt(b, a, eeg)
    eeg_filtered = sp.signal.filtfilt(b, a, eeg)

    # eeg_hfd = hjorth(eeg_filtered)
    # print "mobility: " + str(eeg_hfd)
    # print "signal: " + str(eeg_filtered)

    # eeg_ifft = np.fft.fft(eeg_filtered)
    # eeg_real = np.real(eeg_ifft)

    #print eeg_real
    # eeg_rectified = abs(eeg_real)

    # low_pass = 1.0*low_pass/(1.0*sfreq)
    # b2, a2 = sp.signal.butter(4, low_pass, btype="lowpass")
    # eeg_envelope = sp.signal.filtfilt(b2,a2, eeg_rectified)

    return eeg_filtered
