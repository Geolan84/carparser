from pages.base_page import BasePage
from pages.locators import ItemPageLocators
import random
import time


class ItemPage(BasePage):

    def get_info(self):
        self.go_to_page()
        time.sleep(random.randrange(35, 55))
        return self.driver.page_source
