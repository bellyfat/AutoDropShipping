import Constances, time, sys, os
from Navigation import Tools
from Initialization import driverStarter
from pyrobogui import robo
from urllib.parse import urlparse

url = 'https://www.ebay.com/b/Diecast-Toy-Vehicles/222/bn_1850842?rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&rt=nc&_pgn=166'
driver = driverStarter.startDriver()
driverStarter.effectiveGet(driver, url)
answer = True
last_height = heightToScroll = 0
while answer == True:
    currentPage = driver.current_url
    urllist = urlparse(currentPage)
    website = urllist[1].replace('.com','').lower()
    if 'ebay' in website:
        # Ebay page
        answer = Tools.tryIncreasePageNumber_Ebay(currentPage)
        nextPageHref = Tools.fixHref_Ebay(answer)
        try:
            driverStarter.effectiveGet(driver, nextPageHref)
            if driver.current_url != nextPageHref:
                # Error in server detected. Refresh and try again
                driver.refresh()
                driverStarter.effectiveGet(driver, nextPageHref)
                if driver.current_url != nextPageHref:
                    answer = False
            else:
                answer = True
        except:
            answer = False
