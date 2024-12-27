from Project0Intro import Intro
from Project0Explore import Explore


intro = Intro()
explo = Explore()

class Controller:
    def control(self):
        #print("test")
        while True:
            sav = intro.title()
            loc = explo.startExplore(sav)
            explo.explore(loc,sav)



if __name__ == "__main__":
    cont = Controller()
    cont.control()