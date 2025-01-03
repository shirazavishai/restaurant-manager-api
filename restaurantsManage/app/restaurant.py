class Restaurant:
    def __init__(self):
        self.name = name
        self.address = address
        self.style = style
        self.vegetarian = vegetarian
        self.open_hour = open_hour
        self.close_hour = close_hour
        self.delivery = delivery

    def __str__(self):
        return f"{self.name} - {self.address} - {self.style} - {self.vegetarian} - {self.open_hour} - {self.close_hour} - {self.delivery}"

    def is_open(self, hour):
        return self.open_hour <= hour <= self.close_hour
    
    def is_vegetarian(self):
        return self.vegetarian
    
    def is_delivery(self):
        return self.delivery

