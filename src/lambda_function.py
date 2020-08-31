import time

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()

    driver.get_url('https://www.google.com/')

    print("--------------------------")
    print(driver.get_page_title())
    print("--------------------------")

    driver.close()
