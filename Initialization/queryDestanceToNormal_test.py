import SQLHandler, Constances, ast
import numpy as np
from cv2 import cv2
from ImageSimilartion import ImageSimilartion
from Entities import ProductDestance
from Mediation import byCrossReferencing

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
    returnString = ""
    for list in bigMatrix:
        returnString = returnString + str(list) + ","
    returnStringSize = len(returnString)
    returnString = returnString[0:(returnStringSize - 1)]
    return returnString

orb = cv2.ORB_create()
ImageSimilartion.URL_to_PNG('https://i.ebayimg.com/thumbs/images/g/oEYAAOSwk~xZe9Kx/s-l225.webp', "tempImage")
image = cv2.imread(r'ImageSimilartion\\Products image after convert\\tempImage.png', 0)
# Finds the keypoints and descriptors with SIFT
params = orb.detectAndCompute(image, None)
queryDes = bigMatrixToString(params[1])
newDestance = byCrossReferencing.queryDestanceToNormal(queryDes)
# Check if the destances (before and after) are equals
print(isEqualDestances(params[1], newDestance))
'''
product = ProductDestance.Product('https://images-na.ssl-images-amazon.com/images/I/8102ADu5CiL._AC_SX679_.jpg', queryDes, "Amazon")
# Insert into the data base
index = 0
while index < 1000:
    SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, product)
    index = index + 1
    product = ProductDestance.Product('https://images-na.ssl-images-amazon.com/images/I/8102ADu5CiL._AC_SX679_.jpg' + str(index), queryDes, "Amazon")
# Get all the destances
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
ProductDestancesData = SQLHandler.readAllTable(Constances.PRODUCTS_DESTANCES_TABLE)
matches = []
for productDestance in ProductDestancesData:
    newDestance = queryDestanceToNormal(productDestance.destance)
    match = bf.match(newDestance, newDestance)
    numberOfMatches = len(match)
    matches.append(numberOfMatches)
# Print
for match in matches:
    print(match)
'''
