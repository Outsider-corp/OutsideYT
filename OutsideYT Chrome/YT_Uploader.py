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
        url1 = "https://bot.sannysoft.com/"
        driver.get(url)
        driver.implicitly_wait(7)
        print("start hearing...")
        while True:
            try:
                driver.find_element(By.ID, "top-level-buttons-computed")
                # Проверить, открыто ли видео, тогда выход
                # driver.window_handles
                # break
            except:
                time.sleep(20)
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
                 access=0, publ_time=0):
    url = "https://youtube.com"
    driver.get(url)
    driver.implicitly_wait(7)
    # for cookie in pickle.load(open(f"oyt_info/{user}_cookies", "rb")):
    #     driver.add_cookie(cookie)
    with open("oyt_info/1_cookies", "r") as f:
        driver.add_cookie(json.load(f))
    driver.implicitly_wait(7)
    driver.refresh()
    # upload_button = driver.find_element(By.XPATH, '//*[@id="upload-icon"]')
    # upload_button.click()
    # driver.implicitly_wait(7)
    time.sleep(39)


def start():
    global settings
    settings = Settings()


if __name__ == "__main__":
    start()
    # driver_options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    # driver_options.add_argument(
    #     f"user-agent={user_agent}")
    # driver_options.add_argument("--disable-blink-features=AutomationControlled")

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-save-password-bubble')
    options.add_argument('--disable-translate')
    # options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-logging')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--mute-audio')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')
    options.add_argument(
        f'--user-agent={user_agent}')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(executable_path="chromedriver111.exe",
                              options=options)


    # stealth(driver, user_agent, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
    #         webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True,
    #         run_on_insecure_origins=True)
    login = "outside.tested"
    # google_login("romikfedkov", driver)
    upload_video(driver, login, f"videos/{login}/vid1.mp4")

