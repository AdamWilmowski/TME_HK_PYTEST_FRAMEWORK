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
