import time
import json
import boto3
# import pandas as pd
from io import StringIO

from webdriver_wrapper import WebDriverWrapper

from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

import requests
import re
from datetime import datetime

from multiprocessing import Process, Pipe
from multiprocessing.pool import ThreadPool

import threading

def s3_handler(fileName, data):
    s3 = boto3.client('s3')
    bucket = 'freshket-raw-data'

    # csv_buffer = StringIO()
    # df.to_csv(csv_buffer)
    uploadByteStream = bytes(json.dumps(data).encode('UTF-8'))
    # response = s3.put_object(Bucket=bucket, Key=fileName, Body=csv_buffer.getvalue())
    response = s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)
    return response

def parsing(driver, category_name):
    list_product_id = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]")
    list_product_name = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/a/div")
    list_product_unit_price = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div")
    list_product_image  = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/a/div/div/div/img")
    list_product_price = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]")
    data = []
    for raw_product_id, raw_product_name, raw_product_price, raw_product_unit_price, raw_product_image in zip(list_product_id, list_product_name, list_product_price, list_product_unit_price, list_product_image):
        product_id = raw_product_id.text.split(' ')[-1]
        product_name = raw_product_name.text
        product_price = raw_product_price.text.split(' ')[0].strip()
        product_unit_price = raw_product_unit_price.text.split(' ')[2].strip()
        product_image = raw_product_image.get_attribute("src")
        data.append({"category_name_th": category_name, "makroClick_id": product_id,"product_name": product_name, "product_price": product_price, "unit_price": product_unit_price, "product_image": product_image, "date": datetime.now()})
        # print(product_id, product_name, product_price, product_unit_price)
    print(data)
    # Return data from each page
    return data

def parsing_next(driver, category_name):
    list_product_id = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div/div/div/div[1]")
    list_product_name = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div/div/div/a/div")
    list_product_unit_price = getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div/div/div/div[3]/div")
    list_product_image  = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div/div/a/div/div/div/img")
    list_product_price = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]")
    data = []
    for raw_product_id, raw_product_name, raw_product_price, raw_product_unit_price, raw_product_image in zip(list_product_id, list_product_name, list_product_price, list_product_unit_price, list_product_image):
        product_id = raw_product_id.text.split(' ')[-1]
        product_name = raw_product_name.text
        product_price = raw_product_price.text.split(' ')[0].strip()
        product_unit_price = raw_product_unit_price.text.split(' ')[2].strip()
        product_image = raw_product_image.get_attribute("src")
        data.append({"category_name_th": category_name, "makroClick_id": product_id,"product_name": product_name, "product_price": product_price, "unit_price": product_unit_price, "product_image": product_image, "date": datetime.now()})
        # print(product_id, product_name, product_price, product_unit_price)
    print(data)
    # Return data from each page
    return data

def getElements(driver, XPATH):
    try:
        delay = 3 # seconds
        # Explicit wait with waiting until all elements in XPATH is located 
        elements = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, XPATH)))
        # print("Page is ready!")
        # print(elements)
        return elements
    except TimeoutException:
        # print("Loading took too much time!")
        # Return empty array
        return [None]*10

def scrollDown(driver):
    driver.maximize_window()
    y = 500
    for timer in range(0,10):
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 500
        time.sleep(1)

def getPages(driver):
    try:
        delay = 20
        # Get all page links
        XPATH_PAGE_MAIN = "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div"
        pages = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, XPATH_PAGE_MAIN)))
        return pages
    except TimeoutException:
        print("Cannot load all pages")
        # Return -1
        return [None]*10

def getNumberOfLastPage(driver):
    # Get elements of pages
    # page = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div/div[2]/div/div")
    # print(page[-1].text)
    # print(driver.current_url)
    try:
        delay = 3
        pages = getPages(driver)
        size = len(pages)
        # print(size)
        XPATH_PAGE_MAIN = "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div"
        XPATH_LAST_PAGE = XPATH_PAGE_MAIN + "[{0}]".format(size)
        # print(XPATH_LAST_PAGE)
        last_page = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, XPATH_LAST_PAGE)))
        # last_page = driver.find_element_by_xpath(XPATH_LAST_PAGE)

        # Click on the last icon to go to the last page        
        driver.execute_script("arguments[0].click()", last_page)
        time.sleep(delay)
        
        # Go to the last page by selecting the last elements
        # print(driver.current_url)
        res = re.split('[?&]', driver.current_url)

        # Get the number of the last page (page=XX)
        numberOfLastPage = int(res[1].split("page=")[-1])
        # print(numberOfLastPage)
        # Get elements of the last pages
        return numberOfLastPage
    except TimeoutException:
        print("Cannot load last page")
        # Return -1
        return -1

def getNumberOfCategories(driver):
    category_main = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div")
    hover = ActionChains(driver).move_to_element(category_main)
    hover.perform()
    XPATH = "/html/body/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/p"
    category_elements = driver.find_elements_by_xpath(XPATH)
    return len(category_elements)

def findPossiblePage(driver):
    arr = []
    pages = getPages(driver)
    for page in pages:
        if(page.text.isdigit()):
            arr.append(page.text)
            
def extractData(category_url, category_name, number_pages):
    # print(category_name)
    driver = get_driver()
    temp = []
    for i in range(1, number_pages+1):
        each_page = category_url + "?page=" + str(i)+"&all=true"
        print(each_page)
        driver.get(each_page)
        # print(driver.current_url)

        # Scroll down page to load images completely
        # scrollDown(driver)
        
        # Extract data from each page in the category page
        data = parsing(driver, category_name)
        # Extend data in temp list
        temp.extend(data)
        # print(temp)
    
    print(temp)
    # df = pd.DataFrame(temp)
    # print(df)
    # df.to_csv("csv\makroClick\makroClick_{0}.csv".format(category_name), index=False)

    fileType = '.json'
    fileName = "data" + fileType
    # Upload data as .csv file into S3
    # response = s3_handler(fileName, data)
    # return response

def getCategoryLink(driver):
    driver.get("https://www.makroclick.com/th/category/vegetable-and-fruit?menuFlagId=8&flag=true")
    elements = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/a")
    links = []
    for e in elements:
        url = e.get_attribute("href")
        links.append(url)
        
    return links

threadLocal = threading.local()

def get_driver():
  driver = getattr(threadLocal, 'driver', None)
  if driver is None:
    browser = WebDriverWrapper()
    driver = browser._driver
    setattr(threadLocal, 'driver', driver)
  return driver

def scrap(driver, url):
    category_name = url.split("https://www.makroclick.com/th/category/")[-1]
    # print(url)
    driver = get_driver()
    driver.get(url)
    # number_pages = getNumberOfLastPage(driver)
    XPATH_PAGE_MAIN = "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div"
    XPATH_LAST_PAGE = XPATH_PAGE_MAIN + "[{0}]".format(2)
    # print(XPATH_LAST_PAGE)
    second_page = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, XPATH_LAST_PAGE)))
    # print(second_page)
    driver.execute_script("arguments[0].click()", second_page)
    time.sleep(3)
    print(driver.current_url)
    parsing_next(driver, category_name)
    # print(number_pages)
    # extractData(url, category_name, number_pages)

def lambda_handler(event, context):
    
    # parsing(driver, "butchery")
    browser = WebDriverWrapper()
    driver = browser._driver
    links = getCategoryLink(driver)

    # print(links)
    for url in links:
        # print(driver.current_url)
        scrap(driver, url)

    # print(driver.title)
    # run(driver)

    # data = {url: page_title}
    # data = {}
    # data['url'] = url
    # data['page_title'] = page_title
    # print(data)
    # df = pd.DataFrame(data.items(), columns=['url','page_title'])
    # print(df)

    # fileType = '.json'
    # fileName = "data" + fileType
    # # Upload data as .csv file into S3
    # response = s3_handler(fileName, data)

    return {"Status": "Done"}