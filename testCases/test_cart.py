import pytest

from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage
from TestData.TestDataInput import TestDataInput

class TestCart(BaseClass):

    @pytest.mark.parametrize("products", ([TestDataInput.two_products]))
    def test_add_to_cart(self):
        log = self.getLogger()
        main_page = mainPage(self.driver)

