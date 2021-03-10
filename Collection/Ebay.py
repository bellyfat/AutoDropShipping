import sys, time, Constances, SQLHandler
from Initialization import driverStarter
from Entities import Ebay
from selenium import webdriver
from Navigation import Tools

# Gets all the products from Constances.ebay_categories
def getTheProducts_multiURLs():
    print("Collecting from Ebay...")
    HTML_content_by_Categories = Constances.ebay_categories
    categories_index = 0
    # Get a WebDriver
    driver = driverStarter.startDriver()
    for url in HTML_content_by_Categories:
        # Name of category
        category_name = Constances.ebay_categories_names[categories_index]
        answer = driverStarter.effectiveGet(driver, url)
        numberOfPageCounter = 1
        while answer == True:
            content = driver.page_source
            # Encode & Decode the source data and decode again for string type only
            readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
            # Split and Seek products
            url_products = getTheProducts_singleURL(readable_content, category_name)
            for product in url_products:
                # Adds the new products to the DataBase
                SQLHandler.addProduct(Constances.EBAY_PRODUCTS_TABLE, product)
            answer = Tools.nextPage(driver)
            numberOfPageCounter = numberOfPageCounter + 1
            if numberOfPageCounter > Constances.LIMIT_NUMBER_OF_PAGE_TO_SEARCH:
                answer = False
        categories_index = categories_index + 1
    print("Finish Collecting from Ebay.")
    driver.close()

# Checking the name if is inside href
def checkName(name, href):
    # Check the name and the href
    nameInHref = name.replace(" ", "-")
    for char in nameInHref:
        if char.isalpha() == False and char != "-" and (char < '0' or char > '9'):
            nameInHref = nameInHref.replace(char, "")
    nameInHrefSplited = nameInHref.split("-")
    nameInHrefSplitedSize = len(nameInHrefSplited)
    numberOfMatches = 0
    for string in nameInHrefSplited:
        if string in href:
            numberOfMatches = numberOfMatches + 1
    if (numberOfMatches / nameInHrefSplitedSize) > Constances.MINIMUM_RATION_NAME_IN_HREF:
        return True
    return False

# Handle the href case
# Returning the href and a boolean answer
# If the boolean answer is false - hrefCase finish.
# If the href value is None - No href was found. (Also the answer will be False)
def hrefCase(href, char, counter34, spareChars):
    if counter34 == 0 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
    # Start building the url for the href attribute
        counter34 = 1
        return href, True, counter34, spareChars
    if counter34 == 0 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        spareChars = spareChars + 1
        if spareChars >= Constances.SPARE_CHARS_LIMIT:
        # False case
            return None, False, counter34, spareChars
        return href, True, counter34, spareChars
    if counter34 == 1 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE and ord(char) != Constances.SPACE_ASCII:
        href = href + char
        return href, True, counter34, spareChars
    if counter34 == 1 and ord(char) == Constances.SPACE_ASCII:
    # False case
        return None, False, counter34, spareChars
    # Finish building the url for href attribute
    if counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
        if Constances.HREF_PREFIX in href:
            return href, False, counter34, spareChars
        # False case
        return None, False, counter34, spareChars

# Handle the name case
# Returning the name and a boolean answer
# If the boolean answer is false - nameCase finish.
# If the name value is None - No name was found. (Also the answer will be False)
# The name must be in the href
def nameCase(name, char, href, counter34, spareChars):
    if counter34 == 0 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
    # Start building the url for the name attribute
        counter34 = 1
        return name, True, counter34, spareChars
    if counter34 == 0 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        spareChars = spareChars + 1
        if spareChars >= Constances.SPARE_CHARS_LIMIT:
        # False case
            return None, False, counter34, spareChars
        return name, True, counter34, spareChars
    if counter34 == 1 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        name = name + char
        return name, True, counter34, spareChars
    # Finish building the url for name attribute
    if counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
        # Check the name and the href
        answer = checkName(name, href)
        if answer == True:
            return name, False, counter34, spareChars
        # False case
        return None, False, counter34, spareChars

# Handle the img case
# Returning the img and a boolean answers.
# If the boolean answer is false - imgCase finish.
# If the img value is None - No img was found. (Also the answer will be False)  
def imgCase(img, char, counter34, spareChars):
    if counter34 == 0 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
    # Start building the url for the img attribute
        counter34 = 1
        return img, True, counter34, spareChars
    if counter34 == 0 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        spareChars = spareChars + 1
        if spareChars >= Constances.SPARE_CHARS_LIMIT:
        # False case
            return None, False, counter34, spareChars
        return img, True, counter34, spareChars
    if counter34 == 1 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE and ord(char) != Constances.SPACE_ASCII:
        img = img + char
        return img, True, counter34, spareChars
    if counter34 == 1 and ord(char) == Constances.SPACE_ASCII:
    # False case
        return None, False, counter34, spareChars
    # Finish building the url for img attribute
    if counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
        for imageType in Constances.IMAGE_TYPES:
            if imageType in img:
                # Checking if webp type
                return img, False, counter34, spareChars
        # False case
        return None, False, counter34, spareChars

# Handle the price case
# Returning the price and a boolean answers.
# If the boolean answer is false - priceCase finish.
# If the price value is None - No price was found. (Also the answer will be False)  
def priceCase(price, char, priceFlag):
    # Building the price
    if (char >= '0' and char <= '9') or char == '.':
        price = price + char
        return price, True
    else:
        if price == "" or price == ".":
            # False case
            return None, False
        else:
            # Finish.
            return price, False

# getTheProducts_singleURL(String: HTML_content, String: category_name)
# input => string, string
# output => Product[]
# Gets HTML content and return Product[]
# Gets the attributes:
#   HREF    -   by 'href="www..."'
#   NAME    -   by 'alt="NAME_OF_PRODUCT' - MUST be after href!
#   IMG     -   by 'src="...webp" - MUST be webp type! - MUST be after name!
#   PRICE   -   by '$PRICE_NUMBER' - MUST be after IMG! Search untill Constances.END_OF_PRODUCT found.
def getTheProducts_singleURL(HTML_content, category_name):
    # Start counting the time that takes for the process to collect all the url's products
    start = time.time()
    # The return Products
    products = []
    # Temp products
    productsBeforeTimeSearching = []
    # The attributes that building the Product class
    href = ""
    name = ""
    img = ""
    price = ""
    # A word in HTML_content
    word = ""
    # Counting the quotation marks appearnes
    counter34 = 0
    # Counting the number of chars between the attribute to the quotation marks
    spareChars = 0
    # Saving the attribute in a false case
    savingAttribute = ""
    hrefSaving = ""
    # Flags for each attribute
    hrefFlag = False
    imgFlag = False
    priceFlag = False
    nameFlag = False
    # Extra flag
    endOfProductFlag = False
    # Collecting products from the HTML_content
    for char in HTML_content:
        # 'href' case
        if hrefFlag:
            href, answer, counter34, spareChars = hrefCase(href, char, counter34, spareChars)
            if (href == None or href == '') and answer == False:
                # Not found
                href = savingAttribute
                hrefFlag = False
            if (href != None and href != '') and answer == False:
                # Found href
                hrefFlag = False
                # Checking the name and the href
                if name != "":
                    answer = checkName(name, href)
                    if answer == False and name != "" and img != "" and price != "":
                        # End of product
                        endOfProductFlag = True
                        hrefSaving = savingAttribute
                    elif answer == False:
                        # False case
                        href = savingAttribute
        # 'name' case
        if nameFlag:
            name, answer, counter34, spareChars = nameCase(name, char, href, counter34, spareChars)
            if (name == None or name == '') and answer == False:
                # Not found
                name = savingAttribute
                if savingAttribute == "":
                    # Name MUST be after href
                    href = ""
                nameFlag = False
            if (name != None and name != '') and answer == False:
                # Found name
                nameFlag = False
        # 'img' case
        if imgFlag:
            img, answer, counter34, spareChars = imgCase(img, char, counter34, spareChars)
            if (img == None or img == '') and answer == False:
                # Not found
                img = savingAttribute
                imgFlag = False
            if (img != None and img != '') and answer == False:
                # Found img
                imgFlag = False
        # 'price' case
        if priceFlag:
            price, answer = priceCase(price, char, priceFlag)
            if (price == None or price == '') and answer == False:
                # Not found
                price = savingAttribute
                priceFlag  = False
            if (price != None and price != '') and answer == False:
                # Found price
                priceFlag = False
        # In general - building the word in HTML_content
        if ((char.isalpha() or ord(char) == Constances.DOLLAR_ASCII)and hrefFlag == False and imgFlag == False and priceFlag == False and nameFlag == False):
            word = word + char
        # Checking if the word equals to one of the attributes
        if (char.isalpha() == False and hrefFlag == False and imgFlag == False and priceFlag == False):
            if word == 'href':
                hrefFlag = True
                savingAttribute = href
                href = ""
                counter34 = spareChars = 0
            if word == 'alt':
                if href != "" and name == "":
                    nameFlag = True
                    savingAttribute = name
                    name = ""
                    counter34 = spareChars = 0
            if word == 'src' and img == "":
                if href != "":
                    imgFlag = True
                    savingAttribute = img
                    img = ""
                    counter34 = 0
            if word == '$':
                if img != "" and price == "":
                    priceFlag = True
                    savingAttribute = price
                    price = ""
            word = ""
        # In case that all the attributes were built - Create an instance of Product and start again
        if (href != "" and img != "" and price != "" and name != "" and hrefFlag == False and imgFlag == False
                                                            and priceFlag == False and nameFlag == False and endOfProductFlag):
            addFlag = True
            # Sorting by price
            if float(price) < Constances.MIN_PRICE or float(price) > Constances.MAX_PRICE: addFlag = False
            if addFlag: productsBeforeTimeSearching.append([hrefSaving, name, img, price, category_name])
            # Initialize all the attributes and flags
            spareChars = counter34 = 0
            hrefSaving = savingAttribute = word = href = img = price = name = ""
            endOfProductFlag = hrefFlag = imgFlag = priceFlag = nameFlag = False
    # Calculate time
    end = time.time()
    searchingTimeForAllProducts = end - start
    # Finish the process for the given URL
    if len(productsBeforeTimeSearching) != 0:
        searchingTimePerProducts = searchingTimeForAllProducts / len(productsBeforeTimeSearching)
        for tempProduct in productsBeforeTimeSearching:
            products.append(Ebay.Product(tempProduct[0], tempProduct[1], tempProduct[2], tempProduct[3], 
                                                            tempProduct[4], searchingTimePerProducts))
    return products
