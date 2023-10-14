import asyncio
import os
import pickle
import random
import sys
import time
from functools import partial
from typing import Dict, List

import aiohttp
import playwright.async_api
import requests

import selenium.common.exceptions
import webbrowser
import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from playwright.async_api import async_playwright, Playwright

from outside.YT.download_model import OutsideDownloadVideoYT
from outside.exceptions import BrowserClosedError, NotFoundCookiesError, OutdatedCookiesError
from outside.functions import get_video_id, calc_time_from_string
from outside.message_boxes import error_func, waiting_func
from OutsideYT import project_folder, SAVE_COOKIES_TIME, WAIT_TIME_URL_UPLOADS, \
    chromedriver_location, app_settings_watchers, app_settings_uploaders, YT_URL, YT_STUDIO_URL, \
    VIDEO_WATCH_TIMEOUT, chrome_playwright_location

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class DriverContextSelenium:
    def __init__(self, headless: bool = True, download_dir: str = '', gpu: bool = False,
                 images: bool = False, audio: bool = False, add_args: List = None, **kwargs):
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
        if not self.driver:
            self.driver = webdriver.Chrome(executable_path=chromedriver_location,
                                           options=self.driver_options)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()


class BrowserContextPlayWright:
    def __init__(self, pw: Playwright, cookies: List = None, headless: bool = True,
                 download_dir: str = '',
                 gpu: bool = False,
                 images: bool = False, audio: bool = False, add_args: List = None, **kwargs):
        self.pw = pw
        self.options = {
            'headless': headless,
            'executable_path': chrome_playwright_location,
            'timeout': VIDEO_WATCH_TIMEOUT * 1000
        }
        add_args = add_args or []
        if download_dir:
            self.options['downloads_path'] = download_dir
        if not gpu:
            add_args.append('--disable-gpu')
        if not images:
            add_args.append('--disable-software-rasterizer')
        if not audio:
            add_args.append('--mute-audio')
        if add_args:
            self.options['args'] = add_args
        self.browser = None
        self.cookies = cookies

    async def __aenter__(self):
        if not self.browser:
            self.browser = await self.pw.chromium.launch(**self.options)
            self.context = await self.browser.new_context()
            if self.cookies:
                await self.context.add_cookies(self.cookies)
        return self.context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()


def update_cookies(cookies: List[dict], cookies_file: str):
    save_time = int(time.time() + SAVE_COOKIES_TIME)
    cookies_login = []
    for i, val in enumerate(cookies):
        if 'name' in val:
            cookies[i]['expiry'] = save_time
            cookies_login.append(cookies[i])
    pickle.dump(cookies_login, open(cookies_file, 'wb'))

async def check_cookies_playwright(page: playwright.async_api.Page):
    avatar = await page.query_selector('button[id="avatar-btn"]') is not None
    return avatar


def get_google_login(login: str, mail: str, folder: str):
    added = False
    try:
        with DriverContextSelenium(headless=False, images=True) as driver:
            filename = f'{login}_cookies'
            driver.get(YT_URL)
            driver.implicitly_wait(7)
            time.sleep(15)
            while True:
                time.sleep(1)
                if 'www.youtube.com/watch' in driver.current_url:
                    break
            cookies = driver.get_cookies()
            update_cookies(cookies, os.path.join(project_folder, 'outside', 'oyt_info',
                                                 folder.lower(), filename))
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
        with DriverContextSelenium(headless=driver_headless, images=not driver_headless,
                                   gpu=not driver_headless) as driver:
            driver.get(YT_URL)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            for cookie in pickle.load(
                    open(f'outside/oyt_info/{app_settings_uploaders.__str__()}/{user}_cookies',
                         'rb')):
                driver.add_cookie(cookie)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)

            driver.get(YT_STUDIO_URL)
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
        with DriverContextSelenium(gpu=True, images=True, headless=False) as driver:
            not_add_urls = []
            driver.get(YT_URL)
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


async def watching_selenium(url: str, duration: int, user: str, driver_headless: bool = True,
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
        with DriverContextSelenium(headless=driver_headless) as driver:
            url_yt = 'https://www.youtube.com/'
            driver.get(url_yt)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            file_cookies = f'outside/oyt_info/{app_settings_watchers.__str__()}/{user}_cookies'
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
            for _ in range(duration):
                try:
                    driver.current_url
                except:
                    raise Exception(f'Driver was closed.')
                await asyncio.sleep(1)
                if progress_inc:
                    await progress_inc()
    except BaseException as e:
        print(f"Error. \n {e}")


async def watching_playwright(url: str, duration: int, user: str, driver_headless: bool = True,
                              progress_inc=None):
    """
    Start watching video with Playwright on url link by group watchers.

    Args:
        url: str - link of YT video
        duration: int - duration on video
        user: str - watchers group
        driver_headless: bool - headless argument for driver
        progress_inc: function - function to increment progress_bar value
    """
    try:
        async with (async_playwright() as pw):
            file_cookies = f'outside/oyt_info/{app_settings_watchers.__str__()}/{user}_cookies'
            if not os.path.exists(file_cookies):
                raise NotFoundCookiesError(file_cookies)
            cookies = pickle.load(open(file_cookies, 'rb'))
            async with BrowserContextPlayWright(pw, headless=driver_headless,
                                                cookies=cookies) as browser:
                page = await browser.new_page()
                await page.goto(YT_URL, wait_until='domcontentloaded')
                if not await check_cookies_playwright(page):
                    raise OutdatedCookiesError(user)
                cookies = await page.context.cookies()
                update_cookies(cookies, file_cookies)
                await page.goto(url, timeout=VIDEO_WATCH_TIMEOUT * 1000,
                                wait_until='domcontentloaded')
                await asyncio.sleep(1)
                settings_button = f'xpath=//button[@class="ytp-button ytp-settings-button"]'
                await page.locator(settings_button).click()
                qualities = await page.query_selector_all(
                    f'xpath=//div[@class="ytp-panel-menu"]/div')
                await qualities[-1].click()
                qss = (f'xpath=//div[@class="ytp-panel ytp-quality-menu"]'
                       f'/div[@class="ytp-panel-menu"]/div')
                await page.wait_for_selector(qss, state='attached')
                qual_select = await page.query_selector_all(qss)
                try:
                    await qual_select[-2].click()
                except Exception as e:
                    print(e)
                await asyncio.sleep(1)
                await page.locator('//button[@class="ytp-play-button ytp-button"]').click()
                await asyncio.sleep(0.5)
                await page.locator(settings_button).click()
                # xpath = "//div[@class=\'ytp-play-progress ytp-swatch-background-color\']"
                # script = (f'document.evaluate("{xpath}", document, null, '
                #           f'XPathResult.FIRST_ORDERED_NODE_TYPE, null)'
                #           f'.singleNodeValue.style["transform"]')
                time_xpath = f'//span[@class="ytp-time-current"]'

                real_duration_str = await page.text_content(f'//span[@class="ytp-time-duration"]')
                real_duration = calc_time_from_string(real_duration_str)
                old_progress_value = 0
                while old_progress_value < real_duration:
                    try:
                        time_left = await page.text_content(time_xpath)
                    except:
                        raise BrowserClosedError()
                    if progress_inc:
                        # progress_value = int(
                        #     float(style.replace('scaleX(', '').replace(')', '')) * 100)
                        progress_value = calc_time_from_string(time_left)
                        if old_progress_value != progress_value:
                            await progress_inc(progress_value - old_progress_value)
                            old_progress_value = progress_value
                return True
    except NotFoundCookiesError as e:
        print(f'File cookies not found: {e.cookies}')
    except OutdatedCookiesError as e:
        print(f'Cookies are outdated for user: {e.user}')
    except BrowserClosedError:
        print('Browser was closed.')
    except BaseException as e:
        print(f"Error. \n {e}")
    return False


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


def open_video_in_browser(url):
    target = f'https://youtu.be/{url}'
    webbrowser.open(target)


if __name__ == '__main__':
    driver_options = webdriver.ChromeOptions()
    user_agent = (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  f' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    driver_options.add_argument(
        f'user-agent={user_agent}')

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
