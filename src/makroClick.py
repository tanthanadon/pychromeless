from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

class MakroClick:
    def __init__(self, driver):
        self.driver = driver
    
    def parsing(self, driver, category_name):
        list_product_id = self.getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]")
        list_product_name = self.getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/a/div")
        list_product_unit_price = self.getElements(driver, "/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[3]/div")
        list_product_image  = self.getElements(driver,"/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/a/div/div/div/img")
        list_product_price = self.getElements(driver,"/html/body/div[1]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]")
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

    def getElements(self, driver, XPATH):
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

