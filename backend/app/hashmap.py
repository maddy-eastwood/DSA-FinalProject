from enum import Enum
from sympy import nextprime

class Product:
    def __init__(self, ID, calories):
        self.ID = ID
        self.calories = calories


class Status(Enum):
    NeverUsed = 0
    Occupied = 1
    Deleted = 2


# Hash table - Quadratic Probing
class HashTable:
    def __init__(self, loadFactor=0.7):
        self.capacity = 5
        self.loadFactor = loadFactor
        self.table = [0] * self.capacity
        self.status = [Status.NeverUsed] * self.capacity
        self.size = 0

    def has(self, productID) -> bool:
        index = productID % self.capacity
        if self.status[index] == Status.NeverUsed:
            return False
        if self.status[index] == Status.Occupied and self.table[index] == productID:
            return True
        probe = 1
        iterCount = 0
        while self.status[index] != Status.NeverUsed and iterCount < self.capacity:
            # collision
            index = (index + probe*probe) % self.capacity
            probe += 1
            if self.status[index] == Status.Occupied and self.table[index] == productID:
                return True
        return False

    def rehash(self):
        self.capacity *= 2
        self.capacity = nextprime(self.capacity)
        newTable = [0] * self.capacity
        newStatus = [Status.NeverUsed] * self.capacity
        for i in range(0, len(self.status)):
            if self.status[i] == Status.Occupied:
                newIndex = self.table[i] % self.capacity
                probe = 1
                while newStatus[newIndex] == Status.Occupied:
                    newIndex = (newIndex + probe*probe) % self.capacity
                    probe += 1
                newTable[newIndex] = self.table[i]
                newStatus[newIndex] = Status.Occupied
        self.table = newTable
        self.status = newStatus

    def insert(self, productID) -> bool:
        if self.has(productID):
            return False
        # check if rehash is necessary
        currentLF = (self.size + 1) / self.capacity
        if currentLF >= self.loadFactor:
            self.rehash()
        index = productID % self.capacity
        probe = 1
        while self.status[index] == Status.Occupied:
            # collision
            index = (index + probe*probe) % self.capacity
            probe += 1
        self.table[index] = productID
        self.status[index] = Status.Occupied
        self.size += 1
        return True

    def getSize(self) -> int:
        return self.size

    def remove(self, productID) -> bool:
        if not self.has(productID):
            return False
        index = productID % self.capacity
        if self.status[index] == Status.Occupied and self.table[index] == productID:
            self.status[index] = Status.Deleted
            self.table[index] = 0
            self.size -= 1
            return True
        probe = 1
        while self.status[index] != Status.NeverUsed:
            # collision
            index = (index + probe*probe) % self.capacity
            probe += 1
            if self.status[index] == Status.Occupied and self.table[index] == productID:
                self.status[index] = Status.Deleted
                self.table[index] = 0
                self.size -= 1
                return True
