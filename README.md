# music-downloader README
By using YouTube-dl and python, the names of songs can be entered in a .txt file and the program will search YouTube for the top lyrical video and download the audio to the user's music folder.

### Installation
This program uses the youtube-dl API to fetch audio so it must be installed.

For UNIX users (Linux / OS X ...):

    sudo curl -L https://yt-dl.org/downloads/latest/youtube-d -o /usr/local/bin/youtube-dl
    sudo chmod a+rx /usr/local/bin/youtube-dl

Alternatively, with pip:

    sudo pip install youtube_dl

### Usage
To use the program, type in the names of songs you want downloaded into the *songList.txt* file, then run *musicDownloader.py* and the songs will be downloaded to the *~/Music* directory.
