import random
import sys
import printfunctions

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

def UserSimulation(doorNum:int, usered:bool, simulation_times:int):
    for i in range(simulation_times):
        GenerateRoom(doorNum, doorNum-numberOfGoodDoors)

# Menu

# Main Code
GenerateRoom(100,99)