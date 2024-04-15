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
        #self.get_materiales()
        #self.select_option()
        self.get_data()

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
                if key != 'Aluminio':
                    disable_element = self.webdriver.find_element(By.XPATH, "//option[@value='414687']")
                    self.webdriver.execute_script("arguments[0].removeAttribute('selected')", disable_element)
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
                self.data_links[self.materiales[key]] = href_link
                self.webdriver.implicitly_wait(2)
                self.webdriver.get(self.url)
                time.sleep(10)
            self.webdriver.close()
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)
        except NoSuchElementException as e:
            print(f'Element not found {e}')
        finally:
            self.webdriver.quit()

    def get_data(self):
        links = {
            "Aluminio": "https://www.ine.es/consul/serie.do?d=true&s=IMM32",
            "Materiales bituminosos": "https://www.ine.es/consul/serie.do?d=true&s=IMM55",
            "Cemento": "https://www.ine.es/consul/serie.do?d=true&s=IMM30",
            "Energía": "https://www.ine.es/consul/serie.do?d=true&s=IMM29",
            "Focos y luminarias": "https://www.ine.es/consul/serie.do?d=true&s=IMM28",
            "Materiales cerámicos": "https://www.ine.es/consul/serie.do?d=true&s=IMM27",
            "Madera": "https://www.ine.es/consul/serie.do?d=true&s=IMM26",
            "Productos plásticos": "https://www.ine.es/consul/serie.do?d=true&s=IMM25",
            "Productos quimicos": "https://www.ine.es/consul/serie.do?d=true&s=IMM24",
            "Aridos y rocas": "https://www.ine.es/consul/serie.do?d=true&s=IMM23",
            "Materiales siderúrgicos": "https://www.ine.es/consul/serie.do?d=true&s=IMM54",
            "Materiales electrónicos": "https://www.ine.es/consul/serie.do?d=true&s=IMM21",
            "Cobre": "https://www.ine.es/consul/serie.do?d=true&s=IMM20",
            "Vidrio": "https://www.ine.es/consul/serie.do?d=true&s=IMM19",
            "Materiales explosivos": "https://www.ine.es/consul/serie.do?d=true&s=IMM18"
        }
        #for key, link in self.data_links.items():
        try:
            for key, link in links.items():
                self.webdriver.get(f'{link}')
                self.webdriver.implicitly_wait(2)
                disable_item = self.webdriver.find_element(By.XPATH, "//option[@value='15']")
                self.webdriver.execute_script("arguments[0].removeAttribute('selected')", disable_item)
                self.webdriver.implicitly_wait(1)
                select_form = self.webdriver.find_element(By.XPATH, "//div[@id='a']//select[@class='menuSelect']")
                select = Select(select_form)
                select.select_by_value("100")
                self.webdriver.implicitly_wait(1)
                submit_btn = self.webdriver.find_element(By.XPATH, "//div[@id='a']//input[@class='botonIr']")
                submit_btn.click()
                time.sleep(5)
                table_element = self.webdriver.find_element(By.XPATH, "//table[@class='general']/tbody")
                rows = table_element.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    cells = row.find_elements(By.XPATH, "./th | ./td")
                    for index, cell in enumerate(cells):
                        print(cell.text)
                        if index == 1:
                            break
            self.webdriver.close()
        except StaleElementReferenceException:
            print("stale")
        except NoSuchElementException as e:
            print(f'Element not found {e}')
        finally:
            self.webdriver.quit()
