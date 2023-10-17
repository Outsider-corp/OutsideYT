import os

from outside import settings

ACCESS_TOKEN = ''

project_folder = os.getcwd()
cookies_folder = os.path.join(project_folder, 'outside', 'oyt_info')
app_settings_uploaders = settings.SettingsUsers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_UPLOADERS.json'))
app_settings_watchers = settings.SettingsWatchers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_WATCHERS.json'))
app_settings_download = settings.SettingsDownloads(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_DOWNLOAD.json'))

chromedriver_location = os.path.join(project_folder, 'outside', 'bin', 'chromedriver.exe')
chrome_playwright_location = os.path.join(project_folder, 'outside', 'bin', 'chromium-1080',
                                          'chrome-win', 'chrome.exe')

TEXT_EXTENSIONS = ['.txt']
VIDEO_EXTENSIONS = ['.mp4', '.webm', '.avi', '.mov', '.mpeg-1', '.mpeg-2', '.mpg', '.wmv',
                    '.mpegps', '.flv', '.3gpp', '.WebM', '.DNxHR', '.ProRes', '.CineForm', '.HEVC',
                    '.MP4', '.AVI', '.MOV', '.MPEG-1', '.MPEG-2', '.MPG', '.WMV', '.MPEGPS',
                    '.FLV', '.3GPP', '.WEBM', '.DNXHR', '.PRORES', '.CINEFORM', '.HEVC']
IMAGE_EXTENSIONS = ['.pjp', '.jpg', '.pjpeg', '.jpeg', '.jfif', '.png',
                    '.PJP', '.JPG', '.PJPEG', '.JPEG', '.JFIF', '.PNG']
JSON_EXTENSIONS = ['.json']

FILENAMES_VIDEO_DETAILS = {"Title.txt": 'title', "Description.txt": 'shortDescription',
                           'Tags.txt': 'keywords', 'Playlist.txt': '',
                           'Preview.jpg': 'link',
                           'Cards.json': 'cards'}

FOLDERNAME_FORBIDDEN_SYMBOLS = '`<>:"/\|?*.'

WAIT_TIME_URL_UPLOADS = 5
WAIT_TIME_URL_PLAYWRIGHT = 10
WAIT_TIME_ASYNC_LOOPS = 0.8
WAIT_TIME_THREAD = 1
SAVE_COOKIES_TIME = 60 * 60 * 24 * 30
ASYNC_LIMIT = 20
VIDEO_DOWNLOAD_TIMEOUT = 5
VIDEO_WATCH_TIMEOUT = 30
VIDEO_DOWNLOAD_MAX_RETRIES = 3
DEFAULT_CHUNK_SIZE = 1024 ** 2
MAX_THREADS_COUNT = 5

FFMPEG_LOCATION = os.path.join(project_folder, 'outside', 'bin', 'ffmpeg.exe')

YT_URL = 'https://www.youtube.com/'
YT_STUDIO_URL = 'https://studio.youtube.com/'
