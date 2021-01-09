from thing import Thing

class Character(Thing):

    def __init__(self,attributes):
        self.inventory = {}
#        self.name = attributes['name']
#        self.id = attributes['id']
#        self.description = attributes['description']
#        self.location = attributes['location']
#        if 'attacks' in attributes:
#            self.attacks = attributes['attacks']
        super().__init__(attributes)