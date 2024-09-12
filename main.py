import random
import sys
sys.dont_write_bytecode = True
import PrintFunctions
from termcolor import cprint, colored

# Variables
numberOfGoodDoors = 1
unknownDoorAmount = 2

# Functions
def GenerateRoom(doorNum:int, donkeyCount:int):
    doorDict = {i+1:0 for i in range(doorNum)}
    doorList = list(doorDict.keys())
    for i in range(doorNum-donkeyCount):
        goodDoor = random.choice(doorList)
        doorDict[goodDoor] = 1
        doorList.remove(goodDoor)
    print(doorDict)
    return doorDict

def RevealDoor(doorRevealCount:int, chosenDoor:int, roomDict:dict):
    revealableDoors = list(roomDict.keys())
    revealableDoors.remove(chosenDoor)
    doorsRevealed = []
    for i in range(doorRevealCount):
        while True:
            revealed = random.choice(list(revealableDoors))
            if roomDict[revealed] == 0:
                break
            else:
                list(revealableDoors).remove(revealed)
                continue
        list(revealableDoors).remove(revealed)
        doorsRevealed.append(revealed)
    return doorsRevealed

def UserSimulation(doorNum:int, simulation_times:int):
    for i in range(simulation_times):
        cprint("#Round"+str(i), "green")
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door"))
        doorsToBeRevealed = RevealDoor(doorNum-unknownDoorAmount, chosenDoor, roomDict)
        print(doorsToBeRevealed)

# Menu

# Main Code
UserSimulation(3, 1)