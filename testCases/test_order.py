import time
import pytest
import datetime
from selenium.common import NoSuchElementException
import TestData
from pageObjects.mainPage import mainPage
from utilities.BaseClass import BaseClass
from TestData.SQLDatabase import SQLFunctions
from TestData.RandomData import RandomData
from TestData.TestDataInput import TestDataInput


class TestOrder(BaseClass):

    @pytest.mark.parametrize("product_list", [TestDataInput.two_products])
    def test_basic_order(self, product_list):
        log = self.getLogger()
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        version = main_page.getDBVersion()
        log.info(f"Test started, DB version is {version}")
        self.closeCookies()
        login_page = main_page.getToLoginPage()
        main_page, email = login_page.getToMainPageWithLogging(version)
        products_number = 0
        products_name_list = []
        products_min_qty_list = []
        products_unit_price_list = []
        products_price_list = []
        for product in product_list:
            main_page.searchForProduct(product)
            try:
                product_name = main_page.getProductName().text
                products_name_list.append(product_name)
                product_min_qty = float(main_page.getProductsAtrubbutes()[1].text.split()[1])
                products_min_qty_list.append(product_min_qty)
                product_unit_price = float(main_page.getProductPrices()[0].text)
                products_unit_price_list.append(product_unit_price)
                product_price = round(product_unit_price * product_min_qty, 2)
                products_price_list.append(product_price)
                main_page.getAddToCartButton().click()
                products_number += 1
                main_page.waitTillProductinBasket(str(products_number))
                log.info(f"Product {product} added to cart")
            except NoSuchElementException:
                log.error(f"Product {product} not added to cart")
                pass
            self.back()
            main_page.clearSearch()
        checkout_page = main_page.getToCheckout()
        subtotal = float(checkout_page.getCartSubtotal())
        shipping = float(checkout_page.getShippingTotal())
        total = float(checkout_page.getTotal())
        assert subtotal == sum(products_price_list), log.error("Cart subtotal incorrect")
        assert round(subtotal + shipping, 2) == total, log.error("Cart total incorrect")
        cart_product_codes = checkout_page.getCartProductsCode()
        for i in range(len(cart_product_codes)):
            assert cart_product_codes[i].text == products_name_list[i], log.error("Cart product name incorrect")
        log.info("Cart first step correct")
        checkout_page.getToSecondStep()
        subtotal_second_step = float(checkout_page.getCartSubtotal())
        assert subtotal == subtotal_second_step, log.error("Cart subtotal second step not correct")
        log.info("Cart second step correct")
        checkout_page.getPlaceOrder()
        checkout_page.waitForPaymentGate()
        payment = float(checkout_page.getPaymentValue())
        sap_id = checkout_page.getSapID()
        assert payment == total, log.error("Payment total not correct")
        payment_boxes = checkout_page.getPaymentBoxes()
        boxes = 0
        for payment_box in payment_boxes:
            assert payment_box.is_displayed(), log.critical("Payment gate not displayed")
            boxes += 1
        try:
            assert boxes == 4
        except AssertionError:
            log.error("Not all payment options available")
            pass
        checkout_page.getPaymentBoxes()[1].click()
        checkout_page.getPayByCard().click()
        log.info("Payment gate correct")
        checkout_page.getToPayment()
        pay_u_value = float(checkout_page.getPayUValue())
        assert pay_u_value == total, log.error("PayU not correct")
        self.get_to_main()
        account_page = main_page.getToMyOrders()
        order_econ_number = account_page.getOrdersEcomNrs()[0].text
        order_date = account_page.getOrdersDates()[0].text
        date = datetime.date.today().strftime("%m/%d/%Y")
        assert date == order_date, log.error("Order details not correct")
        total_my_orders = float(account_page.getOrdersTotals()[0].text.split()[1])
        assert total_my_orders == total, log.error("Order details not correct")
        status = account_page.getOrdersStatuses()[0].text
        assert status == "Waiting for payment", log.error("Order details not correct")
        sql_function.inputOrderData(email, sap_id, order_econ_number, total, date, version, registered_user=1)
        log.info(f"Test completed, order {order_econ_number} details added to SQL database")

    @pytest.mark.parametrize("product_one", [TestDataInput.one_product])
    def test_unregistered_order(self, product_one):
        main_page = mainPage(self.driver)
        sql_function = SQLFunctions()
        version = main_page.getDBVersion()
        self.closeCookies()
        main_page.searchForProduct(product_one)
        product_one_name = main_page.getProductName().text
        product_one_min_qty = float(main_page.getProductsAtrubbutes()[1].text.split()[1])
        product_one_unit_price = float(main_page.getProductPrices()[0].text)
        product_one_price = round(product_one_unit_price * product_one_min_qty, 2)
        main_page.getAddToCartButton().click()
        main_page.waitTillProductinBasket("1")
        self.back()
        checkout_page = main_page.getToCheckout()
        random_data = RandomData()
        company_name = random_data.get_CompanyName()
        email_value = sql_function.getEmailValue()
        email = f"chinacustomertme+{email_value}@gmail.com"
        company_phone = random_data.get_random_value(12, "number")
        company_city = random_data.get_city()
        company_street = random_data.get_street()
        company_zip = random_data.get_random_value(6, "number")
        customer_phone = random_data.get_random_value(12, "number")
        customer_name = random_data.get_name()
        customer_surname = random_data.get_surname()
        checkout_page.inputUnRegCompanyName(company_name)
        checkout_page.inputUnRegCompanyEmail(email)
        checkout_page.inputUnRegCompanyPhone(company_phone)
        checkout_page.setUnRegCompanyRegiontoChina()
        checkout_page.inputUnRegCompanyCity(company_city)
        checkout_page.inputUnRegCompanyStreet(company_street)
        checkout_page.inputUnRegCompanyZIP(company_zip)
        checkout_page.inputUnRegCustomerEmail(email)
        checkout_page.inputUnRegCustomerPhone(customer_phone)
        checkout_page.inputUnRegCustomerName(customer_name)
        checkout_page.inputUnRegCustomerSurname(customer_surname)
        checkout_page.getToNextStep()
        checkout_page.inputShippingName(company_name)
        checkout_page.setShippingRegionToChina()
        checkout_page.inputShippingCity(company_city)
        checkout_page.inputShippingStreet(company_street)
        checkout_page.inputShippingZip(company_zip)
        checkout_page.inputShippingPhone(company_phone)
        subtotal = float(checkout_page.getCartSubtotal())
        shipping = float(checkout_page.getShippingTotal())
        total = float(checkout_page.getTotal())
        assert checkout_page.getTransportSelectedRadio().is_selected()
        assert subtotal == product_one_price
        assert round(subtotal + shipping, 2) == total
        assert checkout_page.getCartProductsCode()[0].text == product_one_name
        checkout_page.getToNextStep()
        assert checkout_page.getAdvancePaymentLabel().text == "Advance payment"
        assert checkout_page.getAdvancedPayementRadio().is_selected()
        checkout_page.acceptRequiredRadio()
        assert float(checkout_page.getTotal()) == total
        checkout_page.getPlaceOrder()
        checkout_page.waitForPaymentGate()
        payment = float(checkout_page.getPaymentValue())
        sap_id = checkout_page.getSapID()
        assert payment == total
        checkout_page.getPaymentBoxes()[1].click()
        checkout_page.getPayByCard().click()
        checkout_page.getToPayment()
        pay_u_value = float(checkout_page.getPayUValue())
        assert pay_u_value == total
        date = datetime.date.today()
        sql_function.inputOrderData(email, sap_id, 0, total, date, version, registered_user=0)

    @pytest.mark.parametrize("product_one", [TestDataInput.one_product])
    def test_unregistered_order_validations_elements(self, product_one):
        main_page = mainPage(self.driver)
        self.closeCookies()
        main_page.searchForProduct(product_one)
        main_page.getAddToCartButton().click()
        main_page.waitTillProductinBasket("1")
        self.back()
        checkout_page = main_page.getToCheckout()
        checkout_page.getToNextStep()
        manual_list = ["Company name", "Company e-mail", "Phone number", "Region", "City", "Street Address",
                       "ZIP/Postal Code", "E-mail", "Phone number", "First name", "Last name"]
        raw_label_list = checkout_page.getLabelList()
        label_list = []
        for label in raw_label_list:
            label_list.append(label.text)
        label_list = label_list[3:]
        for i in range(len(manual_list)):
            assert manual_list[i] == label_list[i]
        validations_qty = 0
        for element in checkout_page.getValidationsFirstStep():
            assert element.text == 'This field is obligatory'
            validations_qty += 1
        assert validations_qty == 10
        self.refresh()
        checkout_page.inputAll("朋友")
        checkout_page.getToNextStepUnregistered()
        validations = checkout_page.getValidationsFirstStep()
        for i in range(10):
            if i == 2:
                assert validations[i].text == "The field must contain a minimum of 11 digits."
            elif i == 5:
                assert validations[i].text == "This field is obligatory"
            elif i == 7:
                assert validations[i].text == "The field must contain a minimum of 11 digits."
            else:
                assert validations[i].text == "Please use only latin characters."
        self.refresh()
        checkout_page.clearAll()
        checkout_page.inputAll("x" * 121)
        checkout_page.getToNextStepUnregistered()
        validations = checkout_page.getValidationsFirstStep()
        assert validations[0].text == 'The maximum length for the "Company" field is 120 characters.'
        assert validations[1].text == 'Invalid format. Please enter a valid e-mail address, for example smith@domain.cn'
        assert validations[2].text == 'The maximum length for the "Phone Number" field is 15 digits.'
        assert validations[3].text == 'The maximum length for the "City" field is 35 characters.'
        assert validations[4].text == 'The maximum length for the "Street Address" field is 70 characters.'
        assert validations[5].text == 'This field is obligatory'
        assert validations[6].text == 'The maximum length for the "E-mail" field is 64 characters.'
        assert validations[7].text == 'The maximum length for the "Phone Number" field is 15 digits.'
        assert validations[8].text == 'The maximum length for the "First Name" field is 35 characters.'
        assert validations[9].text == 'The maximum length for the "Last Name" field is 35 characters.'
        self.refresh()
        checkout_page.clearAll()
        checkout_page.inputUnRegCompanyEmail("x" * 65 + "@tme.hk")
        checkout_page.inputUnRegCompanyZIP("12345")
        checkout_page.inputUnRegCustomerEmail("x" * 65 + "@tme.hk")
        checkout_page.getToNextStepUnregistered()
        validations = checkout_page.getValidationsFirstStep()
        for i in range(10):
            if i == 1:
                assert validations[i].text == 'The maximum length for the "E-mail" field is 64 characters.'
            if i == 5:
                assert validations[i].text == 'The field must contain 6 digits.'
        self.refresh()
        checkout_page.clearAll()
        checkout_page.inputUnRegCompanyName("x")
        checkout_page.inputUnRegCompanyEmail("x@c.p")
        checkout_page.inputUnRegCompanyPhone("1" * 12)
        checkout_page.inputUnRegCompanyCity("x")
        checkout_page.inputUnRegCompanyStreet("x")
        checkout_page.inputUnRegCompanyZIP("1" * 6)
        checkout_page.inputUnRegCustomerEmail("x@c.p")
        checkout_page.inputUnRegCustomerPhone("1" * 12)
        checkout_page.inputUnRegCustomerName("x")
        checkout_page.inputUnRegCustomerSurname("x")
        checkout_page.getToNextStepUnregistered()
        checkout_page.getToNextStep()
        validations = checkout_page.getValidationsFirstStep()
        for i in range(5):
            assert validations[i].text == "This field is obligatory"
        self.refresh()
        checkout_page.inputShippingName("x" * 121)
        checkout_page.inputShippingCity("x" * 36)
        checkout_page.inputShippingStreet("x" * 71)
        checkout_page.inputShippingZip("1" * 5)
        checkout_page.inputShippingPhone("1" * 16)
        checkout_page.getToNextStep()
        validations = checkout_page.getValidationsFirstStep()
        for i in range(5):
            if i == 0:
                assert validations[i].text == 'The maximum length for the "Company" field is 120 characters.'
            elif i == 1:
                assert validations[i].text == 'The maximum length for the "City" field is 35 characters.'
            elif i == 2:
                assert validations[i].text == 'The maximum length for the "Street Address" field is 70 characters.'
            elif i == 3:
                assert validations[i].text == 'The field must contain 6 digits.'
            elif i == 4:
                assert validations[i].text == 'The maximum length for the "Phone Number" field is 15 digits.'
        self.refresh()
        checkout_page.clearAll()
        checkout_page.inputShippingName("朋友")
        checkout_page.inputShippingCity("朋友")
        checkout_page.inputShippingStreet("朋友")
        checkout_page.inputShippingZip("1234567")
        checkout_page.inputShippingPhone("1" * 11 + "x")
        checkout_page.getToNextStep()
        validations = checkout_page.getValidationsFirstStep()
        for i in range(3):
            assert validations[i].text == "Please use only latin characters."
        assert validations[3].text == "Phone number is not valid."
