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

	# Change these as needed
	# Streaming frequency
	freq = 1600
	# Window Size, make sure its the same as in stream_data_wifi_high_speed.py
	window = 200

	def __init__(self):
		self.prevEMG = 0
		dirname = os.path.dirname(__file__)
		# make sure the motor is stopped by default
		filename = os.path.join(dirname, 'MotorControllerCode/haltMotor2').replace("\\","/")
		os.system(filename + " > /dev/null &")

	def processEMG(self, EMGSample):
		if self.calibrationPhase == "init":
			print "prepare to flex"
			self.calibrationPhase = "init2"

		if self.calibrationPhase == "init2":
			self.EMGBuffer.append(0)
			# wait 1 second
			if (len(self.EMGBuffer)>=self.freq/self.window):
				self.EMGBuffer = []
				print "FLEX!"
				self.calibrationPhase = "flex"

		if self.calibrationPhase == "flex":
			# Filters the given sample and appends it onto the buffer
			time = np.array([i*1.0/self.freq for i in range(self.window)])
			filteredEMG = filterEMG(time, EMGSample)
			self.EMGBuffer.append(np.std(filteredEMG))

			# Keep sampling for three seconds, and then take the mean of the samples
			# The mean is the average std deviation while flexing
			if (len(self.EMGBuffer)>self.freq*3/self.window):
				self.flexAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				print "Prepare to relax"
				self.calibrationPhase = "wait"

		if self.calibrationPhase == "wait":
			# Wait 1 second
			self.EMGBuffer.append(0)
			if (len(self.EMGBuffer)>=self.freq/self.window):
				self.EMGBuffer = []
				print "Relax"
				self.calibrationPhase = "relax"

		if self.calibrationPhase == "relax":
			# Filters the given samples and appends it onto the buffer
			time = np.array([i*1.0/self.freq for i in range(self.window)])
			filteredEMG = filterEMG(time, EMGSample)
			self.EMGBuffer.append(np.std(filteredEMG))

			# Keeps sampling for three seconds, and then takes the mean of all the filtered samples.
			# The mean is the average deviation while relaxed.
			if (len(self.EMGBuffer)>=self.freq*3/self.window):
				self.relaxAverage = np.mean(self.EMGBuffer)
				self.EMGBuffer = []
				# The activation threshold is set to the value between the flex average and the relax average.
				self.EMGThreshold = ((1.0*self.flexAverage + self.relaxAverage)/2.0)
				print self.EMGThreshold
				print "Done Calibration"
				self.calibrationPhase = "running"

		if self.calibrationPhase == "running":
			# The main routine that runs after the calibration has been completed
			time = np.array([i*1.0/self.freq for i in range(self.window)])
			# Filters the samples, then passes it to the intent processing function
			filteredEMG = filterEMG(time, EMGSample)
			decision = processIntentEMG(filteredEMG, self.prevEMG, self.EMGThreshold)

			# The desired behavior for the decision outcome
			if decision > 0 and self.prevEMG == 0:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, 'MotorControllerCode/initMotor2').replace("\\","/")
				os.system(filename + " > /dev/null &")
			elif decision == 0 and self.prevEMG > 0:
				dirname = os.path.dirname(__file__)
				filename = os.path.join(dirname, 'MotorControllerCode/haltMotor2').replace("\\","/")
				os.system(filename + " > /dev/null &")
			self.prevEMG = decision
			print decision>0
		return 0
