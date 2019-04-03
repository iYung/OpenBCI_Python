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
	freq = 800
	window = 200

	def __init__(self):
		self.prevEMG = 0
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, 'MotorControllerCode/haltMotor').replace("\\","/")
		os.system(filename + " > /dev/null &")

	def processEMG(self, EMGSample):
		if self.calibrationPhase == "init":

			print "prepare to flex"
			self.calibrationPhase = "init2"

		if self.calibrationPhase == "init2":
			self.EMGBuffer.append(0)
			if (len(self.EMGBuffer)>=self.freq/self.window):
				self.EMGBuffer = []
				print "FLEX!"
				self.calibrationPhase = "flex"

		if self.calibrationPhase == "flex":
			time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample)
			self.EMGBuffer.append(np.std(filteredEMG))
			# print out the mean for the previous 3 seconds
			if (len(self.EMGBuffer)>self.freq*3/self.window):
				self.flexAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				print "Prepare to relax"
				self.calibrationPhase = "wait"

		if self.calibrationPhase == "wait":
			self.EMGBuffer.append(0)
			if (len(self.EMGBuffer)>=self.freq/self.window):
				self.EMGBuffer = []
				print "Relax"
				self.calibrationPhase = "relax"

		if self.calibrationPhase == "relax":
			time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample)
			self.EMGBuffer.append(np.std(filteredEMG))

			# print out the mean for the previous 3 seconds
			if (len(self.EMGBuffer)>=self.freq*3/self.window):
				self.relaxAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				self.EMGThreshold = ((1.0*self.flexAverage + self.relaxAverage)/2.0)
				print self.EMGThreshold
				print "Done Calibration"
				self.calibrationPhase = "running"

		if self.calibrationPhase == "running":
			time = np.array([i*0.1 for i in range(100)])
			filteredEMG = filterEMG(time, EMGSample)
			decision = processIntentEMG(filteredEMG, self.prevEMG, self.EMGThreshold)

			if decision > 0 and self.prevEMG == 0:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, 'MotorControllerCode/initMotor').replace("\\","/")
				os.system(filename + " > /dev/null &")
			elif decision == 0 and self.prevEMG > 0:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, 'MotorControllerCode/haltMotor').replace("\\","/")
				os.system(filename + " > /dev/null &")
			self.prevEMG = decision
			#print decision>0
		return 0