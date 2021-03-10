import time, sys, pyautogui
import Constances
from Initialization import driverStarter
from selenium import webdriver

# initChrome_captcha_clicker(driver: WebElement)
# input => WebElement
# output => Install captch clicker
def initChrome_captcha_clicker(driver):
    try:
        isUrlLoaded = False
        refreshIndex = 0
        answer = driverStarter.effectiveGet(driver, Constances.url_captcha_clicker)
        while answer == False and isUrlLoaded != True:
            refreshIndex = refreshIndex + 1
            answer = driverStarter.effectiveGet(driver, Constances.url_captcha_clicker)
            if refreshIndex > Constances.MAXIMUM_NUMBER_OF_REFRESHES:
                isUrlLoaded = True
        if isUrlLoaded:
            return False
        time.sleep(15)
        # Click on Install
        pyautogui.click(416, 354)
        time.sleep(5)
        # Click on Install (popup)
        pyautogui.click(907, 272)
        time.sleep(5)
        return True
    except:
        return False

# initChrome_PriceBlink(driver: WebElement)
# input => WebElement
# output => PriceBlink Install
def initChrome_PriceBlink(driver):
    try:
        isUrlLoaded = False
        refreshIndex = 0
        answer = driverStarter.effectiveGet(driver, Constances.url_priceblink)
        while answer == False and isUrlLoaded != True:
            refreshIndex = refreshIndex + 1
            answer = driverStarter.effectiveGet(driver, Constances.url_priceblink)
            if refreshIndex > Constances.MAXIMUM_NUMBER_OF_REFRESHES:
                isUrlLoaded = True
        if isUrlLoaded:
            return False
        time.sleep(10)
        # Click on the window
        pyautogui.click(1000, 15)
        time.sleep(2)
        # Add to chrome
        pyautogui.click(1472, 354)
        time.sleep(2)
        # Install
        pyautogui.click(999, 270)
        time.sleep(4)
        # Close the new tab after install priceBlink
        pyautogui.click(590, 19)
        time.sleep(2)
        # Close Chrome's declaretion to be automatically controlled
        pyautogui.click(1889, 116)
        time.sleep(2)
        return True
    except:
        return False
