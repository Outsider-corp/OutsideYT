import yt_dlp

options = {'format': 'bestvideo+bestaudio/best',
           'outtmpl': f'title',
           'ffmpeg_location': r'outiside/bin/ffmpeg.exe'}
urls = ['https://www.youtube.com/watch?v=ChoNNKMY9ZI']

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download(urls)
