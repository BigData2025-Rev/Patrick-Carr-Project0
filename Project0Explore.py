"""
Manages exploration, where the player can move between rooms in the Locations.json.
Their current location is updated in the Progress.json
"""
import json
from Project0Battle import Battle

class Explore:

    sav = 0
    bat = Battle()
    def __init__(self):
        test = 0

    # def startExplore(self,savNum):
    #     sav = savNum
    #     with open(f"Saves\{sav}\Locations.json","r") as locJson:
    #         locJ = json.load(locJson)
    #         print(locJ)

    def startExplore(self,savNum):
        sav = savNum
        with open(f"Saves\{sav}\Locations.json","r") as locJson:
            locJ = json.load(locJson)
            #print(locJ)
        return locJ

    #Runs the room exploration loop
    #Returning 0 means the player quit out, return -1 means a gameover
    def explore(self, loc, sav):
        #print(loc.type)
        while True:
            with open(f"Saves\{sav}\Progress.json","r") as Json:
                prog = json.load(Json)
            pLoc = prog.get("playerLoc")
            print(loc[pLoc]["desc"])
            #if loc[pLoc]["enemy"] != 0:
            if pLoc not in prog or prog[pLoc]["enemy"] != 0: 
                dirStr = ""
                for direction in loc[pLoc]["conn"]:
                    dirStr += "[" + direction + "], "
                dirStr = dirStr[:len(dirStr)-2] # remove the last ", "
                act = input("You can move in the following direction(s):" + dirStr +" or [D]isplay stats or [Q]uit to title")
                act = act.upper()
                
                #When Q is input, return to Project0Core which loops back to the titlescreen
                if act == "Q":
                    return 0
                elif act == "D":
                    with open(f"Saves\{sav}\Player.json","r") as Json:
                        player = json.load(Json)
                    for play in prog["party"]:
                        try:
                            dataStr = str(player[play]["name"]) + " HP:" + str(player[play]["hp"]) + "/" + str(player[play]["mhp"]) + " MP:" + str(player[play]["mp"]) + "/" + str(player[play]["mmp"])
                            dataStr += str(player[play]["lvl"]) + str(player[play]["exp"]) + str(player[play]["str"]) + str(player[play]["def"]) + str(player[play]["mag"]) + str(player[play]["res"])             
                            print(dataStr)
                        except:
                            pStr = str(play)
                            dataStr = str(player[pStr]["name"]) + " HP:" + str(player[pStr]["hp"]) + "/" + str(player[pStr]["mhp"]) + " MP:" + str(player[pStr]["mp"]) + "/" + str(player[pStr]["mmp"])
                            dataStr += " Lvl:" +  str(player[pStr]["lvl"]) + " Exp:" + str(player[pStr]["exp"]) + " Str:" + str(player[pStr]["str"])
                            dataStr += " Def:" + str(player[pStr]["def"]) + " Mag:" + str(player[pStr]["mag"]) + " Res:" + str(player[pStr]["res"])             
                            print(dataStr)
                #Check that a valid direction was inputed
                elif act in loc[pLoc]["conn"]:
                    #Alter the player position by turning the string into a list of ints
                    #then back to string to modify Progress.json
                    posList = pLoc.split(',')
                    posNums = [int(posList[0]),int(posList[1])]
                    if act == "N":
                        posNums[1] += 1
                    elif act == "S":
                        posNums[1] -= 1
                    elif act == "E":
                        posNums[0] += 1
                    elif act == "W":
                        posNums[0] -= 1
                    
                    #If the next room has enemies, wait to save the new location unless
                    # the battle is won, so they load in the old location if they lose
                    pLoc = f"{posNums[0]},{posNums[1]}"
                    if loc[pLoc]["enemy"] != 0: 
                        prog["prevLoc"] = prog["playerLoc"]
                        prog["playerLoc"] = pLoc
                        with open(f"Saves\{sav}\Progress.json","w") as Json:
                            json.dump(prog,Json,indent=4)  
                else:
                    print("Invalid Input")
                #while True:
                #    print(loc[pLoc])
            else:
                #0=battle lost, 1=battle won
                #Get the current party from progress.json and turn the string into a list of keys to battleStart, 
                # which it can use to reference Player.json
                #players = prog["party"].split(',')
                #[int(element) for element in players]
                #print(prog[pLoc]["enemy"])
                print("You encountered enemies!")
                #print(loc[pLoc]["enemy"])
                result = self.bat.battleStart(sav,loc[pLoc]["enemy"],prog["party"])
                if result == 1: #A result of 1 means the player won

                    print("You won!")
                    prog[pLoc]["enemy"] = 1 #Set the enemy encounter for the current room to won so it won't trigger again
                    with open(f"Saves\{sav}\Progress.json","w") as Json: #Save the victory to the json
                        json.dump(prog,Json,indent=4)

                    #save the player's new location
                    prog["prevLoc"] = prog["playerLoc"]
                    prog["playerLoc"] = pLoc
                    with open(f"Saves\{sav}\Progress.json","w") as Json:
                        json.dump(prog,Json,indent=4)  

                else: #If the result was not one, the player lost and gets sent to the title screen
                    print("You lost!")
                    return -1