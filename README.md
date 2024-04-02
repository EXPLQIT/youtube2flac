# youtube2flac

This script will prompt the user for a YouTube link, once a link is provided it'll download the YouTube video, extract the audio at the highest quality, and convert it to FLAC. The video is then deleted automatically. 
This works with playlists as well, simply provide any link within a YouTube playlist and it'll download each invdividual video, extract audio, and convert it to FLAC.

It can also embed the relative metadata into the FLAC (assuming it's a song) and embed the album cover as well. (it works about 70% of the time lol)



Requires the following dependencies:
  pip install yt-dlp
  pip install mutagen
  pip install tqdm
  pip install google
  pip install requests
  pip install beautifulsoup4
