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
    def __init__(self, img, destance, site):
        self.img = img
        self.destance = destance
        self.site = site
        self._juniorMembers = list()
        self._seniorMembers = list()
    def addJuniorMembers(self, members):
        self._juniorMembers += members
    def addSeniorMembers(self, members):
        self._seniorMembers += members
    def __iter__(self):
        return ProductIterator(self)

def printProduct(product):
    print(product.img)
    print(product.destance)
    print(product.site)

def printProductList(productList):
    for product in productList:
        printProduct(product)
        print()
