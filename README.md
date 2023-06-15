# AutoVimeoDownloader

## Download segmented videos from Vimeo through different ways

### Install prerequisites

#### ffmpeg 

Example:

7Zip required: https://7-zip.org/

FFmpeg: https://ffmpeg.org/

  * Download 
  * Select your OS
  * Click in "Windows builds from gyan.dev"
  * Download las release "ffmpeg-release-full.7z"
  * Extract the files using 7zip
  * Copy extracted folder
  * Paste extracted folder in main directory of your disk
  * Access bin folder and copy the folder path
  * Add this path inside path in system variables
  * Test if it is installed by typing the following command in cmd "ffmpeg"
  
#### Python 3:

    Debian/Ubuntu: sudo apt install -y ffmpeg python3
    
    Mac OS X: brew install ffmpeg python
    
    Windows: https://python.org.br/instalacao-windows/
  
  Install pip and tqdm module in python

### Instructions to download video
For each video you want to download:
1. Open the page containing the embedded video.
1. Open development console (Chrome: F12).
1. Go to the Network tab.
1. Right click on the `master.json` request, select Copy → Copy link address. An example of how such a URL could look like:

`https://105vod-adaptive.akamaized.net/exp=1686796657~acl=%2F45a16a0c-e390-4a92-9f74-56b84224f6e8%2F%2A~hmac=9ba83ac69819e0794023357dd15b9bdce58da79055f2ccfd5f216b1e6eb21f9a/45a16a0c-e390-4a92-9f74-56b84224f6e8/sep/video/54e87bf0,a581f2f1,dfd03df0,e7ce4e25,fb1e4dac/audio/9e7a4006,a5dfb6c4,f35fcfa7/master.json?base64_init=1\u0026query_string_ranges=1`.


Create a TSV file (In Google Sheets or Excel save the file with format "Text (tab delimited) (*.txt)" in the same folder as the python script), where the first column is output file name (ending with `.mp4`) and the second is this URL to `master.json`.

Then run the script, providing the name of this file with names and URLs in VS Code (install extension python):

Example:
```bash
C:/Python312/python.exe "c:/AutoVimeoDownloader/main.py" -i names_urls.txt
```

## Acknowledgements
Based on work of:
* @AbCthings : https://github.com/AbCthings/vimeo-audio-video 
