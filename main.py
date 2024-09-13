import random
import sys
sys.dont_write_bytecode = True
import PrintFunctions
from termcolor import cprint, colored

# Variables
numberOfGoodDoors = 1
unknownDoorAmount = 2
extendedResults = False
roundCount = 0
doorFirstChoices = []
actions = []
outcomes = []
playingType = None

# Functions

def GenerateRoom(doorNum:int, goatCount:int):
    doorDict = {i+1:0 for i in range(doorNum)}
    doorList = list(doorDict.keys())
    for i in range(doorNum-goatCount):
        goodDoor = random.choice(doorList)
        doorDict[goodDoor] = 1
        doorList.remove(goodDoor)
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
    if type == "switch":
        finalDoor = list(set(roomDict.keys()) - set(revealedDoors))
        finalDoor.remove(chosenDoor)
        finalDoor = int(finalDoor[0])
    elif type == "stay":
        finalDoor = chosenDoor
    else:
        print("Error. Type is not Switch or Stay. [GetResult]")
    return tuple([roomDict[finalDoor] == 1, finalDoor, type])

def UserSimulation(doorNum:int):
    roundNum = 0
    allFirstChoices = []
    allActions = []
    allResults = []
    while True:
        roundNum += 1
        print("-"*20)
        cprint("#Round "+str(roundNum), "green")
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = int(PrintFunctions.LimitedInput(list(roomDict.keys()), "Pick a door", " | "))
        doorsToBeRevealed = RevealDoor(doorNum-unknownDoorAmount, chosenDoor, roomDict)
        print()
        if len(doorsToBeRevealed) > 10:
            for i in range(1, len(roomDict)+1):
                if i not in doorsToBeRevealed and i != chosenDoor:
                    print(f"Door {i} may be the prize door.\n")
                    break
        elif len(doorsToBeRevealed) == 1:
            print(f"Goat is in door {doorsToBeRevealed[0]}\n")
        else:
            print("Goats are in doors:", end=" ")
            for i in doorsToBeRevealed:
                if not i == doorsToBeRevealed[-1]:
                    print(i, end=", ")
                else:
                    print(str(i)+".\n")
        result, finalDoor, action = GetResult(PrintFunctions.LimitedInput(["stay", "switch"], f"Do you want to stay or switch:"), doorsToBeRevealed, chosenDoor, roomDict)
        if result:
            print(f"Door {finalDoor} has the Prize! You Win!")
        else:
            print(f"Door {finalDoor} had the Goat. Too Bad.")
        
        allFirstChoices.append(chosenDoor)
        allActions.append(action.capitalize())
        allResults.append("Win" if result else "Lose")
        
        print()
        if PrintFunctions.LimitedInput(["y", "n"], "Do you want to play again:") == "n":
            break
    print("\n")
    PrintResults(list(i+1 for i in range(roundNum)), allFirstChoices, allActions, allResults, roundNum, extendedResults)

def SilentSimulation(doorNum:int, simulationTimes:int):
    pass

def PrintResults(allRounds:list, allFirstChoices:list, allActions:list, allResults:list, amountOfRounds:int, extendedInfo:bool=False):    
    tableData = [allRounds, allFirstChoices, allActions, allResults]
    PrintFunctions.PrintTable(tableData, amountOfRounds)
    winsCount = allResults.count("Win")
    lossesCount = allResults.count("Lose")
    stayCount = allActions.count("Stay")
    switchCount = allActions.count("Switch")
    switchWinCount, switchLossCount, stayWinCount, stayLossCount = 0, 0, 0, 0
    for i in range(amountOfRounds):
        if allActions[i] == "Switch":
            if allResults[i] == "Win":
                switchWinCount += 1
            else:
                switchLossCount += 1
        elif allActions[i] == "Stay":
            if allResults[i] == "Win":
                stayWinCount += 1
            else:
                stayLossCount += 1

    cprint("SUMMARY\n", attrs=["bold"])
    cprint(f"Wins with switch: {switchWinCount}")
    cprint(f"Wins with stay: {stayWinCount}\n")
    print(f"Pr(Winning with switch): {switchWinCount/amountOfRounds*100}%")
    print(f"Pr(Winning with stay): {stayWinCount/amountOfRounds*100}%\n")

    if extendedInfo:
        cprint("EXTENDED INFO\n", attrs=["bold"])
        print(f"Wins: {winsCount}, {winsCount/amountOfRounds*100}%")
        print(f"Losses: {lossesCount}, {lossesCount/amountOfRounds*100}%\n")
        print(f"Losses with switch: {switchLossCount}, {switchLossCount/amountOfRounds*100}%")
        print(f"Losses with stay: {stayLossCount}, {stayLossCount/amountOfRounds*100}%")


# Menu
playingType = None
while True:
    command = str(PrintFunctions.ListedInput({"p": "Play", "c": "Customisation"}, "Enter a command:")).lower()
    if command == "play":
        break
        # start mode selection
    elif command == "customisation":
        pass
        # customisation options
    
# Main Code
# print(PrintFunctions.LimitedInput(["a", "b", "c"], "Select"))
UserSimulation(3)