# CapRtc 
CapRtc is a custom-based QoE parameter capture tool for WebRTC traffic.  

The tool works by modifying the browser environment. It overrites the native RTCPeerConnection by addition of more event-handler. These event-handlers send the data we require in a periodic manner, which is then available for **Download** from the background.html page.  


## Usage
### Using the chrome-extension:
* Go to chrome://extensions/ and check the box for Developer mode in the top right.
* Click on `Load Unpacked Extension` and select the current folder into it.
* Now this extension would be visible on your extensions section in chrome.
* Click on the extension. This should open a background page. There is a `download` button on that page
* Now open the webRTC application you wish to collect the stats for.
* Click on the `Download` button on the background page to download all the collected stats as a json.
* Before opening a new application. Click on `Reset Stats` to clear the currently accumulated data.

### Collecting stats on the User-Device (Android Chrome Browser):
* Setup your device for [remote debugging](https://developer.chrome.com/docs/devtools/remote-debugging/)
* Once everything is setup and open the console for the session in your android browser.
* Paste the code in the file `Remote.js` directly into remote-console.
* Test the webRTC app now. You can also disconnect the User Device. But donot close the web-page before collecting the stats.
* To gather the statistics, reconnect your device and the console. Inspect the same webpage on which the RTC App is open.
* Type `DownloadData()` into the console. The `data.json` file will start downloading on your deive. ( You might get a pop-up on the device for Download based on your permissions.)
  
### Plotting the Data: (deprecated)
* Create a New Folder. Copy the `plot.py` and `data.json` inside it. 
* Open a terminal inside the folder and run the script using python.
  
        python plot.py <Path_To_Data.Json> <Time_Interval (Put 1 here currently)> 
* This will generate numerours `.png` files each giving out a graph for the specific parameter.
* You may want to elimate graphs which represent no meaningful data.

# Now the Default
### Plotting webrtc-internals Data 
* Create a Folder which will store all the generated plots.
* Store all the data dumps generated from webrtc-internals page _(wont work on files generated from the tool)_ in a new folder.
* Open a terminal inside the folder and run the script using python.

        python scripts/plotInternals.py <Path to Dir Containing data dumps> <Dir to save generated Plots>
* Again numerous `.png` files representing time series graphs will be generated. YOu may want to discard cases which represent no meaningful data.
* To plot all the graphs corresponding to a data-dump file use:

        python scripts/plotInternals.py <Path to Data Dump File> <Plot Dir>
* This will generate all the plots and save them inside `<Plot Dir>/<Name of Data File>/`
* 

### Creating CSV Data File
* To create a csv file :

        python scripts/rawData.py <Path to webrtc dump> <Path to New Data File>
* This will generate a csv/ excel file for the data in the format 


        param1, param2, ....
        data1, data2 ...
        data1, data2 ...

# LICENSE
MIT

This project heavily follows from [webRTC-externals](https://github.com/fippo/webrtc-externals) which is licensed under MIT.
