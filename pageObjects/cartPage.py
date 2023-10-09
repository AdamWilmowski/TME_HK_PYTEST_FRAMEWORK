from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    def __init__(self, driver):
        self.driver = driver

    cart_weights = (By.XPATH, "//td[3]/div/div/p/span")
    weight_total = (By.CSS_SELECTOR, "div[data-update-field='weightTotal']")
    cart_unit_prices = (By.XPATH, "//td[4]/div/div/p/span")
    cart_total_prices = (By.XPATH, "//td[5]/div/div/p/span")
    cart_subtotal = (By.CSS_SELECTOR, "div[data-update-field='orderSubtotal']")
    cart_shipping = (By.CSS_SELECTOR, "div[data-update-field='shippingTotal']")
    increase_qty_button = (By.XPATH, "//i[@class='caret right icon']")
    qty_input_field = (By.ID, "sylius_cart_item_quantity")
    cart_grand_total = (By.CSS_SELECTOR, "span[class='text-size-big color-primary']")

    def getCartWeights(self, number):
        weight_list = []
        element_list = self.driver.find_elements(*CartPage.cart_weights)
        for element in element_list:
            weight_list.append(float(element.text.split()[0]))
        return weight_list[number]

    def getWeightTotal(self):
        weight_uncut = self.driver.find_element(*CartPage.weight_total).text
        weight = float(weight_uncut.split()[0])
        return weight

    def getCartUnitPrices(self, number):
        elements = self.driver.find_elements(*CartPage.cart_unit_prices)
        list_of_unit_prices = []
        for element in elements:
            list_of_unit_prices.append(float(element.text.split()[1]))
        return list_of_unit_prices[number]

    def getCartTotalPrices(self, number):
        element_list = self.driver.find_elements(*CartPage.cart_total_prices)
        prices = []
        for element in element_list:
            prices.append(float(element.text.split()[1]))
        return prices[number]

    def getCartSubtotal(self):
        return float(self.driver.find_element(*CartPage.cart_subtotal).text.split()[1])

    def getCartShipping(self):
        return float(self.driver.find_element(*CartPage.cart_shipping).text.split()[1])

    def getIncreaseQTYButtons(self):
        return self.driver.find_elements(*CartPage.increase_qty_button)

    def inputQTYCart(self):
        return self.driver.find_elements(*CartPage.qty_input_field)


    def getGrandTotal(self):
        return float(self.driver.find_element(*CartPage.cart_grand_total).text.split()[1])
