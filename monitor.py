import time

import pyttsx3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from utils import config
from utils.log import logger
from visa import Visa


def init_driver():
    profile = {
        "profile.default_content_setting_values.notifications": 2  # block notifications
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.implicitly_wait(1)
    driver.delete_all_cookies()
    return driver


def monitor():
    try:
        driver = init_driver()
        visa = Visa(driver)
        visa.go_to_appointment_page()
        visa.login()
        visa.go_to_book_appointment()
        visa.select_centre(config.CENTER[0], config.CENTER[1], config.CENTER[2])
        while True:
            dates = visa.check_available_dates()
            if dates:
                logger.info(f"DAY AVAILABLE: {dates}")
                pyttsx3.speak(f"say day available {dates}")
                time.sleep(120)
            else:
                logger.info(f"NO DAY AVAILABLE..")
                time.sleep(config.TIMEOUT)
                driver.refresh()

    except Exception as e:
        logger.error(f'Monitor runtime error. {e}')
        monitor()


if __name__ == "__main__":
    monitor()
