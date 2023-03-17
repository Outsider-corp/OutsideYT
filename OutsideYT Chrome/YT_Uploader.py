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
                 ends="random", end_duration=20,
                 access=0, publ_time=0, save_title=False):
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
    :param end_duration: длительность конечных заставок (20)
    :param access: 0 - приватное, 1 - доступ по ссылке, 2 - открытое
    :param publ_time:
    :param save_title: Bool - использовать ли название файла с видео в качестве названия
    :param save_preview: Bool - использовать ли стандартное превью
    :return:
    """
    url = "https://youtube.com"
    url2 = "https://studio.youtube.com/"
    driver.get(url)
    driver.implicitly_wait(7)
    for cookie in pickle.load(open(f"oyt_info/{user}_cookies", "rb")):
        driver.add_cookie(cookie)
    driver.implicitly_wait(7)

    driver.get(url2)
    driver.implicitly_wait(4)

    driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
    driver.implicitly_wait(7)

    path = os.path.join(settings.vids_folder, user, video)
    print(path)
    vid = find_files(video_extensions, folder=path)
    driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(os.path.abspath(os.path.join(path, vid)))
    driver.implicitly_wait(7)

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
            driver.implicitly_wait(7)
        except Exception:
            print("Превью невозможно загрузить")

    # Добавить добавление в плейлисты

    if not tags:
        tags = find_files(text_extensions, folder=path, name="Tags")
    if tags:
        driver.find_element(By.XPATH, f'//*[@id="toggle-button"]').click()
        driver.implicitly_wait(4)
        tags_el = driver.find_element(By.XPATH, f'//*[@id="tags-container"]/'
                                                f'*[@id="outer"]/*[@id="child-input"]/'
                                                f'*[@slot="body"]/*[@id="chip-bar"]/div/*[@id="text-input"]')
        tags_el.send_keys(tags)
        driver.implicitly_wait(4)

    driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
    driver.implicitly_wait(4)
    if ends:
        try:
            driver.find_element(By.XPATH, f'//*[@id="endscreens-button"]').click()
            driver.implicitly_wait(4)

            if ends == "import":
                pass
            elif ends == "random":
                ends_el = driver.find_elements(By.XPATH,
                                               f'//*[@class="card style-scope ytve-endscreen-template-picker"]')
                print(ends_el)
                while True:
                    end_num = random.randint(0, len(ends_el) - 1)
                    print(end_num)
                    if "Playlist" not in \
                            ends_el[end_num].find_element(By.XPATH,
                            f'//*[@class="title style-scope ytve-endscreen-template-picker]').text\
                            and "Плейлист" not in \
                            ends_el[end_num].find_element(By.XPATH,
                            f'//*[@class="title style-scope ytve-endscreen-template-picker]').text:
                        ends_el[end_num].click()
                        break

            driver.implicitly_wait(4)
            time.sleep(2)
            driver.find_element(By.XPATH, f'//*[@id="save-button"]').click()
            driver.implicitly_wait(4)
        except Exception as e:
            print(f"Невозможно поставить конечные заставки\n"
                  f"{e}")

    driver.find_element(By.XPATH, f'//*[@id="next-button"]').click()
    driver.implicitly_wait(4)


    time.sleep(40)


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
    upload_video(driver, login, "1")
