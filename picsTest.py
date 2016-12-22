#!/usr/bin/python3.5
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def pullPics(pid):
    driver = webdriver.Firefox()
    driver.get('google.com')
    name = "attachment-post-thumbnail wp-post-image"
    elem = safeElem(driver, name)
    print(elem.text)


def safeElem(driver, name):
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, name))
        )
        return elem
        
    finally:
        print("failed")
        driver.quit()


if __name__ == '__main__':
    pullPics(1)
