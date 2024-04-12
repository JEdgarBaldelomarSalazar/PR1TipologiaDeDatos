from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from Constants import *
class ProcessPage:

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.url = "https://www.ine.es/jaxiT3/Tabla.htm?t=8381"
        self.materiales = {}
        self.root_xpath = f'//select[@class="cajaVariables jax_SELECT"]'

    def process_page(self) -> None:
        self.get_materiales()
        self.hide_cookies_div()
        self.select_option()

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

    def hide_cookies_div(self):
        try:
            self.webdriver.execute_script(f"document.getElementById('{div_cookies_id}').style.display = 'none';")
        except Exception as e:
            print(f'Accept cookies btn not found: {e}')

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
                    EC.presence_of_element_located((By.CLASS_NAME, 'sd')))
                print(content.text)
        except NoSuchElementException as e:
            print(f'Element not found {e}')
        finally:
            self.webdriver.quit()
