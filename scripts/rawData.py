# Plot data in Obs, param1, param2, ...
import json
import sys
from typing import Iterator

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


def getElem(dataList, idx):
    if idx < len(dataList):
        return dataList[idx]

    return 0.0


def dumpIntoFile(fileName, dataDict, maxLen):

    fs = open(fileName + ".csv", "w")

    keys = list(dataDict.keys())

    lines = [",".join(keys)]

    for i in range(maxLen):
        vals = []
        for key in keys:
            vals.append(getElem(dataDict[key], i))
        lines.append(",".join(map(str, vals)))

    for line in lines:
        fs.write(line + "\n")

    fs.close()


if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print(f"usage: {sys.argv[0]} <DATA FILE> <TARGET FILE>\n")
        exit(1)

    DATAFILE = sys.argv[1]
    TARGETFILE = sys.argv[2]

    dataDict = loadFile(DATAFILE)
    maxLen = max( map(len, dataDict.values()) )
    dumpIntoFile(TARGETFILE, dataDict, maxLen)
