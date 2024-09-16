import random
import sys
sys.dont_write_bytecode = True
import PrintFunctions
from termcolor import cprint, colored

# Variables
numberOfGoodDoors = 1
unknownDoorAmount = 2
amountOfDoors = 3
maximumAmountOfDoors = 100
extendedResults = False
roundCount = 0
doorFirstChoices = []
actions = []
outcomes = []

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
    print("Look up the info for Manual Simulation to know how to play.")
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
    print("")
    PrintResults(list(i+1 for i in range(roundNum)), allFirstChoices, allActions, allResults, roundNum, extendedResults)

def SilentSimulations(doorNum:int, simulationTimes:int, simType:str="random choices", runningDefaultSim:bool=False, fileSave:str=""):
    if simType == "always stay": actionRandomChoice = "stay"
    elif simType == "always switch": actionRandomChoice = "switch"
    print(f"Simulating for {simulationTimes} times, with {doorNum} doors. The action is {simType}.")
    print('Progress: 0.0%'+'\r', end="")
    allFirstChoices = []
    allActions = []
    allResults = []
    allRounds = list(i+1 for i in range(simulationTimes))
    for r in allRounds:
        roomDict = GenerateRoom(doorNum, doorNum-numberOfGoodDoors)
        chosenDoor = random.choice(list(roomDict.keys()))
        doorsToBeRevealed = RevealDoor(doorNum-unknownDoorAmount, chosenDoor, roomDict)
        if simType == "random choices": actionRandomChoice = random.choice(["stay", "switch"])
        result, finalDoor, action = GetResult(actionRandomChoice, doorsToBeRevealed, chosenDoor, roomDict)
        allFirstChoices.append(chosenDoor)
        allActions.append(action.capitalize())
        allResults.append("Win" if result else "Lose")
        print(f'Progress: {round(r/simulationTimes*100, 2)}%'+'\r', end="")
    print("\n")
    if fileSave != "":
        SaveToFile(fileSave, allRounds, allFirstChoices, allActions, allResults, simulationTimes)
    if not runningDefaultSim:
        if simulationTimes <= 100:
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults)
        else:
            print("The table was not printed because it was too long.")
            PrintResults(allRounds, allFirstChoices, allActions, allResults, simulationTimes, extendedResults, False)
        return
    return allActions, allResults, allFirstChoices

def RunDefaultSilentSimulations(simType, amountOfDoors):
    simulationTimes = [50, 100, 1000, 5000, 10000]
    allActions, allResults, allFirstChoices = [], [], []
    for sim in simulationTimes:
        actions, results, choices = SilentSimulations(amountOfDoors, sim, simType, True)
        allActions += actions
        allResults += results
        allFirstChoices += choices
    PrintFunctions.PrintTable([list(i+1 for i in range(50)), allFirstChoices[:50], allActions[:50], allResults[:50]], 50, tableTitle="50 ROUND RESULTS TABLE")
    print("\nThe rest were simulated silently...\n")

    stayPrs, switchPrs = [], []
    for i in range(len(simulationTimes)):
        if not i == 0: before = simulationTimes[i-1]
        else: before = 0
        current = simulationTimes[i]
        roundActions = allActions[before+1:current+before+1]
        roundResults = allResults[before+1:current+before+1]
        switchWins, stayWins = 0, 0
        for s in range(len(roundActions)):
            if roundResults[s] == "Win":
                if roundActions[s] == "Stay":
                    stayWins += 1
                else:
                    switchWins += 1
        stayPrs.append(str(round(stayWins/len(roundActions)*100,2))+"%")
        switchPrs.append(str(round(switchWins/len(roundActions)*100,2))+"%")

    PrintFunctions.PrintTable([simulationTimes, switchPrs, stayPrs], 5, "SILENT SIMULATION RESULTS", ["Rounds", "Pr(Win with Switch)", "Pr(Win with Stay)"])

def SilentSimulationMenu():
    print("Check info on types of Silent Simulation if you are struggling to understand.")
    print("You can customise the doors and the amount of simulations.")

    simType = str(PrintFunctions.ListedInput({"1": "Random Choices", "2": "Always Switch", "3": "Always Stay"}, "Pick type of silent simulation: (1/3 Type)")).lower()
    amountOfSims = str(PrintFunctions.ListedInput({"1": "Controlled (50, 100, 1000, 5000, 10000 times)", "2": "Custom Amount"}, "Pick type of silent simulation: (2/3 Simulation Times)", returnKey=True)).lower()
    if amountOfSims == "2":
        amountOfSims = PrintFunctions.RangedInput(1, 1, "Pick amount of Simulation Times:", infiniteEnd=True)
    amountOfDoors = str(PrintFunctions.ListedInput({"1": "Default (3)", "2": "Many Doors (10)", "3": "Custom"}, "Pick type of silent simulation: (3/3 Door Amount)", returnKey=True)).lower()
    if amountOfDoors == "3":
        amountOfDoors = PrintFunctions.RangedInput(1, 1, "Pick amount of Doors:", infiniteEnd=True)
    elif amountOfDoors == "2": amountOfDoors = 10
    elif amountOfDoors == "1": amountOfDoors = 3
    if amountOfSims == "1":
        RunDefaultSilentSimulations(simType, amountOfDoors)
    else:
        SilentSimulations(amountOfDoors, amountOfSims, simType)

def PrintResults(allRounds:list, allFirstChoices:list, allActions:list, allResults:list, amountOfRounds:int, extendedInfo:bool=False, table:bool=True):
    if table:
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
        print(f"Losses with stay: {stayLossCount}, {stayLossCount/amountOfRounds*100}%\n")

def SaveToFile(fileName:str, allRounds:list, allFirstChoices:list, allActions:list, allResults:list, amountOfRounds:int):
    with open(fileName, "w") as file:
        file.truncate()
        file.write("Round,First Choice,Action,Result\n")
        for i in range(amountOfRounds):
            file.write(f"{allRounds[i]},{allFirstChoices[i]},{allActions[i]},{allResults[i]}\n")

def SilentFileUpdate():
    SilentSimulations(3, 1000, "random choices", True, "part2_random.txt")
    SilentSimulations(3, 1000, "always stay", True, "part3_stay.txt")
    SilentSimulations(3, 1000, "always switch", True, "part4_switch.txt")
    SilentSimulations(10, 1000, "random choices", True, "part5_ten_doors.txt")
    print("Files Saved Successfully!\n")

# Main Code
print("-------------------------------------------------------------------")
cprint("The 3-door Problem/Monty Hall Problem Simulator", attrs=["bold", "underline"])
cprint("By Sean Chan", attrs=["bold"])
cprint("Disclaimer: This was made for a school project. Do not take seriously.")
print("-------------------------------------------------------------------\n")
while True:
    command = None
    command = str(PrintFunctions.ListedInput({"p": "Play", "c": "Customisation", "h": "How To Play"}, "Enter a command:")).lower()
    if command == "play":
        command = str(PrintFunctions.ListedInput({"i": "Interactive Simulation", "s": "Silent Simulation", "f": "Update Files", "p": "Previous"}, "Pick type of simulation:")).lower()
        if command == "interactive simulation":
            amountOfDoors = PrintFunctions.RangedInput(3, maximumAmountOfDoors, "Enter amount of doors: (Recommended: 3)")
            UserSimulation(amountOfDoors)
        elif command == "silent simulation":
            SilentSimulationMenu()
        elif command == "update files":
            SilentFileUpdate()
        elif command == "previous":
            continue
    elif command == "customisation":
        while True:
            command = str(PrintFunctions.ListedInput({"c": "Clear files", "e": "Toggle Extended Results", "p": "Previous"}, "Enter a setting to edit:")).lower()
            if command == "clear files":
                files = ["part2_random.txt", "part3_stay.txt", "part4_switch.txt", "part5_ten_doors.txt"]
                for file in files:
                    with open(file, "w") as f: f.truncate()
                cprint("Files cleared successfully.\n", "green")
            elif command == "toggle extended results":
                extendedResults = not extendedResults
                cprint("Extended Info is now set to " + str(extendedResults) + ".\n", "green")
            elif command == "previous":
                break
    elif command == "how to play":
        while True:
            command = str(PrintFunctions.ListedInput({"i": "Interactive Simulations", "s": "Silent Simulations", "p": "Previous"}, "Enter a command:")).lower()
            if command == "previous":
                break
            elif command == "interactive simulations":
                cprint("INTERACTIVE SIMULATION HELP\n", attrs=["bold"])
                print("""Accessing the Interactive Simulation in the Program:
1. Select "Play" from the main menu.
2. Select "Interactive Simulation" from the play menu.
3. Enter the amount of doors you want. (Recommended: 3)

How To Play:
At the start, there are x amount of doors, with each door being numbered 1 to x. One door has a car in it, and the rest have something bad - Goats. The aim is to select the door with the car. You first start by selecting a door, and then the host will reveal x-2 doors that have goats in them. You then can decide to switch to the remaining door, or stay with your current door. Depending what you choose, you can win or lose. Just select 'y' to play again in the program.

When you are done, select 'n' in play again and the results will be printed with statistics. See if you can find a pattern...\n""")
            elif command == "silent simulations":
                cprint("SILENT SIMULATION HELP\n", attrs=["bold"])
                print("""Accessing the Silent Simulation in the Program:
1. Select "Play" from the main menu.
2. Select "Silent Simulation" from the play menu.
3. Enter the type of simulation you want.
        Random Choices means that it will select randomly to do switch or stay.
        Always stay or switch just does what it specifies, always.
4. Enter the amount of times you want to simulate.
        Controlled simulation simulates 100, 500, 1000, 5000, 10000 times and prints a special results table.
        If you customise, it will ask you how many times you want.
5. Enter the amount of doors you want to simulate with.
        Default is 3 door, Many Doors is 10 doors.
        If you customise, it will ask you how many doors you want to simulate with.

The program will then simulate the setting silently and then print results.\n""")