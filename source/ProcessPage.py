from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from constants import *
class ProcessPage:

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.url = "https://www.ine.es/jaxiT3/Tabla.htm?t=8381"
        self.materiales = {}
        self.root_xpath = f'//select[@class="cajaVariables jax_SELECT"]'

    def process_page(self) -> None:
        self.get_materiales()
        self.select_option()
    def pre_scraping(self):
        #read robots txt
        return 0

    def get_materiales(self):
        self.webdriver.implicitly_wait(2)
        self.webdriver.get(self.url)
        try:
            select_element = self.webdriver.find_element(By.XPATH, self.root_xpath)
            options = select_element.find_elements(By.TAG_NAME, "option")
            for option in options:
                key = option.get_attribute("value")
                value = option.text
                self.materiales[key] = value
        except NoSuchElementException:
            print("Element not found")

    def select_option(self):
        try:
            select_element = self.webdriver.find_element(By.XPATH, self.root_xpath)
            for key in self.materiales:
                xpath = f'./option[@value="{key}"]'
                select_option = select_element.find_element(By.XPATH,  xpath)
                select_option.click()
                iframe = self.webdriver.find_element(By.ID, btn_cosultar_seleccion_id)
                ActionChains(self.webdriver).scroll_to_element(iframe).perform()
                button = self.webdriver.find_element(By.ID, btn_cosultar_seleccion_id)
                button.click()
                content = WebDriverWait(self.webdriver, 5).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, 'sd')))
                print(content.text)
        except NoSuchElementException as e:
            print(f'Element not found {e}')
        finally:
            self.webdriver.quit()
