from signalGenerator import *
from filterEEG import *
from filterEMG import *
from processIntent import *
from FrameBuffer import FrameBuffer as fb

# file for testing different processing methods. currently set for EMG.

fb.loadData()
fb.setEMGWindowLength(40)

for i in range((len(fb.emgFromFile)/40)-1):
    emg, time = fb.getNextSample()
    emg_filtered = filterEMG(time, emg, sfreq=40, low_band=19, high_band=4, low_pass=2)
    decision = processIntentEMG(emg_filtered, fb.getBuffer())
    print decision
    print decision
