import time
import pytest
from TestData.SQLDatabase import SQLFunctions
from TestData.RandomData import RandomData
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage
from TestData.secrets import Secrets
from selenium.webdriver import Keys


class TestAddress(BaseClass):

    def test_default_address(self):
        main_page = mainPage(self.driver)
        self.closeCookies()
        db_version = main_page.getDBVersion()
        login_page = main_page.getToLoginPage()
        login_page.getToMainPageWithLogging(db_version)
        account_page = main_page.getToAddressBook()
        account_page.getAddNewAddress()
        random_data = RandomData()
        company_name = random_data.get_CompanyName()
        city = random_data.get_city()
        street_address = random_data.get_street()
        zip_code = random_data.get_random_value(6, "number")
        phone = random_data.get_random_value(13, "number")
        account_page.inputNewAddressCompanyName(company_name)
        account_page.inputNewAddressCity(city)
        account_page.inputNewAddressStreet(street_address)
        account_page.inputNewAddressZip(zip_code)
        account_page.inputNewAddressPhone(phone)
        account_page.getNewAddressSetAsDefault()
        account_page.getNewAddressSave()
        new_address = account_page.getDefaultShippingAddress()
        data_list = [company_name, street_address, city + ",", str(zip_code) + ",", str(phone)]
        for i in range(len(new_address)):
            assert new_address[i] == data_list[i]
        self.get_to_main()
        main_page.searchForProduct("USL1M-DIO")
        main_page.getAddToCartButton().click()
        main_page.waitTillProductinBasket("1")
        checkout_page = main_page.getToCheckout()


