from FrameBuffer import FrameBuffer
from filterEMG import filterEMG
import numpy as np
from processIntent import *
import os

class SignalProcessor:
	prevEMG = 0
	EMGBuffer= []
	calibrationPhase = "init"
	flexAverage = 0
	relaxAverage = 0
	EMGThreshold = 0

	def __init__(self):
		self.prevEMG = 0

	def processEMG(self, EMGSample):
		if self.calibrationPhase == "init":
			print "prepare to flex"
			self.calibrationPhase == "init2"

		if self.calibrationPhase == "init2":
			self.EMGBuffer.append(0)
			if (len(self.EMGBuffer)>=16):
				self.EMGBuffer = []
				print "FLEX!"
				self.calibrationPhase = "flex"

		if self.calibrationPhase == "flex":
			time = time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample, sfreq=100, low_band=49, high_band=10, low_pass=5)
			self.EMGBuffer.append(np.std(filteredEMG))
			# print out the mean for the previous 3 seconds
			if (len(self.EMGBuffer)>=48):
				self.flexAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				print "Prepare to relax"
				self.calibrationPhase = "wait"

		if self.calibrationPhase == "wait":
			self.EMGBuffer.append(0)
			if (len(self.EMGBuffer)>=16):
				self.EMGBuffer = []
				self.calibrationPhase = "relax"

		if self.calibrationPhase == "relax":
			time = time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample, sfreq=100, low_band=49, high_band=10, low_pass=5)
			self.EMGBuffer.append(np.std(filteredEMG))
			# print out the mean for the previous 3 seconds
			if (len(self.EMGBuffer)>=48):
				self.relaxAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				self.EMGThreshold = ((self.flexAverage + self.relaxAverage)/2)
				print "Done Calibration"
				self.calibrationPhase = "running"

		if self.calibrationPhase == "running":
			time = time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample, sfreq=100, low_band=49, high_band=10, low_pass=5)
			decision = processIntentEMG(filteredEMG, self.prevEMG, self.EMGThreshold)
			self.prevEMG = decision
			if decision == 1:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, '../EPOS_Linux_Library/examples/HelloEposCmd/initMotor')
				os.system(filename)
			else:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, '../EPOS_Linux_Library/examples/HelloEposCmd/haltMotor')
				os.system(filename)
			return decision
		return 0

	def calibrateEMG(self, EMGSample):
		time = time = np.array([i*0.1 for i in range(100)])
		filteredEMG = filterEMG(time, EMGSample, sfreq=100, low_band=49, high_band=10, low_pass=5)
		self.EMGBuffer.append(np.std(filteredEMG))

		# print out the mean for the previous 3 seconds
		if (len(self.EMGBuffer)>=48):
			print np.mean(self.EMGBuffer)
			self.EMGBuffer = []