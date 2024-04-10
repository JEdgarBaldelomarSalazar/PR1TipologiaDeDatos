import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def main() -> int:
    options = Options()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome()
    driver.get("https://www.alphabet.com/es-es")
    #interact with webpage
    driver.close()
    return  0

if __name__ == "__main__":
    sys.exit(main())