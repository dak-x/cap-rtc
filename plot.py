import json
import sys
import pprint
import matplotlib.pyplot as plt

DIR = "Plots"

DATA = {}

if (len(sys.argv) != 3):
    print(f"usage: {sys.argv[0]} <Json Data> <Time Interval in s>.\nUse this script from inside the directory you want to generate the images. Too many graphs might be generated!!!")
    exit(1)

FILENAME = sys.argv[1]
TIMEOUT = int(sys.argv[2])
# if( sys.argv[3] is not None):
# DIR = sys.argv[3]

file = open(FILENAME, "rb")
data = file.read()
data = json.loads(data)


class plotData:
    def __init__(self, title: str, param: str, dataPoints) -> None:
        self.title = title
        self.param = param
        self.data = dataPoints[:]

    # Complete this.
    def plot(self):
        global DIR
        plt.figure()
        timeAx = [(TIMEOUT * x) for x in range(len(self.data))]
        plt.plot(timeAx, self.data)
        plt.ylabel(self.param)
        plt.title(self.title)
        # plt.show()
        plt.savefig(self.title+"_"+self.param+".png")


# Merge data on the basis of stream/source + parameter:
for value in data[10:]:
    for streamSource in value:
        if streamSource not in DATA:
            DATA[streamSource] = {}
        for param in value[streamSource]:
            if param not in DATA[streamSource]:
                DATA[streamSource][param] = []
            DATA[streamSource][param].append(value[streamSource][param])

# Create Data for plots:
# pprint.pprint(DATA)

plotDataList = []
for title in DATA:
    for param in DATA[title]:
        plotDataList.append(plotData(title, param, DATA[title][param]))

for i in range(len(plotDataList)):
    plotDataList[i].plot()

# pprint.pprint(plotDataList)
