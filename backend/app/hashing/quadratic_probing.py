from enum import Enum
from sympy import nextprime

class FoodContainer:
    def __init__(self, ID, description, calories, protein, sugar, brand):
        self.ID: int = ID
        self.description: str = description
        self.calories: float = calories
        self.protein: float = protein
        self.sugar: float = sugar
        self.brand: str = brand

    def __repr__(self):
        return f"ID: {self.ID} : {self.description}, {self.calories} cal, {self.protein}g protein"

    def __str__(self):
        return f"ID: {self.ID} : {self.description}, {self.calories} cal, {self.protein}g protein"

class Status(Enum):
    NeverUsed = 0
    Occupied = 1
    Deleted = 2

# Hash table - Quadratic Probing
class HashTable:
    def __init__(self, loadFactor=0.5):
        self.capacity = nextprime(100000)
        self.loadFactor = loadFactor
        self.table: list[FoodContainer | None] = [None] * self.capacity
        self.status = [Status.NeverUsed] * self.capacity
        self.size = 0
        self.numCollisions = 0
        self.totalCollisions = 0

    def __str__(self):
        result = ""
        for i in range (len(self.table)):
            result += "index: " + str(i)
            if self.table[i] is not None:
                result += ", " + str(self.table[i].ID)
            else:
                result += ", None"
            result += '\n'
        return result

    def getCapacity(self):
        return self.capacity

    def getTotalCollisions(self):
        return self.totalCollisions

    def getCollisions(self):
        return self.numCollisions

    def has(self, productID):
        og_index = productID % self.capacity
        index = og_index
        if self.status[index] == Status.NeverUsed:
            return False
        if self.status[index] == Status.Occupied:
            if self.table[index].ID == productID:
                return self.table[index]
        # begin probing
        probe = 1
        while self.status[index] != Status.NeverUsed:
            # keep searching until we come across a spot that's never been used
            index = (og_index + probe*probe) % self.capacity
            probe += 1
            if self.status[index] == Status.Occupied and self.table[index].ID == productID:
                return self.table[index]
            if index == og_index:
                # we probed all spots in the table and did not find productID
                # => productID is not in the table
                break
        return False

    def rehash(self):
        self.capacity *= 2
        self.capacity = nextprime(self.capacity)
        newTable: list[FoodContainer | None] = [None] * self.capacity
        newStatus = [Status.NeverUsed] * self.capacity
        # iterate through old hash table and find occupied spots to rehash into the new table
        for i in range(0, len(self.status)):
            if self.status[i] == Status.Occupied:
                # rehash self.table[i] into new table
                og_newIndex = self.table[i].ID % self.capacity
                newIndex = og_newIndex
                probe = 1
                while newStatus[newIndex] == Status.Occupied:
                    # collision
                    newIndex = (og_newIndex + probe*probe) % self.capacity
                    probe += 1
                newTable[newIndex] = self.table[i]
                newStatus[newIndex] = Status.Occupied
        self.table = newTable
        self.status = newStatus

    def insert(self, productID :int, food: FoodContainer) -> bool:
        if self.has(productID):
            # no duplicates allowed
            return False
        og_index = productID % self.capacity
        index = og_index
        probe = 1
        count = 0
        collision = False
        while self.status[index] == Status.Occupied:
            # collision
            self.totalCollisions += 1
            collision = True
            index = (og_index + probe*probe) % self.capacity
            probe += 1
            count += 1
            # print(f"collision count={count}, new index ={index}")
            if index == og_index:
                # probed through the whole table & couldn't find available spot => rehash
                # this avoids rare case of falling into infinite probing loop
                self.rehash()
                return self.insert(productID, food)
        if collision == True:
            self.numCollisions += 1
        # insert at calculated index
        self.table[index] = food
        self.status[index] = Status.Occupied
        self.size += 1

        # check if rehash is necessary
        lf = self.size / self.capacity
        if lf >= self.loadFactor:
            self.rehash()
        return True

    def getSize(self) -> int:
        return self.size

    def remove(self, productID) -> bool:
        if not self.has(productID):
            # productID not in table
            return False
        og_index = productID % self.capacity
        index = og_index
        if self.status[index] == Status.Occupied and self.table[index].ID == productID:
            self.status[index] = Status.Deleted
            self.table[index] = None
            self.size -= 1
            return True
        probe = 1
        while self.status[index] != Status.NeverUsed:
            # keep searching until we come across a spot that's never been used or we checked the whole table
            index = (og_index + probe*probe) % self.capacity
            probe += 1
            if self.status[index] == Status.Occupied and self.table[index] == productID:
                self.status[index] = Status.Deleted
                self.table[index] = None
                self.size -= 1
                return True
            if index == og_index:
                # not found in table
                break
        return False
