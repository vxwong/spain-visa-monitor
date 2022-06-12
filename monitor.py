import time

import pyttsx3
import undetected_chromedriver

from utils import config
from utils.log import logger
from visa import Visa


def init_driver():
    profile = {
        "profile.default_content_setting_values.notifications": 2  # block notifications
    }
    chrome_options = undetected_chromedriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")

    driver = undetected_chromedriver.Chrome(options=chrome_options)
    driver.implicitly_wait(1)
    driver.delete_all_cookies()
    return driver


def monitor():
    try:
        driver = init_driver()
        visa = Visa(driver)
        visa.go_to_appointment_page()
        time.sleep(config.CLOUDFLARE_TIME_OUT)
        visa.login()
        visa.go_to_book_appointment()
        visa.select_centre(config.CENTER[0], config.CENTER[1], config.CENTER[2])
        while True:
            dates = visa.check_available_dates()
            if dates:
                logger.info(f"DAY AVAILABLE: {dates}")
                pyttsx3.speak(f"DAY AVAILABLE {dates}")
                time.sleep(120)
            else:
                logger.info(f"NO DAY AVAILABLE..")
                time.sleep(config.TIMEOUT)
                driver.refresh()

    except Exception as e:
        logger.error(f'Monitor runtime error. {e}')
        monitor()


if __name__ == "__main__":
    pyttsx3.speak("Notification test OK")
    monitor()
