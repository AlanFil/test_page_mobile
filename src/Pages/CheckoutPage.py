from random import randrange

from selenium.common.exceptions import ElementClickInterceptedException


class CheckoutPage:
    realizuj_button = '//button[@title="Realizuj"]'
    akceptuj_regulamin_checkbox = '//input[@id="agreement-4"]'
    zloz_zamowienie_button = '//button[@id="aitcheckout-place-order"]'

    def __init__(self, driver):
        self.driver = driver

    def intercepted_exception_click(self, xpath_to_element):
        for i in range(10):
            try:
                self.driver.find_element_by_xpath(xpath_to_element).click()
                break
            except ElementClickInterceptedException:
                self.driver.execute_script("window.scrollBy(0, 250)")

    def finalize_order(self):
        self.intercepted_exception_click(self.realizuj_button)

    def fill_form(self, subject='private'):
        if subject == 'company':
            self.driver.find_element_by_xpath('//*[@id="type_f"]').clear()
            self.driver.find_element_by_xpath('//*[@id="type_f"]').click()
            self.driver.find_element_by_xpath('//*[@id="billing:company"]').clear()
            self.driver.find_element_by_xpath('//*[@id="billing:company"]').send_keys('Testerzy Sp. z o.o.')
            self.driver.find_element_by_xpath('//*[@id="billing:vat_id"]').clear()
            self.driver.find_element_by_xpath('//*[@id="billing:vat_id"]').send_keys('0123456789')

        self.driver.find_element_by_xpath('//*[@id="billing:firstname"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:firstname"]').send_keys('Test')
        self.driver.find_element_by_xpath('//*[@id="billing:lastname"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:lastname"]').send_keys('Test')
        self.driver.find_element_by_xpath('//*[@id="billing:email"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:email"]').send_keys('test@matrixmedia.pl')
        self.driver.find_element_by_xpath('//*[@id="billing:street1"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:street1"]').send_keys('ul. Testowa')
        self.driver.find_element_by_xpath('//*[@id="billing:street2"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:street2"]').send_keys('1')
        self.driver.find_element_by_xpath('//*[@id="billing:city"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:city"]').send_keys('Testowo')
        self.driver.find_element_by_xpath('//*[@id="billing:postcode"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:postcode"]').send_keys('11-111')
        self.driver.find_element_by_xpath('//*[@id="billing:telephone"]').clear()
        self.driver.find_element_by_xpath('//*[@id="billing:telephone"]').send_keys('123456789')

        self.driver.hide_keyboard()

    def pick_delivery_method(self, method):
        self.driver.execute_script("window.scrollBy(0, 350)")
        self.intercepted_exception_click(f'//input[contains(@value, "{method}")]')

        drawn_method = ''
        if method == 'Paczkomaty':
            drawn_method = draw_paczkomat(self.driver)
        elif method == 'Odbiór osobisty':
            drawn_method = draw_odbior_osobisty(self.driver)
        elif method == 'Wysyłka z wniesieniem - pakiety':
            drawn_method = draw_wysylka_z_wniesieniem(self.driver)

        print(method if drawn_method == '' else f'{method} - {drawn_method}')

    def pick_payment_method(self):
        i = 0
        while i < 60:
            avaliable_methods = self.driver.find_elements_by_xpath('//div[@id="co-payment-form"]/fieldset/dt')
            if avaliable_methods:
                break
            i += 1
            sleep(1)
        else:
            avaliable_methods = []

        metody = [metoda.get_attribute('id') for metoda in avaliable_methods]
        lista = [metoda for metoda in metody if
                 metoda == 'dt_method_cashondelivery' or metoda == 'dt_method_banktransfer']
        wybrana_metoda = choice(lista)
        if lista:
            self.driver.find_element_by_xpath(
                f'//div[@id="co-payment-form"]/fieldset/dt[@id="{wybrana_metoda}"]').click()
        else:
            print("Brak metody płatności")  # TODO: some error
            return False

    def submit_order(self):
        intercepted_exception_click(self.akceptuj_regulamin_checkbox)
        intercepted_exception_click(self.zloz_zamowienie_button)


def draw_paczkomat(driver):
    liczba_wojewodztw = len(driver.find_elements_by_xpath('//select[@id="paczkomaty_province_select"]/*'))
    losowe_wojewodztwo = randrange(2, liczba_wojewodztw + 1)
    wylosowane_wojewodztwo = driver.find_element_by_xpath(
        f'//select[@id="paczkomaty_province_select"]/*[{losowe_wojewodztwo}]').text
    driver.find_element_by_xpath(f'//select[@id="paczkomaty_province_select"]/*[{losowe_wojewodztwo}]').click()

    liczba_paczkomatow = len(driver.find_elements_by_xpath('//select[@id="paczkomaty_select"]/*'))
    losowy_paczkomat = randrange(2, liczba_paczkomatow + 1)
    wylosowany_paczkomat = driver.find_element_by_xpath(
        f'//select[@id="paczkomaty_select"]/*[{losowy_paczkomat}]').text
    driver.find_element_by_xpath(driver, f'//select[@id="paczkomaty_select"]/*[{losowy_paczkomat}]').click()

    return f'{wylosowane_wojewodztwo}\n{wylosowany_paczkomat}'


def draw_odbior_osobisty(driver):
    liczba_miejsc = len(
        driver.find_elements_by_xpath('//select[@id="pickup_store_shipping_method_selector"]/*')[1:])
    losowe_miejsce = randrange(2, liczba_miejsc + 1)
    wylosowane_miejsce = driver.find_element_by_xpath(
        f'//select[@id="pickup_store_shipping_method_selector"]/*[{losowe_miejsce}]').text
    driver.find_element_by_xpath(driver,
                                 f'//select[@id="pickup_store_shipping_method_selector"]/*[{losowe_miejsce}]') \
        .click()

    return wylosowane_miejsce


def draw_wysylka_z_wniesieniem(driver):
    liczba_pakietow = len(driver.find_elements_by_xpath('//select[@id="pickup_store_shipping_method_selector"]/*'))
    losowy_pakiet = randrange(2, liczba_pakietow + 1)
    wylosowany_pakiet = driver.find_element_by_xpath(
        f'//select[@id="pickup_store_shipping_method_selector"]/*[{losowy_pakiet}]').text
    driver.find_element_by_xpath(driver,
                                 f'//select[@id="pickup_store_shipping_method_selector"]/*[{losowy_pakiet}]') \
        .click()

    return wylosowany_pakiet
