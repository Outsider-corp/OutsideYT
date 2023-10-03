import yt_dlp
import requests

# options = {'format': 'bestvideo+bestaudio/best',
#            'outtmpl': '{title}',
#            'ffmpeg_location': r'outside/bin/ffmpeg.exe'}
# urls = ['https://youtu.be/Gpu7_7RgBKU?si=a6R1tQLexJpuG2qY']
# urls2 = ['https://youtu.be/HkhcAs59j_8?si=z5MeSrmhqMq17e5G']
#
# with yt_dlp.YoutubeDL(options) as ydl:
#     # ydl.download(urls)
#     dd = ydl.extract_info(urls2[0], download=False)
print(1)


res = requests.get('https://www.youtube.com/watch?v=8qoUSy-qTks')
with open("video_dud.html", 'w', encoding="utf-8") as f:
    f.write(res.text)