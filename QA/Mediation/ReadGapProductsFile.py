import csv, Constances
from Entities import GapProduct

# Handle the href case
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
        if asin in href:
            href = Constances.AMAZON_HREF_PREFIX + href
            return href, False, counter34, spareChars
        # False case
        return None, False, counter34, spareChars

# Read the file 'result.txt'
# Return the gap products from the file
def readGapProductsFile():
    returnValues = []
    href = ""
    counter34 = 0
    spareChars = 0
    hrefFlag = False
    with open("result.txt", mode='r') as ProdcutsFile:
        readCSV = csv.reader(ProdcutsFile)
        for row in readCSV:
            for char in row:
                # 'href' case
                if hrefFlag:
                    answer,  = hrefCase(href, char, counter34, spareChars)
                    if (href == None or href == '') and answer == False:
                        # Not found
                        href = savingAttribute
                        hrefFlag = False
                    if (href != None and href != '') and answer == False:
                        # Found href
                        hrefFlag = False
                # In case that all the attributes were built - Create an instance of Product and start again
                if (href != "" and hrefFlag == False):
                    returnValues.append(GapProduct.Product(names, hrefs, img, prices, dire))
                    # Initialize all the attributes and flags
                    numberOfCharsFromImgToSec = spareChars = counter34 = 0
