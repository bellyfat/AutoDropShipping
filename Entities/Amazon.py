# Organized structure for general product

# Auxiliary class for making Product class iteratable
class ProductIterator:
    def __init__(self, product):
        self._product = product
        self._index = 0
    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < (len(self._product._juniorMembers) + len(self._product._seniorMembers)) :
            if self._index < len(self._product._juniorMembers): # Check if junior members are fully iterated or not
                result = (self._product._juniorMembers[self._index] , 'junior')
            else:
                result = (self._product._seniorMembers[self._index - len(self._product._juniorMembers)]   , 'senior')
            self._index +=1
            return result
        # End of Iteration
        raise StopIteration
    
# General product
class Product:
    def __init__(self, asin, href, name, img, price, stars, rating, category, searchingTime):
        self.href = href
        self.asin = asin
        self.img = img
        self.price = price
        self.stars = stars
        self.name = name
        self.rating = rating
        self.category = category
        self.searchingTime = searchingTime
        self._juniorMembers = list()
        self._seniorMembers = list()
    def addJuniorMembers(self, members):
        self._juniorMembers += members
    def addSeniorMembers(self, members):
        self._seniorMembers += members
    def __iter__(self):
        return ProductIterator(self)

def printProduct(product):
    print(product.asin)
    print(product.href)
    print(product.name)
    print(product.img)
    print(product.price)
    print(product.stars)
    print(product.rating)
    print(product.category)
    print(product.searchingTime)

def printProductList(productList):
    for product in productList:
        printProduct(product)
        print()
