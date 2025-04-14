from enum import Enum
from sympy import nextprime
from app.hashing.quadratic_probing import FoodContainer

# Separate Chaining 
class HashMap:
    def __init__(self):
        self.size = 0
        self.capacity = nextprime(100000)
        self.currentCap = self.capacity
        self.loadFactor = 0.5
        self.hashMap = [
            [] for i in range(self.capacity)
        ]
        self.newMap = None

    #calculates the index where the food object should go in hashmap
    def hashFunction(self, id) -> int:
        return id % self.capacity

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
                    index = HashMap.hashFunction(self, foodObj.ID)
                    self.newMap[index].append(foodObj)  # adding to the inner list
        self.setMap()

    #inserting into the hashmap with separate chaining
    def insert(self, foodObj: FoodContainer)->bool:
        if self.has(foodObj.ID):
            return False
        index = self.hashFunction(foodObj.ID)
        self.hashMap[index].append(foodObj) #adding to the inner list
        self.size += 1
        lf = self.size / self.capacity
        if lf >= self.loadFactor:
            #resize and rehash
            self.rehash()
        return True

    def has(self, id):
        index = self.hashFunction(id)
        for i in range(len(self.hashMap[index])):
            if self.hashMap[index][i].ID == id:
                return self.hashMap[index][i]
        return False
    
    def getSize(self):
        return self.size