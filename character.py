from thing import Thing

class Character(Thing):

    def __init__(self,attributes):
        self.hp = 10
        self.actions = 1
        super().__init__(attributes)
        self.fight = True
        self.alive = True
        self.constructThings()

    def constructThings(self):
        if len(self.inventory) > 0:
            for thingID in self.inventory:
                thing = Thing(self.inventory[thingID])
                self.inventory[thingID] = thing

    def getInventory(self):
        invList = []
        for thingID, thing in self.inventory.items():
            invList.append(thing)
        return invList

    def getStatus(self):
        output = self.name + "'s status\n"
        output += "*********************\n"
        output += "HP: " + str(self.hp) + "\n"
        if len(self.inventory) > 0:
            output += "Inventory:\n"
            for thingID in self.inventory:
                output += "* " + self.inventory[thingID].name + "\n"
        return output
