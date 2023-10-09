import time
import pytest
from selenium.common import TimeoutException
from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage
from TestData.TestDataInput import TestDataInput


class TestCart(BaseClass):

    @pytest.mark.parametrize("products", ([TestDataInput.two_products]))
    def test_add_to_cart(self, products):
        log = self.getLogger()
        main_page = mainPage(self.driver)
        self.closeCookies()
        version = main_page.getDBVersion()
        main_page.searchForProduct(products[0])
        assert products[0] == main_page.getProductName().text
        first_product_min_qty = float(main_page.getProductsAtrubbutes()[1].text.split()[1])
        first_product_unit_price = float(main_page.getProductPrices()[0].text)
        first_product_price = round(first_product_unit_price * first_product_min_qty, 2)
        first_product_multi = float(main_page.getProductsAtrubbutes()[0].text.split()[2])
        print(first_product_multi, first_product_min_qty)
        main_page.getAddToCartButton().click()
        main_page.waitTillProductinBasket("1")
        self.back()
        main_page.clearSearch()
        main_page.searchForProduct(products[1])
        assert products[1] == main_page.getProductName().text
        second_product_min_qty = float(main_page.getProductsAtrubbutes()[1].text.split()[1])
        second_product_unit_price = float(main_page.getProductPrices()[0].text)
        second_product_price = round(second_product_unit_price * second_product_min_qty, 2)
        second_product_multi = float(main_page.getProductsAtrubbutes()[0].text.split()[2])
        main_page.getAddToCartButton().click()
        main_page.waitTillProductinBasket("2")
        self.back()
        main_page.clickCartButton()
        cart_page = main_page.getToCart()
        assert cart_page.getCartWeights(0) + cart_page.getCartWeights(1) == cart_page.getWeightTotal()
        assert cart_page.getCartTotalPrices(0) + cart_page.getCartTotalPrices(1) == cart_page.getCartSubtotal()
        assert round(cart_page.getCartShipping() + cart_page.getCartSubtotal(), 2) == cart_page.getGrandTotal()
        assert cart_page.getCartUnitPrices(0) == first_product_unit_price
        assert cart_page.getCartUnitPrices(1) == second_product_unit_price
        assert cart_page.getCartTotalPrices(0) == first_product_price
        assert cart_page.getCartTotalPrices(1) == second_product_price
        cart_page.getIncreaseQTYButtons()[0].click()
        time.sleep(1)
        assert round(first_product_unit_price * (first_product_min_qty + first_product_multi), 2) == cart_page.getCartTotalPrices(0)
        assert round(cart_page.getCartShipping() + cart_page.getCartSubtotal(), 2) == cart_page.getGrandTotal()
        cart_page.inputQTYCart()[0].clear()
        cart_page.inputQTYCart()[0].send_keys(int(first_product_min_qty + first_product_multi * 2))
        cart_page.getIncreaseQTYButtons()[1].click()
        time.sleep(1)
        assert round((first_product_min_qty + first_product_multi * 2) * first_product_unit_price, 2) == cart_page.getCartTotalPrices(0)
        assert round(second_product_unit_price * (second_product_min_qty + second_product_multi), 2) == cart_page.getCartTotalPrices(1)
        assert cart_page.getCartWeights(0) + cart_page.getCartWeights(1) == cart_page.getWeightTotal()
        assert cart_page.getCartTotalPrices(0) + cart_page.getCartTotalPrices(1) == cart_page.getCartSubtotal()
        assert round(cart_page.getCartShipping() + cart_page.getCartSubtotal(), 2) == cart_page.getGrandTotal()
