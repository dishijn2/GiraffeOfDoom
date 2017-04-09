import pickle
import constants as k
from datetime import datetime
import os


# load pickle file and return the min-max array
def loadpickle(file):
    try:
        dataarray = pickle.load(open(file, "rb"))
        # print("Loaded values from file")
    except:
        dataarray = []
        print("No file to load. Creating values of zero")

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

# append output to a file.
def fileoutput(texttowrite, filename):
    try:
        with open(filename, 'a') as f:
            f.write(texttowrite + "\n")
    except IOError:
        print("WARNING: There was a problem")

def createcolour(value):
    A_MDRT = 0.21
    A_ACTV = 0.70
    if value == k.NULLBIN:
        value = 0

    # quiet - Blue
    if value < A_MDRT:
        red = 0
        green = 0
        blue = 255

    # moderate - Orange
    if value >= A_MDRT and value < A_ACTV:
        red = 255
        green = 118
        blue = 17

    # Red Alert!
    if value >= A_ACTV:
        red = 250
        green = 0
        blue = 0

    rd = 255 - ((value) * (255 - red))
    gr = 255 - ((value) * (255 - green))
    bl = 255 - ((value) * (255 - blue))

    # Based on the value (0, quiet; 1 active) adjust the colours so that least activity will be ffffff
    # and most activity will be the supplied colour.
    # Convert decimal values to hex
    rd = str(hex(int(rd)))
    rd = rd.split("x")
    if len(rd[1]) == 1:
        rd = "0" + str(rd[1])
    else:
        rd = str(rd[1])

    gr = str(hex(int(gr)))
    gr = gr.split("x")
    if len(gr[1]) == 1:
        gr = "0" + str(gr[1])
    else:
        gr = str(gr[1])

    bl = str(hex(int(bl)))
    bl = bl.split("x")
    if len(bl[1]) == 1:
        bl = "0" + str(bl[1])
    else:
        bl = str(bl[1])

    # create hex colour string
    finalhex = str(rd) + str(gr) + str(bl)
    # print(finalhex)
    return finalhex


def htmlcreate(array, dateminmaxvalues):
    htmlfile = k.OUTPUTFILE
    try:
        os.remove(htmlfile)
    except OSError:
        print("WARNING: could not delete " + htmlfile)

    fileoutput('<table style="border-radius: 3px; width: 95%; font-size: 0.6em; background-color: #e0f0e0">', htmlfile)

    fileoutput("<tr>", htmlfile)


    for i in range(0, len(array)):
        c1 = '<td style="border-radius: 3px; text-align: center; padding: 2px; background-color: #'
        c2 = '">'
        hexcode = createcolour(array[i])
        c3 = c1 + hexcode + c2
        fileoutput(c3, htmlfile)

        # cell content
        dp = str(array[i])
        dp = dp[:4]
        hr = 23 - i

        if hr == 1:
            hr = "now<b>"
        else:
            hr = str(hr) + " hr<b>"
        cellstring = str(hr) + "</b>"
        # cellstring = str(hr) + '<br>' + str(dp) + '</b>'
        fileoutput(str(cellstring), htmlfile)

        fileoutput("</td>", htmlfile)

    c1 = '<td style="border-radius: 3px; text-align: center; padding: 2px;">'
    c2 = '</td>'
    c3 = c1 + k.STATION_NAME + c2
    fileoutput(c3, htmlfile)

    fileoutput("</tr>", htmlfile)

    fileoutput("</table>", htmlfile)
    currentdt = datetime.utcnow().strftime('%B %d %Y - %H:%M')
    bestmin = dateminmaxvalues[0].strftime('%B %d %Y - %H:%M')
    bestmax = dateminmaxvalues[1].strftime('%B %d %Y - %H:%M')
    # info = "<i>Best min: " + str(bestmin) + " UTC. Best max: " + str(bestmax) +" UTC. </i>  "
    info = ""
    stringtxt = 'Last updated at ' + str(currentdt) + " UTC.   "
    stringtxt = '<div style="font-size: 0.7em;">' + stringtxt + info + '<div>'
    fileoutput(stringtxt, htmlfile)


def getmax(maxvalue):
    maxes = loadpickle("maxvalues.pkl")


    savepickle(maxes, "maxvalues.pkl")

def getmin(minvalue):
    mins = loadpickle("minvalues.pkl")

    savepickle(mins, "minvalues.pkl")

# wrapper function to run this library. Called from the main script
def main(livedata):
    # check the current min/max values from the live data _for_this_24_hour_period_
    currentminvalue = findarraymin(livedata)
    currentmaxvalue = findarraymax(livedata)
    currentdatetime = currentdt = datetime.utcnow()

    # load the current values from the pickle files
    # workingvalues
    # of the format [datetime, minvalue],[datetime, maxvalue]
    workingvalues = loadpickle("workingminmax.pkl")

    #Determine if our current max and min values have changed, if so then append the the correct arrays and get the
    # median values back. This will help ignore blips and over time, will trend to moderate values
    if currentmaxvalue > workingvalues[1][1]:
        workingvalues[1][1] = getmax(currentmaxvalue)
        workingvalues[1][0] = currentdatetime

    if currentminvalue < workingvalues[0][1]:
        workingvalues[0][1] = getmin(currentminvalue)
        workingvalues[0][0] = currentdatetime

    # Save the current working values
    savepickle(workingvalues, "workingvalues.pkl")

    # if currentminmax > working minmax
    #   append current minmax to minmax longterm array
    #   sort and get median value
    #   median value becomes new workingminmax

    maxvalue = workingvalues[0][1]
    minvalue = workingvalues[1][1]
    heatmaparray = heatmapprocess(maxvalue, minvalue, livedata)
    htmlcreate(heatmaparray, currentdatetime)

    print(workingvalues)

    return heatmaparray