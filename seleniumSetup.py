from selenium import webdriver

import requests
import wget
import zipfile
import os

class SeleniumSetup:
    """
    Basic chromedriver setup and driver code for chrome
    """
    
    def __init__(self):
        # get the latest chrome driver version number
        self.url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        self.response = requests.get(self.url)
        self.version_number = self.response.text
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        
        # build the donwload url
        self.download_url = "https://chromedriver.storage.googleapis.com/" + self.version_number +"/chromedriver_win32.zip"
 
    def download_driver(self):
        # download the zip file using the url built above
        self.latest_driver_zip = wget.download(self.download_url,'chromedriver.zip')

        # extract the zip file
        with zipfile.ZipFile(self.latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall() # you can specify the destination folder path here
            
        # delete the zip file downloaded above
        os.remove(self.latest_driver_zip)

    def chrome_driver(self):
        try:
            driver = webdriver.Chrome(options=self.options)    
        except Exception:
            self.download_driver()
            driver = webdriver.Chrome(options=self.options)
        finally:
            chromedriver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            chrome_version = driver.capabilities['browserVersion']
            if chromedriver_version[0:2] != chrome_version[0:2]:
                raise Exception('Driver and Chrome Version Mismatch!! Download latest Chorme version...')
            
        driver.maximize_window()
        return driver

if __name__ == "__main__":
    selenium = SeleniumSetup()
    driver = selenium.chrome_driver()
    url = "https://www.google.com"
    driver.get(url)
    driver.close()