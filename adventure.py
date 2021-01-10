from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from random import randint
from os.path import isfile
from thing import Thing
from character import Character

class Location:

    def __init__(self, attributes):
        self.things = {}
        self.id = attributes['id']
        self.loadThings(attributes['things'])
        self.description = attributes['description']
        self.name = attributes['name']

    def loadThings(self,things):
        for item in things:
            thing = Thing(item)
            self.things[item['id']]= thing

    def describe(self):
        return "You are in " + self.name.replace("_"," ") + ": " + self.description

class Adventure:

    def __init__(self,path):
        self.running = True
        self.data = self.load(path)
        self.name = self.data["name"]
        self.quest = self.data["quest"]
        self.currentNouns = {}
        self.sectionData = {}
        self.npcs = {}
        self.player = Character(self.data["player"])
        self.loadSections()
        self.loadNPCs()
        self.goToLocation(self.data["start"])

    def getQuest(self):
        output = self.quest
        return output

    def getFileContent(self,fileName):
        fileType = ".yaml"
        fName = fileName + fileType
        if isfile(fName):
            with open (fName,'r') as contentFile:
                rawData =  load(contentFile, Loader=Loader)
                return rawData
        return None

    def getNouns(self):
        nounID = 0
        self.currentNouns = {}
        for thingID in self.currentLocation.things:
            self.currentNouns[nounID] = self.currentLocation.things[thingID]
            nounID += 1
        for npcID in self.npcs:
            npc = self.npcs[npcID]
            if npc.location[0] == self.currentSectionID:
                if npc.location[1] == self.currentLocation.id:
                    self.currentNouns[nounID] = npc
                    nounID += 1

    def loadSections(self):
        for sectionFileName in self.data["sections"]:
            rawSection = self.getFileContent(sectionFileName)
            if rawSection:
                self.sectionData[rawSection['id']] = rawSection

    def loadNPCs(self):
        for npcFileName in self.data["npcs"]:
            rawNPC = self.getFileContent(npcFileName)
            if rawNPC:
                npc = Character(rawNPC)
                self.npcs[rawNPC['id']] = npc

    def loadSection(self, sectionID):
        rawSection = self.sectionData[sectionID]
        self.currentSectionID = sectionID
        self.currentSectionName = rawSection["name"]
        self.currentLocations = {}
        for rawLocation in rawSection["locations"]:
            location = Location(rawLocation)
            self.currentLocations[location.id] = location
        self.currentMap = rawSection['map']

    def goToLocation(self,fullLocationID):
        if len(fullLocationID) == 2:
            self.loadSection(fullLocationID[0])
        self.currentLocation = self.currentLocations[fullLocationID[-1]]
        self.getNouns()

    def getLocalDescription(self):
        self.getNouns()
        description = "You are at " + self.currentLocation.name + ": "
        description += self.currentLocation.description + "\n\n"
        description += "You see: \n**********************************\n"
        for thingID in self.currentNouns:
            if not self.currentNouns[thingID].hidden:
                description += str(thingID) + ": " + self.currentNouns[thingID].name + "\n"
        return description

    def listInteractions(self, thing):
        output = "No interactions available."
        interactions = thing.getInteractions()
        if len(interactions) > 0:
            output = "Choose one: \n\n"
            for interaction in interactions:
                output += "* " + interaction + "\n"
        return output

    def executeInteraction(self, thing, choice):
        output = "You can't do that!"
        if choice in thing.interactions:
            i = thing.interactions[choice]
            if i['interacted']:
                output = "Not again..."
            else:
                if i['requires']:
                    req = i['requires']
                    if req[0] == 'inventory':
                        if not req[1] in self.player.inventory:
                            return i['requiresFail']
                    elif req[0] == 'ability':
                        output = 'Abilities not implemented - requires name of ability and value'
                        return
                    elif req[0] == 'skill':
                        if not req[1] in self.player.skills or self.player.skills[req[1]] < req[2]:
                            return i['requiresFail']
                if i['effects']:
                    for e in i['effects']:
                        ID = e[0]
                        method = e[1]
                        args = e[2]
                        for thingID, thing in self.currentNouns.items():
                            if ID == thing.id:
                                output = i['action']
                                getattr(thing,method)(*args)
                                i['interacted'] = True
        return output

    def take(self,thingID):
        output = "Not here to be taken."
        if thingID in self.currentLocation.things:
            thing = self.currentLocation.things[thingID]
            if not thing.canTake:
                output = "Can't take that."
            else:
                output = thing.name + " taken."
                self.player.inventory[thingID] = thing
                del self.currentLocation.things[thingID]
                self.getNouns()
        return output

    def save(self, path,settings):
        with open(path,'w') as outFile:
            output = dump(settings, Dumper=Dumper)
            outFile.write(output)

    def load(self, path):
        adventure = {}
        if isfile(path):
            with open(path) as yamlFile:
                adventure = load(yamlFile, Loader=Loader)
        return adventure

    def listInventory(self, character):
        output = "Nothing in inventory."
        inventory = character.getInventory()
        if len(inventory) > 0:
            output = character.name + " inventory: \n"
            for thing in inventory:
                output += str(thing.id) + " : " + thing.name + "\n"
        return output

    def putFromID(self,characterID,thingID):
        output = "Who am I anyway?"
        if characterID in self.npcs:
            character = self.npcs[characterID]
            output = self.putFromInventory(character,thingID)
        return output

    def putFromInventory(self,character,thingID):
        output = "You don't have that."
        if thingID in character.inventory:
            thing = character.inventory[thingID]
            self.currentLocation.things[thingID] = thing
            del character.inventory[thingID]
            output = "You put down the " + thing.name + "."
        return output

    def listStatus(self,thing):
        return thing.getStatus()

    def addTalkPrompt(self,characterID,prompt,response,effects):
        if characterID in self.npcs:
            character = self.npcs[characterID]
            character.setTalkPrompt(prompt,response,effects)

    def talk(self, thing, selection):
        prompt = thing.getPrompt(selection)
        output = prompt['response']
        if 'effects' in prompt:
            for e in prompt['effects']:
                method = e[0]
                args = e[1]
                getattr(self,method)(*args)
        thing.removePrompt(selection)
        return output

    def attack(self,attacker,defender):
        defender.name + " doesn't seem interested in fighting."
        if defender.fight:
            actions = attacker.actions
            damage = 0
            output = ""
            if actions > 0:
                canAct = True
            while canAct:
                didSomething = False
                for thingID in attacker.inventory:
                    thing = attacker.inventory[thingID]
                    if thing.isAttack:
                        if thing.actionCost <= actions:
                            didSomething = True
                            attackRoll = randint(1, 10)
                            actions -= thing.actionCost
                            output += attacker.name + " attacks with " + thing.name + ". "
                            if attackRoll >= thing.toHit:
                                if len(thing.damage) == 1:
                                    damageRoll = thing.damage[0]
                                else:
                                    damageRoll = randint(thing.damage[0],thing.damage[1])
                                damage += damageRoll
                                output += thing.name + " causes " + str(damageRoll) + " damage.\n"
                            else:
                                output += thing.name + " misses.\n"
                if not didSomething or actions == 0:
                    canAct = False
            defender.hp -= damage
            if defender.hp <= 0:
                defender.alive = False
        return output

    def quit(self):
        self.running = False

