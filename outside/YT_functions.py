import asyncio
import http.client
import json
import os
import pickle
import random
import sys
import time
from functools import partial
from typing import List, Dict

import aiohttp
import requests

import selenium.common.exceptions
import webbrowser
import yt_dlp
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By

import OutsideYT
from outside.exceptions import MaxRetriesError, RequestMethodTypeError
from outside.functions import get_video_id, check_folder_name
from outside.message_boxes import error_func, waiting_func
from OutsideYT import project_folder, SAVE_COOKIES_TIME, WAIT_TIME_URL_UPLOADS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class DriverContext:
    def __init__(self, add_args: list = None, gpu: bool = False, images: bool = False,
                 audio: bool = False,
                 headless: bool = True, download_dir: str = ''):
        self.driver_options = webdriver.ChromeOptions()
        user_agent = (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      f' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
        self.driver_options.add_argument(
            f'user-agent={user_agent}')
        self.driver_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver_options.add_argument('--blink-settings=imagesEnabled=false')
        if not gpu:
            self.driver_options.add_argument('--disable-gpu')
        if not images:
            self.driver_options.add_argument('--disable-software-rasterizer')
        if not audio:
            self.driver_options.add_argument('--mute-audio')
        if headless:
            self.driver_options.add_argument('--headless')
        if download_dir:
            self.driver_options.add_argument(f'--download.default_directory={download_dir}')
        if add_args:
            for arg in add_args:
                self.driver_options.add_argument(arg)
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=
                                       os.path.join(project_folder, 'outside', 'bin',
                                                    'chromedriver.exe'),
                                       options=self.driver_options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()


def get_google_login(login: str, mail: str, folder: str):
    added = False
    try:
        with DriverContext(headless=False, images=True) as driver:
            filename = f'{login}_cookies'
            url = 'https://youtube.com'
            driver.get(url)
            driver.implicitly_wait(7)
            time.sleep(15)
            while True:
                time.sleep(1)
                if 'www.youtube.com/watch' in driver.current_url:
                    break
            cookies = driver.get_cookies()
            for i, val in enumerate(cookies):
                if 'expiry' in val:
                    cookies[i]['expiry'] = int(time.time() + SAVE_COOKIES_TIME)
            pickle.dump(cookies,
                        open(os.path.join(project_folder, 'outside', 'oyt_info',
                                          folder.lower(), filename), 'wb'))
            # subprocess.call(["attrib", "+h", f"oyt_info/{filename}"])
            added = True
    except Exception as e:
        error_func(f'An error occurred while trying to login.\n\n{e}')
    return added


def upload_video(user: str, title: str, publish, video: str, description: str, playlist: str,
                 preview: str, tags: str, ends: str, cards: int, access: int, save_title: bool,
                 driver_headless: bool = True):
    """
    :param user: Имя пользователя
    :param title: Название
    :param publish: время публикации
    :param video: папка с данными для видео
    :param description: Описание
    :param playlist: Плейлист
    :param preview: Превью
    :param tags: теги
    :param ends: import (default) - импортировать конечные заставки из предыдушего видео,
    random - рандомные конечные заставки из стандартных
    :param cards: int - количество подсказок, которые нужно добавить в видео (на рандомных моментах)
    :param access: 0 - приватное, 1 - доступ по ссылке, 2 - открытое.
    Используется, если publ_time = None (не указано)
    :param save_title: bool - использовать ли название файла с видео в качестве названия видео
    :param driver_headless: bool - отключить отображение браузеров
    :return:
    """
    try:
        with DriverContext(headless=driver_headless, images=not driver_headless,
                           gpu=not driver_headless) as driver:
            url = 'https://youtube.com'
            url2 = 'https://studio.youtube.com/'
            driver.get(url)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            for cookie in pickle.load(open(f'outside/oyt_info/uploaders/{user}_cookies', 'rb')):
                driver.add_cookie(cookie)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            driver.get(url2)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)

            driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(video)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            title_el = driver.find_element(By.XPATH, f'//*[@id="title-textarea"]/'
                                                     f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                     f'*[@slot="body"]/*[@id="input"]/div')
            if title:
                time.sleep(1)
                title_el.clear()
                title_el.send_keys(title)
            elif title_el.text != '.'.join(os.path.basename(video).split('.')[:-1]) and save_title:
                title_el.clear()
                title_el.send_keys('.'.join(os.path.basename(video).split('.')[:-1]))

            description_el = driver.find_element(By.XPATH, f'//*[@id="description-textarea"]/'
                                                           f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                           f'*[@slot="body"]/*[@id="input"]/div')
            time.sleep(5)
            description_old = description_el.text
            description_el.clear()
            descs_del = '\n\n' if description_old else ''
            description_el.send_keys(''.join([description, descs_del, description_old]))

            if preview:
                try:
                    driver.find_element(By.XPATH, f'//input[@id="file-loader"]').send_keys(preview)
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
                except Exception:
                    print('Превью невозможно загрузить')

            if playlist:
                try:
                    playlist_el = driver.find_element(By.XPATH, f'//ytcp-text-dropdown-trigger'
                                                                f'[@class="dropdown style-scope'
                                                                f' ytcp-video-metadata-playlists"]')
                    playlist_el.click()
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    if not isinstance(playlist, (tuple, list)):
                        pass
                    for i in playlist:
                        try:
                            playlist_el.find_element(By.XPATH, f'//span[@class="label label-text'
                                                               f' style-scope ytcp-checkbox-group" and'
                                                               f' contains(text(), "{i.rstrip()}")]').click()
                        except:
                            print(f'No playlist: {i}')
                except Exception as e:
                    print('Произошла ошибка на этапе добавления видео в плейлисты')
                    print(e)
                finally:
                    try:
                        driver.find_element(By.XPATH,
                                            f'//*[@class="done-button action-button style-scope ytcp-playlist-dialog"]/div').click()
                        driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    except:
                        pass

            if tags:
                driver.find_element(By.XPATH, f'//*[@id="toggle-button"]').click()
                driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
                tags_el = driver.find_element(By.XPATH, f'//*[@id="tags-container"]/'
                                                        f'*[@id="outer"]/*[@id="child-input"]/'
                                                        f'*[@slot="body"]/*[@id="chip-bar"]/div/*[@id="text-input"]')
                tags_el.send_keys(tags)
                driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            # Добавить добавление подсказок

            if ends:
                try:
                    driver.find_element(By.XPATH, f'//*[@id="endscreens-button"]').click()
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

                    ends_el = driver.find_element(By.XPATH,
                                                  f'//*[@id="cards-row"]')
                    if ends == 'import':
                        end_el = ends_el.find_elements(By.XPATH, f'//*[@class="title'
                                                                 f' style-scope ytve-endscreen'
                                                                 f'-template-picker"]')[0]
                    elif ends == 'random':
                        while True:
                            end_num = random.randint(0, 5)
                            end_el = ends_el.find_elements(By.XPATH, f'//*[@class="title'
                                                                     f' style-scope ytve-endscreen'
                                                                     f'-template-picker"]')[end_num]
                            if 'playlist' not in end_el.text.lower() and 'плейлист' not in end_el.text.lower():
                                break
                    end_el.find_element(By.XPATH, '..').click()
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    time.sleep(2)
                    driver.find_element(By.XPATH, f'//*[@id="save-button"]').click()
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    time.sleep(2)
                except Exception as e:
                    print(f'Невозможно поставить конечные заставки\n{e}')

            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)

            if True:
                # if publish:
                #     pass
                # else:
                publ_el = driver.find_element(By.XPATH, f'//*[@id="privacy-radios"]')
                if access == 'Private':
                    publ_el.find_element(By.XPATH, f'//*[@name="PRIVATE"]').click()
                elif access == 'On link':
                    publ_el.find_element(By.XPATH, f'//*[@name="UNLISTED"]').click()
                    video_url = driver.find_element(By.XPATH, f'//span[@class="video-url-fadeable'
                                                              f' style-scope ytcp-video-info"]/a').text
                    print(video_url)
                elif access == 'Public':
                    publ_el.find_element(By.XPATH, f'//*[@name="PUBLIC"]').click()

            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
            while True:
                try:
                    driver.find_element(By.XPATH,
                                        f'//ytcp-video-upload-progress[@checks-summary-status-v2='
                                        f'"UPLOAD_CHECKS_DATA_SUMMARY_STATUS_COMPLETED"]')
                    break
                except:
                    continue
            driver.find_element(By.XPATH, f'//ytcp-button[@id="done-button"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            print(f'\033[32m\033[1mВидео {os.path.basename(video)} было успешно загружено!\033[0m')
    except Exception as e:
        error_func(f"Error.\n {e}")


async def get_video_info(link, session: aiohttp.ClientSession, headers=None, *args, **kwargs):
    """Функция для получения информации о видео."""
    args = args or []
    vid_info = None
    try:
        async with session.get(link, headers=headers) as response:
            if response.status == 200:
                res_text = await response.text()
                vid_info = OutsideDownloadVideoYT.get_player_video_info_with_response(link,
                                                                                      res_text,
                                                                                      *args,
                                                                                      **kwargs)
            else:
                pass
    except Exception as e:
        print(f'Error in video info getting... \n{e}')
    if 'progress_inc' in kwargs:
        await kwargs['progress_inc']()
    return vid_info


async def post_video_info(link, session: aiohttp.ClientSession, headers=None, **kwargs):
    data = OutsideDownloadVideoYT.full_data
    base_headers = OutsideDownloadVideoYT.base_headers
    if headers:
        base_headers.update(headers)
    url = f'https://www.youtube.com/youtubei/v1/player?videoId={get_video_id(link)}&key={OutsideYT.ACCESS_TOKEN}&contentCheckOk=True&racyCheckOk=True'
    async with session.post(url, data=data, headers=base_headers) as res:
        data = await res.json()
    return data


def get_playlist_info(link):
    """Функция для получения информации о всех видео в плейлисте."""
    error_func('This action will be update latter...')


def select_page(type_add: str):
    """
    Функция для получения ссылки на канал (channel),
    видео (video) или всех видео в плейлисте (playlist).

    Args:
        type_add: str - type of added object (video or playlist).
    """
    ans = None
    try:
        with DriverContext(gpu=True, images=True, headless=False) as driver:
            yt_url = 'https://www.youtube.com/'
            not_add_urls = []
            driver.get(yt_url)
            driver.implicitly_wait(3)
            if type_add == 'video':
                url_search = 'www.youtube.com/watch'
            elif type_add == 'channel':
                url_search = 'www.youtube.com/@'
            elif type_add == 'playlist':
                url_search = 'www.youtube.com/playlist'
            else:
                raise 'Not valid type.'
            while True:
                time.sleep(2)
                if url_search in driver.current_url and driver.current_url not in not_add_urls:
                    if waiting_func(f'This is {type_add} you want to add?', 3):
                        ans = driver.current_url
                        driver.close()
                        break
                    not_add_urls.append(driver.current_url)
    except selenium.common.exceptions.NoSuchWindowException:
        pass
    except Exception as e:
        error_func(f'Error.\n{e}')
    return ans


async def watching(url: str, duration: int, user: str, driver_headless: bool = True,
                   progress_inc=None):
    """
    Start watching video on url link by group watchers.

    Args:
        url: str - link of YT video
        duration: int - duration on video
        user: str - watchers group
        driver_headless: bool - headless argument for driver
        progress_inc: function - function to increment progress_bar value
    """
    try:
        with DriverContext(headless=driver_headless) as driver:
            url_yt = 'https://www.youtube.com/'
            driver.get(url_yt)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            file_cookies = f'outside/oyt_info/watchers/{user}_cookies'
            if not os.path.exists(file_cookies):
                raise Exception(f'Cookies for {user} are not found.')
            cookies = pickle.load(open(file_cookies, 'rb'))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            driver.get(url)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            button = driver.find_element(By.XPATH, '//button[@class="ytp-play-button ytp-button"]')
            button.click()
            for i in range(duration):
                try:
                    driver.current_url
                except:
                    raise Exception(f'Driver was closed.')
                await asyncio.sleep(1)
                if progress_inc:
                    await progress_inc()
    except BaseException as e:
        print(f"Error. \n {e}")


def download_image(url: str, path: str):
    res = requests.get(url)
    if res.status_code == 200:
        with open(path, 'wb') as f:
            f.write(res.content)


def _on_progress_download_video_ylp(progress_dict: dict, progress_bar, total_size: int):
    if progress_dict['status'] == 'downloading' and 'downloaded_bytes' in progress_dict:
        progress_bar.setValue(
            int(progress_dict['downloaded_bytes'] / total_size * 100))


def download_video_dlp(videoname: str, link: str, params: dict, saving_path: str, progress_bar,
                       **kwargs):
    try:
        total_size = 1000000
        ylp_options = {'ffmpeg_location': r'outside/bin/ffmpeg.exe',
                       'format': 'bestvideo+bestaudio/best',
                       'outtmpl': os.path.join(saving_path, f'{videoname}.mp4'),
                       'progress_hooks': [
                           partial(_on_progress_download_video_ylp, progress_bar=progress_bar,
                                   total_size=total_size)]}
        with yt_dlp.YoutubeDL(ylp_options) as ydl:
            ydl.download([link])
        return True
    except Exception as e:
        print(f'Error on downloading video...\n{e}')
        return False


class OutsideDownloadVideoYT:
    """Creates object of download video."""
    full_data = b"{'context': {'client': {'androidSdkVersion': 30, 'clientName': 'ANDROID_EMBEDDED_PLAYER', 'clientScreen': 'EMBED', 'clientVersion': '17.31.35'}}}"
    base_headers = {'Content-Type': 'application/json',
                    'User-Agent': 'com.google.android.apps.youtube.music/'}

    __FFMPEG_LOCATION = OutsideYT.FFMPEG_LOCATION
    __CHUNK_SIZE = OutsideYT.DEFAULT_CHUNK_SIZE
    __TIMEOUT = OutsideYT.VIDEO_DOWNLOAD_TIMEOUT or 10
    __MAX_TRIES = OutsideYT.VIDEO_DOWNLOAD_MAX_RETRIES or 3
    __VIDEO_ITAGS = OutsideYT.VIDEO_ITAG
    __AUDIO_ITAGS = OutsideYT.AUDIO_ITAG
    __SIMPLE_VIDEO_ITAGS = OutsideYT.SIMPLE_VIDEO_ITAG
    __DEFAULT_VIDEO_QUALITY = OutsideYT.DEFAULT_VIDEO_QUALITY
    __DEFAULT_VIDEO_EXT = OutsideYT.DEFAULT_VIDEO_EXT
    __DEFAULT_AUDIO_QUALITY = OutsideYT.DEFAULT_AUDIO_QUALITY
    __DEFAULT_AUDIO_EXT = OutsideYT.DEFAULT_AUDIO_EXT

    def __init__(self, link: str, params: Dict, video_info: Dict = None,
                 api_video_info: Dict = None,
                 ffmpeg_location: str = None,
                 progress_bar=None):
        """
        Initialization of class.
        Args:
            link: str - youtube video link
            params: Dict - parameters of download video. Has keys 'simple', 'video', 'audio',
                    'full_quality'.
            'simple': True/False (simple download without connecting video&audio),
            'video':{
                'video_quality' - quality of video part
                    (4320p, 2160p, 1440p, 1080p, 720p, 480p, 360p, 240p, 144p)
                'video_ext' - extension of video part (MP4, WEBM)},
            'audio':{
                'audio_quality' - quality of audio part ()
                'audio_ext' - extension of audio part(MP4, WEBM)}
            'full_quality':{
                'best' - best of available;
                 'worst' - worst of available;
                  'normal' - gets settings from OutsideYT)
            video_info: Dict - parsed info from video page
            ffmpeg_location: str - ffmpeg.exe location
        """
        self.link = link
        self._video_info = video_info
        self._api_video_info = api_video_info
        self.params = params
        self._itags = []
        self._itags_api = []
        self.ffmpeg_location = ffmpeg_location or OutsideDownloadVideoYT.__FFMPEG_LOCATION
        self.progress_bar = progress_bar
        self.__progress_size = None
        self.__api_key = os.environ.get('YT_KEY', OutsideYT.ACCESS_TOKEN)

    @property
    def api_video_info(self):
        if self._api_video_info is None:
            self._api_video_info = self._post_video_info()
        return self._api_video_info

    @property
    def player_video_info(self):
        if self._video_info is None:
            self._video_info = self._get_video_info()
        return self._video_info

    @staticmethod
    def _get_quality_itags(vars: Dict, quality: str, ext: str, choice: str, normal_q: str = '',
                           normal_ext: str = ''):
        if choice == 'best':
            return list(vars.keys())
        elif choice == 'worst':
            return list(vars.keys())[::-1]
        elif choice == 'normal':
            quality = normal_q
            ext = normal_ext
        if ext:
            var = {key: val for key, val in vars.items() if val[1] == ext}
            if var:
                vars = var
        keys = list(vars.keys())
        for key in keys:
            if vars[key][0] != quality:
                vars.pop(key)
            else:
                return list(vars.keys())
        raise ValueError

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
        data = res.json()
        return data

    def _find_itag(self, itags: List, video_info: Dict):
        if 'streamingData' in video_info:
            video_info = {fmt: val for fmt, val in video_info['streamingData']}
        for itag in itags:
            for fmt in ['formats', 'adaptiveFormats']:
                for video_itag in video_info[fmt]:
                    if video_itag['itag'] == itag:
                        return video_itag

    def get_itags_from_params(self, video_info):
        if self.params.get('simple', True):
            params = self.params.get('video', {})
            itags_list = self._get_quality_itags(vars=self.__SIMPLE_VIDEO_ITAGS,
                                                 quality=params.get('video_quality', ''),
                                                 ext=params.get('video_ext', ''),
                                                 choice=params.get('full_quality', 'normal'),
                                                 normal_q=self.__DEFAULT_VIDEO_QUALITY,
                                                 normal_ext=self.__DEFAULT_VIDEO_EXT)
            self._itags = [self._find_itag(itags_list, video_info)]
        else:
            params = self.params.get('video', {})
            v_itags = self._get_quality_itags(self.__VIDEO_ITAGS,
                                              params.get('video_quality', ''),
                                              params.get('video_ext', ''),
                                              params.get('full_quality', 'normal'),
                                              self.__DEFAULT_VIDEO_QUALITY,
                                              self.__DEFAULT_VIDEO_EXT)

            params = self.params.get('audio', {})
            a_itags = self._get_quality_itags(self.__AUDIO_ITAGS,
                                              params.get('audio_quality', ''),
                                              params.get('audio_ext', ''),
                                              params.get('full_quality', 'normal'),
                                              self.__DEFAULT_AUDIO_QUALITY,
                                              self.__DEFAULT_AUDIO_EXT)
            self._itags = [self._find_itag(v_itags, video_info),
                           self._find_itag(a_itags, video_info)]

    def _post_video_info(self, headers=None, **kwargs):
        return self.get_api_video_info(self.link, headers=headers, **kwargs)

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
                    print(f'trying...{tries}')
                    response = self._execute_request(link + f'&range={downloaded}-{stop_pos}',
                                                     method='GET',
                                                     timeout=timeout,
                                                     stream=True)
                    print('excellent 1st execute')
                except requests.exceptions.InvalidURL as e:
                    print(f'{e}')
                    raise
                except http.client.IncompleteRead:
                    pass
                else:
                    break
                tries += 1

            for chunk in response.iter_content(chunk_size=self.__CHUNK_SIZE):
                if chunk:
                    downloaded += len(chunk)
                    print(f'downloaded - {downloaded}')
                    yield chunk
        return

    def _add_video_audio(self, videofile: str, audiofile: str):
        ...

    def __download_one_format(self, url: str, filesize: int, saving_path: str,
                              timeout: int = __TIMEOUT, max_retries: int = __MAX_TRIES):

        with open(saving_path, 'wb') as file:
            try:
                for chunk in self._stream(url, timeout=timeout,
                                          max_retries=max_retries, file_size=filesize):
                    file.write(chunk)
                    if self.progress_bar:
                        self._on_progress_download_video(len(chunk))
            except requests.exceptions.HTTPError as e:
                raise

    def download_video(self, saving_path: str, use_api: bool = True, **kwargs):
        """
        Download video with API (or without).
        Args:
            saving_path: str - saving path for the video
            use_api: bool - use YouTube API or not
        """
        if use_api:
            if not self._itags_api:
                self.get_itags_from_params(self.api_video_info)
            itags = self._itags_api
            video_info = self.api_video_info
        else:
            if not self._itags:
                self.get_itags_from_params(self.player_video_info)
            itags = self._itags
            video_info = self.player_video_info

        files = []
        self.__progress_size = sum([int(i['contentLength']) for i in itags])
        for i, itag in enumerate(itags):
            url = itag['url']
            filesize = itag['contentLength']
            ext = itag['mimeType'].split(';')[0].split('/')[1].lower()
            file_path = os.path.join(saving_path,
                                     f'{check_folder_name(video_info["title"])}'
                                     f'{f"_{i}" if len(itags) == 2 else ""}.{ext}')
            files.append(file_path)
            self.__download_one_format(url, filesize, file_path)

        if len(files) == 2:
            self._add_video_audio(*files)
        return True

    def _on_progress_download_video(self, add_value: int):
        value = 0
        while True:
            value += add_value
            self.progress_bar.setValue(int(value / self.__progress_size * 100))
            if value >= self.__progress_size:
                break
            yield
        return

    def update_params(self, params: Dict):
        self.params = params

    def create_params(self, **kwargs):
        ...


def open_video_in_browser(url):
    target = f'https://youtu.be/{url}'
    webbrowser.open(target)


if __name__ == '__main__':
    driver_options = webdriver.ChromeOptions()
    user_agent = (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  f' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    driver_options.add_argument(
        f'user-agent={user_agent}')
    driver_options.add_argument('--disable-blink-features=AutomationControlled')

    # options = webdriver.ChromeOptions()
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--disable-infobars')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--disable-notifications')
    # options.add_argument('--disable-popup-blocking')
    # options.add_argument('--disable-save-password-bubble')
    # options.add_argument('--disable-translate')
    # options.add_argument('--headless')
    # options.add_argument('--log-level=3')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-logging')
    # options.add_argument('--hide-scrollbars')
    # options.add_argument('--mute-audio')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--incognito')
    # options.add_argument(
    #     f'--user-agent={user_agent}')
    # options.add_argument('--disable-web-security')
    # options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(executable_path='bin/chromedriver.exe',
                              options=driver_options)
    login = 'outsider.deal3'
    # google_login(login, driver)
    # upload_video(driver, login, "1", ends="import")
