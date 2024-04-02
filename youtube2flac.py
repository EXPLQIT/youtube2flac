import os
import yt_dlp
from mutagen.flac import FLAC, Picture
from tqdm import tqdm
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': 'lossless',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Ignore download errors
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        
        # Check if the URL is for a playlist
        if 'entries' in info_dict:
            # Download all videos in the playlist
            for entry in info_dict['entries']:
                try:
                    ydl.download([entry['webpage_url']])
                    embed_album_cover(
                        os.path.join(output_path, f"{entry['title']}.flac"),
                        entry['title']
                    )
                except Exception as e:
                    print("An error occurred while downloading:", e)
                    continue
        else:
            # Single video download
            try:
                ydl.download([url])
                embed_album_cover(
                    os.path.join(output_path, f"{info_dict['title']}.flac"),
                    info_dict['title']
                )
            except Exception as e:
                print("An error occurred while downloading:", e)

def embed_album_cover(flac_file_path, query):
    flac = FLAC(flac_file_path)
    
    # Extract artist and song name from the file title
    file_title = os.path.splitext(os.path.basename(flac_file_path))[0]
    artist_name, song_name = file_title.split(' - ', 1) if ' - ' in file_title else ('Unknown Artist', file_title)
    
    # Fetch album art URL from Google search
    album_art_url = fetch_album_art(query)
    if album_art_url:
        print("Album art URL:", album_art_url)  # Print the URL for debugging
        with yt_dlp.YoutubeDL() as ydl:
            thumbnail_data = ydl.urlopen(album_art_url).read()
        picture = Picture()
        picture.type = 3  # 3 represents the front cover
        picture.data = thumbnail_data
        flac.clear_pictures()
        flac.add_picture(picture)
        
        # Embed artist and song name into metadata
        flac['artist'] = artist_name
        flac['title'] = song_name
        
        flac.save()
    else:
        print("Album art not found for:", query)

def fetch_album_art(title):
    for url in search(f'{title} album cover', num=5, stop=5):  # Increase the number of search results
        print("Album art URL found:", url)  # Print the URL for debugging
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = soup.find_all('meta', property='og:image')
            if meta_tags:
                img_urls = [tag.get('content') for tag in meta_tags]
                for img_url in img_urls:
                    if img_url:
                        print("Direct image URL:", img_url)
                        # Check if the URL is absolute
                        if img_url.startswith(('http://', 'https://')):
                            return img_url
                        # If not, construct the absolute URL
                        else:
                            parsed_url = urlparse(url)
                            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                            return urljoin(base_url, img_url)
            else:
                print("No Open Graph image tag found on the webpage:", url)
        else:
            print("Failed to fetch webpage:", url)
    return None

def progress_hook(d):
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            pbar = tqdm(total=d['total_bytes'], unit='B', unit_scale=True, desc=d['filename'])
            pbar.update(d['downloaded_bytes'])
    elif d['status'] == 'finished':
        tqdm.write(f'{d["filename"]} downloaded')

# Define the output directory for the FLAC file
output_path = r'CHANGE/THIS/TO/YOUR/PATH'

while True:
    # Prompt the user for a YouTube link
    url = input("Enter the YouTube video URL (or type 'exit' to quit): ")
    
    if url.lower() == 'exit':
        break

    try:
        # Download the audio (FLAC) and embed album cover
        download_audio(url, output_path)
        print("Download complete!")
    except Exception as e:
        print("An error occurred:", e)