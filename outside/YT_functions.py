import asyncio
import contextlib
import json
import os
import pickle
import random
import sys
import time

import requests
import selenium.common.exceptions
from asyncselenium.webdriver.chrome.async_webdriver import AsyncChromeDriver
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By

from outside.message_boxes import error_func, waiting_func
from OutsideYT import project_folder, save_cookies_time, wait_time_url_uploads

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_driver(add_args: list = None, gpu: bool = False, images: bool = False, audio: bool = False,
               headless: bool = True):
    """Return driver for Selenium with added options."""
    driver_options = webdriver.ChromeOptions()
    user_agent = (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  f' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    driver_options.add_argument(
        f'user-agent={user_agent}')
    driver_options.add_argument('--disable-blink-features=AutomationControlled')
    driver_options.add_argument('--blink-settings=imagesEnabled=false')
    if not gpu:
        driver_options.add_argument('--disable-gpu')
    if not images:
        driver_options.add_argument('--disable-software-rasterizer')
    if not audio:
        driver_options.add_argument('--mute-audio')
    if headless:
        driver_options.add_argument('--headless')
    if add_args:
        for arg in add_args:
            driver_options.add_argument(arg)
    return webdriver.Chrome(executable_path=
                            os.path.join(project_folder, 'outside', 'bin', 'chromedriver.exe'),
                            options=driver_options)


def get_google_login(login: str, mail: str, folder: str):
    added = False
    try:
        driver = get_driver(headless=False, images=True)
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
                cookies[i]['expiry'] = int(time.time() + save_cookies_time)
        pickle.dump(cookies,
                    open(os.path.join(project_folder, 'outside', 'oyt_info',
                                      folder.lower(), filename), 'wb'))
        # subprocess.call(["attrib", "+h", f"oyt_info/{filename}"])
        added = True
    except Exception as e:
        error_func(f'An error occurred while trying to login.\n\n{e}')
    finally:
        with contextlib.suppress(Exception):
            driver.quit()
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
        driver = get_driver(headless=driver_headless, images=not driver_headless,
                            gpu=not driver_headless)
        url = 'https://youtube.com'
        url2 = 'https://studio.youtube.com/'
        driver.get(url)
        driver.implicitly_wait(wait_time_url_uploads)
        for cookie in pickle.load(open(f'outside/oyt_info/uploaders/{user}_cookies', 'rb')):
            driver.add_cookie(cookie)
        driver.implicitly_wait(wait_time_url_uploads)

        driver.get(url2)
        driver.implicitly_wait(wait_time_url_uploads // 2)

        driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
        driver.implicitly_wait(wait_time_url_uploads)

        driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(video)
        driver.implicitly_wait(wait_time_url_uploads)

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
                driver.implicitly_wait(wait_time_url_uploads)
            except Exception:
                print('Превью невозможно загрузить')

        if playlist:
            try:
                playlist_el = driver.find_element(By.XPATH, f'//ytcp-text-dropdown-trigger'
                                                            f'[@class="dropdown style-scope'
                                                            f' ytcp-video-metadata-playlists"]')
                playlist_el.click()
                driver.implicitly_wait(wait_time_url_uploads // 2)
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
                    driver.implicitly_wait(wait_time_url_uploads // 2)
                except:
                    pass

        if tags:
            driver.find_element(By.XPATH, f'//*[@id="toggle-button"]').click()
            driver.implicitly_wait(wait_time_url_uploads)
            tags_el = driver.find_element(By.XPATH, f'//*[@id="tags-container"]/'
                                                    f'*[@id="outer"]/*[@id="child-input"]/'
                                                    f'*[@slot="body"]/*[@id="chip-bar"]/div/*[@id="text-input"]')
            tags_el.send_keys(tags)
            driver.implicitly_wait(wait_time_url_uploads)

        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(wait_time_url_uploads)

        # Добавить добавление подсказок

        if ends:
            try:
                driver.find_element(By.XPATH, f'//*[@id="endscreens-button"]').click()
                driver.implicitly_wait(wait_time_url_uploads)

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
                driver.implicitly_wait(wait_time_url_uploads // 2)
                time.sleep(2)
                driver.find_element(By.XPATH, f'//*[@id="save-button"]').click()
                driver.implicitly_wait(wait_time_url_uploads // 2)
                time.sleep(2)
            except Exception as e:
                print(f'Невозможно поставить конечные заставки\n{e}')

        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(wait_time_url_uploads // 2)

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

        driver.implicitly_wait(wait_time_url_uploads // 2)
        while True:
            try:
                driver.find_element(By.XPATH,
                                    f'//ytcp-video-upload-progress[@checks-summary-status-v2='
                                    f'"UPLOAD_CHECKS_DATA_SUMMARY_STATUS_COMPLETED"]')
                break
            except:
                continue
        driver.find_element(By.XPATH, f'//ytcp-button[@id="done-button"]').click()
        driver.implicitly_wait(wait_time_url_uploads)
        print(f'\033[32m\033[1mВидео {os.path.basename(video)} было успешно загружено!\033[0m')
    except Exception as e:
        print('Error!')
        print(e)


def get_video_info(link):
    """Функция для получения информации о видео (название и канал)."""
    response = requests.get(link)
    # with open("123.html", "w", encoding="UTF-8") as f:
    #     f.write(response.text)
    # return
    if response.status_code == 200:
        soup = bs(response.text, 'html.parser')
        script_tags = soup.find_all('script', {'nonce': True})
        video = channel = duration = None
        for script_tag in script_tags:
            script_text = script_tag.get_text()
            if not video and 'ytInitialData' in script_text:
                ytInitialData = json.loads(script_text.replace('var ytInitialData = ',
                                                               '')[:-1])
                video_info = \
                    ytInitialData['playerOverlays']['playerOverlayRenderer']['videoDetails'][
                        'playerOverlayVideoDetailsRenderer']
                video = video_info['title']['simpleText']
                channel = video_info['subtitle']['runs'][0]['text']
                continue
            if not duration and 'ytInitialPlayerResponse' in script_text:
                ytInitialPlayerResponse = json.loads(
                    script_text.replace('var ytInitialPlayerResponse = ', '')[:-1])
                duration = int(ytInitialPlayerResponse['streamingData']['formats'][0][
                                   'approxDurationMs']) // 1000
        if not (video and channel and duration):
            error_func('Не удалось получить информацию о видео...')
        return video, channel, duration
    else:
        error_func('Нет подключения к сайту')
        return None, None, None


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
        yt_url = 'https://www.youtube.com/'
        not_add_urls = []
        driver = get_driver(gpu=True, images=True, headless=False)
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
    finally:
        with contextlib.suppress(Exception):
            driver.close()
        return ans


def watching(url: str, duration: int, user: str, driver_headless: bool = True):
    """
    Start watching video on url link by group watchers.

    Args:
        url: str - link of YT video
        duration: int - duration on video
        user: str - watchers group
        driver_headless: bool - headless argument for driver.
    """
    try:
        url_yt = 'https://www.youtube.com/'
        driver = get_driver(headless=driver_headless)
        driver.get(url_yt)
        driver.implicitly_wait(wait_time_url_uploads)
        file_cookies = f'outside/oyt_info/watchers/{user}_cookies'
        if not os.path.exists(file_cookies):
            raise Exception(f'Cookies for {user} are not found.')
        cookies = pickle.load(open(file_cookies, 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.implicitly_wait(wait_time_url_uploads)
        driver.get(url)
        driver.implicitly_wait(wait_time_url_uploads)
        button = driver.find_element(By.XPATH, '//button[@class="ytp-play-button ytp-button"]')
        button.click()
        for i in range(duration):
            try:
                driver.current_url
            except:
                raise Exception(f'Driver was closed.')
            time.sleep(1)
            yield 1
        driver.close()
    except BaseException as e:
        error_func(f'Error.\n{e}')
        with contextlib.suppress(Exception):
            driver.close()
    finally:
        with contextlib.suppress(Exception):
            driver.close()
    yield 'End'

async def async_watching(url: str, duration: int, user: str, driver_headless: bool = True,
                   progress_bar=None):
    """
    Start watching video on url link by group watchers.

    Args:
        url: str - link of YT video
        duration: int - duration on video
        user: str - watchers group
        driver_headless: bool - headless argument for driver.
    """
    try:
        url_yt = 'https://www.youtube.com/'
        driver = get_driver(headless=driver_headless)
        await driver.get(url_yt)
        await driver.implicitly_wait(wait_time_url_uploads)
        file_cookies = f'outside/oyt_info/watchers/{user}_cookies'
        if not os.path.exists(file_cookies):
            raise Exception(f'Cookies for {user} are not found.')
        cookies = pickle.load(open(file_cookies, 'rb'))
        for cookie in cookies:
            await driver.add_cookie(cookie)
        await driver.implicitly_wait(wait_time_url_uploads)
        await driver.get(url)
        await driver.implicitly_wait(wait_time_url_uploads)
        button = await driver.find_element(By.XPATH,
                                           '//button[@class="ytp-play-button ytp-button"]')
        await button.click()
        for i in range(duration):
            try:
                await driver.current_url
            except:
                raise Exception(f'Driver was closed.')
            await asyncio.sleep(1)
            # yield 1
        await driver.close()
    except BaseException as e:
        error_func(f'Error.\n{e}')
        with contextlib.suppress(Exception):
            await driver.close()
    finally:
        with contextlib.suppress(Exception):
            await driver.close()
    # yield 'End'


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