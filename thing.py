class Thing:

    def __init__(self,attributes):
        self.name = None
        self.hidden = False
        self.description = None
        self.canTake = False
        self.locks = False
        self.goesTo = None
        self.prompts = []
        self.responses = []
        self.inventory = {}
        self.interactions = {}
        for key in attributes:
            setattr(self,key,attributes[key])
        if not self.name or not self.description:
            print("name and description attributes must be set.")
            print(attributes)

    def talk(self):
        if len(self.prompts) > 0:
            promptIndex = 1
            for prompt in self.prompts:
                print(str(promptIndex) + ". " + prompt)
                promptIndex += 1
            selection = input("choice >> ")
            try:
                selection  = int(selection) - 1
            except:
                selection = 1024
            if selection < len(self.responses):
                print(self.responses[int(selection)])
                del self.prompts[selection]
                del self.responses[selection]
            else:
                print("That's odd.")
        else:
            print("I'm not sure " + self.name + " is interested in talking.")

    def set(self, attrName, attrValue):
        setattr(self,attrName,attrValue)

    def look(self):
        print(self.description)

    def getInteractions(self):
        if not self.hidden:
            return self.interactions
        else:
            return {}

    def interact(self, interaction, inventory, things):
        if interaction in self.interactions:
            i = self.interactions[interaction]
        else:
            print("I'd rather not.")
            return
        if i['interacted']:
            print("Not again...")
        else:
            if i['requires']:
                req = i['requires']
                if req[0] == 'inventory':
                    if not req[1] in inventory:
                        print(i['requiresFail'])
                        return
                elif req[0] == 'ability':
                    print('Abilities not implemented - requires name of ability and value')
                elif req[0] == 'skill':
                    print('Skills not implemented - requires name of skill and value')
            if i['effects']:
                for e in i['effects']:
                    name = e[0]
                    method = e[1]
                    args = e[2]
                    if name in things:
                        print(i['action'])
                        getattr(things[name],method)(*args)
                        print(i['description'])
                        i['interacted'] = True

