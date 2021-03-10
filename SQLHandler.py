import pyodbc, Constances, time
from Entities import Amazon, Ebay, ProductDestance, GapProduct, StoreProduct

# Reading and returning all the products from a table
def readAllTable(tableName):
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 0, 0)]) # Coax pyodbc into treating [N]TEXT columns like [n]varchar(max) columns
    # Makes a query
    cursor.execute('SELECT * FROM [dbo].[' + tableName + ']')
    # Turns each row into the appropriate structure
    returnProduct = []
    returnProduct_Index = 0
    try:
        for row in cursor:
            if tableName == Constances.AMAZON_PRODUCTS_TABLE:
                try:
                    product = Amazon.Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    returnProduct.insert(returnProduct_Index, product)
                    returnProduct_Index = returnProduct_Index + 1
                except: None
            if tableName == Constances.EBAY_PRODUCTS_TABLE:
                try:
                    product = Ebay.Product(row[0], row[1], row[2], row[3], row[4], row[5])
                    returnProduct.insert(returnProduct_Index, product)
                    returnProduct_Index = returnProduct_Index + 1
                except: None
            if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
                try:
                    product = ProductDestance.Product(row[0], row[1], row[2])
                    returnProduct.insert(returnProduct_Index, product)
                    returnProduct_Index = returnProduct_Index + 1
                except: None
            if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
                try:
                    product = GapProduct.Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    returnProduct.insert(returnProduct_Index, product)
                    returnProduct_Index = returnProduct_Index + 1
                except: None
            if tableName == Constances.STORE_PRODUCTS_TABLE:
                try:
                    product = StoreProduct.Product(row[0], row[1], row[2], row[3])
                    returnProduct.insert(returnProduct_Index, product)
                    returnProduct_Index = returnProduct_Index + 1
                except: None
        return returnProduct
    except Exception as e:
        print(e)
        # The file does not exists
        print("Error - The table " + tableName + " does not exists")
        return None

# Saving the product in a tableName
def addProduct(tableName, product):
    # First checking if the product if already exsist in the table
    # If so - delete the product and insert him again (update)
    if tableName == Constances.AMAZON_PRODUCTS_TABLE: answer = isProduct(tableName, product.asin)
    if tableName == Constances.EBAY_PRODUCTS_TABLE: answer = isProduct(tableName, product.href)
    if tableName == Constances.PRODUCTS_DESTANCES_TABLE: answer = isProduct(tableName, product.img)
    if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE: answer = isProduct(tableName, product.hrefs)
    if tableName == Constances.STORE_PRODUCTS_TABLE: answer = isProduct(tableName, [product.site1_url, product.site2_url])
    if answer == True: deleteProduct(tableName, product)
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    if tableName == Constances.AMAZON_PRODUCTS_TABLE:
        params = [(product.asin, product.href, product.name, product.img, product.price, product.stars,
                                                    product.rating, product.category, product.searchingTime, str(time.time()))]
        cursor.executemany("INSERT INTO [dbo].[" + tableName + "] ([ASIN], [HREF], [NAME], [IMAGE], [PRICE], [STARS], [RATING], [CATEGORY], [SEARCHING_TIME], [TIME]) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        conn.commit()
    if tableName == Constances.EBAY_PRODUCTS_TABLE:
        params = [(product.href, product.name, product.img, product.price, product.category,
                                                     product.searchingTime, str(time.time()))]
        cursor.executemany("INSERT INTO [dbo].[" + tableName + "] ([HREF], [NAME], [IMAGE], [PRICE], [CATEGORY], [SEARCHING_TIME], [TIME]) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?)", params)
        conn.commit()
    if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
        params = [(product.img, product.destance, product.site)]
        cursor.executemany("INSERT INTO [dbo].[" + tableName + "] ([IMAGE], [DESTANCE], [SITE]) " +
                        "VALUES (?, ?, ?)", params)
        conn.commit()
    if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
        params = [(product.names, product.hrefs, product.imgs, product.prices, product.direction, product.category, product.searchingTime, product.namesSimilar, product.imgsSimilar, str(time.time()))]
        cursor.executemany("INSERT INTO [dbo].[" + tableName + "] ([NAMES], [HREFS], [IMAGES], [PRICES], [DIRECTION], [CATEGORY], [SEARCH_TIME], [NAMES_SIMILAR], [IMAGES_SIMILAR], [TIME]) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        conn.commit()
    if tableName == Constances.STORE_PRODUCTS_TABLE:
        params = [(product.site1_url, product.site2_url, product.store_location, product.status)]
        cursor.executemany("INSERT INTO [dbo].[" + tableName + "] ([SITE1_URL], [SITE2_URL], [STORE_LOCATION], [STATUS]) " +
                        "VALUES (?, ?, ?, ?)", params)
        conn.commit()

# Finding the product in the table
# Return True if the product was found
# Otherwise - False
def isProduct(tableName, productKey):
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    if tableName == Constances.AMAZON_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].ASIN =  ?", productKey)
    # Makes a query
    if tableName == Constances.EBAY_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREF =  ?", productKey)
    # Makes a query
    if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].IMAGE =  ?", productKey)
    # Makes a query
    if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREFS =  ?", productKey)
    # Makes a query
    if tableName == Constances.STORE_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].SITE1_URL =  ? and [dbo].[" + tableName + "].SITE2_URL =  ?", productKey[0], productKey[1])
    # Turns each row into the appropriate structure
    try:
        for row in cursor: return True
        return False
    except Exception as ex:
        # The file does not exists
        print(ex)
        return False

# Deleting the product in the table
# Return True if the product was deleted successfully
# Otherwise - False
def deleteProduct(tableName, product):
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    try:
        if tableName == Constances.AMAZON_PRODUCTS_TABLE:
            cursor.execute("DELETE FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].ASIN =  ?", str(product.asin))
            conn.commit()
        if tableName == Constances.EBAY_PRODUCTS_TABLE:
            cursor.execute("DELETE FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREF =  ?", str(product.href))
            conn.commit()
        if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
            cursor.execute("DELETE FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].IMAGE =  ?", str(product.img))
            conn.commit()
        if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
            cursor.execute("DELETE FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREFS =  ?", str(product.hrefs))
            conn.commit()
        if tableName == Constances.STORE_PRODUCTS_TABLE:
            cursor.execute("DELETE FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].SITE1_URL =  ? and [dbo].[" + tableName + "].SITE2_URL =  ?", product.site1_url, product.site2_url)
            conn.commit()
        return True
    except Exception as ex:
        # The file does not exists
        print(ex)
        return False

# Returning the product from the table
# Otherwise - None
def getProduct(tableName, productKey):
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    if tableName == Constances.AMAZON_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].ASIN =  ?", str(productKey))
    # Makes a query
    if tableName == Constances.EBAY_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREF =  ?", str(productKey))
    # Makes a query
    if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].IMAGE =  ?", str(productKey))
    # Makes a query
    if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].HREFS =  ?", str(productKey))
    # Makes a query
    if tableName == Constances.STORE_PRODUCTS_TABLE:
        cursor.execute("SELECT * FROM [dbo].[" + tableName + "] WHERE [dbo].[" + tableName + "].SITE1_URL =  ? and [dbo].[" + tableName + "].SITE2_URL =  ?", productKey[0], productKey[1])
    try:
        for row in cursor:
            if tableName == Constances.AMAZON_PRODUCTS_TABLE:
                try: product = Amazon.Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                except: None
            if tableName == Constances.EBAY_PRODUCTS_TABLE:
                try: product = Ebay.Product(row[0], row[1], row[2], row[3], row[4], row[5])
                except: None
            if tableName == Constances.PRODUCTS_DESTANCES_TABLE:
                try: product = ProductDestance.Product(row[0], row[1], row[2])
                except: None
            if tableName == Constances.GAPS_AMAZON_EBAY_PRODUCTS_TABLE:
                try: product = GapProduct.Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                except: None
            if tableName == Constances.STORE_PRODUCTS_TABLE:
                try: product = StoreProduct.Product(row[0], row[1], row[2], row[3])
                except: None
        return product
    except Exception as ex:
        # The file does not exists
        print(ex)
        return None

# Just for this version - Control the program from the SQL table Constance.USER_ORDER
def isStoresOpen():
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    cursor.execute("SELECT * FROM [dbo].[UserOrder] WHERE [dbo].[UserOrder].isAmazonStoreOpen =  1 and [dbo].[UserOrder].isEbayStoreOpen =  1")
    try:
        for row in cursor: return True
        return False
    except: return False

# Just for this version - Control the program from the SQL table Constance.USER_ORDER
def updateUserOrderTable():
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    cursor.execute("UPDATE [dbo].[UserOrder] SET [dbo].[UserOrder].isAmazonStoreOpen =  0, [dbo].[UserOrder].isEbayStoreOpen =  0")
    conn.commit()

# Get storeProduct details from Constances.GAPS_AMAZON_EBAY_PRODUCTS
# Return the gap product that match to site1 url and site2 url
def getStoreProductDetails(storeProduct):
    hrefs = [storeProduct.site1_url, storeProduct.site2_url]
    # Connect to Data Base
    conn = pyodbc.connect(r'Driver={SQL Server};'r'Server=DESKTOP-SAE8VJG\GINOSQLSERVER;'r'Database=AutomaticDropshippingDB;'r'Trusted_Connection=yes;')
    cursor = conn.cursor()
    # Makes a query
    cursor.execute("SELECT * FROM [dbo].[GapsAmazonEbayProducts] WHERE [dbo].[GapsAmazonEbayProducts].[HREFS] = ?", str(hrefs))
    try:
        for row in cursor:
            product = GapProduct.Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        return product
    except: None
