from pages.base_page import BasePage
from pages.locators import LoginPageLocators
from selenium.webdriver.common.keys import Keys
import random
import time


class LoginPage(BasePage):

    def login(self, login, password):
        self.go_to_page()
        self._login_by_form(login, password)

    def logout(self):
        self.driver.get('https://bid.cars/ru/user/logout')

    def _login_by_form(self, login, password):
        time.sleep(random.randrange(3, 5))
        login_field = self.find_element(LoginPageLocators.EMAIL_FIELD)
        login_field.clear()
        time.sleep(random.randrange(2, 4))
        login_field.send_keys(login)
        time.sleep(random.randrange(2, 5))
        password_field = self.find_element(LoginPageLocators.PASSWORD_FIELD)
        password_field.clear()
        time.sleep(random.randrange(2, 4))
        password_field.send_keys(password)
        time.sleep(random.randrange(2, 5))
        password_field.send_keys(Keys.ENTER)
