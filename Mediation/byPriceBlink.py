import SQLHandler, Constances, time, sys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from Initialization import driverStarter
from Entities import GapProduct
from Initialization import initialize_Tools

# Global variables
driver = None

# Checking if the text is a float number
# True is so; Otherwise - False
def isNumber(text):
    for char in text:
        if (char < '0' or char > '9') and ord(char) != Constances.DOT_ASCII: return False
    return True

# Gets the price and the shipping price from the text (priceText)
# The price must be in the text. If not - return price = None
# The shipping price may be unknown
def getPriceFromText(priceText):
    returnPrice = ""
    shipping = ""
    priceText = priceText.replace('\n', ' ')
    priceText = priceText.replace('$', ' ')
    priceText = priceText.split()
    # The original price can be on the first index or the second index
    answer = isNumber(priceText[0])
    if answer == True: returnPrice = priceText[0]
    else:
        answer = isNumber(priceText[1])
        if answer == True: returnPrice = priceText[1]
        else: return None, None
    # Looking for the shipping price
    if 'plus' in priceText and 'shipping' in priceText: shipping = None
    else:
        index = 0
        for text in priceText:
            if text == '+': shipping = priceText[index + 1]
            index = index + 1
    return returnPrice, shipping

# Checking if personal site (Or wrong site by PriceBlink)
def checkIfPersonalSite(href):
    global driver
    # Initializes
    isPersonalProductSite = False
    answer = driverStarter.effectiveGet(driver, href)
    if answer:
        # Gets the name by read the HTML source
        content = driver.page_source
        # Encode & Decode the source data and decode again for string type only
        readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
        for char in readable_content:
            if char.isalpha() or ord(char) == Constances.SPACE_ASCII: word = word + char
            else: word = ""
            if word.lower() == Constances.KEY_SORT_PERSONAL_PRODUCT_SITE: isPersonalProductSite = True # The URL address is a personal product site
        return isPersonalProductSite
    else: return isPersonalProductSite

# Finding gaps by checking PriceBlink
# Check for all the sites (Amazon, Ebay)
def findGaps():
    global driver
    # Gets data from data base
    AmazonData = SQLHandler.readAllTable(Constances.AMAZON_PRODUCTS_TABLE)
    EbayData = SQLHandler.readAllTable(Constances.EBAY_PRODUCTS_TABLE)
    # Creates a driver
    driver = driverStarter.startDriver()
    # Install PriceBlink
    initialize_Tools.initChrome_PriceBlink(driver)
    # Checking Amazon
    for amazonProduct in AmazonData:
        answer = driverStarter.effectiveGet(driver, amazonProduct.href)
        if answer:
            try:
                start = time.time() # Start counting the time for all the gap products reference to amazonProduct
                # Switch and wait for PriceBlink iframe
                wait(driver, Constances.PRICE_BLINK_TIME_TO_WAIT_FOR_TOOLBAR_TO_LOAD).until(EC.frame_to_be_available_and_switch_to_it(Constances.PRICE_BLINK_IFRAME_ID))
                # Looking for the compare price button
                for element in driver.find_elements_by_id("comparePricesBtn"): comparePriceElement = element
                comparePriceElement.click() # Open the list
                listOfProducts = comparePriceElement.find_element_by_class_name(Constances.PRICE_BLINK_LIST_CLASS_NAME) # Looking for the list by class name
                # Gets all the product from the list
                priceBlinkProducts = []
                for product in listOfProducts.find_elements_by_class_name(Constances.PRICE_BLINK_PRODUCT_CLASS_NAME): priceBlinkProducts.append(product)
                # Creates the gap product list
                # Gets the price and the href attributes that write in the text for each product
                gapProductList_BeforeTime = []
                for product in priceBlinkProducts:
                    try:
                        time.sleep(Constances.PRICE_BLINK_TIME_TO_WAIT_FOR_PRICES_TO_LOAD)
                        # Get the price and the shipping
                        priceText = product.text
                        price, shipping = getPriceFromText(priceText) # Get the price
                        if shipping == 'FREE': shipping = '0.0'
                        # Determing direction of dropshipping
                        if (shipping != None and (float(price) + float(shipping) < float(amazonProduct.price)) 
                            or (shipping == None and float(price) < float(amazonProduct.price))): direction = 'Amazon_Dropshipping_Direction'
                        else: direction = 'Ebay_Dropshipping_Direction'
                        # Try to get the href of the product
                        try:
                            href = None
                            for element in product.find_elements_by_xpath(".//*"):
                                try:
                                    # Should be only one href attribute in the product
                                    href = element.get_attribute('href')
                                    break
                                except: None
                            if href != None: # Found href
                                isPersonalSite = checkIfPersonalSite(amazonProduct.href) # Checking if the site is for personal product
                                if isPersonalSite: # PriceBlink finds a gap!
                                    # Gets the product name
                                    ebayProductName = ""
                                    # Gets the product image
                                    ebayProductImage = ""
                                    # Category is the same as Amazon
                                    # Simialrity is not calculated (None for both names and images similarity)
                                    gapProductList_BeforeTime.append([str([amazonProduct.name, ebayProductName]), str([amazonProduct.href, href]),
                                                                    str([amazonProduct.img, ebayProductImage]), str([amazonProduct.price, price]), direction,
                                                                    amazonProduct.category, "None", "None"])
                        except: None
                    except: None
                end = time.time() # Stop counting the time
                searchingTimeAllProducts = end - start
                searchingTimeEachProduct = searchingTimeAllProducts / len(gapProductList_BeforeTime)
                for gapProduct_BeforeTime in gapProductList_BeforeTime:
                    gapProduct = GapProduct.Product(gapProduct_BeforeTime[0], gapProduct_BeforeTime[1], gapProduct_BeforeTime[2],
                                                    gapProduct_BeforeTime[3], gapProduct_BeforeTime[4], gapProduct_BeforeTime[5],
                                                    searchingTimeEachProduct, gapProduct_BeforeTime[6], gapProduct_BeforeTime[7])
                    SQLHandler.addProduct(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE, gapProduct)
                # Switch back
                driver.switch_to.default_content()
            except: None
    # Checking Ebay
    for ebayProduct in EbayData:
        answer = driverStarter.effectiveGet(driver, ebayProduct.href)
