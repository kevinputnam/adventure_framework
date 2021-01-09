from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

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
        self.data = self.load(path)
        self.name = self.data["name"]
        self.quest = self.data["quest"]
        self.currentNouns = {}
        self.sectionData = {}
        self.npcs = {}
        self.player = Character({'name':'Kevin','description':'Looking for the end of the circle.','location':self.data['start'],'id':0})
        self.loadSections()
        self.loadNPCs()
        self.goToLocation(self.data["start"])

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
        if len(interactions) >= 1:
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
                            print(i['requiresFail'])
                            return
                    elif req[0] == 'ability':
                        print('Abilities not implemented - requires name of ability and value')
                    elif req[0] == 'skill':
                        print('Skills not implemented - requires name of skill and value')
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

    def put(self, thingID): #TODO
        if thingID in self.player.inventory:
            thing = self.player.inventory[thingID]
            self.currentLocation.things[thingID] = thing
            del self.player.inventory[thingID]
            print("I put down the " + thing.name + ".")
        else:
            print("I don't have that.")

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

# NOT CURRENTLY IN USE

    def changeLocation(self, choice):
        newSection = False
        self.previousLocationName = self.currentLocationName
        nextLocation = self.currentSection["locations"][choice]
        if "section" in nextLocation:
            newSection = True
            self.loadSection(nextLocation["section"])
        else:
            self.currentLocation = self.currentSection["locations"][choice]
            self.currentLocationName = choice
        return newSection

        for sectionFileName in self.data["sections"]:
            fileName = sectionFileName + fileType
            if isfile(fileName):
                with open (fileName,'r') as sectionFile:
                    rawSection =  load(sectionFile, Loader=Loader)
                    self.sectionData[section['id']]=rawSection

    def getChoices(self):
        return self.currentLocation["goto"]

    def getEncounters(self):
        encounters = []
        if "encounters" in self.currentLocation:
            for key, encounter in self.currentLocation["encounters"].items():
                if encounter["resolved"] == "":
                    encounters.append(key)
        return encounters
