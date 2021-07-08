/*CODE IS HEAVILY DERIVED FROM: https://github.com/fippo/webrtc-externals */

var inject = '(' + function () {
    function trace(method, id, args) {
        window.postMessage(['CapRtc', id, method, JSON.stringify(args || {})], '*');
    }

    // transforms a maplike to an object. Mostly for getStats +
    // JSON.parse(JSON.stringify())
    function map2obj(m) {
        if (!m.entries) {
            return m;
        }
        var o = {};
        m.forEach(function (v, k) {
            o[k] = v;
        });
        return o;
    }

    var id = 0;
    var origPeerConnection = window.RTCPeerConnection;
    if (!origPeerConnection) {
        return; // can happen e.g. when peerconnection is disabled in Firefox.
    }
    window.RTCPeerConnection = function () {
        var pc = new origPeerConnection(arguments[0], arguments[1]);
        pc._id = id++;

        window.setTimeout(function poll() {
            if (pc.signalingState !== 'closed') {
                window.setTimeout(poll, 1000);
            }
            pc.getStats()
                .then(function (stats) {
                    let cpy = {};

                    // Put the entire logic here
                    stats.forEach(function (v, k) {
                        let interestedStats = []
                        let stat = {}
                        if (v.type === "media-source") {
                            interestedStats = [
                                "width", 
                                "height", 
                                "framesPerSecond"]

                        } else if (v.type === "inbound-rtp" && v.kind === "audio") {
                            interestedStats = [
                                "packetsReceived", 
                                "packetsLost", 
                                "jitter", 
                                "framesDropped"]

                        } else if (v.type === "inbound-rtp" && v.kind === "video") {
                            interestedStats = [
                                "framesEncoded",
                                "framesSent",
                                "bytesReceived",
                                "packetsReceived",
                                "packetsLost",
                                "jitter",
                                "framesDropped"]

                        } else if (v.type === "remote-inbound-rtp") {

                            interestedStats = [
                                "jitter", 
                                "packetsLost", 
                                "roundTripTime", 
                                "totalRoundTripTime"]
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

                    // console.log(cpy)
                    // Add the forEach method here.
                    trace('getStats', pc._id, map2obj(cpy));
                });
        }, 1000);
        return pc;
    };
} + ')();';

document.addEventListener('DOMContentLoaded', function () {
    var script = document.createElement('script');
    script.textContent = inject;
    (document.head || document.documentElement).appendChild(script);
    script.parentNode.removeChild(script);
});

if (typeof browser === 'undefined') {
    browser = chrome;
}
var channel = browser.runtime.connect();
window.addEventListener('message', function (event) {
    if (typeof (event.data) === 'string') return;
    if (event.data[0] !== 'CapRtc') return;
    channel.postMessage(event.data);
});
