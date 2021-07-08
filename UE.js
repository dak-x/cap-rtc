// EXECUTE THIS ENTIRE SCRIPT IN THE UE CONSOLE AFTER THE CHROME DEV TOOLS.
var allStats = [];
var timeout = 1000;
function map2obj(m) {
    if (!m.entries) {
        return m;
    }
    var o = {};
    m.forEach(function (v, k) {
        o[k] = v;
    });
    return o;
};
var id = 0;
var origPeerConnection = window.RTCPeerConnection;
window.RTCPeerConnection = function () {
    var pc = new origPeerConnection(arguments[0], arguments[1]);
    pc._id = id++;
    window.setTimeout(function poll() {
        if (pc.signalingState !== 'closed') {
            window.setTimeout(poll, timeout);
        }
        pc.getStats()
            .then(function (stats) {
                let cpy = {};
                stats.forEach(function (v, k) {
                    let interestedStats = [];
                    let stat = {};
                    if (v.type === "media-source") {
                        interestedStats = [
                            "width",
                            "height",
                            "framesPerSecond"];

                    } else if (v.type === "inbound-rtp" && v.kind === "audio") {
                        interestedStats = [
                            "packetsReceived",
                            "packetsLost",
                            "jitter",
                            "framesDropped"];

                    } else if (v.type === "inbound-rtp" && v.kind === "video") {
                        interestedStats = [
                            "jitter",
                            "packetsLost",
                            "packetsReceived",
                            "bytesReceived",
                            "framesReceived",
                            "frameWidth",
                            "frameHeight",
                            "framesPerSecond",
                            "framesDecoded",
                            "framesDropped"];

                    } else if (v.type === "remote-inbound-rtp") {

                        interestedStats = [
                            "jitter",
                            "packetsLost",
                            "roundTripTime",
                            "totalRoundTripTime"];
                    }

                    if (interestedStats.length > 0) {
                        Object.keys(v).forEach(function (key) {
                            if (interestedStats.includes(key)) {
                                stat[key] = v[key];
                            }
                        });
                        cpy[k] = stat;
                    }
                });
                // console.log(cpy);
                allStats.push(map2obj(cpy));
            });
    }, timeout);
    return pc;
};
function DownloadData() { let element = document.createElement('a'); var dataDump = new Blob([JSON.stringify(allStats)], { type: "application/json" }); var URL = window.URL.createObjectURL(dataDump); element.href = URL; element.download = "dataDump.json"; document.body.appendChild(element); element.click(); element.remove(); console.log("Fired Download Func"); };