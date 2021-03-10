# This module include image detecting!
import SQLHandler, Constances, sys
from Entities import Amazon, Ebay, GapProduct, StoreProduct
from Initialization import driverStarter
from urllib.parse import urlparse
from selenium import webdriver
from ImageSimilartion import ImageSimilartion, ImageTools

# Deletes the gap product and the problematic product from data base
def deleteGap(gapProduct, productType):
    print("Delete!") # Test!
    hrefs = gapProduct.hrefs.replace("[", "").replace("]", "").replace("'", "").split(",")
    # Delete Amazon product
    if productType == "Amazon":
        # Obtains the ASIN from the href
        urlAfterParsing = urlparse(hrefs[0])
        path = urlAfterParsing[2]
        pathList = path.split("/")
        for partPath in pathList:
            if len(partPath) == Constances.AMAZON_ASIN_SIZE:
                isAsin = True
                for char in partPath:
                    if char.isalpha == False and (char < '0' or char > '9'): isAsin = False
                if isAsin: asin = partPath
        tempProduct = Amazon.Product(asin, "", "", "", "", "", "", "", "")
        SQLHandler.deleteProduct(Constances.AMAZON_PRODUCTS_TABLE, tempProduct)
    # Delete Ebay product
    if productType == "Ebay":
        tempProduct = Ebay.Product(hrefs[1], "", "", "", "", "")
        SQLHandler.deleteProduct(Constances.EBAY_PRODUCTS_TABLE, tempProduct)
    # Delete the gap
    SQLHandler.deleteProduct(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE, gapProduct)

# Checks and returns the shipping price
def checkShippingEbay(driver):
    shipping = ""
    readShippingFlag = False
    # Gets the name by read the HTML source
    content = driver.page_source
    # Encode & Decode the source data and decode again for string type only
    readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
    for char in readable_content:
        if readShippingFlag:
            if (char.isalpha() or ord(char) == Constances.SPACE_ASCII or ord(char) == Constances.DOLLAR_ASCII or
                (char >= '0' and char <= '9') or ord(char) == Constances.DOT_ASCII): shipping = shipping + char
            else:
                if shipping != "": return shipping # Finish
        if readShippingFlag == False and (char.isalpha() or ord(char) == Constances.SPACE_ASCII or
            ord(char) == Constances.HYPHEN_ASCII): word = word + char
        else: word = ""
        if word.lower() == Constances.EBAY_SHIPPING_KEY: readShippingFlag = True

# Checking if personal site (Or wrong site by PriceBlink)
# Just for this version - Only free shipping - Only in USA
def checkIfPersonalSite_Ebay(driver):
    # Initializes
    isPersonalProductSite = False
    # Gets the name by read the HTML source
    content = driver.page_source
    # Encode & Decode the source data and decode again for string type only
    readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
    for char in readable_content:
        if char.isalpha() or ord(char) == Constances.SPACE_ASCII: word = word + char
        else: word = ""
        if word.lower() == Constances.KEY_SORT_PERSONAL_PRODUCT_SITE: isPersonalProductSite = True # The URL address is a personal product site
    return isPersonalProductSite

# Checks and returns the shipping price
# Just for this version - Only free shipping - Only in USA
def checkShippingAmazon(driver):
    return 'Free Shipping'

# Checking if the Amazon site is correct
# If 'asin="..."' is inside the html source - Return true
# Otherwise - Return false
def checkIfPersonalSite_Amazon(driver):
    # Gets the name by read the HTML source
    content = driver.page_source
    # Encode & Decode the source data and decode again for string type only
    readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
    for char in readable_content:
        if char.isalpha() or ord(char) == Constances.EQUAL_ASCII: word = word + char
        else: word = ""
        if word.lower() == 'asin=': return True
    return False

# Gets the real href of the product
# Search the name in Amazon search bar
def getTheCorrectSite_Amazon(driver, amazonProductName, amazonProductImage):
    searchBarElement = driver.find_element_by_xpath(Constances.AMAZON_SEARCH_BAR_KEY)
    searchBarElement.send_keys(amazonProductName)
    searchBarElement.submit()
    # Search for the image in the screen
    imageTempName = "AmazonTempImage"
    ImageSimilartion.URL_to_PNG(amazonProductImage, imageTempName)
    ImageTools.findImageOnScreen(imageTempName)
    ImageSimilartion.deleteImage(imageTempName)
    return driver.current_url

# Split the names
def splitName(names):
    for char in names:
        if char.isalpha() == False and ord(char) != Constances.SPACE_ASCII and (char < '0' or char > '9') and char != ',' and char != "'":
            names = names.replace(char, "")
    return names.split(", '")

# Checks if the gap products available before uploads to the store
# Only for this version - Free shipping + Only USA!
def checkGapProducts():
    # Initialize
    driver = driverStarter.startDriver()
    # Get the gap products from data base
    GapData_AmazonEbay = SQLHandler.readAllTable(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE)
    for gapProduct in GapData_AmazonEbay:
        try:
            # Convert the hrefs from string type
            hrefs = gapProduct.hrefs.replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(",")
            names = splitName(gapProduct.names)
            names[0] = names[0].replace("'", "") # Amazon product name
            names[1] = names[1].replace("'", "") # Ebay product name
            imgs = gapProduct.imgs.replace("[", "").replace("]", "").replace("'", "").split(",")
            # Check if the gap product is already in Constances.STORE_PRODUCTS_TABLE
            isInStore = SQLHandler.isProduct(Constances.STORE_PRODUCTS_TABLE, [hrefs[0], hrefs[1]])
            if isInStore == False:
                if gapProduct.direction == 'Amazon_Dropshipping_Direction':
                    # The store should be open on Amazon while the product is being shipped from eBay
                    # Starts with the first href - Amazon site - Checking if the site is correct
                    isHrefAmazonCorrect = driverStarter.effectiveGet(driver, hrefs[0]) # Checking if the href is correct
                    if isHrefAmazonCorrect:
                        isCorrect_Amazon = checkIfPersonalSite_Amazon(driver) # Checking if product personal site
                        if isCorrect_Amazon == False: hrefs[0] = getTheCorrectSite_Amazon(driver, names[0], imgs[0])
                        isHrefEbayCorrect = driverStarter.effectiveGet(driver, hrefs[1]) # Ebay
                        if isHrefEbayCorrect:
                            # First - Checking if personal product site
                            isPersonal = checkIfPersonalSite_Ebay(driver)
                            if isPersonal:
                                ''' Just for this version - Only free shipping - Only USA!
                                # Checking the shipping details and options
                                shipping = checkShippingEbay(driver) # A browser must be open before with the appropriate site
                                # Just for this version - Only free shipping
                                if shipping == 'Free Shipping':
                                '''
                                # Safe to upload! - Add to data base
                                storeProduct = StoreProduct.Product(hrefs[0], hrefs[1], "Amazon", Constances.STATUS_NOT_UPLOAD)
                                SQLHandler.addProduct(Constances.STORE_PRODUCTS_TABLE, storeProduct)
                        else: deleteGap(gapProduct, "Ebay")
                    else: deleteGap(gapProduct, "Amazon")
                if gapProduct.direction == 'Ebay_Dropshipping_Direction':
                    # The store should be open on Ebay while the product is being shipped from Amazon
                    # Due to the structure of Ebay - there is no need to check if the site exists or is working properly
                    ''' Just for this version - Only free shipping - Only USA!
                    # Checking the shipping details and options in Amazon site
                    shipping = checkShippingAmazon(driver) # A browser must be open before with the appropriate site
                    # Just for this version - Only free shipping
                    # Selling only in USA
                    if shipping == 'Free Shipping':
                    '''
                    # Safe to upload! - Add to data base
                    storeProduct = StoreProduct.Product(hrefs[0], hrefs[1], "Ebay", Constances.STATUS_NOT_UPLOAD)
                    SQLHandler.addProduct(Constances.STORE_PRODUCTS_TABLE, storeProduct)
        except: None
