import youtube_dl
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time as t

# note there are a few file paths that you will have to change such as the following
browser = webdriver.Firefox(executable_path='/home/alex/Downloads/geckodriver')

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
        ydl.download([link])


def initialize():
    # Erase contents
    file = open('songList.txt', 'r+')
    file.truncate(0)
    file.close()
    # Print message to txt file
    file = open('songList.txt', 'w')
    file.write("Enter the names of songs below you wish to download:")
    file.close()
    print("The \"songList.txt\" file is ready to be written to.")


def main():
    usrChoice = input("Type (1) to download from a Spotify playlist link.\nType (2) to download from the \"songList.txt\" file.\n")
    if(usrChoice == '1'):
        # The user wishes to download from the songList.txt file
        print("Launching Selenium bot-driven driver.")

        playlistLink = input("Enter the link of the Spotify Playlist you wish to download:\n")
        print("Requesting webpage.")
        browser.get(playlistLink)

        print("Waiting for the page to load js content.")
        t.sleep(2)
        content = browser.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")


        allSongs = soup.find_all("div", {"class": "tracklist-name"})
        allArtistsRAW = soup.find_all("a", {"class": "tracklist-row__artist-name-link"})

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

        playlistName = soup.find("h1").text
        numSongs = len(allSongs)
        # note that if the song is already downloaded ytdl does not download it twice
        # note that if the file does not exist, ytdl automatically makes it
        for i in range(numSongs):
            searchFor = allSongs[i].text + ", " + allArtists[i]
            print(f"({i+1}/{numSongs}) Downloading {allSongs[i].text} by {allArtists[i]} to {playlistName}...")
            download(searchFor, playlistName)
            print("Download complete.")
        print(f"Completed all downloads ({numSongs})")

    elif(usrChoice == '2'):
        # The user wishes to download from the songList.txt file
        # File minipulation
        file = open('songList.txt', 'r')
        numLines = len(file.readlines())
        file.close()

        if(numLines <= 1):
            print("You didn't add any songs to the text file.\n"
                  "Open the \"songList.txt\" file and add the names of songs you "
                  "wish to download.")

        elif(numLines > 1):
            for i in range(1, numLines):
                file = open('songList.txt', 'r')
                line = str(file.readlines()[i]).rstrip()
                file.close()

                print(f"Downloading: {line}...")
                download(line, "File-Playlist")
                print("Download complete.")
            print(f"Finished all downloads ({i})")

        # Erases contents of file so no need to re-download songs
        initialize()

main()
browser.close()  # close the Selenium browser
