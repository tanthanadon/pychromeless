import time

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys

import time

import json
import boto3
import pandas as pd

if __name__ == "__main__":
    driver = WebDriverWrapper()

    driver.get_url('https://www.google.com/')

    page_title = driver.get_page_title()
    print("--------------------------")
    print(page_title)
    print("--------------------------")

    driver.close()

    data = {}
    data['page_title'] = page_title
    df = pd.DataFrame(data)
    df.to_csv("s3://freshket-marketprice/test.csv", index=False)