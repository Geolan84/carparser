from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver, url: str):
        self.driver = driver
        self.url = url

    def find_element(self, locator,time=10):
        return WebDriverWait(self.driver,time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator,time=10):
        return WebDriverWait(self.driver,time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def go_to_page(self):
        return self.driver.get(self.url)