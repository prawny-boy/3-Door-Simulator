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
                revealableDoors.remove(revealed)
                continue
        revealableDoors.remove(revealed)
        doorsRevealed.append(revealed)
    doorsRevealed.sort()
    return doorsRevealed

def GetResult(type:str, revealedDoors:list, chosenDoor:int, roomDict:dict):
    pass

def UserSimulation(doorNum:int, roundNum:int):
    cprint("#Round "+str(roundNum), "green")
    roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
    chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door"))
    doorsToBeRevealed = RevealDoor(doorNum-unknownDoorAmount, chosenDoor, roomDict)
    print()
    if len(doorsToBeRevealed) > 10:
        for i in range(1, len(roomDict)+1):
            if i not in doorsToBeRevealed and i != chosenDoor:
                print(f"Door {i} may be the prize door.")
                break
    elif len(doorsToBeRevealed) == 1:
        print(f"Goat is in door {i}")
    else:
        print("Goats are in doors:", end=" ")
        for i in doorsToBeRevealed:
            if not i == doorsToBeRevealed[-1]:
                print(i, end=", ")
            else:
                print(str(i)+".")
    result = GetResult(PrintFunctions.LimitedInput(["switch", "stay"], "Do you want to switch or stay:"), doorsToBeRevealed, chosenDoor, roomDict)

def SilentSimulation(doorNum:int, simulationTimes:int):
    pass

# Menu

# Main Code
# print(PrintFunctions.LimitedInput(["a", "b", "c"], "Select"))
UserSimulation(10,1)