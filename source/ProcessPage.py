from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
class ProcessPage:

    def __init__(self, webdriver, url):
        self.webdriver = webdriver
        self.url = url
        self.materiales = {}

    def process_page(self) -> None:
        self.get_materiales()

    def get_materiales(self):
        self.webdriver.get(self.url)
        root_xpath = f'//select[@class="cajaVariables jax_SELECT"]'
        select_element = self.webdriver.find_element(By.XPATH, root_xpath)
        options = select_element.find_elements(By.TAG_NAME, "option")
        for option in options:
            key = option.get_attribute("value")
            value = option.text
            self.materiales[key] = value
