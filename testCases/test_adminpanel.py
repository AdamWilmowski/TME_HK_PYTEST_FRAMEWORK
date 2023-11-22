import time
import pytest
from selenium.common import NoSuchElementException
from TestData.TestDataInput import TestDataInput
from utilities.BaseClass import BaseClass
from TestData.SQLDatabase import SQLFunctions
from pageObjects.adminPage import AdminPage


class TestAdminPanel(BaseClass):

    def test_admin_order_basic(self):
        self.stopLoad()
        self.get_to("https://beta.tme.hk/tme-office/login")
        sql_function = SQLFunctions()
        admin_page = AdminPage(self.driver)
        admin_page.loginToAdmin()
        db_version = admin_page.getDBVersion()
        admin_page.getToOrders()
        try:
            admin_page.createNewOrder()
        except NoSuchElementException:
            admin_page.loginToAdmin()
            admin_page.createNewOrder()
        email = sql_function.getRandomCustomerEmail(db_version)
        admin_page.inputCustomerEmailOrder(email)
        admin_page.submitSearchOrder()
        admin_page.initialPlaceOrderButton()
        time.sleep(1)
        admin_page.inputSku("USL1M-DIO")
        admin_page.inputQTY("100")
        admin_page.waitTillSubmitOrderClickable()
        current_price = admin_page.getCurrentPrice()
        subtotal = admin_page.getSubtotal()
        transport_cost = admin_page.getTransportCost()
        grand_total = admin_page.getAdminGrandTotal()
        assert subtotal == round(current_price * 100, 2)
        assert grand_total == round(subtotal + transport_cost, 2)
        admin_page.submitOrder()
        summary_unit_price = admin_page.getOrderSummaryUnitPrice()
        summary_subtotal = admin_page.getOrderSummarySubtotal()
        summary_qty = admin_page.getOrderSummaryQTY()
        summary_total = admin_page.getOrderSummaryTotal()
        summary_statuses = admin_page.getOrderSummaryStatuses()
        assert subtotal == summary_subtotal
        assert summary_qty == 100
        assert summary_unit_price == current_price
        assert grand_total == summary_total
        #assert summary_statuses[-1] == "-" or summary_statuses[-1] == "200"
        admin_page.waitTillOrderStatus("Placed")

    @pytest.mark.parametrize("test_products", [TestDataInput.two_products])
    def test_admin_order_custom_price(self, test_products):
        self.stopLoad()
        self.get_to("https://beta.tme.hk/tme-office/login")
        sql_function = SQLFunctions()
        admin_page = AdminPage(self.driver)
        admin_page.loginToAdmin()
        db_version = admin_page.getDBVersion()
        admin_page.getToOrders()
        try:
            admin_page.createNewOrder()
        except NoSuchElementException:
            admin_page.loginToAdmin()
            admin_page.createNewOrder()
        email = sql_function.getRandomCustomerEmail(db_version)
        admin_page.inputCustomerEmailOrder(email)
        admin_page.submitSearchOrder()
        admin_page.initialPlaceOrderButton()
        time.sleep(0.5)
        for product in test_products:
            admin_page.inputSku(product)
            admin_page.inputQTY("100")
            admin_page.waitTillSubmitOrderClickable()
        minimal_price = admin_page.getMinimalPrice()
        admin_page.inputCustomPrice(product=1, text=minimal_price * 0.8)
        admin_page.submitOrder()
        time.sleep(5)

