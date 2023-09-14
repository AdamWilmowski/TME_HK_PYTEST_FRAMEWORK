from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver

    cart_subtotal = (By.ID, "sylius-summary-items-subtotal")
    product_codes = (By.CSS_SELECTOR, "span[class='sub header sylius-product-variant-code']")
    product_price_qty_details = (By.XPATH, "//div[@class='d-flex justify-content-end']")
    shipping = (By.ID, "shipping-total")
    total = (By.ID, "sylius-summary-grand-total")
    next_button = (By.ID, "next-step")
    place_order_button = (By.ID, "place-order")
    payment_value = (By.CSS_SELECTOR, "span[class='c-payment__proforma-gross-value-text']")
    payment_boxes = (By.XPATH, "//div[@class='payment-box']")
    pay_by_card = (By.ID, "t_payu_bank_c")
    redirect_payment = (By.ID, "t_pay_button")
    pay_u_total = (By.XPATH, '//*[@id="app"]/div/div[2]/main/div[1]/aside/div/div[2]/em/div[2]')
    sap_id = (By.CSS_SELECTOR, "span[class='c-payment__order-number-text']")
    transport_selected = (By.ID, "app_checkout_shipping_shipments_0_method_0")
    advance_payment_radio = (By.ID, "sylius_checkout_complete_payments_0_method_0")
    advance_payment_label = (By.CSS_SELECTOR, "a[class='header']")
    terms_radio_1 = (By.CSS_SELECTOR, "label[for='sylius_checkout_complete_agreements_139_approved_0']")
    terms_radio_2 = (By.CSS_SELECTOR, "label[for='sylius_checkout_complete_agreements_245_approved_0']")

    #unregisteredcheckout
    company_name = (By.ID, "app_checkout_company_data_customer_companyUser_company_name")
    company_email = (By.ID, "app_checkout_company_data_customer_companyUser_company_email")
    company_phone = (By.ID, "app_checkout_company_data_customer_companyUser_company_phoneNumber")
    company_city = (By.ID, "app_checkout_company_data_customer_companyUser_company_city")
    company_street = (By.ID, "app_checkout_company_data_customer_companyUser_company_street")
    company_zip = (By.ID, "app_checkout_company_data_customer_companyUser_company_postcode")
    customer_email = (By.ID, "app_checkout_company_data_customer_email")
    customer_phone = (By.ID, "app_checkout_company_data_customer_phoneNumber")
    customer_name = (By.ID, "app_checkout_company_data_customer_firstName")
    customer_surname = (By.ID, "app_checkout_company_data_customer_lastName")
    company_shipping_name = (By.ID, "app_checkout_shipping_shippingAddress_company")
    company_shipping_city = (By.ID, "app_checkout_shipping_shippingAddress_city")
    company_shipping_street = (By.ID, "app_checkout_shipping_shippingAddress_street")
    company_shipping_zip = (By.ID, "app_checkout_shipping_shippingAddress_postcode")
    company_shipping_phone = (By.ID, "app_checkout_shipping_shippingAddress_phoneNumber")
    validations_first_step = (By.XPATH, "//div[@class='ui red pointing label sylius-validation-error']")
    fields_labels = (By.XPATH, "//label")
    all_fields = (By.XPATH, "//input[@type='text']")
    email_fields = (By.XPATH, "//input[@type='email']")


    def getCartSubtotal(self):
        price_full = self.driver.find_element(*CheckoutPage.cart_subtotal).text
        price = price_full.split()[1]
        return price

    def getCartProductsCode(self):
        return self.driver.find_elements(*CheckoutPage.product_codes)

    def getProductPriceAndQTYDetails(self):
        return self.driver.find_elements(*CheckoutPage.product_price_qty_details)

    def getShippingTotal(self):
        shipping_full = self.driver.find_element(*CheckoutPage.shipping).text
        shipping = shipping_full.split()[1]
        return shipping

    def getTotal(self):
        total_full = self.driver.find_element(*CheckoutPage.total).text
        total = total_full.split()[1]
        return total

    def getToSecondStep(self):
        actions = ActionChains(self.driver)
        actions.move_to_element(*CheckoutPage.next_button).click(*CheckoutPage.next_button).perform()

    def getPlaceOrder(self):
        self.driver.find_element(*CheckoutPage.place_order_button).click()

    def getPaymentValue(self):
        payment_full = self.driver.find_element(*CheckoutPage.payment_value).text
        payment = payment_full.split()[0]
        return payment

    def getSapID(self):
        return self.driver.find_element(*CheckoutPage.sap_id).text

    def waitForPaymentGate(self):
        WebDriverWait(self.driver, 60*3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='payment-box']")))

    def getPaymentBoxes(self):
        return self.driver.find_elements(*CheckoutPage.payment_boxes)

    def getPayByCard(self):
        return self.driver.find_element(*CheckoutPage.pay_by_card)

    def getToPayment(self):
        self.driver.find_element(*CheckoutPage.redirect_payment).click()

    def getPayUValue(self):
        full_payment = self.driver.find_element(*CheckoutPage.pay_u_total).text
        payment = full_payment.replace('$', '')
        return payment

    def getTransportSelectedRadio(self):
        return self.driver.find_element(*CheckoutPage.transport_selected)

    def getAdvancedPayementRadio(self):
        return self.driver.find_element(*CheckoutPage.advance_payment_radio)

    def getAdvancePaymentLabel(self):
        return self.driver.find_element(*CheckoutPage.advance_payment_label)

    def acceptRequiredRadio(self):
        self.driver.find_element(*CheckoutPage.terms_radio_1).click()
        self.driver.find_element(*CheckoutPage.terms_radio_2).click()

    #Uregistered functions
    def inputUnRegCompanyName(self, text):
        self.driver.find_element(*CheckoutPage.company_name).send_keys(text)

    def inputUnRegCompanyEmail(self, text):
        self.driver.find_element(*CheckoutPage.company_email).send_keys(text)

    def inputUnRegCompanyPhone(self, text):
        self.driver.find_element(*CheckoutPage.company_phone).send_keys(text)

    def inputUnRegCompanyCity(self, text):
        self.driver.find_element(*CheckoutPage.company_city).send_keys(text)

    def inputUnRegCompanyStreet(self, text):
        self.driver.find_element(*CheckoutPage.company_street).send_keys(text)

    def inputUnRegCompanyZIP(self, text):
        self.driver.find_element(*CheckoutPage.company_zip).send_keys(text)

    def inputUnRegCustomerEmail(self, text):
        self.driver.find_element(*CheckoutPage.customer_email).send_keys(text)

    def inputUnRegCustomerPhone(self, text):
        self.driver.find_element(*CheckoutPage.customer_phone).send_keys(text)

    def inputUnRegCustomerName(self, text):
        self.driver.find_element(*CheckoutPage.customer_name).send_keys(text)

    def inputUnRegCustomerSurname(self, text):
        self.driver.find_element(*CheckoutPage.customer_surname).send_keys(text)

    def getToNextStep(self):
        self.driver.find_element(*CheckoutPage.next_button).click()

    def inputShippingName(self, text):
        self.driver.find_element(*CheckoutPage.company_shipping_name).send_keys(text)

    def inputShippingCity(self, text):
        self.driver.find_element(*CheckoutPage.company_shipping_city).send_keys(text)

    def inputShippingStreet(self, text):
        self.driver.find_element(*CheckoutPage.company_shipping_street).send_keys(text)

    def inputShippingZip(self, text):
        self.driver.find_element(*CheckoutPage.company_shipping_zip).send_keys(text)

    def inputShippingPhone(self, text):
        self.driver.find_element(*CheckoutPage.company_shipping_phone).send_keys(text)

    def getValidationsFirstStep(self):
        return self.driver.find_elements(*CheckoutPage.validations_first_step)

    def getLabelList(self):
        return self.driver.find_elements(*CheckoutPage.fields_labels)

    def inputAll(self, text):
        fields = self.driver.find_elements(*CheckoutPage.all_fields)
        email_fields = self.driver.find_elements(*CheckoutPage.email_fields)
        for field in fields:
            field.send_keys(text)
        for field in email_fields:
            field.send_keys(text)

    def clearAll(self):
        fields = self.driver.find_elements(*CheckoutPage.all_fields)
        for field in fields:
            field.clear()
        try:
            email_fields = self.driver.find_elements(*CheckoutPage.email_fields)
            for field in email_fields:
                field.clear()
        except NoSuchElementException:
            pass

    def getToNextStepUnregistered(self):
        self.driver.find_element(*CheckoutPage.customer_surname).send_keys(Keys.ENTER)




