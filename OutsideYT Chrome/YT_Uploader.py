import os
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import pickle

from oyt_info.settings import Settings


def google_login(login: str, driver: webdriver):
    try:
        url = "https://youtube.com"
        login = login.split('@')[0]
        filename = f"{login}_cookies"
        driver.get(url)
        driver.implicitly_wait(7)
        while True:
            try:

                # Проверить, открыто ли видео, тогда выход
                # driver.window_handles
                cookies = driver.get_cookies()
                continue
            except:
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


def upload_video(driver, user, video, preview=None, title=None, description=None, playlist=None, tags=None, ends=None, access=0, publ_time=0):
    driver.get("https://youtube.com")
    driver.implicitly_wait(7)
    for cookie in pickle.load(open(f"oyt_info/{user}_cookies", "rb")):
        driver.add_cookie(cookie)
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
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    driver_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              options=driver_options)
    login = "outside.tested"
    # google_login(login, driver)
    upload_video(driver, login, f"videos/{login}/vid1.mp4")
