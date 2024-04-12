import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ProcessPage import ProcessPage
from GetRobotsFile import GetRobotsFile
import pandas as pd


def main() -> int:
    driver = get_web_driver()
    robotsFiles = GetRobotsFile()
    robotsFiles.get_robots_file()
    process_page = ProcessPage(driver)
    process_page.process_page()
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
