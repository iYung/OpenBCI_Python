from signalGenerator import *
from filterEEG import *
from filterEMG import *
from processIntent import *
from FrameBuffer import FrameBuffer as fb

# eeg, time = getEEGSample()
# eeg_filtered = filterEEG(time, eeg, low_pass=3, sfreq=200, high_band=25, low_band=7)
# for i in range((len(eeg_filtered)/20)-1):
#     print bandpower(eeg_filtered[i:i+20], 200, 8,30)
# for value in eeg_filtered:
#     print value


fb.loadData()
fb.setEMGWindowLength(40)

for i in range((len(fb.emgFromFile)/40)-1):
    emg, time = fb.getNextSample()
    emg_filtered = filterEMG(time, emg, sfreq=40, low_band=19, high_band=4, low_pass=2)
    decision = processIntentEMG(emg_filtered, fb.getBuffer())
    print decision
    print decision
