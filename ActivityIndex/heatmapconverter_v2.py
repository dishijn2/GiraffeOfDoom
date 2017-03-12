import pickle
import constants as k

# load pickle file and return the min-max array
def loadpickle(file):
    try:
        dataarray = pickle.load(open(file, "rb"))
        # print("Loaded values from file")
    except:
        dataarray = []
        print("No minmax file to load. Creating values of zero")

    return dataarray


# save array to pickle file. Prints a result
def savepickle(array, file):
    try:
        pickle.dump(array, open(file, "wb"))
        print("Save ok")
    except:
        print("ERROR saving array")


# return the median value of an list
# the array is a list of single values
# this function could also be used to reset a large array to a seed value as part of a periodic
# pruning process to manage the size of the arrays.
def findarraymedian(array):
    if len(array) > 2:
        medpoint = int(len(array) / 2)
    else:
        medpoint = 0

    if medpoint == k.NULLBIN:
        medianvalue = 0
    else:
        medianvalue = array[medpoint]

    return medianvalue


# find min and max values in a list
def findarraymin(array):
    values = []
    for item in array:
        if item == k.NULLBIN:
            item = 0
        dp = float(item)
        values.append(dp)

    values.sort()
    minvalue = values[0]

    if minvalue == k.NULLBIN:
        minvalue = 0

    return minvalue


def findarraymax(array):
    values = []
    for item in array:
        if item == k.NULLBIN:
            item = 0

        dp = float(item)
        values.append(dp)

    values.sort()
    values.reverse()
    maxvalue = values[0]

    if maxvalue == k.NULLBIN:
        maxvalue = 0

    return maxvalue

# this is the functon that will scale the data according to the _median_ max and min values. It will return
# a list
def heatmapprocess(maxv, minv, array):
    returnarray = []

    window = maxv - minv

    # If we have sufficient max and min values to calculate a meaningful result
    if window != 0:
        # then calculate values....
        for item in array:
            if item != k.NULLBIN:
                dp = float(item) - minv
                dp = dp / window
                returnarray.append(dp)
            else:
                returnarray.append(k.NULLBIN)
    else:
        print("ERROR: window value is too small: " + str(window))

    # for item in array:
    #     dp = str(item) + "," + str(minv) + "," + str(maxv)
    #     returnarray.append(dp)

    return returnarray


# wrapper function to run this library. Called from the main script
def main(livedata):
    # minmax only contains 2 values: [minv, maxv]. These are the highest and lowest recorded results to date. These
    # are appended to the max and min arrays and form the long-term "memory" of highest and lowest values for the
    # device. Outlier data will be appended the should be missed when grabbing the median value
    minmax = loadpickle("minmax.pkl")
    print("LIVE LOW & HIGH: " + str(minmax))

    # get the current max and min values from the live data. if the minmax array is empty, then start with
    # whatever minmax values we can find
    if len(minmax) == 0:
        d = findarraymin(livedata)
        minmax.append(d)
        d = findarraymax(livedata)
        minmax.append(d)
    # Otherwise compare current stored values with live. The assumption is larger values than stored are valid...
    else:
        livemin = findarraymin(livedata)
        # print("Live MIN is " + str(livemin))
        if livemin <= minmax[0]:
            minmax[0] = livemin

        livemax = findarraymax(livedata)
        # print("Live MAX is " + str(livemax))
        if livemax >= minmax[1]:
            minmax[1] = livemax

    maxvalue = minmax[1]
    minvalue = minmax[0]
    heatmaparray = heatmapprocess(maxvalue, minvalue, livedata)

    savepickle(minmax, "minmax.pkl")

    return heatmaparray