import time

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys

import json
import boto3
# import pandas as pd
from io import StringIO

def s3_handler(fileName, data):
    s3 = boto3.client('s3')
    bucket = 'freshket-raw-data'

    # csv_buffer = StringIO()
    # df.to_csv(csv_buffer)
    uploadByteStream = bytes(json.dumps(data).encode('UTF-8'))
    # response = s3.put_object(Bucket=bucket, Key=fileName, Body=csv_buffer.getvalue())
    response = s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)
    return responses

def lambda_handler(event, context):
    driver = WebDriverWrapper()
    url = 'https://www.google.com/'
    driver.get_url(url)

    page_title = driver.get_page_title()
    print("--------------------------")
    print(page_title)
    print("--------------------------")

    driver.close()

    # data = {url: page_title}
    data = {}
    data['url'] = url
    data['page_title'] = page_title
    print(data)
    # df = pd.DataFrame(data.items(), columns=['url','page_title'])
    # print(df)

    fileType = '.json'
    fileName = "data" + fileType
    # Upload data as .csv file into S3
    response = s3_handler(fileName, data)

    return response