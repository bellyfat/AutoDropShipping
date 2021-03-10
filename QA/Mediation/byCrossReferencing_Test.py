import sys, time, Constances, SQLHandler, cv2
from scipy.linalg import norm
from Entities import GapProduct, Amazon
from Collection import Ebay
from Mediation import byCrossReferencing
from Initialization import driverStarter
from PIL import Image
from ImageSimilartion import ImageSimilartion

ASIN = "B07HDBZN7Q"
URL_miniImage = 'https://www.ebay.com/itm/Roku-Premiere-Version-HD-4K-HDR-Streaming-Media-Player-W-Remote-HDMI-Cable/233731309644?epid=13024702758&hash=item366b78c04c:g:LWYAAOSwtV1dTN2C'
URL_HARD = 'https://www.ebay.com/itm/Roku-Premiere-4K-Digital-Media-Streamer-Black-Brand-New/164407070651?epid=13024702758&hash=item26476ccfbb:g:0fsAAOSwJntfcnzi'
URL_SIMPLE = 'https://www.ebay.com/itm/ROKU-HD-4K-HDR-Streaming-Simple-Remote-Premium-HDMI-Cable-NEW-FREESHIP/114463459420?epid=13024702758&hash=item1aa68dc85c:g:SvsAAOSwsklfaRNU'
URL_FLASH = 'https://www.ebay.com/itm/NEW-Roku-Premiere-3920RW-4K-Streaming-Media-Player-Black-Streams-HD-4K-HDR/184496169818?epid=13024702758&hash=item2af4d4235a:g:4WIAAOSwUdZeV1Xi'

# Check if the products are similar
# product1 is AmazonProduct
# product2 is EbayProduct
# Return the name similartion and the image similartion
def CheckProducts(product1, product2):
    # Name
    isNameSimilarAnswer = byCrossReferencing.isNameSimilar(product1.name, product2.name)
    # Image
    amazonProductDestance = byCrossReferencing.getDestance(product1.img, "Amazon")
    ebayProductDestance = byCrossReferencing.getDestance(product2.img, "Ebay")
    amazonProductDestance = byCrossReferencing.queryDestanceToNormal(amazonProductDestance)
    ebayProductDestance = byCrossReferencing.queryDestanceToNormal(ebayProductDestance)
    isImageSimilarAnswer = ImageSimilartion.isImageSimilar(amazonProductDestance, ebayProductDestance)
    return isNameSimilarAnswer, isImageSimilarAnswer

# Test if four similar products from ebay can be catch
def test_4GapProducts():
    amazonProduct = SQLHandler.getProduct(Constances.AMAZON_PRODUCTS_TABLE, ASIN)
    product1 = SQLHandler.getProduct(Constances.EBAY_PRODUCTS_TABLE, URL_miniImage)
    product2 = SQLHandler.getProduct(Constances.EBAY_PRODUCTS_TABLE, URL_HARD)
    product3 = SQLHandler.getProduct(Constances.EBAY_PRODUCTS_TABLE, URL_SIMPLE)
    product4 = SQLHandler.getProduct(Constances.EBAY_PRODUCTS_TABLE, URL_FLASH)
    print(CheckProducts(amazonProduct, product1))
    print(CheckProducts(amazonProduct, product2))
    print(CheckProducts(amazonProduct, product3))
    print(CheckProducts(amazonProduct, product4))

start = time.time()
byCrossReferencing.findGaps()
end = time.time()
print("Finish ##################\n@@@@@@@@@@@@\n%%%%%%%%%%%%%%%\n********")
print(end - start)
