import SQLHandler, Constances, time
from Initialization import driverStarter
from StoreUploading import availableProduct
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# Uploading all the products from Constances.STORE_PRODUCTS_TABLE
# Uploading only products with status 'WAITING_FOR_UPLOADING'
def uploadProducts():
    # Initialize
    storeProducts = SQLHandler.readAllTable(Constances.STORE_PRODUCTS_TABLE)
    # Open store at the specific location
    try:
        # Open the stores (Amazon and Ebay)
        # Just for this version - Manually!
        print("Open Ebay store... (Please update 'UserOrders.txt' after finish!)")
        ebayDriver = driverStarter.startDriver()
        driverStarter.effectiveGet(ebayDriver, Constances.EBAY_SITE)
        # Just for this version - The program knows the store are opened only when there is an update on DataBase
        answer = SQLHandler.isStoresOpen()
        while answer == False: answer = SQLHandler.isStoresOpen()
        # Update DataBase
        SQLHandler.updateUserOrderTable()
        print("The phase of opening store has ended")
    except Exception as e: print("The code stopped because: " + e)
    # Run over the data and uploading to Ebay store
    searchBarElement_Ebay = None
    continueElement_Ebay = None
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    for storeProduct in storeProducts:
        if storeProduct.status == Constances.STATUS_NOT_UPLOAD:
            if storeProduct.store_location == 'Ebay': # Ebay cases
                # Gets the full data of the store product from gap products table
                gapProduct = SQLHandler.getStoreProductDetails(storeProduct)
                names = availableProduct.splitName(gapProduct.names)
                imgs = gapProduct.imgs.replace("[", "").replace("]", "").replace("'", "").split(", ")
                prices = gapProduct.prices.replace("[", "").replace("]", "").replace("'", "").split(", ")
                # In ebayDriver - search for the search bar element and searching for the name of the product
                if searchBarElement_Ebay == None:
                    iframe = ebayDriver.find_element_by_xpath(Constances.EBAY_SELLING_PRODCUT_SEARCH_BAY_IFRAME)
                    ebayDriver.switch_to.frame(iframe) # Switch to iframe
                    searchBarElement_Ebay = WebDriverWait(ebayDriver, 10, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.ID, Constances.EBAY_SELLING_PRODUCT_SEARCH_BAR_KEY)))   
                searchBarElement_Ebay.send_keys(names[1] + "\n") # Ebay
                # Continue to the 'Create a list' page
                if continueElement_Ebay == None:
                    continueElement_Ebay = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_PRODUCT_CONTINUE)))
                continueElement_Ebay.click()
                # Fills in the fields
                ebayDriver.switch_to.default_content() # Get out from the iframe
                #   UPC
                upcElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_UPC)))
                upcElement.click()
                #   Condition
                WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_UPC_OPTION_2))).click()
                conditionElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_CONDITION)))
                conditionElement.send_keys("New")
                #   Photos
                iframe = ebayDriver.find_element_by_id(Constances.EBAY_SELLING_CREATE_A_LIST_PHOTOS_IFRAME)
                ebayDriver.switch_to.frame(iframe) # Switch to iframe
                importFromWebElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_IMPORT_IMAGE_FROM_WEB)))
                importFromWebElement.click()
                enterImageURLElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_ENTER_IMAGE_URL)))
                enterImageURLElement.send_keys(imgs[0]) # Using Amazon's product's image
                importImageButtonElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_IMPORT_IMAGE_BUTTON)))
                importImageButtonElement.click()
                ebayDriver.switch_to.default_content() # Get out from the iframe
                #   Brand
                brandElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_BRAND)))
                brandElement.send_keys("Unbranded")
                #   MPN
                MPNElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_MPN)))
                MPNElement.send_keys("Does Not Apply")
                #   Item description
                iframe = ebayDriver.find_element_by_id(Constances.EBAY_SELLING_CREATE_A_LIST_ITEM_DESCRIPTION_IFRAME)
                ebayDriver.switch_to.frame(iframe) # Switch to iframe
                itemDescriptionElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_ITEM_DESCRIPTION_TEXT)))
                itemDescriptionElement.send_keys(names[1]) # Just for this version - The name is the item description
                ebayDriver.switch_to.default_content() # Get out from the iframe
                #   Selling details
                sellingDetailsElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_SELLING_DETAILS)))
                sellingDetailsElement.click()
                sellingDetailsElement.send_keys(Keys.DOWN)
                sellingDetailsElement.send_keys(9) # Tab
                sellingDetailsElement.click()
                time.sleep(5) # Saves and updates information
                priceElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_SELLING_DETAILS_PRICE)))
                pricesRatio = float(prices[0]) / float(prices[1]) # The maximum profit price
                # Just for this version - 10% off from ebay price
                # For example - Amazon price (10$); Ebay price (15$)
                #               Maximum profit price is 5$ (pricesRatio = 0.666...)
                #               The price on our store (pricesRatio * 1.1 * EbayPrice = 11$)
                #               Our profit price is 4$
                priceElement.send_keys(str(pricesRatio * 1.1 * float(prices[1])))
                payPalChooseElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                            .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_SELLING_PAYPAL)))
                payPalChooseElement.click()
                receivingPaymentEmailTextElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                                    .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_SELLING_RECEIVING_PAYMENT_EMAIL)))
                receivingPaymentEmailTextElement.send_keys(Constances.AD_GINO_TEAM_EMAIL)
                
                #   Lists the item
                listItemElement = WebDriverWait(ebayDriver, 20, ignored_exceptions=ignored_exceptions)\
                                                    .until(EC.presence_of_element_located((By.XPATH, Constances.EBAY_SELLING_CREATE_A_LIST_LIST_ITEM)))
                listItemElement.click()
    print("Finish") # Just for test
