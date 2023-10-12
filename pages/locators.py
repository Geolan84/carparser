from selenium.webdriver.common.by import By

class LoginPageLocators():
    EMAIL_FIELD = (By.ID, 'exampleInputEmail1')
    PASSWORD_FIELD = (By.ID, 'exampleInputPassword1')
    SIGN_IN_BUTTON = (By.CLASS_NAME, 'btn btn-primary g-recaptcha')


class SearchPageLocators():
    LOGOUT = (By.CLASS_NAME, 'dropdown-item logout')
    MENU = (By.ID, 'dropdownMenuProfile')
    LOAD_MORE_BUTTON = (By.LINK_TEXT, "Загрузить больше...")
    FOOTER = (By.CLASS_NAME, 'footer-bg-new')

class ItemPageLocators():
    pass