
class MainPage:
    page_link = 'http://matrixmedia.pl/'

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.page_link)

    def get_title(self):
        return self.driver.title
