import datetime
from outside.YT.download_model import OutsideDownloadVideoYT
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


# res = requests.get('https://www.youtube.com/watch?v=8qoUSy-qTks')
# with open("video_dud.html", 'w', encoding="utf-8") as f:
#     f.write(res.text)

# time = datetime.datetime.now()
# print(time.strftime('%c'))



OutsideDownloadVideoYT.add_video_audio(r'D:\Py_Projects\OutsideYT\videos\ deal1\FastAPI что это такое_ _ Django School\FastAPI что это такое_ _ Django School_0.webm',
                 r'D:\Py_Projects\OutsideYT\videos\ deal1\FastAPI что это такое_ _ Django School\FastAPI что это такое_ _ Django School_1.webm',
                 r'D:\Py_Projects\OutsideYT\videos\ deal1\FastAPI что это такое_ _ Django School\FastAPI что это такое_ _ Django School.webm',)