# Navigation tools
import Constances, time, sys, os
from pyrobogui import robo
from Initialization import driverStarter
from selenium import webdriver
from urllib.parse import urlparse

# Disable output
def blockPrint():
    sys.__stdout__ = sys.stdout
    sys.stdout = open(os.devnull, 'w')

# Restore output
def enablePrint():
    sys.stdout = sys.__stdout__

# Trying to increase the page number in the current url
# Returns the next page href
# Return None if failed
def tryIncreasePageNumber_Ebay(currentPage):
    pFlag = False
    gFlag = False
    nFlag = False
    currentPageNumber = ""
    index = 0
    startNumberIndex = 0
    for char in currentPage:
        if nFlag:
            if ord(char) != Constances.EQUAL_ASCII:
                if (char < '0' or char > '9'):
                    # Stop building the number
                    if currentPageNumber == "":
                        pFlag = gFlag = nFlag = False
                    else:
                        break
                else:
                    if currentPageNumber == "":
                        startNumberIndex = index
                    currentPageNumber = currentPageNumber + char
        # 'n' letter case
        if gFlag and nFlag == False:
            if char == 'n':
                if pFlag and gFlag:
                    nFlag = True
            else:
                pFlag = gFlag = False
        # 'g' letter case
        if pFlag and gFlag == False and nFlag == False:
            if char == 'g':
                if pFlag:
                    gFlag = True
            else:
                pFlag = False
        # 'p' letter case
        if char == 'p' and pFlag == False and gFlag == False and nFlag == False:
            pFlag = True
        index = index + 1
    if currentPageNumber == "":
        return None
    else:
        nextPageNumber = str(int(currentPageNumber) + 1)
        newHref = currentPage[0:startNumberIndex]
        newHref = newHref + nextPageNumber
        return newHref

# Fix and clean the href
# Add 'rt=nc&' after a quetion mark
# Remove 'amp;rt=nc&amp;'
# After removing - turn every semi-colon to ampersand (';' -> '&')
def fixHref_Ebay(answer):
    oldHref = answer
    newHref = ""
    addFlag = False
    addedFlag = False
    index = 0
    # Remove 'amp;rt=nc&amp;'
    oldHref = oldHref.replace("amp;rt=nc&amp;", "")
    for char in oldHref:
        if addFlag:
            # Add 'rt=nc&' after a quetion mark
            newHref = oldHref[0:index]
            newHref = newHref + 'rt=nc&'
            addFlag = False
            addedFlag = True
        if ord(char) == Constances.QUESTING_MARK_ASCII and addedFlag == False:
            addFlag = True
        index = index + 1
        if ord(char) == Constances.SEMI_COLON_ASCII and addedFlag:
            newHref = newHref + '&'
        elif addedFlag:
            newHref = newHref + char
    return newHref

# Trying to increase the page number in the current url
# Returns the next page href
# Return None if failed
# Increas 'page=NUMBER_OF_CURRENT_PAGE', NOT pg_NUMBER!
# Note that the first page of the category does'nt woriking like that
def tryIncreasePageNumber_Amazon(currentPage):
    pageFlag = False
    word = ""
    currentPageNumber = ""
    index = 0
    startNumberIndex = 0
    for char in currentPage:
        if pageFlag:
            if currentPageNumber == "":
                startNumberIndex = index
            if (char < '0' or char > '9'):
                # Stop building the number
                break
            currentPageNumber = currentPageNumber + char
        if char.isalpha() or ord(char) == Constances.EQUAL_ASCII:
            word = word + char
        if char.isalpha() == False and ord(char) != Constances.EQUAL_ASCII:
            word = ""
        if word == 'page=':
            pageFlag = True
        index = index + 1
    if currentPageNumber == "":
        return None
    else:
        nextPageNumber = str(int(currentPageNumber) + 1)
        newHref = currentPage[0:startNumberIndex]
        newHref = newHref + nextPageNumber
        return newHref 

# Moves to the next page
# Return True for success
# Otherwise - False
def nextPage(driver):
    # Get the current url
    currentPage = driver.current_url
    # Determents if is Amazon page or Ebat page
    urllist = urlparse(currentPage)
    website = urllist[1].replace('.com','').lower()
    if 'amazon' in website:
        # Amazon page
        # First - Try to increase the number in the href
        newHref = tryIncreasePageNumber_Amazon(currentPage)
        try:    
            driverStarter.effectiveGet(driver, newHref)
            if currentPage != driver.current_url:
                return True
            else:
                return False
        except:
            # Second - Scroll down and click on 'next page' button
            driver.execute_script("window.scrollTo(0, 0)")
            heightToScroll = 0
            tryCounting = 0
            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
            except:
                last_height = Constances.DEFAULT_HEIGHT
            while heightToScroll <= Constances.MAX_HEIGHT:
                current_url = driver.current_url
                driver.execute_script("window.scrollTo(0, " + str(int((last_height * 2) / 5) + heightToScroll) + ")")
                try:
                    blockPrint()
                    robo.click(Constances.IMAGE_PATH_AMAZON_NEXTPAGE, timeout=Constances.SCROLL_TIME_LIMIT)
                    enablePrint()
                except:
                    try:
                        blockPrint()
                        robo.click(Constances.IMAGE_PATH_AMAZON_NEXTPAGE_2, timeout=Constances.SCROLL_TIME_LIMIT)
                        enablePrint()
                    except:
                        tryCounting = tryCounting + 1
                if int((last_height * 1) / 2) + heightToScroll >= int(last_height):
                    return False
                if tryCounting > Constances.MAX_NUMBER_OF_TRYING:
                    return False
                if current_url == driver.current_url:
                    heightToScroll = heightToScroll + Constances.SCROLL_INCREASE
                else:
                    return True
            return False
    if 'ebay' in website:
        # Ebay page
        answer = tryIncreasePageNumber_Ebay(currentPage)
        nextPageHref = fixHref_Ebay(answer)
        try:
            driverStarter.effectiveGet(driver, nextPageHref)
            if driver.current_url != nextPageHref:
                # Error in server detected. Refresh and try again
                driver.refresh()
                driverStarter.effectiveGet(driver, nextPageHref)
                if driver.current_url != nextPageHref:
                    return False
            return True
        except:
            return False
