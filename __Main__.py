import Constances, time, threading, SQLHandler
import tkinter as tk
from Collection import Amazon, Ebay
from tkinter import Listbox, Scrollbar, Frame, RIGHT, LEFT, BOTTOM, HORIZONTAL, Y, X, END
from tkinter.ttk import Progressbar
from Initialization import driverStarter
from Mediation import byCrossReferencing

# Global flags
amazonSearchFlag = False
ebaySearchFlag = False
findFlag = False

# Print a message to the user
def printMessage(string):
    print(string)

# btnSearchProducts - Handle the function getTheProducts_multiURLs()
def pressSearchingProducts_Amazon():
    global amazonSearchFlag
    if amazonSearchFlag == False:
        searchThread = threading.Thread(target=Amazon.getTheProducts_multiURLs)
        searchThread.start()
        amazonSearchFlag = True
    else:
        printMessage("The system is already searching...")

# btnSearchProducts - Handle the function getTheProducts_multiURLs()
def pressSearchingProducts_Ebay():
    global ebaySearchFlag
    if ebaySearchFlag == False:
        searchThread = threading.Thread(target=Ebay.getTheProducts_multiURLs)
        searchThread.start()
        ebaySearchFlag = True
    else:
        printMessage("The system is already searching...")

# btnFindingGaps - Handle the function findGaps() (byCrossReferencing)
def pressFindingGaps():
    global findFlag
    if findFlag == False:
        findThread = threading.Thread(target=byCrossReferencing.findGaps)
        findThread.start()
        findFlag = True
    else:
        printMessage("The system is already finding...")

# Main UI
class startUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Creates the main container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # Initialize all the pages
        for page in (StartPageViewer, ActionsViewer, GapsListViewer, ReportsViewer):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # Show the main page
        self.show_frame(StartPageViewer)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# The main page
class StartPageViewer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Gino Team - Automatic Dropshipping", font=Constances.LARGE_FONT)
        label.pack(pady=10,padx=10)
        actionsButton = tk.Button(self, text="Actions", command=lambda: controller.show_frame(ActionsViewer))
        actionsButton.pack()
        viewGapsListButton = tk.Button(self, text="Gaps list", command=lambda: controller.show_frame(GapsListViewer))
        viewGapsListButton.pack()
        reportsButtons = tk.Button(self, text="Reports", command=lambda: controller.show_frame(ReportsViewer))
        reportsButtons.pack()

# All the software functions
class ActionsViewer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Gino Team - Automatic Dropshipping", font=Constances.LARGE_FONT)
        label.pack(pady=10,padx=10)
        # Search products from amazon's URLs
        lbl = tk.Label(self, text="Search Amazon prodcuts:", font=Constances.LARGE_FONT)
        lbl.pack()
        btnSearchProducts = tk.Button(self, text="Search", command = pressSearchingProducts_Amazon)
        btnSearchProducts.pack()
        # Search products from ebay's URLs
        lbl = tk.Label(self, text="Search Ebay prodcuts:", font=Constances.LARGE_FONT)
        lbl.pack()
        btnSearchProducts = tk.Button(self, text="Search", command = pressSearchingProducts_Ebay)
        btnSearchProducts.pack()
        # Finding gaps
        lbl = tk.Label(self, text="Finding gaps:", font=Constances.LARGE_FONT)
        lbl.pack()
        btnFindingGaps = tk.Button(self, text="Finding", command = pressFindingGaps)
        btnFindingGaps.pack()
        # Back button
        backButton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPageViewer))
        backButton.pack()

# Table of all the gap products
class GapsListViewer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Gino Team - Automatic Dropshipping", font=Constances.LARGE_FONT)
        label.grid(row=0, column=0)
        # Gets all the final products
        '''
        finalProducts = getFinalProducts()
        '''
        finalProducts = ""
        # Create the table
        root = self
        root.grid_rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        frame_main = tk.Frame(root, bg="gray")
        frame_main.grid(sticky='news')
        # Create a frame for the canvas with non-zero row&column weights
        frame_canvas = tk.Frame(frame_main)
        frame_canvas.grid(row=2, column=2, pady=(7, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)
        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky="news")
        # Link a scrollbar to the canvas
        vsbV = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsbV.grid(row=0, column=1, sticky='ns')
        vsbH = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
        vsbH.grid(row=1, column=0, sticky='nw')
        canvas.configure(yscrollcommand=vsbV.set, xscrollcommand=vsbH.set)
        # Create a frame to contain the Labels
        frame_Labels = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_Labels, anchor='nw')
        # Creates the table
        row = 1
        cells = [[tk.Label() for j in range(len(finalProducts) + 1)] for i in range(8)]
        cells[0][0] = tk.Label(frame_Labels, width=5, relief=tk.RIDGE, text=("#"))
        cells[0][0].grid(row=0, column=0, sticky='news')
        cells[1][0] = tk.Label(frame_Labels, padx=7, pady=7, width=15, relief=tk.RIDGE, text=("ASIN"))
        cells[1][0].grid(row=0, column=1, sticky='news')
        cells[2][0] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("Other site price"))
        cells[2][0].grid(row=0, column=2, sticky='news')
        cells[3][0] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("Shipping"))
        cells[3][0].grid(row=0, column=3, sticky='news')
        cells[4][0] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("Original Price"))
        cells[4][0].grid(row=0, column=4, sticky='news')
        cells[5][0] = tk.Label(frame_Labels, padx=7, pady=7, width=40, relief=tk.RIDGE, text=("Url  "))
        cells[5][0].grid(row=0, column=5, sticky='nw')
        cells[6][0] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("The gap ($)"))
        cells[6][0].grid(row=0, column=6, sticky='nw')
        cells[7][0] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("The gap (%)"))
        cells[7][0].grid(row=0, column=7, sticky='nw')
        for product in finalProducts:
            cells[0][row] = tk.Label(frame_Labels, width=5, relief=tk.RIDGE, text=(str(row)))
            cells[0][row].grid(row=row, column=0, sticky='news')
            cells[1][row] = tk.Label(frame_Labels, padx=7, pady=7, width=15, relief=tk.RIDGE, text=(product.amazonAsin))
            cells[1][row].grid(row=row, column=1, sticky='news')
            cells[2][row] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=(product.price))
            cells[2][row].grid(row=row, column=2, sticky='news')
            cells[3][row] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=(product.shipping))
            cells[3][row].grid(row=row, column=3, sticky='news')
            cells[4][row] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=(product.amazonPrice.replace("]", "").replace("[", "").replace("'", "")))
            cells[4][row].grid(row=row, column=4, sticky='news')
            cells[5][row] = tk.Label(frame_Labels, width=40, relief=tk.RIDGE, text=(product.href))
            cells[5][row].grid(row=row, column=5, sticky='nw')
            cells[6][row] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("%.2f" % product.gapPrice))
            cells[6][row].grid(row=row, column=6, sticky='nw')
            cells[7][row] = tk.Label(frame_Labels, padx=7, pady=7, width=10, relief=tk.RIDGE, text=("%.2f" % product.gapPrecent))
            cells[7][row].grid(row=row, column=7, sticky='nw')
            row = row + 1
        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_Labels.update_idletasks()
        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        frame_canvas.config(width=1050, height=500)
        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))
        backButton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPageViewer))
        backButton.grid(row=len(finalProducts) + 2, column=0)

# Reports and statistics
class ReportsViewer(tk.Frame):
    # Calculate attributes
    amazonProducts = None
    ebayProducts = None
    amazon_ebay_gaps = None
    totalGaps = 0
    profitSum = 0
    precentAvg = 0
    avgTime_amazonProducts = 0
    avgTime_ebayProducts = 0
    # Update text attributes
    totalGapsText = ""
    sumProfitText = ""
    avgProfitText = ""
    avgTimePerProductTextAmazon = ""
    avgTimePerProductTextEbay = ""
    numberOfProductEbayText = ""
    sumOfProducts = 0

    def calculation(self):
        # Gets Amazon products
        self.amazonProducts = SQLHandler.readAllTable(Constances.AMAZON_PRODUCTS_TABLE)
        # Gets Ebay products
        self.ebayProducts = SQLHandler.readAllTable(Constances.EBAY_PRODUCTS_TABLE)
        # Gets Amazon and Ebay gaps
        self.amazon_ebay_gaps = SQLHandler.readAllTable(Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE)
        if len(self.amazonProducts):
            # Avg Amazon product searching time
            for product in self.amazonProducts: self.avgTime_amazonProducts = self.avgTime_amazonProducts + float(product.searchingTime)
            self.avgTime_amazonProducts = self.avgTime_amazonProducts / len(self.amazonProducts)
        if len(self.ebayProducts):
            # Avg Ebay product searching time
            for product in self.ebayProducts: self.avgTime_ebayProducts = self.avgTime_ebayProducts + float(product.searchingTime)
            self.avgTime_ebayProducts = self.avgTime_ebayProducts / len(self.ebayProducts)
        self.totalGaps = len(self.amazon_ebay_gaps)
        if len(self.amazon_ebay_gaps):
            for gap in self.amazon_ebay_gaps:
                prices = gap.prices.replace("[", "").replace("]", "").replace("'", "").split(",")
                profit = float(prices[0]) - float(prices[1])
                if profit < 0: # prices[1] is bigger
                    profit = profit * (-1)
                    precent = profit / float(prices[1])
                else: precent = profit / float(prices[0])
                self.profitSum = self.profitSum + profit
                self.precentAvg = self.precentAvg + precent
            self.precentAvg = self.precentAvg / self.totalGaps

    def __init__(self, parent, controller):
        # Calculate
        self.calculation()
        # Initialize
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Gino Team - Automatic Dropshipping", font=Constances.LARGE_FONT)
        label.pack(pady=10, padx=10)
        ###     Total       ###
        totalLabel = tk.Label(self, text="Dropshipping", font=Constances.LARGE_FONT)
        totalLabel.pack()
        self.sumOfProducts = tk.StringVar()
        self.sumOfProducts.set("Total products:    " + f'{(len(self.amazonProducts) + len(self.ebayProducts)):,}')
        sumOfProductsLabel = tk.Label(self, textvariable=self.sumOfProducts, font=Constances.SMALL_FONT)
        sumOfProductsLabel.pack()
        self.totalGapsText = tk.StringVar()
        self.totalGapsText.set("Total gaps (Amazon-Ebay):    " + str(self.totalGaps))
        totalInvestmentLabel = tk.Label(self, textvariable=self.totalGapsText, font=Constances.SMALL_FONT)
        totalInvestmentLabel.pack()
        self.sumProfitText = tk.StringVar()
        self.sumProfitText.set("Total profit price:    " + "$" + str("%.2f" % self.profitSum))
        sumProfitLabel = tk.Label(self, textvariable=self.sumProfitText, font=Constances.SMALL_FONT)
        sumProfitLabel.pack()
        self.avgProfitText = tk.StringVar()
        self.avgProfitText.set("Profit average precent:    " + str("%.3f" % self.precentAvg) + "%")
        avgProfitLabel = tk.Label(self, textvariable=self.avgProfitText, font=Constances.SMALL_FONT)
        avgProfitLabel.pack()
        ###     Timming     ###
        timeLabel = tk.Label(self, text="Average time per product", font=Constances.LARGE_FONT)
        timeLabel.pack()
        self.avgTimePerProductTextAmazon = tk.StringVar()
        self.avgTimePerProductTextAmazon.set("Amazon:      " + str("%.4f" % self.avgTime_amazonProducts) + " sec'")
        avgTimePerProductLable = tk.Label(self, textvariable=self.avgTimePerProductTextAmazon, font=Constances.SMALL_FONT)
        avgTimePerProductLable.pack()
        self.numberOfProductAmazonText = tk.StringVar()
        self.numberOfProductAmazonText.set("(from " + str(len(self.amazonProducts)) + " products)")
        numberOfProductAmazonLable = tk.Label(self, textvariable=self.numberOfProductAmazonText, font=Constances.SMALL_FONT)
        numberOfProductAmazonLable.pack()
        self.avgTimePerProductTextEbay = tk.StringVar()
        self.avgTimePerProductTextEbay.set("Ebay:      " + str("%.4f" % self.avgTime_ebayProducts) + " sec'")
        avgTimePerProductLable = tk.Label(self, textvariable=self.avgTimePerProductTextEbay, font=Constances.SMALL_FONT)
        avgTimePerProductLable.pack()
        self.numberOfProductEbayText = tk.StringVar()
        self.numberOfProductEbayText.set("(from " + str(len(self.ebayProducts)) + " products)")
        numberOfProductEbayLabel = tk.Label(self, textvariable=self.numberOfProductEbayText, font=Constances.SMALL_FONT)
        numberOfProductEbayLabel.pack()
        refreshButton = tk.Button(self, text="Refresh", command=self.changeText)
        refreshButton.pack()
        # Going back button
        backButton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPageViewer))
        backButton.pack()

    # Refresh the data
    def changeText(self):
        self.calculation()
        self.totalGapsText.set("Total gaps (Amazon-Ebay)    :" + str(self.totalGaps))
        self.sumProfitText.set("Total profit price:    " + "$" + str("%.2f" % self.profitSum))
        self.avgProfitText.set("Profit average precent:    " + str("%.3f" % self.precentAvg) + "%")
        self.avgTimePerProductTextAmazon.set("Amazon:      " + str("%.4f" % self.avgTime_amazonProducts) + " sec'")
        self.avgTimePerProductTextEbay.set("Ebay:      " + str("%.4f" % self.avgTime_ebayProducts) + " sec'")
        self.numberOfProductEbayText.set("(from " + str(len(self.ebayProducts)) + " products)")
        self.numberOfProductAmazonText.set("(from " + str(len(self.amazonProducts)) + " products)")
        self.sumOfProducts.set("Total products:    " + str(len(self.amazonProducts) + len(self.ebayProducts)))

app = startUI()
app.mainloop()
