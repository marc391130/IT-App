class Order:
    def __init__(self, name, price, stars):
        self.name = name
        self.price = price
        self.stars = stars

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getStars(self):
        return self.stars

    def setName(self, name):
        self.name = name

    def setPrice(self, price):
        self.price = price

    def setStars(self, stars):
        self.stars = stars