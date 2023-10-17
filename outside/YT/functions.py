import asyncio
import os
import pickle
import random
import sys
import time
from functools import partial
from typing import List

import aiohttp
import playwright.async_api
import requests

import selenium.common.exceptions
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from playwright.async_api import async_playwright, Playwright
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from outside.YT.download_model import OutsideDownloadVideoYT
from outside.exceptions import BrowserClosedError, NotFoundCookiesError, OutdatedCookiesError
from outside.functions import calc_time_from_string
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
    try:
        avatar = await page.query_selector('button[id="avatar-btn"]') is not None
        return avatar
    except:
        return False


def get_google_login(login: str, mail: str, folder: str):
    added = False
    try:
        with DriverContextSelenium(headless=False, images=True, gpu=True, audio=True) as driver:
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


def upload_video(user: str, title: str, video: str, access: int, save_title: bool,
                 publish: str = None, description: str = None, playlist: str = None,
                 preview: str = None, tags: str = None, ends: str = None, cards: int = None,
                 driver_headless: bool = True, _callback_func=None, _callback_info=None,
                 _callback_error=None):
    """
    Uploads one video to YouTube.
    Args:
        user: str - username, on which account need to upload video
        title: str - title of video
        publish: str - publish time
        video: str - path to the video file
        description: str - description of video
        playlist: str - playlist on the channel
        preview: str - path to preview
        tags: str - list of tags
        ends: import (default) - import ends from last video,
                random - random ends from standard set
        cards: int - count of cards that needs to add to the video
        access: 0 - private, 1 - access by link, 2 - open.
        Used if publ_time = None
        save_title: bool - use filename as name of video on YT
        driver_headless: bool - enable headless
        callback_func - callback of process
        callback_info - callback with sending current stage info
        callback_error - callback on errors
    :return:
    """
    stage_count = 18
    curr_stage = 1

    if not _callback_func:
        _callback_func = lambda x: ...
    if not _callback_info:
        _callback_info = lambda x: ...
    if not _callback_error:
        _callback_error = lambda x: ...

    try:
        with (DriverContextSelenium(headless=driver_headless, images=not driver_headless,
                                    gpu=not driver_headless) as driver):
            _callback_info("Connecting to YT")
            _callback_func(int(curr_stage/stage_count*100))
            curr_stage+=1
            driver.get(YT_URL)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            for cookie in pickle.load(
                    open(f'{app_settings_uploaders.cookies_folder}/{user}_cookies', 'rb')):
                driver.add_cookie(cookie)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.get(YT_STUDIO_URL)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
            if 'accounts.google.com' in driver.current_url:
                raise OutdatedCookiesError(user)
            _callback_info("Fill info about video")
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(video)
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
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
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            description_el = driver.find_element(By.XPATH, f'//*[@id="description-textarea"]/'
                                                           f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                           f'*[@slot="body"]/*[@id="input"]/div')
            time.sleep(5)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            description_old = description_el.text
            description_el.clear()
            descs_del = '\n\n' if description_old else ''
            description_el.send_keys(''.join([description, descs_del, description_old]))
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            if preview:
                try:
                    driver.find_element(By.XPATH, f'//input[@id="file-loader"]').send_keys(preview)
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
                except Exception as e:
                    print(f"Can't upload preview.\n{e}")
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
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
                    print('Error on add video to playlists')
                    print(e)
                finally:
                    try:
                        driver.find_element(By.XPATH,
                                            f'//*[@class="done-button action-button style-scope ytcp-playlist-dialog"]/div').click()
                        driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    except:
                        pass
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            if tags:
                driver.find_element(By.XPATH, f'//*[@id="toggle-button"]').click()
                driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
                tags_el = driver.find_element(By.XPATH, f'//*[@id="tags-container"]/'
                                                        f'*[@id="outer"]/*[@id="child-input"]/'
                                                        f'*[@slot="body"]/*[@id="chip-bar"]/div/*[@id="text-input"]')
                driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
                tags_count = driver.find_element(By.ID, 'tags-count')
                tags_int = int(tags_count.text.split('/')[0])
                av_len = 500 - tags_int
                tags_list = tags.split(',')
                for i, tag in enumerate(tags_list):
                    if len(tag) <= av_len:
                        av_len -= len(tag) + 1
                    else:
                        tags_list = tags_list[:i]
                        break
                if tags_list:
                    tags_el.send_keys(','.join(tags_list))
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1

            # TODO Need to add cards

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
                            end_el.find_element(By.XPATH, '..').click()
                            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                            save_button = driver.find_element(By.ID, 'save-button')
                            if save_button.get_attribute('disabled'):
                                driver.find_element(By.ID, 'discard-button').click()
                                driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                            else:
                                break
                    driver.find_element(By.ID, 'save-button').click()
                    driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
                    time.sleep(2)
                except Exception as e:
                    print(f"Can't add endscreens.\n{e}")
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            if publish:
                driver.find_element(By.XPATH,
                                    f'//tp-yt-paper-radio-button['
                                    f'@name="SCHEDULE"]').click()
                driver.implicitly_wait(0.5)
                driver.find_element(By.XPATH, f'//ytcp-text-dropdown-trigger['
                                              f'@id="datepicker-trigger"]').click()
                driver.implicitly_wait(0.5)
                date_input = driver.find_element(By.XPATH, f'//div[@id="control-area"]/'
                                                           f'form[@id="form"]/*[@id="textbox"]')
                date_input.click()
                date_input.send_keys(webdriver.Keys.CONTROL + 'a')
                date_input.send_keys(webdriver.Keys.BACKSPACE)
                date_input.send_keys(publish.split()[0])
                date_input.submit()

                time_el = driver.find_element(By.XPATH, f'//ytcp-form-input-container['
                                                        f'@id="time-of-day-container"]//'
                                                        f'*[@id="textbox"]')
                time_el.click()
                time_input = time_el.find_element(By.XPATH, f'//input[@class="style-scope'
                                                            f' tp-yt-paper-input"]')
                time_input.send_keys(webdriver.Keys.CONTROL + 'a')
                time_input.send_keys(webdriver.Keys.BACKSPACE)
                time_input.send_keys(publish.split()[1])
                time_input.submit()

            else:
                publ_el = driver.find_element(By.XPATH, f'//*[@id="privacy-radios"]')
                if access == 'Private':
                    publ_el.find_element(By.XPATH, f'//*[@name="PRIVATE"]').click()
                elif access == 'On link':
                    publ_el.find_element(By.XPATH, f'//*[@name="UNLISTED"]').click()
                    video_url = driver.find_element(By.XPATH, f'//span[@class="video-url-fadeable'
                                                              f' style-scope ytcp-video-info"]'
                                                              f'/a').text
                elif access == 'Public':
                    publ_el.find_element(By.XPATH, f'//*[@name="PUBLIC"]').click()
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS // 2)

            _callback_info("Uploading video")
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            while True:
                try:
                    if publish:
                        text = driver.find_element(By.XPATH, f'//span[@class="progress-label'
                                                             f' style-scope ytcp-video'
                                                             f'-upload-progress"]').text
                        if '%' in text:
                            continue
                    else:
                        driver.find_element(By.XPATH,
                                            f'//ytcp-video-upload-progress[@checks-summary-status-v2='
                                            f'"UPLOAD_CHECKS_DATA_SUMMARY_STATUS_COMPLETED"]')
                    break
                except:
                    continue
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            while True:
                try:
                    driver.find_element(By.XPATH, f'//ytcp-button[@id="done-button"]').click()
                    break
                except:
                    pass
            driver.implicitly_wait(WAIT_TIME_URL_UPLOADS)
            _callback_func(int(curr_stage / stage_count * 100))
            curr_stage += 1
            print(f'\033[32m\033[1mVideo {os.path.basename(video)} was successfully upload!\033[0m')
            return True
    except OutdatedCookiesError as e:
        _callback_error(f'Cookies are dead for user {e.user}...')
    except Exception as e:
        _callback_error(f"Error.\n {e}")
    return False


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


async def watching_playwright(url: str, user: str, driver_headless: bool = True,
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
        async with async_playwright() as pw:
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
