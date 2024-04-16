import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from Constants import *
from CreateDataSet import CreateDataSet
from Driver import Driver


class ProcessPage:
    """Clase que representa el responsable de procesar una página web"""

    def __init__(self):
        """Constructor que nnicializa propiedades de la clase que se usarán"""
        self.url = "https://www.ine.es/jaxiT3/Tabla.htm?t=8381"
        self.materiales = {}
        self.root_xpath = f'//select[@class="cajaVariables jax_SELECT"]'#Xpath para buscar en la página la sección select
        self.data_links = {}

    def process_page(self) -> None:
        """Llama a los métodos que procesan la página web"""
        self.get_materiales()
        self.select_option()
        self.process_data()

    def get_materiales(self):
        """
            Este método de las opciones del desplegable procesa cada una

            Navega a la página web, selecciona cada material
            disponible en el menú desplegable, procesa cada opcion y guarda el value y el texto del tag
        """
        driver = Driver()
        web_driver = driver.get_web_driver()
        web_driver.implicitly_wait(2)
        web_driver.get(self.url)
        try:
            select_element = web_driver.find_element(By.XPATH, self.root_xpath)
            options = select_element.find_elements(By.TAG_NAME, "option")
            for option in options:
                key = option.get_attribute("value")
                value = option.text
                self.materiales[key] = value
            web_driver.close()
            web_driver.quit()
        except NoSuchElementException:
            print("Element not found")
        finally:
            web_driver.quit()

    def hide_cookies_div(self, web_driver):
        """
            Dado el driver ejecuta un script para que obtener del DOM un elemento el el ID: div_cookies_id para no mostarlo
            :param web_driver:
            :return: None
        """
        try:
            web_driver.implicitly_wait(3)
            web_driver.execute_script(f"document.getElementById('{div_cookies_id}').style.display = 'none';")
        except Exception as e:
            print(f'Accept cookies btn not found: {e}')

    def select_option(self):
        """
            Este método instancia un driver con la página web.

            Por cada opción, cerramos el div de cookies y verificamos que el valor de la opción no sea "Aluminio".
            En caso de serlo, la deshabilitamos con JavaScript.
            Luego de seleccionar la opción, hacemos scroll y buscamos el botón de submit.
            En la siguiente página, indicamos que espere hasta la presencia del elemento
            .//table[@id='tablaDatos']//td[@class='sd'] para obtener su atributo href.
            Guardamos, para cada clave, su href.
            Al finalizar las opciones, cerramos el webdriver y salimos.
            :return:
            - None
        """
        max_attemps = 3
        attempts = 0
        driver = Driver()
        web_driver = driver.get_web_driver()
        web_driver.get(self.url)
        try:
            for key in self.materiales:
                element_found = False
                self.hide_cookies_div(web_driver)
                if key != 'Aluminio':
                    web_driver.implicitly_wait(2)
                    disable_element = web_driver.find_element(By.XPATH, "//option[@value='414687']")
                    web_driver.execute_script("arguments[0].removeAttribute('selected')", disable_element)
                select_element = web_driver.find_element(By.XPATH, self.root_xpath)
                select = Select(select_element)
                select.select_by_value(key)
                time.sleep(1)
                iframe = web_driver.find_element(By.ID, btn_cosultar_seleccion_id)
                ActionChains(web_driver).scroll_to_element(iframe).perform()
                button = web_driver.find_element(By.ID, btn_cosultar_seleccion_id)
                button.click()
                time.sleep(1)
                while attempts < max_attemps and not element_found:
                    td_element = WebDriverWait(web_driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, ".//table[@id='tablaDatos']//td[@class='sd']")))
                    td_element.click()
                    element_found = True
                time.sleep(1)
                grid_btn = web_driver.find_element(By.XPATH,
                                                       "//div[@id='tooltipWindow']//a[@class='icosTabla flotaderecha']")
                href_link = grid_btn.get_attribute("href")
                self.data_links[self.materiales[key]] = href_link
                web_driver.implicitly_wait(2)
                web_driver.get(self.url)
                time.sleep(10)
            web_driver.close()
            web_driver.quit()
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)
        except NoSuchElementException as e:
            print(f'Element not found {e}')

    def get_data_table(self, link) -> {}:
        """
            Este método instancia un driver con el enlace proporcionado.

            Busca la opción con el valor 15 para deshabilitarla con JavaScript.
            Luego, busca todas las opciones y las selecciona todas, identificadas con el valor 0.
            Posteriormente, busca el botón "Ir" y hace clic para procesar la tabla con los índices.
            Por cada fila, procesa cada celda, pero solo se almacenan los datos de las dos primeras celdas,
            las demás se omiten.
            Finalmente, cierra el webdriver y sale.

            :param link: El enlace de la página web de la cual se extraerán los datos de la tabla.
            :return: None
        """
        data = []
        driver = Driver()
        web_driver = driver.get_web_driver()
        try:
            time.sleep(2)
            web_driver.get(link)
            web_driver.implicitly_wait(2)
            disable_item = web_driver.find_element(By.XPATH, "//option[@value='15']")
            web_driver.execute_script("arguments[0].removeAttribute('selected')", disable_item)
            web_driver.implicitly_wait(1)
            select_form = web_driver.find_element(By.XPATH, "//div[@id='a']//select[@class='menuSelect']")
            select = Select(select_form)
            select.select_by_value("0")#option value todos es 0
            web_driver.implicitly_wait(1)
            submit_btn = web_driver.find_element(By.XPATH, "//div[@id='a']//input[@class='botonIr']")
            submit_btn.click()
            time.sleep(5)
            table_element = web_driver.find_element(By.XPATH, "//table[@class='general']/tbody")
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                row_data = []
                cells = row.find_elements(By.XPATH, "./th | ./td")
                for index, cell in enumerate(cells):
                    row_data.append(cell.text)
                    if index == 1:
                        break
                data.append(row_data)
            web_driver.close()
            web_driver.quit()
            time.sleep(1)
            return data
        except NoSuchElementException as e:
            print(f'Element not found {e}')

    def process_data(self):
        """
            Instancia un objeto para exportar los datos a un archivo CSV.
            Para cada enlace en self.data_links, se llama al método get_data_table para obtener la información de la tabla.
            La información obtenida se pasa como parámetro al método export_csv para ser exportada a un archivo CSV.

            :return: None
        """
        save_data = CreateDataSet()
        try:
            for key, link in self.data_links.items():
                content = self.get_data_table(link)
                save_data.export_csv(key, content)
        except Exception as e:
            print(f"An error occurred: {e}")
