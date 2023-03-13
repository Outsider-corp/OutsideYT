import time

# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import pickle


youtube = "https://www.youtube.com/"
agent = "https://wtools.io/ru/check-my-user-agent"
ip = "https://2ip.ru"
login = "https://accounts.google.com/"

useragent = UserAgent()
driver_options = webdriver.ChromeOptions()
# driver_options.add_argument(f"user-agent={useragent.random}")
driver_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
driver_options.add_argument("--disable-blink-features=AutomationControlled")
# driver_options.add_argument(f"--proxy-server=203.24.102.11:0080")
driver = webdriver.Chrome(executable_path="chromedriver110.exe",
                          options=driver_options)


try:
    driver.get(url=youtube)
    # login_button = driver.find_element(by=By.CLASS_NAME, value="yt-spec-touch-feedback-shape__fill")
    # time.sleep(10)
    # login_button.click()
    # time.sleep(60)
    # pickle.dump(driver.get_cookies(), open(f"cookies", "wb"))

    for cookie in pickle.load(open("cookies", "rb")):
        driver.add_cookie(cookie)

    time.sleep(5)

    driver.refresh()

    time.sleep(50)

except Exception as e:
    print(e)

finally:
    driver.close()
    driver.quit()
