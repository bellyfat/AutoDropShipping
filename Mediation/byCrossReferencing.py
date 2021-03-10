# Doing mediation by cross-referencing data from Amazon and Ebay.
import Constances, SQLHandler, time, os, math, imageio, ast
import numpy as np
import urllib.request, urllib.parse
from Entities import GapProduct, ProductDestance
from urllib.parse import urlparse
from PIL import Image
from ImageSimilartion import ImageSimilartion
from wordfreq import word_frequency

# Gets two numbers and returns the minimum between them
def maximum(numberOne, numberTwo):
    if numberOne > numberTwo:
        return numberOne
    return numberTwo

# Splits and cleans the name
def splitName(name):
    name = name.replace("-", " ")
    name = name.replace("  ", " ")
    for char in name:
        if char.isalpha() == False and ord(char) != Constances.SPACE_ASCII and (char < '0' or char > '9'):
            name = name.replace(char, "")
    nameSplited = name.split(" ")
    for string in nameSplited:
        if string == "" or string == '':
            nameSplited.remove(string)
    return nameSplited

# Gets the minimum value
def getMinmumValue(splitedName, splitedName_Priority):
    name = ""
    while name == "":
        index = 0
        minValue = min(splitedName_Priority)
        for frequency in splitedName_Priority:
            if frequency == minValue:
                firstPartOfTheWord = int(len(splitedName_Priority) / 3)
                if firstPartOfTheWord == 1 or firstPartOfTheWord == 2: firstPartOfTheWord = 4
                if index <= firstPartOfTheWord: name = splitedName[index]
                splitedName_Priority[index] = 1.0
            index = index + 1
    return [minValue, name], splitedName_Priority

# Makes a key words for both sites
# Creates the key words by priority
# The goal is to discover how many similar words
# between the two names are important and meaningful to each name
# Using word frequency of the English language
def makeKeyWords(amazonNameSplited, ebayNameSplited):
    # Makes a priority list for Amazon
    amazonNameSplited_Priority = []
    keyWords_Amazon = []
    for word in amazonNameSplited:
        wordFrequency = word_frequency(word, 'en')
        amazonNameSplited_Priority.append(wordFrequency)
    # Gets the minimum value
    returnParams = getMinmumValue(amazonNameSplited, amazonNameSplited_Priority)
    keyWords_Amazon.append(returnParams[0])
    amazonNameSplited_Priority = returnParams[1]
    returnParams = getMinmumValue(amazonNameSplited, amazonNameSplited_Priority)
    keyWords_Amazon.append(returnParams[0])
    # Makes a priority list for Ebay
    ebayNameSplited_Priority = []
    keyWords_Ebay = []
    for word in ebayNameSplited:
        wordFrequency = word_frequency(word, 'en')
        ebayNameSplited_Priority.append(wordFrequency)
    # Gets the minimum value
    returnParams = getMinmumValue(ebayNameSplited, ebayNameSplited_Priority)
    keyWords_Ebay.append(returnParams[0])
    ebayNameSplited_Priority = returnParams[1]
    returnParams = getMinmumValue(ebayNameSplited, ebayNameSplited_Priority)
    keyWords_Ebay.append(returnParams[0])
    return keyWords_Amazon, keyWords_Ebay
    
# Checking if the name of the products is simillar
# Returns a value between [0.0, 1.0] - 1.0 for 100% similarion
def isNameSimilar(amazonName, ebayName):
    # Splits the names
    amazonNameSplited = splitName(amazonName)
    ebayNameSplited = splitName(ebayName)
    # Gets the maximum size
    maximumSize = maximum(len(amazonNameSplited), len(ebayNameSplited))
    # Gets key word for both names
    keyWords_Amazon, keyWords_Ebay = makeKeyWords(amazonNameSplited, ebayNameSplited)
    # Counting the number of matches
    ebayNameSplited_Copy = ebayNameSplited.copy()
    matchCounter = 0
    matchWords = []
    for amazonString in amazonNameSplited:
        for ebayString in ebayNameSplited_Copy:
            if amazonString.lower() == ebayString.lower():
                matchCounter = matchCounter + 1
                ebayNameSplited_Copy.remove(ebayString)
                matchWords.append(ebayString)
    matchWord_LongestName_Ratio = float(matchCounter) / maximumSize
    # Check the priority of the match words
    isKeyWordAmazon = False
    for keyWord_Amazon in keyWords_Amazon: 
        if keyWord_Amazon[1] in matchWords: isKeyWordAmazon = True
    isKeyWordEbay = False
    for keyWord_Ebay in keyWords_Ebay: 
        if keyWord_Ebay[1] in matchWords: isKeyWordEbay = True
    if isKeyWordAmazon and isKeyWordEbay: return matchWord_LongestName_Ratio
    return 0.0

# Checks if the destances is equal
def isEqualDestances(oldDes, newDes):
    isEqual = True
    valueArray = []
    valueArray_index = 0
    for oldList in oldDes:
        for oldnNumber in oldList:
            valueArray.append(oldnNumber)
    for newList in newDes:
        for newNumber in newList:
            try:
                if newNumber != valueArray[valueArray_index]:
                    isEqual = False
                valueArray_index = valueArray_index + 1
            except:
                return False
    return isEqual

# Convert the matrix to string
def bigMatrixToString(bigMatrix):
    try:
        returnString = ""
        for list in bigMatrix:
            returnString = returnString + str(list) + ","
        returnStringSize = len(returnString)
        returnString = returnString[0:(returnStringSize - 1)]
        return returnString
    except:
        return None

# Get a string of destance from data base
# Return the normal type of the destance (a matrix, dtype = uint8)
def queryDestanceToNormal(queryDestance):
    returnDestance = []
    newRow = []
    # Create a new format
    queryDestance = queryDestance.replace("  ", " ").replace("   ", " ").replace(" ", ",").replace(",,", ",").replace("[,", "[").replace(",]", "]").replace("\n", "")
    queryDestanceNewFormat = ast.literal_eval(queryDestance)
    # Build the new destance
    try:
        for list in queryDestanceNewFormat:
            for number in list:
                newRow.append(np.asarray(number, dtype="uint8"))
            returnDestance.append(np.asarray(newRow, dtype="uint8"))
            newRow = []
        returnDestance = np.asarray(returnDestance, dtype="uint8")
    except: None
    return returnDestance

# Returning two lists, for both sites.
# Returning for site1 all the images's destances
# Same for site2
def updateImagesDestances(site1, site2, site1Data, site2Data):
    site1Data_Img= []
    site2Data_Img = []
    # Calculates the images's destances using SIFT
    # (only if the product's img is not in the database)
    # Creates lists from products that are not in the data base:
    for site1Product in site1Data:
        answer = SQLHandler.isProduct(Constances.PRODUCTS_DESTANCES_TABLE, site1Product.img)
        if answer == False:
            site1Data_Img.append(site1Product.img)
    for site2Product in site2Data:
        answer = SQLHandler.isProduct(Constances.PRODUCTS_DESTANCES_TABLE, site2Product.img)
        if answer == False:
            site2Data_Img.append(site2Product.img)
    # Gets the new destances
    newAmazonDestances = ImageSimilartion.detectAndComputeAllImages(site1Data_Img)
    newEbayDestances = ImageSimilartion.detectAndComputeAllImages(site2Data_Img)
    # Updates Database
    index = 0
    for amazonDestance in newAmazonDestances:
        amazonDestanceString = bigMatrixToString(amazonDestance) # Convert destance to string
        productDestance = ProductDestance.Product(site1Data_Img[index], amazonDestanceString, site1)
        SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, productDestance) # Adds to data base
        index = index + 1
    index = 0
    for ebayDestance in newEbayDestances:
        ebayDestanceString = bigMatrixToString(ebayDestance) # Convert destance to string
        productDestance = ProductDestance.Product(site2Data_Img[index], ebayDestanceString, site2)
        SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, productDestance) # Adds to data base
        index = index + 1

# Checks if the img has a destance in data base
# If so - Return the destance
# Otherwise - Calculate the destance, upload it to data base and return it
def getDestance(img, site):
    answer = SQLHandler.isProduct(Constances.PRODUCTS_DESTANCES_TABLE, img)
    if answer:
        destance = SQLHandler.getProduct(Constances.PRODUCTS_DESTANCES_TABLE, img).destance # The second attribute
        return destance
    else:
        destance = ImageSimilartion.detectAndComputeAllImages([img])[0] # The first element in the list
        destance = bigMatrixToString(destance) # Convert destance to string
        product = ProductDestance.Product(img, destance, site)
        SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, product) # Update data base
        return destance

# Finding gaps between Amazon and Ebay
# Cross-referencing only products with the same category
def findGaps():
    print("Finding gap products...")
    amazonProductsIndex = 0
    ebayProductIndex = 0
    try:
        # Gets the data from the DataBase
        AmazonData = SQLHandler.readAllTable(Constances.AMAZON_PRODUCTS_TABLE)
        EbayData = SQLHandler.readAllTable(Constances.EBAY_PRODUCTS_TABLE)
        if AmazonData == None or EbayData == None: return None # No data
        # Run over the products from AmazonData
        # For each Amazon product cross-referencing with products from EbayDaya with the same category
        for amazonProduct in AmazonData:
            ebayProductIndex = 0
            # Search for ebay categories that can be similiar to amazonProduct.category
            for similar_categories in Constances.similar_categories_Amazon_Ebay:
                for category in similar_categories[0]: # Amazon
                    if amazonProduct.category == category: ebayCategories = similar_categories[1] # Saves the Ebay categories
            # Create images at 'Products image before convert' and 'Products image after convert' folders
            for ebayProduct in EbayData:
                # Check if ebayProduct.category is similiar to amazonProduct.category
                checkFlag = False
                for category in ebayCategories:
                    if ebayProduct.category == category: checkFlag = True
                if checkFlag:
                    try:
                        start = time.time()
                        # Names similartion
                        isNameSimilarAnswer = isNameSimilar(amazonProduct.name, ebayProduct.name)
                        if isNameSimilarAnswer >= Constances.MINIMUM_VALUE_NAME_SIMILAR:
                            # Images similartion - Only when names are similar
                            # isImageSimilarAnswer[0] = Number of matches   ;   isImageSimilarAnswer[1] = avarage distances
                            # Gets the products's destances from the data base
                            amazonProductDestance = getDestance(amazonProduct.img, "Amazon")
                            ebayProductDestance = getDestance(ebayProduct.img, "Ebay")
                            # Convert from string
                            amazonProductDestance = queryDestanceToNormal(amazonProductDestance)
                            ebayProductDestance = queryDestanceToNormal(ebayProductDestance)
                            isImageSimilarAnswer = ImageSimilartion.isImageSimilar(amazonProductDestance, ebayProductDestance)
                            # Checks threshold
                            if (isImageSimilarAnswer[0] >= Constances.MINIMUM_VALUE_IMAGE_NUMBER_OF_MATCHES and
                                            isImageSimilarAnswer[1] <= Constances.MAXIMUM_VALUE_IMAGE_AVARAGE_DISTANCES):
                                # Found two products with similar images and names
                                if float(amazonProduct.price) < float(ebayProduct.price): direction = 'Ebay_Dropshipping_Direction'
                                else: direction = 'Amazon_Dropshipping_Direction'
                                end = time.time()
                                searchingTime = end - start
                                gapProduct = GapProduct.Product(str([amazonProduct.name, ebayProduct.name]), str([amazonProduct.href, ebayProduct.href]),
                                                                str([amazonProduct.img, ebayProduct.img]), str([amazonProduct.price, ebayProduct.price]), direction,
                                                                amazonProduct.category, searchingTime, str(isNameSimilarAnswer), str(isImageSimilarAnswer))
                                SQLHandler.addProduct(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE, gapProduct)
                                # If there is cheaper product on Ebay - No need to continue due to the structure of Ebay
                                if direction == 'Amazon_Dropshipping_Direction': break # Move on to the next amazon product
                    except Exception as e: print(e) # Prints the Error
                ebayProductIndex = ebayProductIndex + 1
            amazonProductsIndex = amazonProductsIndex + 1
    except Exception as e: print(e) # Prints the Error
    print("Finish finding gaps.")
