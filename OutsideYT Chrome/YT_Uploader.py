import json
import os
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium_stealth import stealth
# import undetected_chromedriver as uc
import webbrowser
import pickle

from oyt_info.settings import Settings


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


def upload_video(driver, user, video, preview=None, title=None, description=None, playlist=None, tags=None, ends=None,
                 access=0, publ_time=0, save_title=False, def_title=False):
    url = "https://youtube.com"
    url2 = "https://studio.youtube.com/"
    driver.get(url)
    driver.implicitly_wait(7)
    for cookie in pickle.load(open(f"oyt_info/{user}_cookies", "rb")):
        driver.add_cookie(cookie)
    driver.implicitly_wait(7)

    driver.get(url2)
    driver.implicitly_wait(7)

    driver.find_element(By.XPATH, '//*[@id="upload-icon"]').click()
    driver.implicitly_wait(7)

    path = f"videos/{user}/{video}/"
    vid = find_files(".mp4", ".avi", folder=path)
    driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(os.path.abspath(path + vid))
    driver.implicitly_wait(7)

    if not save_title:
        if not title:
            title = find_files(".txt", folder=path, name="Title")
        title_el = driver.find_element(By.XPATH, f'//*[@id="title-textarea"]/'
                                                 f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                 f'*[@slot="body"]/*[@id="input"]/div')
        if title_el.text == ".".join(vid.split(".")[:-1]) or not def_title:
            title_el.clear()
            title_el.send_keys(title)

    if not description:
        description = find_files(".txt", folder=path, name="Description")
    description_el = driver.find_element(By.XPATH, f'//*[@id="description-textarea"]/'
                                                   f'*[@id="container"]/*[@id="outer"]/*[@id="child-input"]/'
                                                   f'*[@slot="body"]/*[@id="input"]/div')
    description_old = description_el.text
    description_el.clear()
    if description_old:
        descs_del = "\n\n"
    else:
        descs_del = ""
    description_el.send_keys("".join([description, descs_del, description_old]))

    time.sleep(40)


def find_files(*args, folder, name: str = ""):
    for file in os.listdir(folder):
        if file.endswith(args) and file.startswith(name):
            if args.count(".txt"):
                with open(folder + file, "r", encoding="UTF-8") as f:
                    return f.read()
            return file
    print("File not founded")


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
