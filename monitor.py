import time
import telebot
from utils import config
from utils.log import logger
from visa import Visa
from selenium import webdriver

bot = telebot.TeleBot(config.BOT_TOKEN)


def init_driver():
    profile = {
        "profile.default_content_setting_values.notifications": 2  # block notifications
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', profile)

    # chrome_options.add_argument("--user-data-dir=/Users/vxwong/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def monitor():
    try:
        driver = init_driver()
        visa = Visa(driver)
        visa.go_to_appointment_page()
        visa.login()
        visa.go_to_book_appointment()
        visa.select_centre('England', 'Manchester', 'Normal')
        while True:
            dates = visa.check_available_dates()
            if dates:
                logger.info(f"DAY AVAILABLE: {dates}")
                bot.send_message(chat_id=config.CHAT_ID, text=f'DAY AVAILABLE: {dates}')
                # driver.back()
            else:
                logger.info(f"NO DAY AVAILABLE..")
                time.sleep(config.TIMEOUT)
                driver.refresh()

    except Exception as e:
        logger.error(f'Monitor runtime error. {e}')
        monitor()


def test_notify():
    try:
        bot.send_message(chat_id=config.CHAT_ID, text='hello, test ok')
    except Exception as e:
        logger.error(
            f'Test notify error. please make sure that you\'ve sent a message to wongs_bot if you didn\'t change the CHAT_ID in the config.\n\n {e}')
        exit(0)


if __name__ == "__main__":
    test_notify()
    monitor()
