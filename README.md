# music-downloader README
By using YouTube-dl, Selenium, Beautifulsoup, and python, the names of songs can be entered in a .txt file, or scraped from a Spotify playlist, and the program will search YouTube for the top lyrical video and download the audio to the user's Music folder in a folder named after the playlist.

### Installation
This program uses the youtube-dl, Selenium, and the beatifulsoup4 API to fetch and download YouTube audio so it must be installed.

For UNIX users (Linux / OS X ...), youtube-dl can be installed with:

    sudo curl -L https://yt-dl.org/downloads/latest/youtube-d -o /usr/local/bin/youtube-dl
    sudo chmod a+rx /usr/local/bin/youtube-dl

Alternatively, with pip, youtube-dl, Selenium, and beautifulsoup4 can be installed by:

    sudo pip install youtube_dl
    sudo pip install selenium
    sudo pip install beautifulsoup4

Note that Selenium requires a driver associated with your browser of choice, which can be downloaded off the Selenium website.
The path to the driver must be specified, in my code this is done on line 8 and the syntax is slightly different for different browsers. In my case I'm using FireFox, which uses Geckodriver to run Selenium.

Note that a few lines will have to be changed as they reference my file system.
### Usage
To use the program, type in the names of songs you want downloaded into the *songList.txt* file. Alternatively, paste a link of a Spotify **online** playlist and the program will scrape all the songs. You will have a choice of what method you wish to use when the script is run. To run the program, type *musicDownloader.py* and the songs will be downloaded to the *~/Music/"Playlist name"* directory.
