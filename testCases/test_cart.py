import pytest

from utilities.BaseClass import BaseClass
from pageObjects.mainPage import mainPage

class TestCart(BaseClass):

    @pytest.mark.parametrize()
    def test_add_to_cart(self):
        main_page = mainPage(self.driver)