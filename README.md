<!-- GETTING STARTED -->
## YouTube2FLAC

This script will prompt the user for a YouTube link, once a link is provided it'll download the YouTube video, extract the audio at the highest quality, and convert it to FLAC. The video is then deleted automatically. 
This works with playlists as well, simply provide any link within a YouTube playlist and it'll download each invdividual video, extract audio, and convert it to FLAC.

It can also embed the relative metadata into the FLAC (assuming it's a song) and embed the album cover as well. (it works about 70% of the time lol)

The quality of the audio is entirely dependant on the audio quality of the video and it's also worth noting that YouTube can't be lossless.

### Required Dependencies

Here's a list of the required dependencies needed for the script to run properly.
* yt-dlp
  ```sh
  pip install yt-dlp
  ```
* mutagen
  ```sh
  pip install mutagen
  ```
* tqdm
  ```sh
  pip install tqdm
  ```
* google
  ```sh
  pip install google
  ```
* requests
  ```sh
  pip install requests
  ```
* beautifulsoup4
  ```sh
  pip install beautifulsoup4
  ```
  
  
  
  
  
