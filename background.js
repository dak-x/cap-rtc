// https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/runtime/onConnect
if (typeof browser === 'undefined') {
    browser = chrome;
}

var allStats = []
browser.runtime.onConnect.addListener(function (channel) {
    if (window === browser.extension.getBackgroundPage()) {
        return;
    }
    var url = channel.sender.url;
    var pid = Math.random().toString(36).substr(2, 10);
    channel.onDisconnect.addListener(function () {
        // TODO: remove / mark everything associated with that page/pid
    });
    channel.onMessage.addListener(function (message, port) {
        if (message[0] !== 'CapRtc') return;

        var method = message[2];
        var rtcData = message[3] ? JSON.parse(message[3]) : undefined;
        // emulate webrtc-internals format
        var data = { lid: message[1], pid: pid, type: message[2], time: Date.now() };
        // data.value = typeof args === 'string' ? args : message[3];
        console.log(rtcData)
        allStats.push(rtcData)
    });
});

var content;

function downloadFunc() {
    let element = content;
    var dataDump = new Blob([JSON.stringify(allStats)], { type: "application/json" })

    var URL = window.URL.createObjectURL(dataDump)
    element.href = URL;
    element.download = "dataDump.json"
    console.log("Fired Download Func")
}

function resetStat() {
    allStats = []
}

function init() {
    content = document.getElementsByTagName('a')[0];
    content.addEventListener('click', downloadFunc);

    let resetButton = document.getElementsByTagName('a')[1];
    resetButton.addEventListener('click', resetStat);

    console.log("Download Button Loaded")
}
document.addEventListener('DOMContentLoaded', init);


// function exportToJsonFile(jsonData) {
//     let dataStr = JSON.stringify(jsonData);
//     let dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

//     let exportFileDefaultName = 'data.json';

//     let linkElement = document.createElement('a');
//     linkElement.setAttribute('href', dataUri);
//     linkElement.setAttribute('download', exportFileDefaultName);
// }

