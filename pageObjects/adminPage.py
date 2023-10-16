from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from TestData.secrets import Secrets
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage:
    def __init__(self, driver):
        self.driver = driver

    admin_username = (By.ID, "_username")
    admin_password = (By.ID, "_password")
    db_version = (By.XPATH, "//body/div[2]/div[4]/div/i")
    admin_username_submit = (By.XPATH, "//button")
    admin_orders_button = (By.LINK_TEXT, "Orders")
    create_new_order = (By.LINK_TEXT, "Create New Order")
    customer_email_order = (By.ID, "sylius_admin_order_creation_new_order_customer_select_customerEmail")
    search_submit_button = (By.CSS_SELECTOR, "button[type='submit']")
    initial_place_order_button = (By.XPATH, "//td[8]/button")
    sku_input = (By.CSS_SELECTOR, "input[class='product-sku']")
    qty_input = (By.CSS_SELECTOR, "input[type='number']")
    current_price = (By.XPATH, "//tr/td[8]/p[1]")
    minimal_price = (By.XPATH, "//tr/td[8]/p[2]")
    subtotal = (By.XPATH, "//tr/td[9]/p[1]")
    transport_cost = (By.XPATH, "//div[5]/div/div[2]/div[2]/div/div/div")
    grand_total = (By.XPATH, "//div[9]/table/tbody/tr/td[4]")
    submit_order = (By.ID, "create-button")
    order_summary_unit_price = (By.CSS_SELECTOR, "td[class='right aligned unit-price']")
    order_summary_qty = (By.CSS_SELECTOR, "td[class='right aligned quantity']")
    order_summary_subtotal = (By.CSS_SELECTOR, "td[class='right aligned subtotal']")
    order_summary_total = (By.ID, "total")
    order_summary_response_codes = (By.XPATH, "//tbody/tr/td[7]")
    order_summary_order_status = (By.CSS_SELECTOR, "span[class='ui label']")

    def loginToAdmin(self):
        self.driver.find_element(*AdminPage.admin_username).send_keys(Secrets.admin_username)
        self.driver.find_element(*AdminPage.admin_password).send_keys(Secrets.admin_password)
        self.driver.find_element(*AdminPage.admin_username_submit).click()

    def getDBVersion(self):
        return self.driver.find_element(*AdminPage.db_version).text

    def getToOrders(self):
        self.driver.find_element(*AdminPage.admin_orders_button).click()

    def createNewOrder(self):
        self.driver.find_element(*AdminPage.create_new_order).click()

    def inputCustomerEmailOrder(self, text):
        self.driver.find_element(*AdminPage.customer_email_order).send_keys(text)

    def submitSearchOrder(self):
        self.driver.find_element(*AdminPage.search_submit_button).click()

    def initialPlaceOrderButton(self):
        self.driver.find_element(*AdminPage.initial_place_order_button).click()

    def inputSku(self, text):
        self.driver.find_element(*AdminPage.sku_input).send_keys(text)

    def inputQTY(self, text):
        self.driver.find_element(*AdminPage.qty_input).send_keys(text)
        self.driver.find_element(*AdminPage.qty_input).send_keys(Keys.ENTER)

    def getCurrentPrice(self):
        return float(self.driver.find_element(*AdminPage.current_price).text.split()[2])

    def getMinimalPrice(self):
        return float(self.driver.find_element(*AdminPage.minimal_price).text.split()[2])

    def getSubtotal(self):
        return float(self.driver.find_element(*AdminPage.subtotal).text.split()[1])

    def getTransportCost(self):
        return float(self.driver.find_element(*AdminPage.transport_cost).text.split()[1])

    def getAdminGrandTotal(self):
        return float(self.driver.find_element(*AdminPage.grand_total).text.split()[1])

    def submitOrder(self):
        self.driver.find_element(*AdminPage.submit_order).click()

    def getOrderSummaryUnitPrice(self):
        return float(self.driver.find_element(*AdminPage.order_summary_unit_price).text.split()[1])

    def getOrderSummaryQTY(self):
        return int(self.driver.find_element(*AdminPage.order_summary_qty).text)

    def getOrderSummarySubtotal(self):
        return float(self.driver.find_element(*AdminPage.order_summary_subtotal).text.split()[1])

    def getOrderSummaryTotal(self):
        return float(self.driver.find_element(*AdminPage.order_summary_total).text.split()[2])

    def getOrderSummaryStatuses(self):
        elements = self.driver.find_elements(*AdminPage.order_summary_total)
        elements_text = []
        for element in elements:
            if element.text.split()[0] != "USD":
                elements_text.append(element.text)
        return elements_text

    def waitTillSubmitOrderClickable(self):
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(AdminPage.submit_order))

    def waitTillOrderStatus(self, text):
        WebDriverWait(self.driver, 120).until(
            EC.text_to_be_present_in_element(AdminPage.order_summary_order_status, text))
