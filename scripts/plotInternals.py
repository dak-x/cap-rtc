from genericpath import isfile
import os
import json
import sys
import matplotlib

import matplotlib.pyplot as plt

# All the required Stats
desiredParams = {

    "RTCRemoteInboundRtpVideoStream":
    [
        "jitter",
        "packetsLost",
        "roundTripTime",
        # "totalRoundTripTime"
    ],

    "RTCInboundRTPVideoStream":
    [
        "-jitter",
        "-packetsLost",
        "-packetsReceived",
        "-[packetsReceived/s]",
        "-bytesReceived",
        "-[bytesReceived_in_bits/s]",
        # "-framesReceived",
        # "-[framesReceived/s]",
        "-frameWidth",
        "-frameHeight",
        "-framesPerSecond",
        "-framesDecoded",
        "-[framesDecoded/s]",
        "-framesDropped",
    ],

    "RTCMediaStreamTrack_receiver":
    [
        "-framesReceived",
        "-[framesReceived/s]",
        "-freezeCount*",
        "-pauseCount*",
        "-totalFreezesDuration*",
        "-totalPausesDuration*",
        "-totalFramesDuration*",
    ]

}


# Filter out the desired keys from the data dump.
def filterKeys(key):
    for k in desiredParams.keys():
        if key.startswith(k):
            for param in desiredParams[k]:
                if key.endswith(param):
                    return True
    return False


# Filters all the desired keys from a given data dump file.
def getStats(dataDump: dict):
    try:
        peerConnections: dict = dataDump["PeerConnections"]
        stats: dict = next(iter(peerConnections.values()))["stats"]

        allStats = dict((k, json.loads(v["values"]))
                        for k, v in stats.items() if filterKeys(key=k))

        return allStats
    except:
        return None


# Process Contents of a data dump file.
def loadFile(fileName: str):
    try:
        file = open(fileName, 'rb')
        data = file.read()
        data = json.loads(data)
        return getStats(data)
    except:
        return None


def sortTimeStamps(dir: str):
    os.chdir(dir)
    files = [x for x in os.listdir(".") if x.endswith(
        ".txt") or x.endswith(".json")]

    files.sort(key=os.path.getctime)
    return files


# Computes the Average Value to Plot on top of the stack.
def computeAverage(data):
    N = len(data)
    T = min(len(x) for x in data)
    avg = []
    for t in range(T):
        s = 0.0
        for i in range(N):
            s += data[i][t]
        avg.append(s/N)
    return avg

# Generate a vertically stacked plot with a common time axis


def plotStacked(data, title, fileName=""):
    N = len(data)

    if N > 1:
        fig, ax = plt.subplots(nrows=(N + 1), sharex=True)

        fig.suptitle(title)

        plt.subplots_adjust(hspace=0.01)  # Vertical Spacing between the plots
        plt.xlabel("Time (sec)")
        for i in range(N):
            ax[i + 1].set_ylabel(f"Test: {N - i - 1}")
            ax[i + 1].grid()
            ax[i + 1].plot(data[N - i - 1])

        ax[0].set_ylabel("Average: ")
        ax[0].grid()
        ax[0].plot(computeAverage(data))

        filename = "".join(i for i in title if i not in "\/:*?<>|")
        plt.savefig(filename + ".png")
        plt.close()
    else:
        plt.suptitle(title)
        plt.xlabel("Time (sec)")
        plt.ylabel(title)

        plt.plot(data[0])

        filename = fileName + \
            "".join(i for i in title if i not in "\/:*?<>|") + ".png"
        plt.savefig(filename)
        plt.close()


# Some helpers for mapping a param name to what it actaully contains
def matchKey(val, key):
    return key[0] in val and key[1] in val


def getKey(k, Keys):
    for key in Keys:
        if matchKey(k, key):
            return key


# Merges the common parameters across the tests
def mergeCommons(allFileData):
    Keys = []
    for k in desiredParams:
        for y in desiredParams[k]:
            Keys.append((k, y))

    sepData = {}
    for key in Keys:
        sepData[key] = []

    for fileData in allFileData:
        for (statKey, statValue) in fileData.items():
            sepData[getKey(statKey, Keys)].append(statValue)

    return sepData


# Load and Process all the files in the directory in timeStamp sorted order.
def loadDir(dirName: str):
    files = sortTimeStamps(dirName)

    testsData = []
    for file in files:
        stats = loadFile(file)
        if stats is None:
            print(
                f"Skipping file: {file}, doesnot adhere to webrtc-internals dump format")
            continue
        testsData.append(stats)

    # print(testsData)
    return mergeCommons(testsData)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print(f"usage: {sys.argv[0]} <DATA DIR> <TARGET DIR>\n")
        exit(1)

    DATAPATH = sys.argv[1]
    TARGETDIR = sys.argv[2]

    allData = {}

    isFile = os.path.isfile(DATAPATH)

    # Stacked Plots for all inside a directory.
    if(os.path.isdir(DATAPATH)):
        currDir = os.getcwd()
        allData = loadDir(DATAPATH)
        os.chdir(currDir)
        # Create the output directory
        if not os.path.exists(TARGETDIR):
            os.mkdir(TARGETDIR)
        os.chdir(TARGETDIR)

    # Data from a single file.
    else:
        fileData = loadFile(DATAPATH)
        allData = mergeCommons([fileData])
        fileName = os.path.basename(DATAPATH).split(".")[0]

        if not os.path.exists(TARGETDIR):
            os.mkdir(TARGETDIR)
        os.chdir(TARGETDIR)
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)

    for param in allData.keys():
        n = len(allData[param])
        print(param[0] + param[1] + ":", n)
        if n > 0:
            if(isfile):
                plotStacked(allData[param], param[0] + param[1])
            else:
                plotStacked(allData[param], param[0] + param[1])
