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
        self.talkPrompts = {}
        self.responses = []
        self.inventory = {}
        self.interactions = {}
        for key in attributes:
            setattr(self,key,attributes[key])
        if not self.name or not self.description:
            print("name and description attributes must be set.")
            print(attributes)
        self.promptList = []

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
        self.talkPrompts[prompt] = {}
        self.talkPrompts[prompt]['response']=response
        self.talkPrompts[prompt]['effects']=effects

    def getPrompts(self):
        self.promptList = []
        for prompt in self.talkPrompts:
            self.promptList.append(prompt)
        return self.promptList

    def getPromptResponse(self,selection):
        prompt = self.promptList[selection]
        return self.talkPrompts[prompt]

    def removePrompt(self,selection):
        prompt = self.promptList[selection]
        del self.talkPrompts[prompt]
        self.getPrompts()

    def getStatus(self):
        return "Nothing much to report here."

