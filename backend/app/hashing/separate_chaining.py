from enum import Enum
from sympy import nextprime
from app.hashing.quadratic_probing import FoodContainer

# Separate Chaining 
class HashMap:
    def __init__(self):
        self.size = 0
        self.capacity = nextprime(100000)
        self.currentCap = self.capacity
        self.loadFactor = 0.7
        self.hashMap = [
            [] for i in range(self.capacity)
        ]
        self.newMap = None

    #calculates the index where the food object should go in hashmap
    def hashFunction(self, foodObj) -> int:
        return foodObj.ID % self.capacity

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
    def insert(self, foodObj: FoodContainer)->bool:
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

    # def has(self, foodObj):
    #     for i in range(self.currentCap):
    #         if len(self.hashMap[i]) != 0:
    #             for j in range(len(self.hashMap[i])):
    #                 if self.hashMap[i][j] == foodObj:
    #                     return True
    #     return False

    def has(self, foodObj):
        index = self.hashFunction(foodObj)
        for i in range(len(self.hashMap[index])):
            if self.hashMap[index][i].ID == foodObj.ID:
                return foodObj
        return False
    
    def getSize(self):
        return self.size