import time

import pytest
from TestData.SQLDatabase import SQLFunctions
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage
from TestData.secrets import Secrets
from selenium.webdriver import Keys


class TestLogin(BaseClass):

    def test_login(self):
        log = self.getLogger()
        log.info("Test started")
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        self.closeCookies()
        db_version = main_page.getDBVersion()
        log.info(f"Database version is {db_version}")
        email = sql_function.getRandomCustomerEmail(db_version)
        log.info(f"Logging to customer account: {email}")
        login_page = main_page.getToLoginPage()
        login_page.inputUsername(email)
        login_page.inputPassword(Secrets.default_password)
        account_page = login_page.getToAccountPage()
        customer_name = sql_function.getCustomerData("customer_name", "email", email)
        log.info(f"Successful login")
        assert customer_name in account_page.getNameHeader().text, log.error("CUSTOMER INFO NOT CORRECT")
        log.info("Test passed")

    def test_password_reset(self):
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        self.closeCookies()
        db_version = main_page.getDBVersion()
        login_page = main_page.getToLoginPage()
        email = sql_function.getRandomCustomerEmail(db_version)
        login_page.getForgotPasswordPage()
        login_page.inputForgotPasswordEmail(email)
        login_page.resetPassword()
        username = Secrets.email_username
        password = Secrets.email_password
        imap_server = Secrets.email_imap_server
        time.sleep(25)
        hyperlinks = self.get_hyperlinks_from_first_email(username, password, imap_server, subject="You")
        self.get_to(hyperlinks[7])
        login_page.inputNewPassword(Secrets.default_password)
        login_page.inputConfirmNewPassword(Secrets.default_password+"1")
        login_page.resetPasswordResetButton()
        login_page.inputUsername(email)
        login_page.inputPassword(Secrets.default_password+"1")
        login_page.getToAccountPage()
        try:
            assert self.getCurrentURL() == "https://beta.tme.hk/en/"
        except AssertionError:
            assert self.getCurrentURL() == "https://beta.tme.hk/en/account/agreements"
        

    def test_login_incorrect(self):
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        self.closeCookies()
        login_page = main_page.getToLoginPage()
        login_page.inputUsername("xxx")
        login_page.inputPassword("xxx")
        login_page.getLogginButton()
        assert login_page.getPopup().is_displayed
        assert login_page.getPopup().text == 'Login or password is incorrect'
        login_page.inputUsername("xxx")
        login_page.inputPassword("xxx")
        login_page.getLogginButton()
        assert login_page.getPopup().is_displayed
        assert login_page.getPopup().text == 'Login or password is incorrect'
        login_page.inputUsername("xxx")
        login_page.inputPassword("xxx")
        login_page.getLogginButton()
        assert login_page.getPopup().is_displayed
        assert login_page.getPopup().text == 'Login or password is incorrect'
        assert login_page.getCaptcha().is_displayed
        assert login_page.getCaptcha().value_of_css_property('width') == '200px'
        assert login_page.getCaptcha().value_of_css_property('height') == '60px'
        assert login_page.getCaptchaInput().is_displayed
        login_page.getCaptchaInput().send_keys("xxx")
        login_page.getCaptchaInput().send_keys(Keys.ENTER)
        assert login_page.getCaptchaValidation().text == "The signs do not match"
