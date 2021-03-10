import SQLHandler, Constances, time
from Entities import GapProduct
from Initialization import driverStarter

driver = driverStarter.startDriver()
GapData_AmazonEbay = SQLHandler.readAllTable(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE)
nameSimilarity = []
imgSimilarity_NumberOfMatch = []
imgSimilarity_Avg = []
for GapProduct in GapData_AmazonEbay: nameSimilarity.append(GapProduct.namesSimilar)
nameSimilarity.sort()
for sortedName in nameSimilarity:
    for GapProduct in GapData_AmazonEbay:
        imgSimilar = GapProduct.imgsSimilar.replace("(", "").replace(")", "").replace("'", "").replace(" ", "").split(",")
        if (sortedName == GapProduct.namesSimilar and sortedName >= str(0.6) and 
            imgSimilar[0] >= str(100) and imgSimilar[1] <= str(50)):
            print(sortedName)
            hrefs = GapProduct.hrefs.replace("[", "").replace("]", "").replace("'", "").split(",")
            driverStarter.effectiveGet(driver, hrefs[0]) # Amazon
            time.sleep(2)
            driverStarter.effectiveGet(driver, hrefs[1]) # Ebay
            time.sleep(2)
