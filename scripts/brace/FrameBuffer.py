import numpy as np
from processIntent import processIntentEMG, processIntentEEG
from signalGenerator import *

class FrameBuffer(object):
    frameBuffer = np.zeros(1)
    frameBufferEEG = np.zeros(0)
    emgFromFile = []
    eegFromFile = []
    timeFromFile = []
    eegTimeFromFile = []
    currentIndex = 0
    emgWindowLength = 200
    eegWindowLength = 200
    fromFile = True

    @staticmethod
    def getBuffer():
        return FrameBuffer.frameBuffer

    @staticmethod
    def getBufferEEG():
        return FrameBuffer.frameBufferEEG

    @staticmethod
    def setEMGWindowLength(x):
        FrameBuffer.emgWindowLength = x

    @staticmethod
    def addElement(x):
        FrameBuffer.frameBuffer = np.concatenate([[x], FrameBuffer.frameBuffer[:-1]])

    @staticmethod
    def addEEGBuffer(x):
        FrameBuffer.frameBufferEEG = np.concatenate([[x], FrameBuffer.frameBufferEEG[:-1]])

    @staticmethod
    def loadData():
        FrameBuffer.emgFromFile, FrameBuffer.timeFromFile = getRealSample()
        FrameBuffer.eegFromFile, FrameBuffer.eegTimeFromFile = getEEGSample()

    @staticmethod
    def getNextSample():
        emg = FrameBuffer.emgFromFile[0:FrameBuffer.emgWindowLength]
        if FrameBuffer.fromFile:
            FrameBuffer.emgFromFile = np.concatenate([FrameBuffer.emgFromFile[FrameBuffer.emgWindowLength:],FrameBuffer.emgFromFile[0:FrameBuffer.emgWindowLength]])
        time = np.array([i*1.0/FrameBuffer.emgWindowLength for i in range(0, len(emg), 1)])

        return np.array(emg).astype(np.float), time

    @staticmethod
    def getNextEEGSample():
        eeg = FrameBuffer.eegFromFile[0:FrameBuffer.eegWindowLength]
        if FrameBuffer.fromFile:
            FrameBuffer.eegFromFile = np.concatenate([FrameBuffer.eegFromFile[FrameBuffer.eegWindowLength:],FrameBuffer.eegFromFile[0:FrameBuffer.eegWindowLength]])
        time = np.array([i*1.0/FrameBuffer.eegWindowLength for i in range(0, len(eeg), 1)])

        return np.array(eeg).astype(np.float), time