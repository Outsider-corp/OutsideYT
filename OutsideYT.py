import os

from outside.oyt_info import settings

project_folder = os.getcwd()
app_settings_uploaders = settings.SettingsUsers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_UPLOADERS.json'))
app_settings_watchers = settings.SettingsWatchers(
    os.path.join(project_folder, 'outside', 'oyt_info', 'SETTINGS_WATCHERS.json'))

TEXT_EXTENSIONS = ['.txt']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mpeg-1', '.mpeg-2', '.mpg', '.wmv',
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

FOLDERNAME_FORBIDDEN_SYMBOLS = '`<>:"/\|?*'

WAIT_TIME_URL_UPLOADS = 5
WAIT_TIME_ASYNC_LOOPS = 0.8
WAIT_TIME_THREAD = 0.5
SAVE_COOKIES_TIME = 60 * 60 * 24 * 30
ASYNC_LIMIT = 20
VIDEO_DOWNLOAD_TIMEOUT = 30
VIDEO_DOWNLOAD_MAX_RETRIES = 3
DEFAULT_CHUNK_SIZE = 9437184

FFMPEG_LOCATION = os.path.join(project_folder, 'outside', 'bin', 'ffmpeg.exe')

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

SIMPLE_VIDEO_ITAG = {
    38: ("3072p", "192kbps"),
    96: ("1080p", "256kbps"),
    85: ("1080p", "192kbps"),
    46: ("1080p", "192kbps"),
    37: ("1080p", "192kbps"),
    301: ("1080p", "128kbps"),
    95: ("720p", "256kbps"),
    102: ("720p", "192kbps"),
    84: ("720p", "192kbps"),
    45: ("720p", "192kbps"),
    22: ("720p", "192kbps"),
    300: ("720p", "128kbps"),
    151: ("720p", "24kbps"),
    101: ("480p", "192kbps"),
    94: ("480p", "128kbps"),
    83: ("480p", "128kbps"),
    44: ("480p", "128kbps"),
    59: ("480p", "128kbps"),
    78: ("480p", "128kbps"),
    35: ("480p", "128kbps"),
    100: ("360p", "128kbps"),
    93: ("360p", "128kbps"),
    43: ("360p", "128kbps"),
    82: ("360p", "128kbps"),
    34: ("360p", "128kbps"),
    18: ("360p", "96kbps"),
    6: ("270p", "64kbps"),
    5: ("240p", "64kbps"),
    132: ("240p", "48kbps"),
    92: ("240p", "48kbps"),
    91: ("144p", "48kbps"),
    17: ("144p", "24kbps"),
}

VIDEO_ITAG = {272: ('4320p', 'WEBM'), 702: ('4320p', 'MP4'), 571: ('4320p', 'MP4'),
              402: ('4320p', 'MP4'), 337: ('2160p', 'WEBM'), 315: ('2160p', 'WEBM'),
              313: ('2160p', 'WEBM'), 701: ('2160p', 'MP4'), 401: ('2160p', 'MP4'),
              266: ('2160p', 'MP4'), 138: ('2160p', 'MP4'), 336: ('1440p', 'WEBM'),
              308: ('1440p', 'WEBM'), 271: ('1440p', 'WEBM'), 700: ('1440p', 'MP4'),
              400: ('1440p', 'MP4'), 264: ('1440p', 'MP4'), 335: ('1080p', 'WEBM'),
              303: ('1080p', 'WEBM'), 248: ('1080p', 'WEBM'), 170: ('1080p', 'WEBM'),
              699: ('1080p', 'MP4'), 399: ('1080p', 'MP4'), 299: ('1080p', 'MP4'),
              137: ('1080p', 'MP4'), 334: ('720p', 'WEBM'), 302: ('720p', 'WEBM'),
              247: ('720p', 'WEBM'), 169: ('720p', 'WEBM'), 698: ('720p', 'MP4'),
              398: ('720p', 'MP4'), 298: ('720p', 'MP4'), 136: ('720p', 'MP4'),
              333: ('480p', 'WEBM'), 246: ('480p', 'WEBM'), 245: ('480p', 'WEBM'),
              244: ('480p', 'WEBM'), 219: ('480p', 'WEBM'), 218: ('480p', 'WEBM'),
              168: ('480p', 'WEBM'), 697: ('480p', 'MP4'), 397: ('480p', 'MP4'),
              212: ('480p', 'MP4'), 135: ('480p', 'MP4'), 332: ('360p', 'WEBM'),
              243: ('360p', 'WEBM'), 167: ('360p', 'WEBM'), 696: ('360p', 'MP4'),
              396: ('360p', 'MP4'), 134: ('360p', 'MP4'), 331: ('240p', 'WEBM'),
              242: ('240p', 'WEBM'), 695: ('240p', 'MP4'), 395: ('240p', 'MP4'),
              133: ('240p', 'MP4'), 330: ('144p', 'WEBM'), 278: ('144p', 'WEBM'),
              694: ('144p', 'MP4'), 394: ('144p', 'MP4'), 160: ('144p', 'MP4')}

AUDIO_ITAG = {                                          #FIXME
    258: ("384kbps", 'MP4'),
    172: ("256kbps", 'WEBM'),
    141: ("256kbps", 'MP4'),
    256: ("192kbps", 'MP4'),
    251: ("160kbps", 'WEBM'),
    171: ("128kbps", 'WEBM'),
    140: ("128kbps", 'MP4'),
    250: ("70kbps", 'WEBM'),
    249: ("50kbps", 'WEBM'),
    139: ("48kbps", 'MP4'),
}

DEFAULT_VIDEO_QUALITY = '1080p'
DEFAULT_VIDEO_EXT = 'WEBM'
DEFAULT_AUDIO_QUALITY = '256kbps'
DEFAULT_AUDIO_EXT = 'WEBM'

HDR = [330, 331, 332, 333, 334, 335, 336, 337]
_3D = [82, 83, 84, 85, 100, 101, 102]
LIVE = [91, 92, 93, 94, 95, 96, 132, 151]
