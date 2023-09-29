import yt_dlp
import requests

# options = {'format': 'bestvideo+bestaudio/best',
#            'outtmpl': f'title',
#            'ffmpeg_location': r'outiside/bin/ffmpeg.exe'}
# urls = ['https://www.youtube.com/watch?v=ChoNNKMY9ZI']
#
# with yt_dlp.YoutubeDL(options) as ydl:
#     ydl.download(urls)


res = requests.get('https://www.youtube.com/watch?v=HkhcAs59j_8&t=1076s')
with open("video.html", 'w', encoding="utf-8") as f:
    f.write(res.text)