from selenium.webdriver.common.by import By
import time
class ProcessPage:

    def __init__(self, webdriver, url):
        self.webdriver = webdriver
        self.url = url

    def process_page(self, elements) -> None:
        self.webdriver.get(self.url)
        for element in elements:
            try:
                self.webdriver.implicitly_wait(2)
                xpath = f"//option[text()='{element}']"
                selected_option = self.webdriver.find_element(By.XPATH, xpath)
                selected_option.click()
                send_button = self.webdriver.find_element(By.ID, 'botonConsulSele')
                send_button.click()
            except Exception as e:
                print("Error occurred", e)

# Wait for the search input element to be visible
   #wait = WebDriverWait(driver, 10)