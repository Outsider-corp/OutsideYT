import yt_dlp
import requests

options = {'format': 'bestvideo+bestaudio/best',
           'outtmpl': '{title}',
           'ffmpeg_location': r'outside/bin/ffmpeg.exe'}
urls = ['https://www.youtube.com/watch?v=anh5sbdJCNY']

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download(urls)


# res = requests.get('https://www.youtube.com/watch?v=QwmFHVsl9e4&list=PLezM3LFevqM986L3M0DRAUT2FsbbSA1gy&index=13&t=14s')
# with open("video.html", 'w', encoding="utf-8") as f:
#     f.write(res.text)