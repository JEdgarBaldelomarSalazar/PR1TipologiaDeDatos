import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from Constants import *


class ProcessPage:

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.url = "https://www.ine.es/jaxiT3/Tabla.htm?t=8381"
        self.materiales = {}
        self.root_xpath = f'//select[@class="cajaVariables jax_SELECT"]'
        self.data_links = {}

    def process_page(self) -> None:
        self.get_materiales()
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
        max_attemps = 3
        attempts = 0
        try:
            for key in self.materiales:
                element_found = False
                self.hide_cookies_div()
                select_element = self.webdriver.find_element(By.XPATH, self.root_xpath)
                select = Select(select_element)
                select.select_by_value(key)
                time.sleep(1)
                iframe = self.webdriver.find_element(By.ID, btn_cosultar_seleccion_id)
                ActionChains(self.webdriver).scroll_to_element(iframe).perform()
                button = self.webdriver.find_element(By.ID, btn_cosultar_seleccion_id)
                button.click()
                time.sleep(1)
                while attempts < max_attemps and not element_found:
                    td_element = WebDriverWait(self.webdriver, 15).until(
                        EC.presence_of_element_located((By.XPATH, ".//table[@id='tablaDatos']//td[@class='sd']")))
                    td_element.click()
                    element_found = True
                time.sleep(1)
                grid_btn = self.webdriver.find_element(By.XPATH, "//div[@id='tooltipWindow']//a[@class='icosTabla flotaderecha']")
                href_link = grid_btn.get_attribute("href")
                self.data_links[key] = href_link
                self.webdriver.implicitly_wait(2)
                self.webdriver.get(self.url)
                time.sleep(10)
            print(self.data_links)
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)
        except NoSuchElementException as e:
            print(f'Element not found {e}')
        finally:
            self.webdriver.quit()
