#1(2)
class Vehicle:
    def start(self):
        print("Vehicle starts!")

class Car(Vehicle):
    def start(self):
        print("Car starts!")

class Bike(Vehicle):
    def start(self):
        print("Bike starts!")

def GoGoGo(vehicle):
    vehicle.start()

car = Car()
bike = Bike()

GoGoGo(car)
GoGoGo(bike)