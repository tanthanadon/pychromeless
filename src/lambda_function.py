import time

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys

import boto3
from botocore.config import Config

import pandas as pd


def connectS3():
    # Hard coded strings as credentials, not recommended.
    ACCESS_KEY = 'AKIAVWC2ULHFJG47BFKC'
    SECRET_KEY = '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'
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    return s3_resource


def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


def lambda_handler(*args, **kwargs):
    s3_resource = connectS3()
    driver = WebDriverWrapper()

    driver.get_url('https://www.google.com/')
    page_title = driver.get_page_title()
    print("--------------------------")
    print(page_title)
    print("--------------------------")

    data = {'web': ['test', 'google'], 'page_title': ['page_test', page_title]}
    df = pd.DataFrame(data)
    print(df)
    df.to_csv("data.csv", index=False)
    Filename = "data.csv"
    Bucketname = "aws-ap-southeast-1-391032101322-marketprice-pipe"

    s3_resource.meta.client.upload_file(
        Filename=Filename, Bucket=Bucketname,
        Key=Filename)
    print(s3_resource)
    driver.close()
