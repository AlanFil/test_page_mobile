from selenium.common.exceptions import ElementClickInterceptedException


class TestProductPage:
    page_link = 'https://matrixmedia.pl/produkt-testowy-dostepny.html'
    do_koszyka_button = '//button[@onclick="productAddToCartForm.submit(this)"]'

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.page_link)

    def get_title(self):
        return self.driver.title

    def add_to_chart(self):
        for i in range(10):
            try:
                self.driver.find_element_by_xpath(self.do_koszyka_button).click()
                break
            except ElementClickInterceptedException:
                self.driver.execute_script("window.scrollBy(0, 250)")

