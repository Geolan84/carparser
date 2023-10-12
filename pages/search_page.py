import time
import random

from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from pages.locators import SearchPageLocators

class SearchPage(BasePage):

    def search(self, limit=10):
        self.go_to_page()
        time.sleep(random.randrange(5, 10))
        return self.open_full(limit)
        

    def open_full(self, limit):
        actions = ActionChains(self.driver)
        counter = 0
        while limit != 0 and counter < limit:
            counter += 1
            try:
                button = self.find_element(SearchPageLocators.LOAD_MORE_BUTTON)
                actions.move_to_element(button).perform()
                button.click()
                time.sleep(random.randrange(6, 10))
            except:
                break

        
        actions.move_to_element(self.find_element(SearchPageLocators.FOOTER, 5)).perform()
        time.sleep(random.randrange(6, 10))
        return self.driver.page_source
