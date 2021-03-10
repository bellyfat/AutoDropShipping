# Doing mediation by cross-referencing data from Amazon and Ebay.
import time, requests, os, SQLHandler, Constances
import numpy as np
from io import BytesIO
from cv2 import cv2
from Entities import GapProduct, ProductDestance
from PIL import Image

# Saves the images from the given URLs as PNG type
def URL_to_PNG(imageURL, name):
    # Saves the images from the given URLs
    # The images will be save in the folder 'Products image before convert'
    response = requests.get(imageURL)
    # Converts the image from jpg format to png format
    # image - Open, save as png and then open again
    image = Image.open(BytesIO(response.content))
    image.save(r'ImageSimilartion\\Products image after convert\\' + name + '.png')
    image.close()

# Delete from both folders: 'Products image before convert' and 'Products image after convert' at ImageSimilartion folder
def deleteImage(name):
    # Closes and deletes
    os.remove(r'ImageSimilartion\\Products image after convert\\' + name + '.png')

# Gets a list of images URLs
# Return a list of destances using SIFT algorithm
def detectAndComputeAllImages(listOfImages):
    destances = []
    # Initiates SIFT detector
    orb = cv2.ORB_create()
    for imageURL in listOfImages:
        try:
            URL_to_PNG(imageURL, "tempImage")
            image = cv2.imread(r'ImageSimilartion\\Products image after convert\\tempImage.png', 0)
            # Finds the keypoints and descriptors with SIFT
            params = orb.detectAndCompute(image, None)
            destances.append(params[1]) # destance
            deleteImage("tempImage")
        except: destances.append(None)
    return destances

# Checking if the images of the products is simillar
# Using SIFT algorithm
# Gets the images's names
# Returns the number of matches and the avarage distaces between them
def isImageSimilar(des1, des2):
    # Creates BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Matches descriptors.
    matches = bf.match(des1, des2)
    numberOfMatches = len(matches)
    if numberOfMatches == 0:
        return None, None
    # Calculates
    avgDistance = 0
    for match in matches:
        avgDistance = avgDistance + match.distance
    avgDistance = avgDistance / numberOfMatches
    return numberOfMatches, avgDistance

# Remove all the Null value in DESTANCE attribute at Constances.PRODUCTS_DESTANCES_TABLE
def removeNullFromDatabase():
    ProductDestanceData = SQLHandler.readAllTable(Constances.PRODUCTS_DESTANCES_TABLE)
    for productDestance in ProductDestanceData:
        try:
            if productDestance.destance == None:
                SQLHandler.deleteProduct(Constances.PRODUCTS_DESTANCES_TABLE, productDestance)
        except: None
