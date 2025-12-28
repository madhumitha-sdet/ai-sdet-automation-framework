from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserManager:

    @staticmethod
    def get_chrome_driver():
        options = Options()

        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        return driver

