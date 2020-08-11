import youtube_dl
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import PySimpleGUI as sg
import time as t


# Change the following line to match your browser and driver path
print("Launching Selenium bot-driven driver.")
browser = webdriver.Firefox(executable_path='./selenium-driver/geckodriver')


class MyLogger(object):
    # For debugging and error throwing
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download(title, folder):
    # Downloads a m4a audio file with the provided title to the provided folder
    # in the Music directory
    outtmpl = '~/Music/' + folder + '/' + title + '.%(ext)s'

    ydl_opts = {
        'format': 'm4a',
        'outtmpl': outtmpl,
        'logger': MyLogger(),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Get the top result off youtube, let's use Selenium to find the link
        # and let's use ytdl to download the YouTube video
        titleSearch = title.replace(" ", "+")
        browser.get(f"https://www.youtube.com/results?search_query={titleSearch}+lyrics")
        link = browser.find_element_by_id("thumbnail").get_attribute("href")
        # let's try and download it
        try:
            ydl.download([link])
        except Exception as e:
            print(f"{title} could not be downloaded.")
            raise e


def driver(link, songs):
    playlistName = ''
    if(len(link) > 34):
        # the user added to the spotify link, let's try to use it

        print("Requesting webpage.")
        t.sleep(2)

        browser.get(link)

        content = browser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")

        allSongs = soup.find_all("div", {"class": "tracklist-name"})
        allArtistsRAW = soup.find_all("a", {"class": "tracklist-row__artist-name-link"})

        pageRequestSuccess = True
        if(len(allSongs) == 0):
            print("This playlist doesn't exist. Make sure you entered the playlist link correctly.")
            pageRequestSuccess = False;

        if(pageRequestSuccess):

            allArtists = []

            # for handling features
            # always get the first artist
            i = step = 0;
            while(i < len(allArtistsRAW)):
                thisArtist = allArtistsRAW[i].parent.parent.parent.text.split(',')
                if(len(thisArtist) > 1):
                    # then there is a feature
                    i += len(thisArtist) - 1
                allArtists.append(thisArtist[0])
                i += 1

            playlistName = soup.find_all("h1")[1].text
            print(playlistName)
            numSongs = len(allSongs)
            # note that if the song is already downloaded ytdl does not download it twice
            # note that if the file does not exist, ytdl automatically makes it
            for i in range(numSongs):
                searchFor = allSongs[i].text + ", " + allArtists[i]
                print(f"({i+1}/{numSongs}) Downloading {allSongs[i].text} by {allArtists[i]} to {playlistName}...")
                download(searchFor, playlistName)
                print("Download complete.")
            print(f"Completed all downloads ({numSongs})")


    # download any additional songs typed
    typedSongs = songs.split(',')  # [''] on empty

    if(typedSongs[0] != '' or len(typedSongs) > 1):
        if(playlistName == ''):
            playlistName = "File-Playlist"

        for song in typedSongs:
            print(f"Downloading: {song}...")
            download(song, playlistName)
        print("Completed all downloads")


def main():
    sg.theme('DarkBlue14')
    layout = [
        [sg.Text('Spotify Playlist Link '), sg.InputText('https://open.spotify.com/playlist/', size=(41, 1))],
        [sg.Text('Additionally, type the songs you want below separated by commas:')],
        [sg.InputText(size=(60, 20))],
        [sg.Submit('Download'), sg.Cancel()]
    ]
    window = sg.Window('Music Downloader', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            browser.quit()  # close the Selenium browser
            window.close()  # close the GUI
            break
        if(event == 'Download'):
            driver(values[0], values[1])

    window.close()


if __name__ == '__main__':
    main()


browser.quit()  # close the Selenium browser
