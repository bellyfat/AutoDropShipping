import time, Constances
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Return the driver after initialize to only English, full screen and etc.
def startDriver():
    # options: properties of webdriver chrome while running
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    options.add_argument("--lang=en-US")
    options.add_argument("--lang=en-GB")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    # Base on the location of webdriver
    # r => conver from string to raw string
    driver = webdriver.Chrome(options=options, executable_path=r'C:\\Users\\ASUS\\Desktop\\פרוייקטים\\AD - Automatic Dropshipping\\AutomaticDropshipping\\chromedriver.exe')
    return driver

# Effectively switch between pages
# Return True if new page loaded
# Otherwise - Return False
def effectiveGet(driver, nextPageUrl):
    driver.get(nextPageUrl)
    startTime = time.time()
    while driver.current_url != nextPageUrl and driver.current_url != (nextPageUrl + '/'):
        currentTime = time.time()
        if currentTime - startTime > Constances.TIME_DELAY_GET_NEW_URL:
            return False
    return True
