import SQLHandler, Constances
from Entities import ProductDestance

def false_detectAndComputeAllImages(images):
    returnDestances = []
    for image in images:
        returnDestances.append("100.0")
    return returnDestances

# Returning two lists, for both sites.
# Returning for site1 all the images's destances
# Same for site2
def getImagesDestances(site1, site2, site1Data, site2Data):
    site1Data_Img= []
    site2Data_Img = []
    site1Destances = []
    site2Destances = []
    # Calculates the images's destances using SIFT
    for site1Product in site1Data:
        site1Data_Img.append(site1Product.img)
    for site2Product in site2Data:
        site2Data_Img.append(site2Product.img)
    # Gets the data from the DataBase
    ProductsDestancesData = SQLHandler.readAllTable(Constances.PRODUCTS_DESTANCES_TABLE)
    for productDestance in ProductsDestancesData:
        if productDestance.site == site1:
            for site1Img in site1Data_Img:
                # Looking for the img, if found - remove from the list (destance already exsists)
                if site1Img == productDestance.img:
                    site1Data_Img.remove(site1Img)
                    site1Destances.append(productDestance.destance)
        if productDestance.site == site2:
            for site2Img in site2Data_Img:
                # Looking for the img, if found - remove from the list (destance already exsists)
                if site2Img == productDestance.img:
                    site2Data_Img.remove(site2Img)
                    site2Destances.append(productDestance.destance)
    # Gets the new destances and adds to the site list
    newAmazonDestances = false_detectAndComputeAllImages(site1Data_Img)
    for newDestace in newAmazonDestances:
        site1Destances.append(newDestace)
    newEbayDestances = false_detectAndComputeAllImages(site2Data_Img)
    for newDestace in newEbayDestances:
        site2Destances.append(newDestace)
    # Updates Database
    index = 0
    for amazonDestance in newAmazonDestances:
        productDestance = ProductDestance.Product(site1Data_Img[index], amazonDestance, site1)
        SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, productDestance)
        index = index + 1
    index = 0
    for ebayDestance in newEbayDestances:
        productDestance = ProductDestance.Product(site2Data_Img[index], ebayDestance, site2)
        SQLHandler.addProduct(Constances.PRODUCTS_DESTANCES_TABLE, productDestance)
        index = index + 1
    return site1Destances, site2Destances

# Gets the data from the DataBase
AmazonData = SQLHandler.readAllTable(Constances.AMAZON_PRODUCTS_TABLE)
EbayData = SQLHandler.readAllTable(Constances.EBAY_PRODUCTS_TABLE)
# Calculates the images's destances using SIFT
AmazonDestances, EbayDestances = getImagesDestances('Amazon', 'Ebay', AmazonData, EbayData)
