# This module include image detecting!
import sys, time, Constances, SQLHandler
from Initialization import driverStarter
from Entities import Amazon
from selenium import webdriver
from Navigation import Tools

# Gets all the products from Constances.amazon_categories
def getTheProducts_multiURLs():
    print("Collecting from Amazon...")
    categories_index = 0
    # Get a WebDriver
    driver = driverStarter.startDriver()
    for url in Constances.amazon_categories:
        # Name of category
        category_name = Constances.categories_name_amazon[categories_index]
        answer = True
        driverStarter.effectiveGet(driver, url)
        numberOfPageCounter = 1
        while answer == True:
            content = driver.page_source
            # Encode & Decode the source data and decode again for string type only
            readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
            # Split and Seek products
            url_products = getTheProducts_singleURL(readable_content, category_name)
            for product in url_products:
                # Adds the new products to the DataBase
                SQLHandler.addProduct(Constances.AMAZON_PRODUCTS_TABLE, product)
            answer = Tools.nextPage(driver)
            numberOfPageCounter = numberOfPageCounter + 1
            if numberOfPageCounter > Constances.LIMIT_NUMBER_OF_PAGE_TO_SEARCH:
                answer = False
        categories_index = categories_index + 1
    print("Finish Collecting from Amazon.")
    driver.close()

# cleanStarsAttribute(String: stars)
# input => string
# output => string
# Gets stars attribute and clean the unneccery chars
def cleanStarsAttribute(stars):
    returnStars = ""
    for char in stars:
        if char >= '0' and char <= '9' or char == '.':
                returnStars = returnStars + char
    return returnStars

# Handle the href case
# Returning the href and a boolean answer
# If the boolean answer is false - hrefCase finish.
# If the href value is None - No href was found. (Also the answer will be False)
# The asin must be in the final href
def hrefCase(href, char, asin, counter34, spareChars):
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
        if asin in href:
            href = Constances.AMAZON_HREF_PREFIX + href
            return href, False, counter34, spareChars
        # False case
        return None, False, counter34, spareChars

# Handle the name case
# Returning the name and a boolean answer
# If the boolean answer is false - nameCase2 finish.
# If the name value is None - No name was found. (Also the answer will be False)
def nameCase2(name, char, counter34, spareChars):
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
        return name, False, counter34, spareChars

# Handle the asin case
# Returning the asin and a boolean answer
# If the boolean answer is false - asinCase finish.
# If the asin value is None - No asin was found. (Also the answer will be False)  
def asinCase(asin, char, counter34, spareChars):
    if counter34 == 0 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
    # Start building the url for asin attribute
        counter34 = 1
        char = ""
        return asin, True, counter34, spareChars
    if counter34 == 0 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        spareChars = spareChars + 1
        if spareChars >= Constances.SPARE_CHARS_LIMIT:
        # False case
            return None, False, counter34, spareChars
        return asin, True, counter34, spareChars
    if counter34 == 1 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE  and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE and char != "":
        asin = asin + char
        # if asin bigger than ASIN_SIZE
        if len(asin) > Constances.ASIN_SIZE:
        # False case
            return None, False, counter34, spareChars
        return asin, True, counter34, spareChars
    if counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE and len(asin) == Constances.ASIN_SIZE:
    # Finish building the url for asin attribute
        return asin, False, counter34, spareChars
    if counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE  or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE and len(asin) < Constances.ASIN_SIZE:
    # False case
        return None, False, counter34, spareChars

# Handle the img case
# Returning the img, two boolean answers and a word.
# If the first boolean answer is false - imgCase finish.
# The second boolean answer represent if the word 'src' found.
# If the img value is None - No img was found. (Also the answer will be False)  
def imgCase(img, char, srcFlag, word, counter34, spareChars, numberOfCharsFromImgToSec):
    # check if the word is src
    if word == 'src':
        word = ""
        return img, True, True, word, counter34, spareChars, numberOfCharsFromImgToSec
    if srcFlag == False and counter34 == 0:
        if char.isalpha():
            word = word + char
        numberOfCharsFromImgToSec = numberOfCharsFromImgToSec + 1
        if len(word) > len('src'):
            word = ""
        if numberOfCharsFromImgToSec > Constances.MAX_NUMBER_OF_CHARS_FROM_IMG_TO_SRC:
        # False case
            return None, False, False, word, counter34, spareChars, numberOfCharsFromImgToSec
        return img, True, False, word, counter34, spareChars, numberOfCharsFromImgToSec
    # 'src' was found
    if srcFlag and counter34 == 0 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
    # Start building the url for img attribute
        counter34 = 1
        return img, True, True, word, counter34, spareChars, numberOfCharsFromImgToSec
    if srcFlag and counter34 == 0 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        spareChars = spareChars + 1
        if spareChars >= Constances.SPARE_CHARS_LIMIT:
        # False case
            return None, False, True, word, counter34, spareChars, numberOfCharsFromImgToSec
        return img, True, True, word, counter34, spareChars, numberOfCharsFromImgToSec
    if srcFlag and counter34 == 1 and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and ord(char) != Constances.QUOTATION_MARKS_ASCII_SINGLE:
        if ord(char) == Constances.SPACE_ASCII:
        # False case
            return None, False, True, word, counter34, spareChars, numberOfCharsFromImgToSec
        img = img + char
        return img, True, True, word, counter34, spareChars, numberOfCharsFromImgToSec
    if srcFlag and counter34 == 1 and ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE or ord(char) == Constances.QUOTATION_MARKS_ASCII_SINGLE:
        # Finish building the url for img attribute
        return img, False, False, word, counter34, spareChars, numberOfCharsFromImgToSec

# Handle the price case
# Returning the price and two boolean answers.
# If the first boolean answer is false - priceCase finish.
# The second boolean answer represent if the char '$' found.
def priceCase(price, char, priceFlag, numberAfterDolarFlag, spareChars):
    if char == '$':
    # Price must start with '$'
        numberAfterDolarFlag = True
        price = ""
        return price, True, True, spareChars
    else:
        # Building the price
        if numberAfterDolarFlag and (char >= '0' and char <= '9') or char == '.':
            price = price + char
            return price, True, True, spareChars
        elif numberAfterDolarFlag:
            if price == "" or price == ".":
                # False case
                return None, False, True, spareChars
            else:
                # Finish.
                return price, False, True, spareChars
        elif numberAfterDolarFlag == False:
            spareChars = spareChars + 1
            if spareChars >= Constances.PRICE_ZONE:
                return None, False, False, spareChars
            return price, True, False, spareChars

# Handle the stars case
# Returning the stars ,a boolean answer and an word.
# If the boolean answer is false - starsCase finish.
def starsCase(stars, char, word, starsFlag):
    # Building a sentence
    word = word + char
    # The sentence must include the string 'out of 5 stars' (STARS_SUFFIX)
    if Constances.STARS_SUFFIX in word:
        splited_words = word.split()
        index = 0
        # Gets the index of 'out' in the list
        for str in splited_words:
            if str == 'out':
                # For extra check
                if splited_words[index + 1] == 'of' and splited_words[index + 2] == '5' and splited_words[index + 3] == 'stars':
                    stars = splited_words[index - 1]
                    word = ""
                    starsFlag = False
                    splited_words = ""
                    stars = cleanStarsAttribute(stars)
                    # Finish.
                    return stars, False, word
            index = index + 1
        return None, False, word
    # False case
    elif len(word) > 200:
        return None, False, word
    return stars, True, word

# getTheProducts_singleURL(String: HTML_content, String: category_name)
# input => string, string
# output => Product[]
# Gets HTML content and return Product[]
# Gets the attributes:
#   ASIN   -   by 'asin="ASIN_NUMBER_IS_HERE"
#   HREF   -   by 'href="www..."'
#   IMG    -   by 'img src="...jpg"'
#   PRICE  -   by 'price ... $NUMBER'
#   STARS  -   by 'stars ... STARS_NUMBER out of 5 stars'
#   NAME   -   by Constances.NAME_KEY_FULL_1 or Constances.NAME_KEY_FULL_2
#   RATING -   by Constances.RATING_KEY
def getTheProducts_singleURL(HTML_content, category_name):
    # Start counting the time that takes for the process to collect all the url's products
    start = time.time()
    # The return Products
    products = []
    # Temporary product
    productsBeforeTimeSearching = []
    # The attributes that building the Product class
    asin = ""
    href = ""
    name = ""
    img = ""
    price = ""
    stars = ""
    rating = ""
    # A word in HTML_content
    word = ""
    # Counting the quotation marks appearnes
    counter34 = 0
    # Saving the attribute in a false case
    savingAttribute = ""
    # Counting the number of chars between the attribute to the quotation marks
    spareChars = 0
    # Counting the number of chars between 'img' appears to 'src'
    numberOfCharsFromImgToSec = 0
    # Saving the asin
    asinSaver = ""
    # Flags for each attribute
    hrefFlag = False
    asinFlag = False
    imgFlag = False
    priceFlag = False
    starsFlag = False
    ratingFlag = False
    nameFlag = False
    nameFlag_Second = False
    ratingFlag_Second = False
    # Extra flags
    buildRating = False
    numberAfterDolarFlag = False
    srcFlag = False
    isName = False
    isRating = False
    # Collecting products from the HTML_content
    for char in HTML_content:
        # 'asin' case
        if asinFlag:
            asin, answer, counter34, spareChars = asinCase(asin, char, counter34, spareChars)
            if (asin == None or asin == '') and answer == False:
                # Not found
                asin = savingAttribute
                asinFlag = False
            if (asin != None and asin != '') and answer == False:
                if href != "" and asin not in href:
                    href = ""
                if asinSaver != "" and asinSaver != asin:
                    # Diffrent asin detect - New prodcut information
                    # Initialize attributes (without asin)
                    numberOfCharsFromImgToSec = spareChars = counter34 = 0
                    asinSaver = savingAttribute = word = href = img = price = stars = name = rating = ""
                    buildRating = ratingFlag_Second = nameFlag_Second = isKey1 = isKey2 = isRating = isName = hrefFlag = imgFlag = priceFlag = starsFlag = ratingFlag = nameFlag = False
                # Found asin
                asinFlag = False
        # 'href' case
        if hrefFlag:
            href, answer, counter34, spareChars = hrefCase(href, char, asin, counter34, spareChars)
            if (href == None or href == '') and answer == False:
                # Not found
                href = savingAttribute
                hrefFlag = False
            if (href != None and href != '') and answer == False:
                # Found href
                hrefFlag = False
        # 'name' case 1
        if nameFlag:
            name = name + char
            if isName:
                # Building the name
                if Constances.NAME_STOP_BUILD_KEY in name:
                    # Finishing build the name
                    if isKey1:
                        name = name.replace(Constances.NAME_KEY_FULL_1, "").replace(Constances.NAME_STOP_BUILD_KEY, "")
                    if isKey2:
                        name = name.replace(Constances.NAME_KEY_FULL_2, "").replace(Constances.NAME_STOP_BUILD_KEY, "")
                    nameFlag = isName = isKey1 = isKey2 = False
                if len(name) > (len(Constances.NAME_KEY_FULL_1) + Constances.NAME_LIMIT):
                    # Not found
                    nameFlag = isName = False
                    name = savingAttribute
            else:
                if (name not in Constances.NAME_KEY_FULL_1 and name not in Constances.NAME_KEY_FULL_2 
                    or len(name) > len(Constances.NAME_KEY_FULL_1)):
                    # Not found
                    nameFlag = False
                    name = savingAttribute
                elif name == Constances.NAME_KEY_FULL_1:
                    isName = isKey1 = True
                elif name == Constances.NAME_KEY_FULL_2:
                    isName = isKey2 = True
        # 'name' case 2
        if nameFlag_Second:
            name, answer, counter34, spareChars = nameCase2(name, char, counter34, spareChars)
            if (name == None or name == '') and answer == False:
                # Not found
                name = savingAttribute
                nameFlag_Second = False
            if (name != None and name != '') and answer == False:
                # Found name
                nameFlag_Second = False
        # 'img' case
        if imgFlag:
            img, answer, srcFlag, word, counter34, spareChars, numberOfCharsFromImgToSec = imgCase(img, char, srcFlag, word, counter34, spareChars, numberOfCharsFromImgToSec)
            if (img == None or img == '') and answer == False:
                # Not found
                img = savingAttribute
                imgFlag = srcFlag = False
            if (img != None and img != '') and answer == False:
                # Found img
                imgFlag = srcFlag = False
        # 'price' case
        if priceFlag:
            price, answer, numberAfterDolarFlag, spareChars = priceCase(price, char, priceFlag, numberAfterDolarFlag, spareChars)
            if (price == None or price == '') and answer == False:
                # Not found
                price = savingAttribute
                priceFlag = numberAfterDolarFlag = False
            if (price != None and price != '') and answer == False:
                # Found price
                priceFlag = numberAfterDolarFlag = False
        # 'stars' case
        if starsFlag:
            stars, answer, word = starsCase(stars, char, word, starsFlag)
            if (stars == None or stars == '') and answer == False:
                # Not found
                stars = savingAttribute
                starsFlag = False
            if (stars != None and stars != '') and answer == False:
                # Found stars
                starsFlag = False
        # 'rating' case 1
        if ratingFlag and stars != "":
            rating = rating + char
            if isRating:
                if ((char < '0' or char > '9') and ord(char) != Constances.QUOTATION_MARKS_ASCII_DOUBLE and
                     ord(char) != Constances.DOT_ASCII and ord(char) != Constances.COMMA_ASCII):
                    # Must be a number - False case
                    ratingFlag = isRating = False
                    rating = savingAttribute
                elif ord(char) == Constances.QUOTATION_MARKS_ASCII_DOUBLE:
                    # Finish
                    rating = rating.replace(Constances.RATING_KEY, "").replace('''"''', "").replace(",", "")
                    ratingFlag = isRating = False
            else:
                if rating not in Constances.RATING_KEY:
                    # False case
                    ratingFlag = False
                    rating = savingAttribute
                elif rating == Constances.RATING_KEY:
                    isRating = True
        # 'rating' case 2
        if ratingFlag_Second:
            if char == '>':
                buildRating = True
            if buildRating:
                if len(rating) > 20:
                    rating = ""
                    ratingFlag_Second = False
                if char >= '0' and char <= '9':
                    rating = rating + char
                if char == '<':
                    ratingFlag_Second = False
            if buildRating == False:
                counter = counter + 1
                if counter > Constances.MAX_NUMBER_OF_CHARS_FROM_IMG_TO_SRC:
                    # False case
                    buildRating = ratingFlag_Second = False
                    counter = 0
                    rating = ""
        # In general - building the word in HTML_content
        if (char.isalpha() and hrefFlag == False and asinFlag == False and imgFlag == False and priceFlag == False and
            starsFlag == False and ratingFlag == False and nameFlag == False and nameFlag_Second == False and
            ratingFlag_Second == False):
            word = word + char
        # Checking if the word equals to one of the attributes
        if (char.isalpha() == False and nameFlag == False and hrefFlag == False and asinFlag == False and 
            imgFlag == False and priceFlag == False and starsFlag == False and ratingFlag == False and
            nameFlag_Second == False and ratingFlag_Second == False):
            if word == 'asin':
                if asin != "":
                    # Save the asin in case that next product information start
                    asinSaver = asin
                asinFlag = True
                savingAttribute = asin
                asin = ""
                spareChars = counter34 = 0
            if word == 'href':
                if asin != "" and stars == "":
                    hrefFlag = True
                    savingAttribute = href
                    href = ""
                    spareChars = counter34 = 0
            if word == 'title':
                if href != "" and stars == "":
                    nameFlag_Second = True
                    savingAttribute = name
                    spareChars = counter34 = 0
                    name = ""
            if word == 'customerReviews' and rating == "":
                buildRating = False
                ratingFlag_Second = True
                savingAttribute = rating
                rating = ""
                counter = 0
            if word == 'span':
                if href != "" and stars == "":
                    nameFlag = True
                    isName = isKey1 = isKey2 = False
                    savingAttribute = name
                    name = word + char
                if stars != "" and rating == "":
                    savingAttribute = rating
                    ratingFlag = True
                    isRating = False
                    rating = word + char
            if word == 'img':
                if href != "":
                    imgFlag = True
                    srcFlag = False
                    savingAttribute = img
                    img = ""
                    numberOfCharsFromImgToSec = spareChars = counter34 = 0
            if word == 'price':
                if img != "" and price == "":
                    priceFlag = True
                    savingAttribute = price
                    price = ""
                    spareChars = 0
            if word == 'star':
                if img != "":
                    starsFlag = True
                    stars = ""
            word = ""
        # In case that all the attributes were built - Create an instance of Product and start again
        if (href != "" and asin != "" and img != "" and price != "" and stars != "" and name != "" and rating != ""
            and hrefFlag == False and asinFlag == False and imgFlag == False and priceFlag == False and starsFlag == False
            and nameFlag == False and nameFlag_Second == False and ratingFlag == False and ratingFlag_Second == False):
            addFlag = True
            # Removing all amazon brand's products
            for amazonBrand in Constances.AMAZON_BRANDS:
                if amazonBrand in name: addFlag = False
            # Sorting by price
            if float(price) < Constances.MIN_PRICE or float(price) > Constances.MAX_PRICE: addFlag = False
            # Sorting by stars
            if float(stars) < Constances.MIN_STARS or float(stars) > Constances.MAX_STARS: addFlag = False
            # Sorting by rating
            if float(rating) < Constances.MIN_RATING: addFlag = False
            if addFlag: productsBeforeTimeSearching.append([asin, href, name, img, price, stars, rating, category_name])
            # Initialize all the attributes and flags
            numberOfCharsFromImgToSec = spareChars = counter34 = 0
            asinSaver = savingAttribute = word = href = asin = img = price = stars = name = rating = ""
            buildRating = ratingFlag_Second = nameFlag_Second = isKey1 = isKey2 = isRating = isName = hrefFlag = asinFlag = imgFlag = priceFlag = starsFlag = ratingFlag = nameFlag = False
    # Calculate time
    end = time.time()
    searchingTimeForAllProducts = end - start
    # Finish the process for the given URL
    if len(productsBeforeTimeSearching) != 0:
        searchingTimePerProducts = searchingTimeForAllProducts / len(productsBeforeTimeSearching)
        for tempProduct in productsBeforeTimeSearching:
            products.append(Amazon.Product(tempProduct[0], tempProduct[1], tempProduct[2], tempProduct[3],
                                    tempProduct[4], tempProduct[5], tempProduct[6], tempProduct[7], searchingTimePerProducts))
    return products
