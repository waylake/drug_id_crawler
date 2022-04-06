from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import requests
import pickle

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

drug_dict = {
    'xpath': {
        'drug_id': '/html/body/div[1]/div/div/main/div[2]'
    },
}
class Drug_scraper:
    def __init__(self):
        self.drug_id_list = []
        self.url = "http://idrblab.net/ttd/search/ttd/drm-drug?page="


    def get_drug_id_list(self):
        for i in range(3):
            driver = webdriver.Chrome()
            driver.get(self.url + str(i))
            driver.find_element(By.XPATH, drug_dict['xpath']['drug_id'])



if __name__ == "__main__":
    Drug_scraper()

