
import random
import numpy as np


# Collection of functions used to generate sample signals, or read them from
# text files

fileNames = [
    "EMG2sec.txt",
    "normalFlexRelease-4-sec.txt",
    "record.csv_2019-1-15_21-48-27.txt"
]

selectedFile = fileNames[1]

# Generates a signal with three zones, each zone is either high or low
def getSampleOne():

    # for testing purposes, generates random emg signals that are either high or low
    emg = []
    quiet = np.random.uniform(-0.05, 0.05, 25) + 0.08
    burst = np.random.uniform(-1, 1, 25) + 0.08
    for index in range(0, 4):
        if (random.randint(0,2) == 1):
            emg = np.concatenate([emg, burst])
        else:
            emg = np.concatenate([emg, quiet])
    time = np.array([i*1.0/1000.0 for i in range(0, len(emg), 1)])

    return emg, time

def getSampleTwo():
    emg = []
    size = 0.0
    for index in range(0,25):
        chanceOfBigJump = random.randint(0,5)
        if (random.randint(0,2)==1):
            if (chanceOfBigJump == 0):
                if (size <= 0.5):
                    size = size + 0.5
                else:
                    size = 0.9;
            if (size<1.0):
               size = size + 0.1
        else:
            if (chanceOfBigJump == 0):
                if (size >= 0.5):
                    size = size - 0.5
                else:
                    size = 0.1;
            if (size > 0.0):
                size = size - 0.1
        signalSection = np.random.uniform(-size, size, 4) + 0.08
        emg = np.concatenate([emg, signalSection])
    time = np.array([i*1.0/1000.0 for i in range(0, len(emg), 1)])

    return emg, time

def getRealSample():
    # 1= tricep, 2 = bicep, 3/4 are EEG
    emg = []
    file_object = open(selectedFile, "r")
    lines = file_object.readlines()
    for line in lines:
        items = line.split(",")
        emg = emg + [items[1]]
    time = np.array([i*1.0/200.0 for i in range(0, len(emg), 1)])

    return np.array(emg).astype(np.float), time

def getEEGSample():
    eeg = []
    file_object = open(selectedFile, "r")
    lines = file_object.readlines()
    for line in lines:
        items = line.split(", ")
        eeg = eeg + [items[3]]
    time = np.array([i*1.0/200.0 for i in range(0, len(eeg), 1)])

    return np.array(eeg).astype(np.float), time

# emg, time = getRealSample()
# print max(abs(emg))