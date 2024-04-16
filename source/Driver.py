from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Driver:

    def __init__(self):
        options = Options()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        options.add_argument(f'--user-agent={user_agent}')
        self.webdriver = webdriver.Chrome()

    def get_web_driver(self):
        return self.webdriver

    def close_web_driver(self):
        self.webdriver.close()

    def quit_web_driver(self):
        self.webdriver.quit()