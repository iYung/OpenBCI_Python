import numpy as np

# given a filtered EMG signal, determines whether or not the brace should move
def processIntentEMG(filteredSignal, frameBuffer, moveThres):
    # if the mean signal is above moveThres, the brace should move
    stanadardDeviation = np.std(filteredSignal)
    if (stanadardDeviation > moveThres):
        #print 1
        return 1
    elif frameBuffer == 1:
        #print 1
        return 2
    else:
        # print 0
        return 0

# given a filtered EEG signal, determines whether or not the brace should move
def processIntentEEG(filteredSignal, frameBuffer):
    hjorthVal = hjorth(filteredSignal)

    if (hjorthVal < 1.06):
        return 1
    elif 1 in frameBuffer:
        return 2
    else:
        return 0

def hjorth(a):
    first_deriv = np.diff(a)
    second_deriv = np.diff(a,2)

    var_zero = np.mean(a ** 2)
    var_d1 = np.mean(first_deriv ** 2)
    var_d2 = np.mean(second_deriv ** 2)

    activity = var_zero
    mobility = np.sqrt(var_d1 / var_zero)
    complexity = np.sqrt(var_d2 / var_d1) / mobility

    return complexity
    # Change the return variable to select which Hjorth param is returned
    # return activity, mobility, complexity