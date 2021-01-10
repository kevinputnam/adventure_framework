class Thing:

    def __init__(self,attributes):
        self.name = None
        self.hidden = False
        self.description = None
        self.canTake = False
        self.locks = False
        self.goesTo = None
        self.isAttack = False
        self.fight = False
        self.talkPrompts = []
        self.responses = []
        self.inventory = {}
        self.interactions = {}
        for key in attributes:
            setattr(self,key,attributes[key])
        if not self.name or not self.description:
            print("name and description attributes must be set.")
            print(attributes)

    def set(self, attrName, attrValue):
        setattr(self,attrName,attrValue)

    def look(self):
        print(self.description)

    def getInteractions(self):
        if not self.hidden:
            return self.interactions
        else:
            return {}

    def setTalkPrompt(self,prompt,response,effects):
        tPrompt = {'prompt':prompt,'response':response,'effects':effects}
        self.talkPrompts.append(tPrompt)

    def getPrompts(self):
        promptList = []
        for item in self.talkPrompts:
            promptList.append(item['prompt'])
        return promptList

    def getPrompt(self,selection):
        return self.talkPrompts[selection]

    def removePrompt(self,selection):
        del self.talkPrompts[selection]

    def getStatus(self):
        return "Nothing much to report here."

