from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects import registrationPage
from pageObjects import loginPage
from pageObjects import cartPage
from pageObjects import checkoutPage
from pageObjects import accountPage


class mainPage:

    def __init__(self, driver):
        self.driver = driver

    register_button = (By.LINK_TEXT, "Register")
    login_button = (By.LINK_TEXT, "Login")
    version = (By.XPATH, "//div[@class='site-footer__text']")
    search = (By.XPATH, "//input[@type='search']")
    add_to_cart = (By.XPATH, "//button[normalize-space()='Add to cart']")
    cart_button = (By.XPATH, '//*[@id="sylius-cart-button"]/button')
    view_cart = (By.LINK_TEXT, "View and edit cart")
    go_to_checkout = (By.LINK_TEXT, "Go to checkout")
    product_name = (By.CSS_SELECTOR, ".product-name.font-weight-bold.m-t-5")
    product_prices = (By.CSS_SELECTOR, "td[class='right aligned']")
    products_attributes = (By.CSS_SELECTOR, "p[class='no-wrap']")
    dropdown_button = (By.XPATH, "//i[@class='dropdown icon']")
    my_orders_button = (By.LINK_TEXT, "My Orders")

    def getToRegistrationPage(self):
        self.driver.find_element(*mainPage.register_button).click()
        registration_page = registrationPage.RegistrationPage(self.driver)
        return registration_page

    def getDBVersion(self):
        version = self.driver.find_element(*mainPage.version).text
        db_version = version.split()[-1]
        return db_version

    def getToLoginPage(self):
        self.driver.find_element(*mainPage.login_button).click()
        login_page = loginPage.LoginPage(self.driver)
        return login_page

    def getToMyOrders(self):
        self.driver.find_element(*mainPage.dropdown_button).click()
        self.driver.find_element(*mainPage.my_orders_button).click()
        account_page = accountPage.AccountPage(self.driver)
        return account_page

    def searchForProduct(self, text):
        self.driver.find_element(*mainPage.search).send_keys(text)
        self.driver.find_element(*mainPage.search).send_keys(Keys.ENTER)

    def getAddToCartButton(self):
        return self.driver.find_element(*mainPage.add_to_cart)

    def clearSearch(self):
        self.driver.find_element(*mainPage.search).clear()

    def getProductName(self):
        return self.driver.find_element(*mainPage.product_name)

    def getProductPrices(self):
        return self.driver.find_elements(*mainPage.product_prices)

    def getProductsAtrubbutes(self):
        return self.driver.find_elements(*mainPage.products_attributes)

    def waitTillProductinBasket(self, text):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="sylius-cart-button"]/button'), text))

    def clickCartButton(self):
        self.driver.find_element(*mainPage.cart_button).click()

    def getToCart(self):
        self.driver.find_element(*mainPage.cart_button).click()
        self.driver.find_element(*mainPage.view_cart).click()
        cart_page = cartPage.CartPage(self.driver)
        return cart_page

    def getToCheckout(self):
        self.driver.find_element(*mainPage.cart_button).click()
        self.driver.find_element(*mainPage.go_to_checkout).click()
        checkout_page = checkoutPage.CheckoutPage(self.driver)
        return checkout_page

