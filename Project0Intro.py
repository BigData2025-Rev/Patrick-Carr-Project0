import os
from Project0Init import Init
import json

locat = Init()

class Intro:

    def __init__(self):
        test = 0

    def title(self):
        print("Welcome to Project Zero!")
        print("Progress is saved automatically to json files")
        loop = True
        while loop:
            act = input("[N] for New Game, [L] for Load Game, & [Q] to exit")
            if act == "Q":
                exit(0)
                loop = False
            if act == "N":
                saveNum = self.newGame()
                return saveNum
            if act == "L":
                saveNum = self.loadGame()
                if saveNum == -1 or saveNum == 0:
                    continue
                else:
                    return saveNum
            if act not in "QNL" or len(act)!=1:
                print("Invalid Input")
        return act
    
    def loadGame(self):
        savesNum = self.numberOfSaves()
        saveNum = 0
        while True:
            if savesNum == 0:
                print("No saves found")
                return 0
            else:
                for r, dirs, f in os.walk("Saves\\"):
                    dir = dirs
                    break
                #print(dir)
                act = input(f"[Q] to return to title or input one of the following save names:{dir}")
                
                if act == "Q":
                    return -1
                
                validInput = False
                for element in dir:
                    if act == element:
                        validInput = True
                        break
                if validInput:
                    print(f"You are using save {act}")
                    return act
                else:
                    print("Invalid save name")
                    continue
                

    def numberOfSaves(self):
        #Check if the saves directory exists, if not make it
        if not os.path.exists("Saves\\"):
            os.mkdir("Saves")
        #dir = os.listdir("Saves\\")
        #dir = os.walk().next()[1]
        dir = 0
        for r, dirs, f in os.walk("Saves\\"):
            dir = dirs.__len__()
            break
        #print(dir)
        folderNum = dir
        # folderNum = 0
        # for element in dir:
        #     if os.path.isdir(element):
        #         folderNum += 1
        return folderNum


    def newGame(self):
        savesNum = self.numberOfSaves()
        #sav = savesNum + 1
        sav = 1
        loc = locat.initLoc()
        #print(loc)
        #locJ = json.dumps(loc, indent=4)

        #Create save folder named the next available number
        while os.path.exists(f"Saves\{sav}"):
            sav +=1
        os.mkdir(f"Saves\{sav}")

        #Initialize the jsons
        with open(f"Saves\{sav}\Locations.json","w") as locJson:
            #locJson.write("test")
            json.dump(loc,locJson,indent=4)

        prog = locat.initProg()
        with open(f"Saves\{sav}\Progress.json","w") as Json:
            json.dump(prog,Json,indent=4)

        player = locat.initPlayer()
        with open(f"Saves\{sav}\Player.json","w") as Json:
            json.dump(player,Json,indent=4)    

        enemies = locat.initEnemies()
        with open(f"Saves\{sav}\Enemies.json","w") as Json:
            json.dump(enemies,Json,indent=4) 
        
        comms = locat.initCommands()
        with open(f"Saves\{sav}\Commands.json","w") as Json:
            json.dump(comms,Json,indent=4) 
        
        print(f"Save {sav} was created")
        return sav

    # def newGame(self):
    #     loc = locat.initLoc()
    #     print(loc)
        
        
    #     with open("Locations.json","w") as locJson:
    #         locJson.write("test")
    #         #json.dump(loc,locJson,indent=4)

    #     return 1

        
