import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ProcessPage import ProcessPage
import pandas as pd
def main() -> int:
    materiales = ['Aluminio']#, 'Materiales bituminosos', 'Cemento', 'Energía', 'Focos y luminarias', 'Focos y luminarias', 'Madera', 'Productos plásticos', 'Productos quimicos', 'Aridos y rocas', 'Materiales siderúrgicos', 'Materiales electrónicos', 'Cobre', 'Vidrio', 'Materiales explosivos']
    driver = get_web_driver()
    url = "https://www.ine.es/jaxiT3/Tabla.htm?t=8381&L=0"
    process_page = ProcessPage(driver, url)
    process_page.process_page(materiales)
    driver.close()
    return 0

def get_web_driver() -> webdriver:
    options = Options()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome()
    return driver

if __name__ == "__main__":
    sys.exit(main())