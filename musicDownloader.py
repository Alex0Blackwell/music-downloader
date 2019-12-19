import youtube_dl


class MyLogger(object):
    # For debugging and error throwing
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download(title):
    # Downloads a m4a audio file with the provided title
    outtmpl = '~/Music/' + title + '.%(ext)s'
    ydl_opts = {
        'format': 'm4a',
        'outtmpl': outtmpl,
        'logger': MyLogger(),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Get the top result off youtube
        ydl.extract_info("ytsearch:"+title+"lyrics", download=True)


def main():
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
            download(line)
            print("Download complete.")
        print(f"Finished all downloads ({i})")

    # Erases contents of file so no need to re-download songs
    initialize()


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


main()
