import asyncio
import os

import aiohttp
import pytube
import requests

import OutsideYT
from outside.YT_functions import get_video_info, OutsideDownloadVideoYT, post_video_info

link = 'https://youtu.be/RIx0JhCno3o'
link2 = f'https://www.youtube.com/youtubei/v1/player/RIx0JhCno3o/'
u = 'https://rr4---sn-gvnuxaxjvh-axq6.googlevideo.com/videoplayback?expire=1696814703&ei=DwIjZaucCayYv_IPh7KJIA&ip=178.71.224.153&id=o-AHhMU8A3oK94LGdqSB0lC8uLfz_2mmPGdnX5Q6F7y3_v&itag=251&source=youtube&requiressl=yes&mh=KO&mm=31%2C29&mn=sn-gvnuxaxjvh-axq6%2Csn-axq7sn7e&ms=au%2Crdu&mv=m&mvi=4&pl=21&initcwndbps=286250&vprv=1&mime=audio%2Fwebm&gir=yes&clen=15669002&dur=1071.901&lmt=1694463405731800&mt=1696792870&fvip=8&keepalive=yes&fexp=24007246&beids=24350018&c=ANDROID_EMBEDDED_PLAYER&txp=4432434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AGM4YrMwRgIhAOxWg2N6Jev66_jARKDcp8z_RNBKqskjfCcWCAa5KnDAAiEAlraLLdcEr0UAwYYyRzyw7DqkOuUeVp05lMMdy4jpvWM%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AK1ks_kwRQIhAN2zD8riz1DY2V5Wm1rZu9FSPJ-ox49Y3t0Pyip_pmPjAiAk6zQRwGRjyWi2pk2EMMV09Hy_KxbGLd0YrI2M3-Qvpg%3D%3D'
u2 = f'https://www.youtube.com/get_video_info?video_id=RIx0JhCno3o&el=vevo&fmt=301'
async def run():
    async with aiohttp.ClientSession() as session:
        video_info = await asyncio.gather(get_video_info(link, session, ['streamingData']))
        return video_info


async def main():
    async with aiohttp.ClientSession() as session:
        video_info = await asyncio.gather(
            post_video_info(link, session))
    video = OutsideDownloadVideoYT(link, video_info[0], {'full_quality': 'normal'})
    video.download_video(saving_path='')


asyncio.run(main())

# vid = pytube.YouTube('https://youtu.be/RIx0JhCno3o')
#
# vid.streams[0]


# data = requests.post(link2, headers={'Content-Type': 'application/json',
#                                      'Authorization': f'Bearer {OutsideYT.ACCESS_TOKEN}'},
#                      params={'key': OutsideYT.ACCESS_TOKEN,
#                              'contentCheckOk': True,
#                              'racyCheckOk': True})
print(1)
