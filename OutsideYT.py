import os

from outside.oyt_info import settings

project_folder = os.getcwd()
app_settings_uploaders = settings.SettingsUsers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_UPLOADERS.json'))
app_settings_watchers = settings.SettingsWatchers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_WATCHERS.json'))

text_extensions = ['.txt']
video_extensions = ['.mp4', '.avi', '.mov', '.mpeg-1', '.mpeg-2', '.mpg', '.wmv',
                    '.mpegps', '.flv', '.3gpp', '.WebM', '.DNxHR', '.ProRes', '.CineForm', '.HEVC',
                    '.MP4', '.AVI', '.MOV', '.MPEG-1', '.MPEG-2', '.MPG', '.WMV', '.MPEGPS',
                    '.FLV', '.3GPP', '.WEBM', '.DNXHR', '.PRORES', '.CINEFORM', '.HEVC']
image_extensions = ['.pjp', '.jpg', '.pjpeg', '.jpeg', '.jfif', '.png',
                    '.PJP', '.JPG', '.PJPEG', '.JPEG', '.JFIF', '.PNG']
json_extensions = ['.json']

filenames_video_details = {"Title.txt": 'title', "Description.txt": 'shortDescription',
                           'Tags.txt': 'keywords', 'Playlist.txt': '',
                           'Preview.jpg': 'link',
                           'Cards.json': 'cards'}

foldername_forbidden_symbols = '`<>:"/\|?*'

wait_time_url_uploads = 5
wait_time_async_loops = 0.8
wait_time_threads = 0.5
save_cookies_time = 60 * 60 * 24 * 30
async_limit = 20

download_video_params = {
    'format': 'best',
    'ffmpeg_location': r'outside/bin/ffmpeg.exe',
}

formats = {'full': ['best',
                    'standard',
                    'worst'],
           'video_quality': ['2160p',
                             '1440p',
                             '1080p',
                             '720p',
                             '480p',
                             '360p',
                             '240p',
                             '144p'],
           'video_type': ['mp4', 'webm'],
           'audio_quality': ['AUDIO_QUALITY_LOW',
                             'AUDIO_QUALITY_MEDIUM',
                             ],
           'audio_type': ['mp4', 'webm']

           }
