from thing import Thing

class Character(Thing):

    def __init__(self,attributes):
        self.hp = 10
        self.actions = 1
        self.fight = True
        self.alive = True
        self.abilities = {}
        abilityList = ['strength','stamina','agility','reaction','intelligence','logic','personality','leadership']
        for ability in abilityList:
            self.abilities[ability] = 3
        super().__init__(attributes)
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
        output += "Abilities:\n"
        for ability in self.abilities:
            output += "* " + ability + ": " + str(self.abilities[ability]) + "\n"
        if len(self.skills) > 0:
            output += "Skills:\n"
            for skill in self.skills:
                output += "* " + skill + ": " + str(self.skills[skill]) + "\n"
        return output
