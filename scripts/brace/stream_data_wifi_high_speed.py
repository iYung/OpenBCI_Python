from __future__ import print_function
import sys

sys.path.append('..')  # help python find cyton.py relative to scripts folder
from openbci import wifi as bci
import SignalProcessor as SP
import thread

def printData(sample):
    print(sample.sample_number)
    print(sample.channel_data)

class State:
    def __init__(self):
        self.sp = SP.SignalProcessor()
        self.bicep = []

    def update(self, sample):
        if len(sample.channel_data) > 3:
            self.bicep.append(sample.channel_data[1])
        # Make sure the window size here is the same as in SignalProcessor.py
        if len(self.bicep) >= 200:
            thread.start_new_thread( self.sp.processEMG, (self.bicep, ) )
            self.bicep = []

if __name__ == '__main__':
    state = State()
    shield = bci.OpenBCIWiFi(ip_address='192.166.0.2', log=True, high_speed=True)
    shield.set_sample_rate(1600)
    shield.start_streaming(state.update)
    shield.loop()