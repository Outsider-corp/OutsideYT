import json
import os
import random
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# import undetected_chromedriver as uc
import webbrowser
import pickle

from oyt_info.settings import Settings

text_extensions = [".txt"]
video_extensions = [".mp4", ".avi"]
image_extensions = [".pjp", ".jpg", ".pjpeg", ".jpeg", ".jfif", ".png"]
wait_time = 5


def google_login(login: str, driver: webdriver):
    try:
        login = login.split('@')[0]
        filename = f"{login}_cookies"
        url = "https://youtube.com"
        url_log = "https://accounts.google.com/"
        url1 = "https://bot.sannysoft.com/"
        driver.get(url)
        driver.implicitly_wait(7)
        print("start hearing...")
        time.sleep(20)
        while True:
            if driver.current_url.find("www.youtube.com/watch") != -1:
                break
        if not os.path.exists("oyt_info/"):
            os.mkdir("oyt_info/")
        pickle.dump(driver.get_cookies(), open(f"oyt_info/{filename}", "wb"))
        # subprocess.call(["attrib", "+h", f"oyt_info/{filename}"])
        settings.add_account(login)
    except Exception as e:
        print("Error!\n", e)
    finally:
        # driver.close()
        driver.quit()


def upload_video(driver, user, video, preview=None, title=None,
                 description=None, playlist=None, tags=None,
                 ends="random", cards=1, publ_time=None,
                 access=0, save_title=False):
    """
    :param driver: Объект драйвера
    :param user: Имя пользователя
    :param video: папка с данными для видео
    :param preview: Превью
    :param title: Название
    :param description: Описание
    :param playlist: Плейлист
    :param tags: теги
    :param ends: import (default) - импортировать конечные заставки из другого видео (рандомного),
    random - рандомные конечные заставки из стандартных
    :param cards: int - количество подсказок, которые нужно добавить в видео (на рандомных моментах)
    :param publ_time: время публикации
    :param access: 0 - приватное, 1 - доступ по ссылке, 2 - открытое.
    Используется, если publ_time = None (не указано)
    :param save_title: Bool - использовать ли название файла с видео в качестве названия
    :param save_preview: Bool - использовать ли стандартное превью
    :return:
    """
    try:
        url = "https://youtube.com"
        url2 = "https://studio.youtube.com/"
        driver.get(url)
        driver.implicitly_wait(wait_time)
        for cookie in pickle.load(open(f"oyt_info/{user}_cookies", "rb")):
            driver.add_cookie(cookie)
        driver.implicitly_wait(wait_time)

        driver.get(url2)
        driver.implicitly_wait(wait_time//2)

        driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
        driver.implicitly_wait(wait_time)

        path = os.path.join(settings.vids_folder, user, video)
        vid = find_files(video_extensions, folder=path)
        driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(os.path.abspath(os.path.join(path, vid)))
        driver.implicitly_wait(wait_time)

        if not title:
            title = find_files(text_extensions, folder=path, name="Title")
        title_el = driver.find_element(By.XPATH, f'//*[@id="title-textarea"]/'
                                                 f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                 f'*[@slot="body"]/*[@id="input"]/div')
        if title:
            time.sleep(1)
            title_el.clear()
            title_el.send_keys(title)
        elif title_el.text != ".".join(vid.split(".")[:-1]) and save_title:
            title_el.clear()
            title_el.send_keys(".".join(vid.split(".")[:-1]))

        if not description:
            description = find_files(".txt", folder=path, name="Description")
        description_el = driver.find_element(By.XPATH, f'//*[@id="description-textarea"]/'
                                                       f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                       f'*[@slot="body"]/*[@id="input"]/div')
        time.sleep(5)
        description_old = description_el.text
        description_el.clear()
        if description_old:
            descs_del = "\n\n"
        else:
            descs_del = ""
        description_el.send_keys("".join([description, descs_del, description_old]))

        if not preview:
            preview = find_files(image_extensions, folder=path)
        if preview:
            try:
                driver.find_element(By.XPATH, f'//input[@id="file-loader"]').send_keys(
                    os.path.abspath(os.path.join(path, preview)))
                driver.implicitly_wait(wait_time)
            except Exception:
                print("Превью невозможно загрузить")

        if not playlist:
            playlist = find_files(text_extensions, folder=path, name="Playlist").split("\n")
        if playlist:
            try:
                playlist_el = driver.find_element(By.XPATH, f'//ytcp-text-dropdown-trigger'
                                                            f'[@class="dropdown style-scope'
                                                            f' ytcp-video-metadata-playlists"]')
                playlist_el.click()
                driver.implicitly_wait(wait_time // 2)
                if not isinstance(playlist, (tuple, list)):
                    playlist = [playlist]
                for i in playlist:
                    try:
                        playlist_el.find_element(By.XPATH, f'//span[@class="label label-text'
                                                           f' style-scope ytcp-checkbox-group" and'
                                                           f' contains(text(), "{i.rstrip()}")]').click()
                    except:
                        print(f"No playlist: {i}")
            except Exception as e:
                print("Произошла ошибка на этапе добавления видео в плейлисты")
                print(e)
            finally:
                try:
                    driver.find_element(By.XPATH,
                                        f'//*[@class="done-button action-button style-scope ytcp-playlist-dialog"]/div').click()
                    driver.implicitly_wait(wait_time // 2)
                except:
                    pass

        if not tags:
            tags = find_files(text_extensions, folder=path, name="Tags")
        if tags:
            driver.find_element(By.XPATH, f'//*[@id="toggle-button"]').click()
            driver.implicitly_wait(wait_time)
            tags_el = driver.find_element(By.XPATH, f'//*[@id="tags-container"]/'
                                                    f'*[@id="outer"]/*[@id="child-input"]/'
                                                    f'*[@slot="body"]/*[@id="chip-bar"]/div/*[@id="text-input"]')
            tags_el.send_keys(tags)
            driver.implicitly_wait(wait_time)

        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(wait_time)

        # Добавить добавление подсказок

        if ends:
            try:
                driver.find_element(By.XPATH, f'//*[@id="endscreens-button"]').click()
                driver.implicitly_wait(wait_time)

                ends_el = driver.find_element(By.XPATH,
                                              f'//*[@id="cards-row"]')
                if ends == "import":
                    end_el = ends_el.find_elements(By.XPATH, f'//*[@class="title'
                                                             f' style-scope ytve-endscreen'
                                                             f'-template-picker"]')[0]
                elif ends == "random":
                    while True:
                        end_num = random.randint(0, 5)
                        end_el = ends_el.find_elements(By.XPATH, f'//*[@class="title'
                                                                 f' style-scope ytve-endscreen'
                                                                 f'-template-picker"]')[end_num]
                        if "playlist" not in end_el.text.lower() and "плейлист" not in end_el.text.lower():
                            break
                end_el.find_element(By.XPATH, "..").click()
                driver.implicitly_wait(wait_time // 2)
                time.sleep(2)
                driver.find_element(By.XPATH, f'//*[@id="save-button"]').click()
                driver.implicitly_wait(wait_time // 2)
                time.sleep(2)
            except Exception as e:
                print(f"Невозможно поставить конечные заставки\n{e}")

        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
        driver.implicitly_wait(wait_time // 2)

        if publ_time:
            pass
        else:
            publ_el = driver.find_element(By.XPATH, f'//*[@id="privacy-radios"]')
            if access == 0:
                publ_el.find_element(By.XPATH, f'//*[@name="PRIVATE"]').click()
            elif access == 1:
                publ_el.find_element(By.XPATH, f'//*[@name="UNLISTED"]').click()
                video_url = driver.find_element(By.XPATH, f'//span[@class="video-url-fadeable'
                                                          f' style-scope ytcp-video-info"]/a').text
                print(video_url)
            elif access == 2:
                publ_el.find_element(By.XPATH, f'//*[@name="PUBLIC"]').click()

        driver.implicitly_wait(wait_time // 2)
        while True:
            try:
                driver.find_element(By.XPATH, f'//ytcp-video-upload-progress[@checks-summary-status-v2='
                                              f'"UPLOAD_CHECKS_DATA_SUMMARY_STATUS_COMPLETED"]')
                break
            except:
                continue
        driver.find_element(By.XPATH, f'//ytcp-button[@id="done-button"]').click()
        driver.implicitly_wait(wait_time)
        print(f"\033[32m\033[1mВидео {video} было успешно загружено!\033[0m")
    except Exception as e:
        print("Error!")
        print(e)


def find_files(args: list, folder: str, name: str = ""):
    for file in os.listdir(folder):
        if file.endswith(tuple(args)) and file.startswith(name):
            if ".txt" in args:
                with open(os.path.join(folder, file), "r", encoding="UTF-8") as f:
                    return f.read()
            return file
    print("File not founded")
    return None


def change_def_title(account: str, title: str):
    pass


def change_def_description(account: str, description: str):
    pass


def change_def_tags(account: str, tags):
    pass


def change_def_access(account: str, access: int):
    """
    :param account: Название аккаунта
    :param access: 0 - приватное, 1 - доступ по ссылке, 2 - открытое
    :return:
    """
    pass


def get_playlists(account: str):
    pass


def start():
    global settings
    settings = Settings()


if __name__ == "__main__":
    start()
    driver_options = webdriver.ChromeOptions()
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
                 f" AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    driver_options.add_argument(
        f"user-agent={user_agent}")
    driver_options.add_argument("--disable-blink-features=AutomationControlled")

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
    driver = webdriver.Chrome(executable_path="chromedriver111.exe",
                              options=driver_options)

    # stealth(driver, user_agent, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
    #         webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True,
    #         run_on_insecure_origins=True)
    login = "outsider.deal3"
    # google_login(login, driver)
    upload_video(driver, login, "1", ends="import")
