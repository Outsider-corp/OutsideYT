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
save_cookies_time = 60 * 60 * 24 * 30
