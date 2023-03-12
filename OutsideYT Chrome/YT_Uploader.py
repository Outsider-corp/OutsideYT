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
        url = "https://accounts.google.com/"
        login = login.split('@')[0]
        driver.get(url)
        driver.implicitly_wait(7)
        while True:
            try:
                driver.find_element(by=By.CLASS_NAME, value="wVreme")
                break
            except:
                continue
        if not os.path.exists("oyt_info/"):
            os.mkdir("oyt_info/")
        filename = f"{login}_cookies"
        pickle.dump(driver.get_cookies(), open(f"oyt_info/{filename}", "wb"))
        # subprocess.call(["attrib", "+h", f"oyt_info/{filename}"])
        settings.add_account(login)
    except Exception as e:
        print("Error!\n", e)
    finally:
        driver.close()
        driver.quit()

def start():
    global settings
    settings = Settings()


if __name__ == "__main__":
    start()
    useragent = UserAgent()
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    driver_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              options=driver_options)
    login = "outside.tested"
    google_login(login, driver)
