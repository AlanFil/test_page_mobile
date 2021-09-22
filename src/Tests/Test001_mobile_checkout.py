import unittest
from time import sleep

from appium import webdriver

from src.Pages.CheckoutPage import CheckoutPage
from src.Pages.MainPage import MainPage
from src.Pages.TestProductPage import TestProductPage
from src.common.delivery_methods import DeliveryMethods


class Test001(unittest.TestCase):

    def setUp(self):
        desired_capabilities = {
            "platformName": "Android",
            "platformVersion": "11",
            "deviceName": "emulator-5554",  # cmd -> adb devices
            "browserName": "Chrome"
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_capabilities)
        self.driver.implicitly_wait(10)

    def test_check_title(self):
        main_page = MainPage(self.driver)
        assert 'MatrixMedia.pl' in main_page.get_title()

        test_product_page = TestProductPage(self.driver)
        test_product_page.add_to_chart()

        checkout_page = CheckoutPage(self.driver)
        checkout_page.finalize_order()
        checkout_page.fill_form(subject='private')
        checkout_page.pick_delivery_method(DeliveryMethods.KURIER_DHL)

    def tearDown(self):
        sleep(15)
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
