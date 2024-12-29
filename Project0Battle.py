import json
import random
import math

class Battle:
    def __init__(self):
        test = 0

    #E is a list of enemy names
    def battleStart(self, sav, enemies, players):
        with open(f"Saves\{sav}\Enemies.json","r") as Json:
            enemy = json.load(Json)

        index = 0
        E = [] #Will contain the data for the enemies used in the battle
        #Use the enemy list receive from the current location to look up
        #their data in Enemies.json and load them into a list
        while index < len(enemies):
            #print(enemies)
            try: #Make a shallow copy so multiples of the same enemy won't share hp
                E.append(enemy[enemies[index]].copy())
            except:
                E.append(enemy[enemies[str(index)]].copy())
            #E.append(enemy[enemies[999999]])
            index += 1
        
        
        with open(f"Saves\{sav}\Player.json","r") as Json:
            player = json.load(Json)
        eNum = len(enemies)
        pNum = len(player)

        index = 0
        P = [] #Will contain the data for the players used in the battle

        #players is the list of keys for the players currently in the party
        #player is a dict holding the player data
        #p is a list of dicts
        # while index < len(players):
        #     P.append(player[str(players[index])])
        

        for play in players:
            pStr = str(play)
            P.append(player[pStr])
        E, P, result = self.battleControl(sav, E, P) 


        #If battle was won, update player json
        #The dict for index 0 of P corresponds to the key at players index 0
        #This is a bit convoluted and could be streamlined later
        if result == 1:
            index = 0
            while index < len(P):
                #P.append(player[players[index]])
                player[players[index]] = P[index]
                index += 1
            with open(f"Saves\{sav}\Player.json","w") as Json:
                json.dump(player,Json,indent=4)                           
        return result

    #Returns 0 if the battle is lost and 1 if the battle is won
    #E is the list of enemies, P is the list of players
    #***Battlers should always have at least one command that can always be used to prevent softlocks***
    #Due to this, be careful about addiing an effect that disables the attack command.
    def battleControl(self, sav, E, P):
        with open(f"Saves\{sav}\Commands.json","r") as Json:
            comms = json.load(Json)

        with open(f"Saves\{sav}\Commands.json","w") as Json:
            json.dump(comms,Json,indent=4) 

        with open(f"Saves\{sav}\Progress.json","r") as Json:
            prog = json.load(Json)
        pLen = len(P)
        eLen = len(E)
        index = 0
        resultNum = 1
        while True:
            index = 0
            while index < pLen:
                if P[index]["hp"] > 0:#Player can only act if they have positive hp
                    E, P, result = self.playerTurn(sav, E, P, index, comms)
                    if result == 0: #If an enemy was defeated, check for a victory
                        if self.defeatCheck(E):
                            P = self.expFunction(E, P)
                            return E, P, 1
                    if result == 1: #If a player was defeated, check for a gameover
                        if self.defeatCheck(P):
                            return E, P, 0
                index += 1
            #print("Player Turn Done")
            index = 0
            while index < eLen:
                #print("Enemy hp check")
                #print("Enemy hp=" + str(E[index]["hp"]))
                if E[index]["hp"] > 0:
                    #print("Turn Starting")
                    E, P, result = self.enemyTurn(sav, E, P, index, comms)
                    if result == 0: #If an enemy was defeated, check for a victory
                        if self.defeatCheck(E):
                            P = self.expFunction(E, P)
                            return E, P, 1
                    if result == 1: #If a player was defeated, check for a gameover
                        if self.defeatCheck(P):
                            return E, P, 0                         
                index += 1
            #print("Enemy Turn Done")
        P = self.expFunction(E, P)
        return E, P, resultNum

    def expFunction(self, E, P):
        exp = 0
        for enemy in E:#Add up the exp of each enemy
            exp += enemy["exp"]
        for player in P:#Give the player exp and check if they have enough to level up
            player["exp"] += exp
            if player["exp"] >= 10*player["lvl"] and player["lvl"] < 99:
                player["exp"] -= 10*player["lvl"]
                player["lvl"] += 1
                print(player["name"] + " leveled up to level " + str(player["lvl"]) + "!")
                hpRatio = player["hp"]/player["mhp"]
                mpRatio = player["mp"]/player["mmp"]

                #Update the player stats based on their level as well as the level 1 original "o" stats and the 
                #level 99 final "f" stats
                player["mhp"] = round((player["fmhp"] - player["omhp"]) * ((player["lvl"]-1)/98) + player["omhp"])
                player["mmp"] = round((player["fmmp"] - player["ommp"]) * ((player["lvl"]-1)/98) + player["ommp"])
                player["str"] = round((player["fstr"] - player["ostr"]) * ((player["lvl"]-1)/98) + player["ostr"])
                player["def"] = round((player["fdef"] - player["odef"]) * ((player["lvl"]-1)/98) + player["odef"])
                player["mag"] = round((player["fmag"] - player["omag"]) * ((player["lvl"]-1)/98) + player["omag"])
                player["res"] = round((player["fres"] - player["ores"]) * ((player["lvl"]-1)/98) + player["ores"])

                #Maintain the same hp and mp ratios as before the levelup, rounding up to avoid rounding down to zero
                player["hp"] = math.ceil(player["mhp"]*hpRatio)
                player["mp"] = math.ceil(player["mmp"]*hpRatio)
        return P

    #Return number 0: enemy was defeated, 1: player was defeated, 2: default
    def playerTurn(self, sav, E, P, index, comms):
        dataStr = ""
        result = 2
        for play in P:
            dataStr = dataStr + str(play["name"]) + " HP:" + str(play["hp"]) + "/" + str(play["mhp"]) + " MP:" + str(play["mp"]) + "/" + str(play["mmp"])              
        print(dataStr)
        result = self.selectCommand(sav,E,P,index,comms)
            
        return E, P, result

    #Return number 0: enemy was defeated, 1: player was defeated, 2: default
    def enemyTurn(self, sav, E, P, index, comms):
            result = 2
            while True:               
                commList = E[index]["commands"].split(",")
                act = commList[random.randint(0,len(commList)-1)] #The enemy selects a random command
                E, P, res = self.executeCommand(act, E, P, 0, index, comms)
                if res != -1: #res is -1, then the enemy had no valid selection
                    result = res
                    break #exit while loop since a valid command was used
            return E, P, result

    def selectCommand(self, sav, E, P, index, comms):
        result = 2
        commList = P[index]["commands"].split(",")
        mainList = [] #List of main commands that don't go in the spell menu
        mainStr = ""
        spellStr = ""
        spellList = [] #List of commands that go in the spell menu
        spells = False
        i = 0
        for element in commList:
            if spells == False:
                mainList.append(commList[i])
                mainStr = mainStr + "[" + element + "]" + " for " + comms[element]["name"] + ", "
            else:
                spellList.append(commList[i])
                spellStr = spellStr + "[" + element + "]" + " for " + comms[element]["name"] + " (" + str(comms[element]["cost"]) + " MP, " + str(comms[element]["power"]) + " Pwr" +"), "

            if element == "S": #Commands after S go in the spell select menu
                spells = True
            i += 1
        if len(mainStr) > 1:
            mainStr = mainStr[:len(mainStr)-2]
        if len(spellStr) > 1:
            spellStr = spellStr[:len(spellStr)-2]
         #Get rid of the final ", "
        while True:
            result = 2
            act = input(P[index]["name"] + " can use " + mainStr)
            act = act.upper()
            skip = False
            if act in mainList: #Check if a valid command was inputted
                if act == "S":#Display and recieve input for the spell menu
                    while True:
                        actS = input(P[index]["name"] + " can cast " + spellStr + " or [Q]uit back")
                        actS = actS.upper()
                        if actS == "Q":
                            skip = True
                            break
                        if actS in spellList: #Check if a valid spell was inputted
                            if comms[actS]["cost"] > P[index]["mp"]:#Check if the user has enough mp to cast the spell
                                print("Not enough MP")
                                continue
                            act = actS #The inputted spell is valid, so set is as the player's action
                            break
                        else: #No valid spell command was inputted
                            print("Invalid Spell")
                            continue                             
                if skip: #if skip is set to true, do not executeCommand and do the loop again
                    continue
                E, P, res  = self.executeCommand(act, E, P, 1, index, comms)
                if res != -1: #res is -1, then the player backed out of selection or there were no valid targets
                    result = res                          
                    break #exit while loop since a valid command was used
            else:
                print("Invalid Command")
        return result

    #userParty of 0 means an enemy is acting, 1 means a player is acting
    #If the returned number is -1 the command was canceled, 0: enemy was defeated, 1: player was defeated, 2: standard
    def executeCommand(self, act, E, P, userParty, userIndex, comms):
        #Check if the user is a player to get targetting input
        result = 2
        result, validIndexes = self.buildTargeting(E, P, userParty, userIndex, comms[act]["target"],comms[act]["formula"])
        if len(validIndexes) < 1:
            print("No valid targets")
            result = -1
            return E, P, result
        if comms[act]["range"] == "single":
            #if comms[act]["target"] == "enemy":           
            targetList = []
            if userParty == 1:
                while True:
                    act2 = input("Select a target: " + result + " or [Q]uit back")
                    act2 = act2.upper()
                    if act2 == "Q":
                        result = -1
                        return E, P, result
                    #print("act2=" + act2)
                    #print(validIndexes)
                    if act2 in validIndexes:
                        targetList.append(act2)
                        break #valid target selected, exit targetting loop
                    else: 
                        print("Invalid Target")
                #userParty, targetParty = executeDamage()
                if comms[act]["target"] == "allyHeal" or comms[act]["target"] == "ally":
                    P, P, defeat = self.executeDamage(act, P, P, userIndex, comms, targetList)
                else:
                    P, E, defeat = self.executeDamage(act, P, E, userIndex, comms, targetList)
                if defeat:#Set result to 0 if the command defeated an enemy to check for a victory
                    result = 0
            if userParty == 0: #Enemy randomly selects a target
                targetList.append(random.randint(0,len(validIndexes)-1))
                if comms[act]["target"] == "allyHeal" or comms[act]["target"] == "ally":
                    E, E, defeat = self.executeDamage(act, P, P, userIndex, comms, targetList)
                else:
                    E, P, defeat = self.executeDamage(act, E, P, userIndex, comms, targetList)
                if defeat:#Set result to one if the command defeated a player to check for a gameover
                    result = 1
        elif comms[act]["range"] == "two":       
            targetList = []
            if userParty == 1:
                tNum = 0
                while tNum < 2 and len(validIndexes) > 0:
                    act2 = input("Select a target: " + result + " or [Q]uit back")
                    act2 = act2.upper()
                    if act2 == "Q":
                        result = -1
                        return E, P, result

                    if act2 in validIndexes:
                        targetList.append(act2)
                        validIndexes.remove(act2)#Two targetting cannot hit the same target twice
                        tNum += 1 #valid target selected, increase the total number of selected targets
                        if tNum < 2:
                            result = "" #Rebuild the list of targets without the previously chosen target
                            index = 0
                            while index < len(validIndexes):
                                validIndexNum = int(validIndexes[index])
                                if E[validIndexNum]["hp"] > 0:
                                    result += "[" + validIndexes[index] + "]" + " for " + E[validIndexNum]["name"] + ", "
                                index += 1
                            if len(result) > 1:
                                result = result[:len(result)-2] #Get rid of the final ", "

                    else: 
                        print("Invalid Target")

                if comms[act]["target"] == "allyHeal" or comms[act]["target"] == "ally":
                    P, P, defeat = self.executeDamage(act, P, P, userIndex, comms, targetList)
                else:
                    P, E, defeat = self.executeDamage(act, P, E, userIndex, comms, targetList)
                if defeat:#Set result to 0 if the command defeated an enemy to check for a victory
                    result = 0
            if userParty == 0: #Enemy randomly selects a target
                targetList.append(random.randint(0,len(validIndexes)-1))
                if comms[act]["target"] == "allyHeal" or comms[act]["target"] == "ally":
                    E, E, defeat = self.executeDamage(act, P, P, userIndex, comms, targetList)
                else:
                    E, P, defeat = self.executeDamage(act, E, P, userIndex, comms, targetList)
                if defeat:#Set result to one if the command defeated a player to check for a gameover
                    result = 1
            
        return E, P, result

    #targetList is the list of the target's indexes in the T list
    #targetParty 1 means the player party is target, 0 means the enemy party is targetted
    #U is the userParty list, T is the targetParty list
    def executeDamage(self, act, U, T, userIndex, comms, targetList):
        defeat = False
        U[userIndex]["mp"] -= comms[act]["cost"] #Subtract the cost from the player's mp
        print(U[userIndex]["name"] + " used " + comms[act]["name"])
        for targetIndexStr in targetList:

            targetIndex = int(targetIndexStr)
            if comms[act]["formula"] == "phys":
                damage = U[userIndex]["str"] + comms[act]["power"] - T[targetIndex]["def"]
                print(U[userIndex]["name"] + " delt " + str(damage) + " damage to " + T[targetIndex]["name"])
            elif comms[act]["formula"] == "mag":
                damage = U[userIndex]["mag"] + comms[act]["power"] - T[targetIndex]["res"]
                print(U[userIndex]["name"] + " delt " + str(damage) + " damage to " + T[targetIndex]["name"])
            elif comms[act]["formula"] == "magHeal":
                damage = (U[userIndex]["mag"] + comms[act]["power"])
                print(T[targetIndex]["name"] + " gained " + str(damage) + " HP" )
                damage = damage  * (-1) #Make the damage negative so the healing raises the target's hp

            T[targetIndex]["hp"] -= damage
            T[targetIndex]["hp"] = max(0,T[targetIndex]["hp"]) #ensure hp doesn't go below zero
            T[targetIndex]["hp"] = min(T[targetIndex]["mhp"],T[targetIndex]["hp"]) #ensure hp doesn't go above max hp
            if T[targetIndex]["hp"] == 0:
                print(T[targetIndex]["name"] + " was defeated!")
                defeat = True
        return U, T, defeat

    #Used to check if a party, either player or enemy, as been defeated
    def defeatCheck(self,P):
        for battler in P:
            # if at least one of the party's battlers has positive hp, then they aren't defeated
            if battler["hp"] > 0: 
                return False
        #None of the party's battlers have positive hp, so they are defeated
        return True

    #Create the list of valid targets, as well as the string of targets for players
    #healing is a boolean to check if it is heal targeting to except full hp targets
    def buildTargeting(act, E, P, userParty, userIndex, target, formula):
        result = ""
        validIndexes = []
        if target == "enemy":
            index = 0
            if userParty == 1:
                while index < len(E):
                    if E[index]["hp"] > 0:
                        result += "[" + str(index) + "]" + " for " + E[index]["name"] + ", "
                        validIndexes.append(str(index))
                    index += 1
            else:
                while index < len(P):
                    if P[index]["hp"] > 0:
                        validIndexes.append(str(index)) 
                    index += 1               
                
        if target == "ally" or target == "allyHeal":
            index = 0
            if userParty == 1:
                while index < len(P):
                    if P[index]["hp"] < P[index]["mhp"] or target != "allyHeal":
                        result += "[" + str(index) + "]" + " for " + P[index]["name"] + ", "
                        validIndexes.append(str(index))
                    index += 1
            else:
                while index < len(E):
                    if P[index]["hp"] < E[index]["mhp"] or target != "allyHeal":
                        validIndexes.append(str(index))   
                    index += 1 

        if len(result) > 1:
            result = result[:len(result)-2] #Get rid of the final ", "    
        return result, validIndexes        
    