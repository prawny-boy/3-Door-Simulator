import random
import sys
import PrintFunctions

# Variables
numberOfGoodDoors = 1

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

def RevealDoor(doorRevealCount, chosenDoor):
    pass

def UserSimulation(doorNum:int, simulation_times:int):
    for i in range(simulation_times):
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door"))

# Menu

# Main Code
UserSimulation(3, 1)