from adventure import Adventure
from termcolor import colored

ad = Adventure('testAdventure.yaml')
print(ad.getQuest())

while ad.running:
    print(ad.getLocalDescription())
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
        ad.quit()
    elif verb == 'g':
        if not thing.goesTo == None:
            ad.goToLocation([thing.goesTo])
    elif verb == 'l':
        if thing:
            print(thing.description)
    elif verb == 'a':
        if thing:
            output = ad.listInteractions(thing)
            print(output)
            if "No" not in output:
                choice = input(colored("Choose an interaction >> ", 'red'))
                print(ad.executeInteraction(thing, choice))
    elif verb == 'f':
        if thing:
            if thing.fight:
                fighting = True
                while fighting:
                    print(ad.attack(ad.player,thing))
                    print(ad.attack(thing,ad.player))
                    print(ad.player.name + " has " + str(ad.player.hp) + "hp left.")
                    if not ad.player.alive:
                        print("You are dead. Welcome to the afterlife.")
                        ad.quit()
                        fighting = False
                    elif not thing.alive:
                        print("You have vanquished your foe. Congrats!")
                        fighting = False
                    else:
                        choice = input(colored("Continue fighting(y/n) >> ",'red'))
                        print(" ")
                        if choice == 'n':
                            print("Phew.")
                            fighting = False
    elif verb == 't':
        if thing:
            print(ad.take(thing.id))
    elif verb == 'p':
        output = ad.listInventory(ad.player)
        print(output)
        if "No" not in output:
            choice = input(colored("Enter ID of thing to put >> ", 'red'))
            try:
                invThingID = int(choice)
            except:
                invThingID = None
            print(ad.putFromInventory(ad.player,invThingID))
    elif verb == 'i':
        print(ad.listInventory(ad.player))
    elif verb == 's':
        if thing:
            print(ad.listStatus(thing))
        else:
            print(ad.listStatus(ad.player))
    elif verb == 'talk':
        if thing:
            prompts = thing.getPrompts()
            if len(prompts) > 0:
                promptIndex = 0
                for promptString in prompts:
                    print(str(promptIndex) + ". " + promptString)
                    promptIndex += 1
                selection = input(colored("choice >> ", 'red'))
                try:
                    selection  = int(selection)
                except:
                    selection = 1024
                if selection < promptIndex:
                    print(ad.talk(thing,selection))
                else:
                    print("That's odd.")
            else:
                print("I'm not sure " + thing.name + " is interested in talking.")


