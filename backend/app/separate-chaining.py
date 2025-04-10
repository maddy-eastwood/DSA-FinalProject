from enum import Enum
from sympy import nextprime

#python time

class Food:
    def __init__(self, ID, description, brand, protein, calories = 0):
        self.ID = ID
        self.description = description
        self.brand = brand
        self.protein = protein
        self.calories = calories
    def __repr__(self):
        return f"ID: {self.ID} : {self.description}, {self.calories} cal, {self.protein}g protein"

    def __str__(self):
        return f"ID: {self.ID} : {self.description}, {self.calories} cal, {self.protein}g protein"



class HashMap:
    def __init__(self):
        self.size = 0
        self.capacity = 10
        self.currentCap = 10
        self.loadFactor = 0.7
        self.hashMap = [
            [] for i in range(self.capacity)
        ]
        self.newMap = None

    #calculates the index where the food object should go in hashmap
    def hashFunction(self, foodObj) -> int:
        return int(foodObj.ID) % self.capacity

    def setMap(self):
        self.currentCap = self.capacity
        self.hashMap = self.newMap

    def rehash(self):
        self.currentCap = self.capacity
        self.capacity *= 2
        self.capacity = nextprime(self.capacity)
        self.newMap = []
        for i in range(self.capacity):
            self.newMap.append([])
        for i in range(self.currentCap):
            if len(self.hashMap[i]) != 0:
                for j in range(len(self.hashMap[i])):
                    foodObj = self.hashMap[i][j]
                    index = HashMap.hashFunction(self, foodObj)
                    self.newMap[index].append(foodObj)  # adding to the inner list
        self.setMap()

    #inserting into the hashmap with separate chaining
    def insert(self, foodObj)->bool:
        if self.has(foodObj):
            return False
        index = self.hashFunction(foodObj)
        self.hashMap[index].append(foodObj) #adding to the inner list
        self.size += 1
        lf = self.size / self.capacity
        if lf >= self.loadFactor:
            #resize and rehash
            self.rehash()
        return True

    def has(self, foodObj):
        for i in range(self.currentCap):
            if len(self.hashMap[i]) != 0:
                for j in range(len(self.hashMap[i])):
                    if self.hashMap[i][j] == foodObj:
                        return True
        return False