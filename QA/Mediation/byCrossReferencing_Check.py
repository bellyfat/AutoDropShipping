import sys, time, csv
from Entities import GapProduct
from Collection import Ebay
from Mediation import byCrossReferencing
from Initialization import driverStarter

def readFromResult():
    lines = ["names", "hrefs", "img", "prices", "", "", "", "Enter",]
    lines_index = 0
    names = []
    hrefs = []
    gapProducts = []
    gapProducts_index = 0
    with open("GapProducts.txt", mode='r') as ProdcutsFile:
        readCSV = csv.reader(ProdcutsFile)
        for row in readCSV:
            if lines[lines_index] == "names":
                names = row
            if lines[lines_index] == "hrefs":
                hrefs = row
            if lines[lines_index] == "Enter":
                gapProducts.insert(gapProducts_index, GapProduct.Product(names, hrefs, "", "", "", "", ""))
                gapProducts_index = gapProducts_index + 1
                names = []
                hrefs = []
                lines_index = 0
            lines_index = lines_index + 1
    return gapProducts

gapProducts = readFromResult()
GapProduct.printProductList(gapProducts)
