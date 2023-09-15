import time

import pytest
from selenium.common import NoSuchElementException

from pageObjects.registrationPage import RegistrationPage
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage
from TestData.SQLDatabase import SQLFunctions
from TestData.RandomData import RandomData
from pageObjects.loginPage import LoginPage
from TestData.secrets import Secrets


class TestUserRegistration(BaseClass):

    def test_register_user(self):
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        random_data = RandomData()
        self.closeCookies()
        db_version = main_page.getDBVersion()
        registration_page = main_page.getToRegistrationPage()
        company_name = random_data.get_CompanyName()
        email_value = sql_function.getEmailValue()
        email = f"chinacustomertme+{email_value}@gmail.com"
        company_phone = random_data.get_random_value(12, "number")
        company_city = random_data.get_city()
        company_street = random_data.get_street()
        company_zip = random_data.get_random_value(6, "number")
        customer_job = "SeleniumCreated"
        customer_phone = random_data.get_random_value(12, "number")
        customer_name = random_data.get_name()
        customer_surname = random_data.get_surname()
        registration_page.inputCompanyName(company_name)
        registration_page.inputCompanyEmail(email)
        registration_page.inputCompanyPhone(company_phone)
        registration_page.inputCompanyCity(company_city)
        registration_page.inputCompanyStreet(company_street)
        registration_page.inputCompanyZip(company_zip)
        registration_page.inputCustomerJob(customer_job)
        registration_page.inputCustomerEmail(email)
        registration_page.inputCustomerPhone(customer_phone)
        registration_page.inputCustomerName(customer_name)
        registration_page.inputCustomerSurname(customer_surname)
        registration_page.acceptAllAgreements()
        time.sleep(15)
        registration_page.getSubmitButton().click()
        assert company_name in registration_page.getThankHeader().text
        value_list = [company_name, email, company_phone, company_city, company_street, company_zip, email,
                      customer_phone, customer_name, customer_surname]
        thank_elements = registration_page.getThankValues()
        i = 0
        for element in thank_elements:
            if element.text != "China":
                assert element.text == value_list[i]
                i += 1
        username = Secrets.email_username
        password = Secrets.email_password
        imap_server = Secrets.email_imap_server
        time.sleep(25)
        hyperlinks = self.get_hyperlinks_from_first_email(username, password, imap_server)
        print(hyperlinks)
        registration_hyperlink = hyperlinks[7]
        self.driver.get(registration_hyperlink)
        login_page = LoginPage(self.driver)
        login_page.inputFirstPassword(Secrets.default_password)
        login_page.inputConfirmPassword(Secrets.default_password)
        login_page.getSavePasswordButton().click()
        login_page.inputUsername(email)
        login_page.inputPassword(Secrets.default_password)
        account_page = login_page.getToAccountPage()
        sql_function.inputCustomerData(email_value, company_name, email, company_phone, company_city, company_street,
                                       company_zip, customer_job, customer_phone, customer_name,customer_surname,
                                       db_version)
        assert account_page.getNameHeader().text == customer_name
        account_page.getAccountDashboardButton().click()
        dashboard_values = account_page.getDashboardValues()
        value_list = [company_name, email, company_phone, customer_name, customer_surname, email, customer_phone]
        i = 0
        for value in dashboard_values:
            assert value.text == value_list[i]
            i += 1
        assert account_page.getDashboardBillingAddress()[1] == company_name
        assert account_page.getDashboardBillingAddress()[2] == company_street
        assert account_page.getDashboardBillingAddress()[4] == f"T: {company_phone}"

    @pytest.mark.validations
    @pytest.mark.form
    def test_obligatory_validation(self):
        main_page = mainPage(self.driver)
        self.closeCookies()
        registration_page = main_page.getToRegistrationPage()
        registration_page.getSubmitButton().click()
        for i in range(12):
            assert registration_page.getValidations()[i].is_displayed()
            assert registration_page.getValidations()[i].value_of_css_property("font-size") == '14px'
        for i in range(10):
            assert registration_page.getValidations()[i].text == "This field is obligatory"
        assert registration_page.getValidations()[10].text == "This value should be true."
        assert registration_page.getValidations()[11].text == "The signs do not match"

    @pytest.mark.validations
    @pytest.mark.form
    def test_max_length_validation(self):
        registration_page = RegistrationPage(self.driver)
        self.checkPage("https://beta.tme.hk/en/register")
        registration_page.inputCompanyName("x" * 121)
        registration_page.inputCompanyEmail("x" * 61 + "@x.x")
        registration_page.inputCompanyPhone("1" * 16)
        registration_page.inputCompanyCity("x" * 36)
        registration_page.inputCompanyStreet("x" * 71)
        registration_page.inputCompanyZip("1" * 7)
        registration_page.inputCustomerJob("x" * 36)
        registration_page.inputCustomerEmail("x" * 61 + "@x.x")
        registration_page.inputCustomerPhone("1" * 16)
        registration_page.inputCustomerName("x" * 36)
        registration_page.inputCustomerSurname("x" * 36)
        registration_page.getSubmitButton().click()
        assert registration_page.getValidations()[
                   0].text == 'The maximum length for the "Company" field is 120 characters.'
        assert registration_page.getValidations()[
                   1].text == 'The maximum length for the "E-mail" field is 64 characters.'
        assert registration_page.getValidations()[
                   2].text == 'The maximum length for the "Phone Number" field is 15 digits.'
        assert registration_page.getValidations()[3].text == 'The maximum length for the "City" field is 35 characters.'
        assert registration_page.getValidations()[
                   4].text == 'The maximum length for the "Street Address" field is 70 characters.'
        assert registration_page.getValidations()[
                   5].text == 'The maximum length for the "Job title" field is 35 characters.'
        assert registration_page.getValidations()[
                   6].text == 'The maximum length for the "E-mail" field is 64 characters.'
        assert registration_page.getValidations()[
                   7].text == 'The maximum length for the "Phone Number" field is 15 digits.'
        assert registration_page.getValidations()[
                   8].text == 'The maximum length for the "First Name" field is 35 characters.'
        assert registration_page.getValidations()[
                   9].text == 'The maximum length for the "Last Name" field is 35 characters.'

    @pytest.mark.validations
    @pytest.mark.form
    def test_latin_only_validation(self):
        registration_page = RegistrationPage(self.driver)
        self.checkPage("https://beta.tme.hk/en/register")
        registration_page.clearInputFields()
        registration_page.inputCompanyName("亂數產")
        registration_page.inputCompanyEmail("亂數產@x.x")
        registration_page.inputCompanyPhone("亂數產")
        registration_page.inputCompanyCity("亂數產")
        registration_page.inputCompanyStreet("亂數產")
        registration_page.inputCompanyZip("亂數產")
        registration_page.inputCustomerJob("亂數產")
        registration_page.inputCustomerEmail("亂數產")
        registration_page.inputCustomerPhone("亂數產")
        registration_page.inputCustomerEmail("亂數產")
        registration_page.inputCustomerName("亂數產")
        registration_page.inputCustomerSurname("亂數產")
        registration_page.getSubmitButton().click()
        for i in range(11):
            if i != 2 and i != 5 and i != 8:
                assert registration_page.getValidations()[i].text == "Please use only latin characters."
            else:
                assert registration_page.getValidations()[i].text == "This field is obligatory"

    @pytest.mark.validations
    @pytest.mark.form
    def test_correct_format_validation(self):
        registration_page = RegistrationPage(self.driver)
        self.checkPage("https://beta.tme.hk/en/register")
        registration_page.clearInputFields()
        registration_page.inputCompanyEmail("xxxx.com")
        registration_page.inputCustomerEmail("xxxx.com")
        registration_page.inputCompanyPhone("1" * 10)
        registration_page.inputCustomerPhone("1" * 10)
        registration_page.inputCompanyZip("1" * 5)
        registration_page.getSubmitButton().click()
        assert registration_page.getValidations()[
                   1].text == "Invalid format. Please enter a valid e-mail address, for example smith@domain.cn"
        assert registration_page.getValidations()[2].text == "The field must contain a minimum of 11 digits."
        assert registration_page.getValidations()[5].text == "The field must contain 6 digits."
        assert registration_page.getValidations()[
                   6].text == "Invalid format. Please enter a valid e-mail address, for example smith@domain.cn"
        assert registration_page.getValidations()[7].text == "The field must contain a minimum of 11 digits."
        self.refresh()
        registration_page.clearInputFields()
        registration_page.inputCompanyPhone("123abc456#@$789[](][1011")
        registration_page.inputCustomerPhone("123abc456#@$789[](][1011")
        registration_page.inputCompanyZip("aa123$%456")
        registration_page.getSubmitButton().click()
        assert registration_page.getCompanyPhone().get_attribute("value") == "1234567891011"
        assert registration_page.getCustomerPhone().get_attribute("value") == "1234567891011"
        assert registration_page.getCompanyZip().get_attribute("value") == "123456"

