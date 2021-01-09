from adventure import Adventure
from termcolor import colored

ad = Adventure('testAdventure.yaml')
print(ad.getLocalDescription())

running = True
while running:
    action = input(colored(ad.player.name + " >> ",'red')).split()

    if len(action) == 0:
        verb = ' '
    else:
        verb = action[0]

    noun = None
    thing = None

    if len(action) > 1:
        try:
            noun = int(action[1])
        except:
            noun = None
        if noun in ad.currentNouns:
            thing = ad.currentNouns[noun]
        else:
            print("Um, no.")
            continue

    if verb == 'q':
        running = False
    elif verb == 'g':
        if not thing.goesTo == None:
            ad.goToLocation([thing.goesTo])
            print(ad.getLocalDescription())
    elif verb == 'l':
        if thing:
            print(thing.description)
        else:
            print(ad.getLocalDescription())
    elif verb == 'i':
        if thing:
            print(ad.listInteractions(thing))
            choice = input(colored(ad.player.name + " >> ", 'red'))
            print(ad.executeInteraction(thing, choice))
    elif verb == 't':
        if thing:
            print(ad.take(thing.id))

#     noun = None
#     thing = None
#     if len(action) > 1:
#         noun = action[1].lower()
#     if noun in self.currentLocation.things:
#         thing = self.currentLocation.things[noun]
#     elif noun in self.characters:
#         character = self.characters[noun]
#         if character.location == self.currentLocation.name:
#             thing = character
#     if verb == 'debug':
#         print(self.characters)
#     elif verb == 'l':
#         if not noun:
#             self.fullDescription()
#         elif thing:
#             thing.look()
#     elif verb == 'm':
#         if noun and thing:
#             thing.interact("move",self.player.inventory,self.currentLocation.things)
#     elif verb == 'o':
#         if noun and thing:
#             thing.interact("open",self.player.inventory,self.currentLocation.things)
#     elif verb == 't':
#         if noun and thing:
#             game.take(noun)
#     elif verb == 'p':
#         if noun:
#             game.put(noun)
#     elif verb == 'i':
#         printInventory(self.player)
#     elif verb == 'g':
#         if noun and thing:
#             goTo = thing.go()
#             if goTo:
#                 self.goLocation(goTo)
#                 self.fullDescription()
#     elif verb == 'talk':
#         if thing:
#                 thing.talk()
#     elif verb == 'q':
#         self.running = False
