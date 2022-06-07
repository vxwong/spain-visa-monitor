from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Basic:
    def __init__(self, driver):
        self.driver = driver

    def click_el(self, xpath=None, id=None, name=None, text=None):
        locator = None
        if xpath:
            locator = (By.XPATH, xpath)
        elif id:
            locator = (By.ID, id)
        elif name:
            locator = (By.NAME, name)
        else:
            locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(locator), message="No element").click()

    def wait_for_loading(self):
        WebDriverWait(self.driver, 10).until(ec.invisibility_of_element_located((By.ID, "overlay")))

    def enter_message(self, message, xpath=None, id=None, name=None, text=None):
        if xpath:
            locator = (By.XPATH, xpath)
        elif id:
            locator = (By.ID, id)
        elif name:
            locator = (By.NAME, name)
        else:
            locator = (By.XPATH, "//*[contains(text(), '{}')]".format(text))
        element = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(locator),
                                                       message="No element {}".format(locator))
        element.clear()
        element.send_keys(message)

    def wait_for_secs(self, secs=1):
        WebDriverWait(self.driver, secs)
