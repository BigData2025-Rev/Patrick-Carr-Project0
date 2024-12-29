class Init:
    def __init__(self):
        test = 0

    # { "X,Y":{"conn":["Direction","Direction2",etc.],"desc":"Text","enemy":"None" means no enemy}}
    #"enemy":{1:"EnemyName"} enemy 1 the EnemyName enemy to look up in Enemies.json, 
    # whether or not the enemy is defeated is in Progress.json
    def initLoc(self):
        loc = {
            "1,1":{"conn":["N"],"desc":"You are in an empty room","enemy":"None"},
            "1,2":{"conn":["S","N","E"],"desc":"You are in a different room","enemy":{0:"Slime",1:"Slime"}},
            "2,2":{"conn":["N","W"],"desc":"You are in a room full of bones","enemy":{0:"Skeleton"}},
            "1,3":{"conn":["S"],"desc":"You are in a room with a little fountain","enemy":"None"},
            "2,3":{"conn":["S","E"],"desc":"You are in a chamber with an alter","enemy":{0:"Hexer"}},
            "3,3":{"conn":["W"],"desc":"Congats, you finished the game!","enemy":"None"}
        }
        return loc

    #"X,Y": {"enemy": 0 means encounter is not defeated, 1 means encounter is defeated}
    #"enemy" keeps track of defeated enemies. It is formatted this way to allow for 
    # more entries like "switch":{} or "button":{}
    #
    def initProg(self):
        dict = {
            "playerLoc":"1,1",
            "prevLoc":"1,1",
            "1,2":{"enemy":0},
            "2,2":{"enemy":0},
            "2,3":{"enemy":0},
            "party":[0]
        }
        return dict
    
    def initPlayer(self):
        dict = {#All commands that come after S are spells
            0:{"name":"Player","lvl":10,"exp":0,"hp":83, "mhp":83,"mp":45, "mmp":45, "str":18, "def":6,"mag":18, "res":16,
               "omhp":35, "ommp":20, "ostr":7, "odef":2,"omag":7, "ores":6,
               "fmhp":560, "fmmp":290, "fstr":130, "fdef":42,"fmag":130, "fres":120,
               "commands":"A,S,H,E,L"}
        }
        return dict
    
    def initEnemies(self): #Enemies do not use the "S" commands
        dict = {
            "Slime":{"name":"Slime","lvl":10,"hp":42, "mhp":42, "mp":0, "mmp":0, "str":14, "def":6,"mag":4, "res":11,"commands":"A","exp":25},
            "Skeleton":{"name":"Skeleton","lvl":10,"hp":53, "mhp":53, "mp":0, "mmp":0, "str":15, "def":6,"mag":4, "res":11,"commands":"A","exp":50},
            "Hexer":{"name":"Hexer","lvl":11,"hp":40, "mhp":40, "mp":30, "mmp":30, "str":13, "def":4,"mag":12, "res":15,"commands":"A,E","exp":110}
        }
        return dict
    
    #"target": "enemy" means target opposite party, "ally" means target same party, "category" is a category of command, like Spells
    #power is usually added to the damage/healing
    def initCommands(self):
        dict = {
            "A":{"name":"Attack","target":"enemy","range":"single","formula":"phys","power":0,"cost":0},
            "S":{"name":"Spells","target":"user","range":"user","formula":"category","power":0,"cost":0},
            "H":{"name":"Heal","target":"allyHeal","range":"single","formula":"magHeal","power":20,"cost":4},
            "E":{"name":"Earth","target":"enemy","range":"single","formula":"mag","power":30,"cost":3},
            "L":{"name":"Lightning","target":"enemy","range":"two","formula":"mag","power":15,"cost":4}
        }
        return dict