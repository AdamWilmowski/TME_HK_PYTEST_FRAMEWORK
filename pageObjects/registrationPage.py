import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from pageObjects.checkoutPage import CheckoutPage


class RegistrationPage:

    def __init__(self, driver):
        self.driver = driver

    submit_button = (By.CSS_SELECTOR, "button[class='button -primary -register']")
    validations = (By.CSS_SELECTOR, "div[class='ui red pointing label sylius-validation-error']")
    company_name = (By.ID, "app_company_user_company_name")
    company_email = (By.ID, "app_company_user_company_email")
    company_phone = (By.ID, "app_company_user_company_phoneNumber")
    company_city = (By.ID, "app_company_user_company_city")
    company_street = (By.ID, "app_company_user_company_street")
    company_zip = (By.ID, "app_company_user_company_postcode")
    customer_job = (By.ID, "app_company_user_jobTitle")
    customer_email = (By.ID, "app_company_user_customer_email")
    customer_phone = (By.ID, "app_company_user_customer_phoneNumber")
    customer_name = (By.ID, "app_company_user_customer_firstName")
    customer_surname = (By.ID, "app_company_user_customer_lastName")
    input_fields = (By.XPATH, "//input[@type='text']")
    required_radio = (By.XPATH, "//label[@for='app_company_user_agreements_245_approved_0']")
    thank_header = (By.XPATH, "//h2")
    region_select = (By.XPATH, '//form/div[4]/div')
    region_china = (By.CSS_SELECTOR, 'div[data-value="CN"]')
    agreements_all_labels = (By.XPATH, "//div/div/div/label")
    thank_values = (By.CSS_SELECTOR, "span[class='item-value']")


    def getSubmitButton(self):
        return self.driver.find_element(*RegistrationPage.submit_button)

    def getRequiredRadio(self):
        return self.driver.find_element(*RegistrationPage.required_radio)

    def getValidations(self):
        return self.driver.find_elements(*RegistrationPage.validations)

    def inputCompanyName(self, text):
        return self.driver.find_element(*RegistrationPage.company_name).send_keys(text)

    def inputCompanyEmail(self, text):
        return self.driver.find_element(*RegistrationPage.company_email).send_keys(text)

    def inputCompanyPhone(self, text):
        return self.driver.find_element(*RegistrationPage.company_phone).send_keys(text)

    def getCompanyPhone(self):
        return self.driver.find_element(*RegistrationPage.company_phone)

    def setRegiontoChina(self):
        region_select = self.driver.find_element(*RegistrationPage.region_select)
        ActionChains(self.driver).scroll_to_element(region_select).perform()
        self.driver.find_element(*RegistrationPage.region_select).click()
        self.driver.find_element(*RegistrationPage.region_china).click()

    def inputCompanyCity(self, text):
        return self.driver.find_element(*RegistrationPage.company_city).send_keys(text)

    def inputCompanyStreet(self, text):
        return self.driver.find_element(*RegistrationPage.company_street).send_keys(text)

    def inputCompanyZip(self, text):
        return self.driver.find_element(*RegistrationPage.company_zip).send_keys(text)

    def getCompanyZip(self):
        return self.driver.find_element(*RegistrationPage.company_zip)

    def inputCustomerJob(self, text):
        return self.driver.find_element(*RegistrationPage.customer_job).send_keys(text)

    def inputCustomerEmail(self, text):
        return self.driver.find_element(*RegistrationPage.customer_email).send_keys(text)

    def inputCustomerPhone(self, text):
        return self.driver.find_element(*RegistrationPage.customer_phone).send_keys(text)

    def getCustomerPhone(self):
        return self.driver.find_element(*RegistrationPage.customer_phone)

    def inputCustomerName(self, text):
        return self.driver.find_element(*RegistrationPage.customer_name).send_keys(text)

    def inputCustomerSurname(self, text):
        return self.driver.find_element(*RegistrationPage.customer_surname).send_keys(text)

    def clearInputFields(self):
        fields = self.driver.find_elements(*RegistrationPage.input_fields)
        for field in fields:
            field.clear()
        self.driver.find_element(*RegistrationPage.company_email).clear()
        self.driver.find_element(*RegistrationPage.customer_email).clear()

    def getThankHeader(self):
        return self.driver.find_element(*RegistrationPage.thank_header)

    def getThankValues(self):
        return self.driver.find_elements(*RegistrationPage.thank_values)

    def acceptAllAgreements(self):
        agreements_list = self.driver.find_elements(*RegistrationPage.agreements_all_labels)[0::2]
        for agreement in agreements_list:
            agreement.click()

