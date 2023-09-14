import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pageObjects import registrationPage, accountPage, mainPage
from TestData.SQLDatabase import SQLFunctions
from TestData.secrets import Secrets


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    set_first_password = (By.ID, "app_user_set_password_password_first")
    confirm_password = (By.ID, "app_user_set_password_password_second")
    login_button_first = (By.XPATH, "//button[@class='button -primary -login m-t-30 m-b-10']")
    login_button = (By.CSS_SELECTOR, "button[class='button -primary -login m-t-30 m-b-45']")
    username = (By.ID, "_username")
    password = (By.ID, "_password")
    incorrect_popup = (By.XPATH, "/html/body/div[1]/section[2]/div/form/div[1]")
    captcha = (By.CLASS_NAME, 'captcha_image')
    captcha_validation = (By.CSS_SELECTOR, "span[class='color-error validation-error']")
    captcha_input = (By.ID, 'captcha')

    def inputFirstPassword(self, text):
        self.driver.find_element(*LoginPage.set_first_password).send_keys(text)

    def inputConfirmPassword(self, text):
        self.driver.find_element(*LoginPage.confirm_password).send_keys(text)

    def getSavePasswordButton(self):
        return self.driver.find_element(*LoginPage.login_button_first)

    def inputUsername(self, text):
        self.driver.find_element(*LoginPage.username).send_keys(text)

    def inputPassword(self, text):
        self.driver.find_element(*LoginPage.password).send_keys(text)

    def getLogginButton(self):
        self.driver.find_element(*LoginPage.login_button).click()

    def getToAccountPage(self):
        self.driver.find_element(*LoginPage.login_button).click()
        account_page = accountPage.AccountPage(self.driver)
        return account_page

    def getPopup(self):
        return self.driver.find_element(*LoginPage.incorrect_popup)

    def getCaptchaInput(self):
        return self.driver.find_element(*LoginPage.captcha_input)

    def getCaptchaValidation(self):
        return self.driver.find_element(*LoginPage.captcha_validation)


    def getToMainPageWithLogging(self, version):
        sql_function = SQLFunctions()
        password = Secrets.default_password
        email = sql_function.getRandomCustomerEmail(version)
        self.driver.find_element(*LoginPage.username).send_keys(email)
        self.driver.find_element(*LoginPage.password).send_keys(password)
        self.driver.find_element(*LoginPage.login_button).click()
        main_page = mainPage.mainPage(self.driver)
        return main_page, email

    def getCaptcha(self):
        return self.driver.find_element(*LoginPage.captcha)
