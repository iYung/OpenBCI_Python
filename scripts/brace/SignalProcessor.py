from FrameBuffer import FrameBuffer
from filterEMG import filterEMG
import numpy as np
from processIntent import *

class SignalProcessor:
	prevEMG = [0]

	def __init__(self):
		self.prevEMG = [0]

	def processEMG(self, EMGSample):
		time = time = np.array([i*0.1 for i in range(100)])
		filteredEMG = filterEMG(time, EMGSample, sfreq=len(EMGSample), low_band=(len(EMGSample)/2) - 1, high_band=len(EMGSample)/10, low_pass=len(EMGSample)/20)
		decision = processIntentEMG(EMGSample, self.prevEMG)
		prevEMG = [decision]
		print(decision)
		return decision
