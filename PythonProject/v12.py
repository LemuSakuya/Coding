#1(1):
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def discribe_restaurant(self):
        print(f"Restaurant: {self.restaurant_name}, Cuisine:    {self.cuisine_type}")

    def open_restaurant(self):
        print(f"{self.restaurant_name} is now open")

my_restaurant = Restaurant("Geidontei", "Japanese")
my_restaurant.discribe_restaurant()
my_restaurant.open_restaurant()