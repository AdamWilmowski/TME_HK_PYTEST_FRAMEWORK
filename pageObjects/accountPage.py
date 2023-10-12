from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pageObjects import registrationPage


class AccountPage:

    def __init__(self, driver):
        self.driver = driver

    name_header = (By.CSS_SELECTOR, "div[class='header-security-dropdown-title d-flex align-items-center justify-content-between']")
    dashboard_values = (By.XPATH, "//tr/td[2]")
    address_book_button = (By.LINK_TEXT, "Address Book")
    account_dashboard_button = (By.LINK_TEXT, "Account Dashboard")
    dashboard_billing_address = (By. XPATH, "//div[@class='p-r-50 m-b-20']")
    order_ecom_numbers = (By.XPATH, "//td/a")
    order_date = (By.XPATH, "//td[@aria-label='Date']")
    order_created_by = (By.XPATH, "//td[@aria-label='Created By']")
    order_total = (By.XPATH, "//td[@aria-label='Total']")
    order_status = (By.XPATH, "//td[@aria-label='Status']")
    agreements_label = (By.XPATH, "//div/div/div/label")
    agreements_save_button = (By.XPATH, "//main/div/div/div[2]/form/button")
    company_users = (By.XPATH, "//td[@aria-label='Name']")
    add_new_company_user = (By.XPATH, "//section/a")
    company_user_job = (By.ID, "app_company_user_jobTitle")
    company_user_name = (By.ID, "app_company_user_customer_firstName")
    company_user_surname = (By.ID, "app_company_user_customer_lastName")
    company_user_email = (By.ID, "app_company_user_customer_email")
    company_user_phone = (By.ID, "app_company_user_customer_phoneNumber")
    company_user_submit = (By.CSS_SELECTOR, "button[class='button -primary']")
    company_users_list_emails = (By.CSS_SELECTOR, "td[aria-label='Email']")
    company_users_list_status = (By.CSS_SELECTOR, "td[aria-label='Status']")

    def getNameHeader(self):
        return self.driver.find_element(*AccountPage.name_header)

    def getDashboardValues(self):
        return self.driver.find_elements(*AccountPage.dashboard_values)

    def getAddressBookButton(self):
        return self.driver.find_element(*AccountPage.address_book_button)

    def getAccountDashboardButton(self):
        return self.driver.find_element(*AccountPage.account_dashboard_button)

    def getDashboardBillingAddress(self):
        elements = self.driver.find_element(*AccountPage.dashboard_billing_address).text
        elements_list = elements.splitlines()
        return elements_list

    def getOrdersEcomNrs(self):
        return self.driver.find_elements(*AccountPage.order_ecom_numbers)

    def getOrdersDates(self):
        return self.driver.find_elements(*AccountPage.order_date)

    def getOrdersCreatedBy(self):
        return self.driver.find_elements(*AccountPage.order_created_by)

    def getOrdersTotals(self):
        return self.driver.find_elements(*AccountPage.order_total)

    def getOrdersStatuses(self):
        return self.driver.find_elements(*AccountPage.order_status)


    def acceptAllAgreements(self):
        try:
            agreement_list = self.driver.find_elements(*AccountPage.agreements_label)[0::2]
            for agreement in agreement_list:
                agreement.click()
            buttons = self.driver.find_elements(*AccountPage.agreements_save_button)
            for button in buttons:
                button.click()
        except NoSuchElementException:
            pass

    def getCompanyUsers(self):
        return self.driver.find_elements(*AccountPage.company_users)

    def getAddNewCompanyUser(self):
        self.driver.find_element(*AccountPage.add_new_company_user).click()

    def inputCompanyUserJob(self, text):
        self.driver.find_element(*AccountPage.company_user_job).send_keys(text)

    def inputCompanyUserName(self, text):
        self.driver.find_element(*AccountPage.company_user_name).send_keys(text)

    def inputCompanyUserSurname(self, text):
        self.driver.find_element(*AccountPage.company_user_surname).send_keys(text)

    def inputCompanyUserEmail(self, text):
        self.driver.find_element(*AccountPage.company_user_email).send_keys(text)

    def inputCompanyUserPhone(self, text):
        self.driver.find_element(*AccountPage.company_user_phone).send_keys(text)

    def submitCompanyUser(self):
        self.driver.find_element(*AccountPage.company_user_submit).click()

    def getCompanyUsersEmails(self):
        users_emails = self.driver.find_elements(*AccountPage.company_users_list_emails)
        users_emails_text = []
        for user in users_emails:
            users_emails_text.append(user.text)
        return users_emails_text

    def getCompanyUsersStatus(self):
        users_statuses = self.driver.find_elements(*AccountPage.company_users_list_status)
        user_statuses_text = []
        for user in users_statuses:
            user_statuses_text.append(user.text)
        return user_statuses_text
