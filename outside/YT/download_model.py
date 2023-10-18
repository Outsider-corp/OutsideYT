import http.client
import json
import os
import subprocess
from typing import Dict, List

import requests
from bs4 import BeautifulSoup as bs

from OYT_Settings import FFMPEG_LOCATION, DEFAULT_CHUNK_SIZE, VIDEO_DOWNLOAD_TIMEOUT, \
    VIDEO_DOWNLOAD_MAX_RETRIES, ACCESS_TOKEN
import outside.video_qualities
from outside.exceptions import StatusCodeRequestError, RequestMethodTypeError, MaxRetriesError, \
    NoAvailableQualityError, StopActionError
from outside.functions import get_video_id, get_video_link, check_folder_name


class OutsideDownloadVideoYT:
    """Creates object of download video."""
    full_data = b"{'context': {'client': {'androidSdkVersion': 30, 'clientName': 'ANDROID_EMBEDDED_PLAYER', 'clientScreen': 'EMBED', 'clientVersion': '17.31.35'}}}"
    base_headers = {'Content-Type': 'application/json',
                    'User-Agent': 'com.google.android.apps.youtube.music/'}

    __FFMPEG_LOCATION = FFMPEG_LOCATION
    __CHUNK_SIZE = DEFAULT_CHUNK_SIZE
    __TIMEOUT = VIDEO_DOWNLOAD_TIMEOUT or 10
    __MAX_TRIES = VIDEO_DOWNLOAD_MAX_RETRIES or 3
    __VIDEO_ITAGS = outside.video_qualities.VIDEO_ITAG
    __AUDIO_ITAGS = outside.video_qualities.AUDIO_ITAG
    __SIMPLE_VIDEO_ITAGS = outside.video_qualities.SIMPLE_VIDEO_ITAG
    __DEFAULT_VIDEO_QUALITY = outside.video_qualities.DEFAULT_VIDEO_QUALITY
    __DEFAULT_VIDEO_EXT = outside.video_qualities.DEFAULT_VIDEO_EXT
    __DEFAULT_AUDIO_QUALITY = outside.video_qualities.DEFAULT_AUDIO_QUALITY
    __DEFAULT_PREFER = outside.video_qualities.DEFAULT_PREFER_QUALITY
    __DEFAULT_K_MS_TO_SIZE = 200

    def __init__(self, link: str, params: Dict, video_info=None,
                 api_video_info=None,
                 ffmpeg_location: str = None,
                 callback_func=None,
                 callback_info=None,
                 callback_err=None,
                 _stop=None):
        """
        Initialization of class.
        Args:
            link: str - youtube video link
            params: Dict - parameters of download video. Has keys 'simple', 'video', 'audio',
                    'prefer', 'download_type'.
            'simple': True/False (simple download without connecting video&audio),
            'video':{
                'video_quality' - quality of video part
                    (4320p, 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p, Any)
                'video_ext' - extension of video part (MP4, WEBM, Any)},
            'audio':{
                'audio_quality' - quality of audio part (384, 256, 192, 168, 128, 70, 50, 48, Any)
                'audio_ext' - extension of audio part(MP4, WEBM, Any)}
            'prefer' - (
                'best' - best of available;
                 'worst' - worst of available;
                  'normal' - gets settings from OutsideYT,
                  'equals' - settings only equals to sent)
            'download_type' - (
                'full' - download video with audio,
                'audio' - download only audio,
                'video' - download only video)
            'if_exists' - action if output video_file is already exists
            ('replace' - delete old video and add a new, 'add' - add video with "_n" suffix,
            'nothing' - don't download video)
            video_info: Dict - parsed info from video page
            ffmpeg_location: str - ffmpeg.exe location
            callback_func - function that will be called on every step of downloading
            callback_info - function that will be called on changing type of process
            callback_err - function that will be called on errors
            _stop - check if process was stopped from outside
        """
        self.video_id = get_video_id(link)
        self.link = get_video_link(self.video_id, 'embed')
        self._player_video_info = video_info
        self._api_video_info = api_video_info
        self.params = params
        self._itags = None
        self._itags_api = None
        self.ffmpeg_location = ffmpeg_location or OutsideDownloadVideoYT.__FFMPEG_LOCATION
        self._callback = callback_func
        self._callback_info = callback_info
        self._callback_err = callback_err
        self.__progress_size = None
        self.__api_key = os.environ.get('YT_KEY', ACCESS_TOKEN)

        def _stop_():
            if _stop():
                raise StopActionError()

        self.__stop = _stop_

    @property
    def api_video_info(self):
        if self._api_video_info is None:
            self._api_video_info = self._post_video_info()
        return self._api_video_info

    @property
    def player_video_info(self):
        if self._player_video_info is None:
            self._player_video_info = self._get_video_info()
        return self._player_video_info

    @staticmethod
    def _get_quality_itags(vars: Dict, quality: str = None, ext: str = None, choice: str = 'better',
                           normal_q: str = '', normal_ext: str = ''):
        if quality:
            quality = quality.split()[0]
        if quality.lower() == 'any':
            quality = None
        if ext.lower() == 'any':
            ext = None
        if choice.lower() == 'worse':
            rev_keys = list(vars.keys())[::-1]
            vars = {key: vars[key] for key in rev_keys}
        elif choice.lower() == 'normal':
            quality = normal_q.split()[0]
            ext = normal_ext
        elif choice.lower() == 'equals':
            vars = {key: val for key, val in vars if val[0] == quality}
        if ext:
            vars = {key: val for key, val in vars.items() if val[1] == ext}
        keys = list(vars.keys())
        if quality:
            for key in keys:
                if vars[key][0] != quality:
                    vars.pop(key)
                else:
                    break
        return list(vars.keys())

    @classmethod
    def get_player_video_info(cls, link: str, *args, **kwargs):
        res = requests.get(link)
        return cls.get_player_video_info_with_response(link, res.text, *args, **kwargs)

    @classmethod
    def get_player_video_info_with_response(cls, link: str, response_text, *args, **kwargs):
        soup = bs(response_text, 'html.parser')
        script_tags = soup.find_all('script', {'nonce': True})
        video_info_raw = dict()
        for script_tag in script_tags:
            script_text = script_tag.get_text()
            if ('cards' in args and 'cards' not in video_info_raw and
                    'ytInitialData' in script_text):
                try:
                    ytInitialData = json.loads(script_text.replace(
                        'var ytInitialData = ', '')[:-1])
                    cards_panels = ytInitialData['engagementPanels']
                    for panel in cards_panels:
                        if 'panelIdentifier' in panel[
                            'engagementPanelSectionListRenderer'] and panel[
                            'engagementPanelSectionListRenderer'][
                            'panelIdentifier'] == 'engagement-panel-structured-description':
                            cards_content = panel['engagementPanelSectionListRenderer'][
                                'content']['structuredDescriptionContentRenderer']
                            if 'items' in cards_content:
                                cards_items = cards_content['items']
                            else:
                                video_info_raw['cards'] = {}
                                break
                            for cards in cards_items:
                                if 'videoDescriptionInfocardsSectionRenderer' in cards:
                                    cards_list = cards[
                                        'videoDescriptionInfocardsSectionRenderer'][
                                        'infocards']
                                    video_info_raw['cards'] = dict()
                                    for ind, card in enumerate(cards_list):
                                        card_info = card['compactInfocardRenderer']['content'][
                                            'structuredDescriptionVideoLockupRenderer']
                                        video_info_raw['cards'].update({
                                            get_video_id(card_info[
                                                             'navigationEndpoint'][
                                                             'commandMetadata'][
                                                             'webCommandMetadata'][
                                                             'url']): int(
                                                ytInitialData['cards']['cardCollectionRenderer'][
                                                    'cards'][ind]['cardRenderer']['cueRanges'][0][
                                                    'startCardActiveMs'])})
                                    break
                            break
                except KeyError:
                    video_info_raw['cards'] = {}
            elif ('link' not in video_info_raw
                  and 'ytInitialPlayerResponse' in script_text):
                ytInitialPlayerResponse = json.loads(script_text.replace(
                    'var ytInitialPlayerResponse = ', '')[:-1])
                video_info_raw.update(ytInitialPlayerResponse['videoDetails'])
                video_info_raw['link'] = link
                if 'streamingData' in args:
                    video_info_raw.update(ytInitialPlayerResponse['streamingData'])
                if 'cards' not in args:
                    return video_info_raw
            if 'cards' in video_info_raw and 'link' in video_info_raw:
                return video_info_raw

    @classmethod
    def get_api_video_info(cls, link: str, api_key, headers=None, **kwargs):
        data = cls.full_data
        base_headers = cls.base_headers
        if headers:
            base_headers.update(headers)
        url = (f'https://www.youtube.com/youtubei/v1/player?'
               f'videoId={get_video_id(link)}&key={api_key}&'
               f'contentCheckOk=True&racyCheckOk=True')
        res = requests.post(url, data=data, headers=base_headers)
        if res.status_code == 200:
            data = res.json()
            return data
        else:
            raise StatusCodeRequestError(res.reason)

    def _get_api_video_info(self, link: str, headers=None, **kwargs):
        return self.get_api_video_info(link, api_key=self.__api_key, headers=headers, **kwargs)

    def _find_itag(self, itags: List, video_info: Dict):
        if 'streamingData' in video_info:
            video_info = {fmt: val for fmt, val in video_info['streamingData'].items() if
                          isinstance(video_info['streamingData'], dict)}
        for itag in itags:
            for fmt in ['formats', 'adaptiveFormats']:
                for i, video_itag in enumerate(video_info[fmt]):
                    if video_itag['itag'] == itag:
                        if 'contentLength' not in video_itag:
                            video_itag['contentLength'] = self.__get_video_size(video_itag)
                        return video_itag
        raise NoAvailableQualityError()

    def get_itags_from_params(self, video_info):
        ans = []
        if self.params['simple'] and self.params['download_type'] == 'full':
            params = self.params.get('video', {})
            itags_list = self._get_quality_itags(vars=self.__SIMPLE_VIDEO_ITAGS,
                                                 quality=params.get('video_quality', ''),
                                                 ext=params.get('video_ext', ''),
                                                 choice=params.get('prefer', self.__DEFAULT_PREFER),
                                                 normal_q=self.__DEFAULT_VIDEO_QUALITY,
                                                 normal_ext=self.__DEFAULT_VIDEO_EXT)
            ans.append(self._find_itag(itags_list, video_info))
        else:
            if self.params['download_type'] != 'audio':
                params = self.params.get('video', {})
                v_itags = self._get_quality_itags(self.__VIDEO_ITAGS,
                                                  params.get('video_quality', ''),
                                                  params.get('video_ext', ''),
                                                  params.get('full_quality', self.__DEFAULT_PREFER),
                                                  self.__DEFAULT_VIDEO_QUALITY,
                                                  self.__DEFAULT_VIDEO_EXT)
                ans.append(self._find_itag(v_itags, video_info))
            if self.params['download_type'] != 'video':
                params = self.params.get('audio', {})
                a_itags = self._get_quality_itags(self.__AUDIO_ITAGS,
                                                  params.get('audio_quality', ''),
                                                  params.get('audio_ext', ''),
                                                  params.get('full_quality', self.__DEFAULT_PREFER),
                                                  self.__DEFAULT_AUDIO_QUALITY,
                                                  self.__DEFAULT_VIDEO_EXT)
                ans.append(self._find_itag(a_itags, video_info))
        return ans

    def _post_video_info(self, headers=None, **kwargs):
        return self._get_api_video_info(self.link, headers=headers, **kwargs)

    def _get_video_info(self, *args, **kwargs):
        return self.get_player_video_info(self.link, *args, **kwargs)

    def _execute_request(self, url: str,
                         method: str,
                         timeout: int = __TIMEOUT,
                         add_headers: Dict = None,
                         data=None,
                         stream=False):
        headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
        if add_headers:
            headers.update(add_headers)
        if data:
            if not isinstance(data, bytes):
                data = bytes(json.dumps(data), encoding='UTF-8')
        if not url.lower().startswith('http'):
            raise ValueError("Invalid URL")
        if method.lower() == 'get':
            return requests.get(url, data=data, headers=headers, timeout=timeout, stream=stream)
        elif method.lower() == 'post':
            return requests.post(url, data=data, headers=headers, timeout=timeout, stream=stream)
        else:
            raise RequestMethodTypeError()

    def _stream(self, link: str, file_size: int, timeout: int = __TIMEOUT,
                max_retries: int = __MAX_TRIES):
        downloaded = 0
        while downloaded < file_size:
            stop_pos = min(downloaded + self.__CHUNK_SIZE, file_size) - 1
            tries = 0

            while True:
                if tries >= max_retries:
                    raise MaxRetriesError()
                try:
                    response = self._execute_request(link + f'&range={downloaded}-{stop_pos}',
                                                     method='GET',
                                                     timeout=timeout,
                                                     stream=True)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.RequestException:
                    raise
                except http.client.IncompleteRead:
                    pass
                else:
                    break
                tries += 1

            key_add = False
            for chunk in response.iter_content(chunk_size=self.__CHUNK_SIZE):
                if chunk:
                    key_add = True
                    downloaded += len(chunk)
                    yield chunk
            if not key_add:
                break
        return

    def __download_one_format(self, url: str, filesize: int, saving_path: str,
                              timeout: int = __TIMEOUT, max_retries: int = __MAX_TRIES,
                              downloaded: int = 0):
        with open(saving_path, 'wb') as file:
            try:
                for chunk in self._stream(url, timeout=timeout,
                                          max_retries=max_retries, file_size=filesize):
                    self.__stop()
                    file.write(chunk)
                    downloaded += len(chunk)
                    if self._callback and self.__progress_size:
                        self._callback(int(downloaded / self.__progress_size * 100))
            except requests.exceptions.HTTPError as e:
                raise

    def download_video(self, saving_path: str, use_api: bool = True, **kwargs):
        """
        Download video with API (or without).
        Args:
            saving_path: str - saving path for the video
            use_api: bool - use YouTube API or not
        """
        try:
            self.__stop()
            if use_api:
                if self._itags_api is None:
                    self._itags_api = self.get_itags_from_params(self.api_video_info)
                itags = self._itags_api
                video_info = self.api_video_info
            else:
                if self._itags is None:
                    self._itags = self.get_itags_from_params(self.player_video_info)
                itags = self._itags
                video_info = self.player_video_info
            self.__stop()
            files = []
            self.__progress_size = sum([int(i['contentLength']) for i in itags])
            filename = os.path.join(saving_path,
                                    f'{check_folder_name(video_info["videoDetails"]["title"])}')
            downloaded = 0
            for i, itag in enumerate(itags):
                url = itag['url']
                filesize = int(itag['contentLength'])
                ext = itag['mimeType'].split(';')[0].split('/')[1].lower()
                file_path = os.path.join(f'{filename}_{i if len(itags) == 2 else ""}.{ext}')
                files.append(file_path)
                self.__download_one_format(url, filesize, file_path, downloaded=downloaded)
                downloaded = filesize
                if i == 1:
                    self._add_video_audio(*files, f'{filename}.{ext}')
            return True
        except StopActionError:
            pass
        except Exception as e:
            self._callback_err(f'Error on download video!\n{e}')
        return False

    def __get_video_size(self, video_info):
        try:
            url = video_info['url']
            resp = requests.head(url, allow_redirects=True)
            if resp.status_code == 200:
                if 'Content-Length' in resp.headers:
                    return int(resp.headers['Content-Length'])
        except (KeyError, IndexError, ValueError) as e:
            pass
        return self.__DEFAULT_K_MS_TO_SIZE * video_info['approxDurationMs']

    def update_params(self, params: Dict):
        self.params = params

    def create_params(self, **kwargs):
        ...

    def _add_video_audio(self, file1: str, file2: str, output_file: str):
        try:
            if_exists = self.params['if_exists']
            if if_exists != 'nothing':
                if if_exists == 'replace':
                    if os.path.exists(output_file):
                        os.remove(output_file)
                elif if_exists == 'add':
                    i = 1
                    of = output_file
                    while os.path.exists(of):
                        of_list = output_file.split('.')
                        of = f'{of_list[0]}_{i}.{of_list[1]}'
                        i += 1
                    output_file = of
                self.__stop()
                command = [self.__FFMPEG_LOCATION,
                           '-i', file1,
                           '-i', file2,
                           '-c:v', 'copy',
                           '-c:a', 'copy',
                           output_file]
                subprocess.run(command)
        finally:
            os.remove(file1)
            os.remove(file2)

    @classmethod
    def add_video_audio(cls, file1: str, file2: str, output_file: str):
        command = [cls.__FFMPEG_LOCATION,
                   '-i', file1,
                   '-i', file2,
                   '-c:v', 'copy',
                   '-c:a', 'copy',
                   output_file]
        subprocess.run(command)
        os.remove(file1)
        os.remove(file2)
